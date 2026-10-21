from datetime import datetime
from collections import defaultdict
from cassandra.query import BatchStatement, BatchType
from .models import Movement

COLS_WH = "warehouse_id, day, ts, movement_id, product_id, movement_type, quantity, operator, doc_ref, comment"
COLS_PR = "product_id, year_month, ts, movement_id, warehouse_id, movement_type, quantity, operator, doc_ref, comment"


class MovementRepository:
    """CRUD над двумя таблицами: запись всегда в обе (LOGGED BATCH), чтение - из подходящей."""

    def __init__(self, session):
        s = session
        self.s = s
        self.ins_wh = s.prepare(f"INSERT INTO movements_by_warehouse_day ({COLS_WH}) VALUES (?,?,?,?,?,?,?,?,?,?)")
        self.ins_pr = s.prepare(f"INSERT INTO movements_by_product ({COLS_PR}) VALUES (?,?,?,?,?,?,?,?,?,?)")
        self.upd_wh = s.prepare("UPDATE movements_by_warehouse_day SET comment=? WHERE warehouse_id=? AND day=? AND ts=? AND movement_id=?")
        self.upd_pr = s.prepare("UPDATE movements_by_product SET comment=? WHERE product_id=? AND year_month=? AND ts=? AND movement_id=?")
        self.del_wh = s.prepare("DELETE FROM movements_by_warehouse_day WHERE warehouse_id=? AND day=? AND ts=? AND movement_id=?")
        self.del_pr = s.prepare("DELETE FROM movements_by_product WHERE product_id=? AND year_month=? AND ts=? AND movement_id=?")
        self.q_wh_day = s.prepare("SELECT * FROM movements_by_warehouse_day WHERE warehouse_id=? AND day=?")
        self.q_wh_day_lim = s.prepare("SELECT * FROM movements_by_warehouse_day WHERE warehouse_id=? AND day=? LIMIT ?")
        self.q_wh_range = s.prepare("SELECT * FROM movements_by_warehouse_day WHERE warehouse_id=? AND day=? AND ts>=? AND ts<?")
        self.q_pr_month = s.prepare("SELECT * FROM movements_by_product WHERE product_id=? AND year_month=?")
        self.q_pr_month_lim = s.prepare("SELECT * FROM movements_by_product WHERE product_id=? AND year_month=? LIMIT ?")
        self.q_pr_range = s.prepare("SELECT * FROM movements_by_product WHERE product_id=? AND year_month=? AND ts>=? AND ts<?")

    # ---------- CREATE ----------
    def add(self, m: Movement):
        b = BatchStatement(batch_type=BatchType.LOGGED)
        b.add(self.ins_wh, (m.warehouse_id, m.day, m.ts, m.movement_id, m.product_id,
                            m.movement_type, m.quantity, m.operator, m.doc_ref, m.comment))
        b.add(self.ins_pr, (m.product_id, m.year_month, m.ts, m.movement_id, m.warehouse_id,
                            m.movement_type, m.quantity, m.operator, m.doc_ref, m.comment))
        self.s.execute(b)

    # ---------- READ: по складу и дню (AP1-AP4) ----------
    def by_warehouse_day(self, warehouse_id, day):
        return list(self.s.execute(self.q_wh_day, (warehouse_id, day)))

    def last_by_warehouse_day(self, warehouse_id, day, n=5):
        return list(self.s.execute(self.q_wh_day_lim, (warehouse_id, day, n)))

    def by_warehouse_range(self, warehouse_id, day, t_from: datetime, t_to: datetime):
        return list(self.s.execute(self.q_wh_range, (warehouse_id, day, t_from, t_to)))

    def daily_totals(self, warehouse_id, day):
        """Нетривиально: агрегат по типам операций (GROUP BY по не-ключу невозможен -> считаем в приложении)."""
        totals = defaultdict(int)
        for r in self.by_warehouse_day(warehouse_id, day):
            totals[r.movement_type] += r.quantity
        return dict(totals)

    # ---------- READ: по товару (AP5-AP8) ----------
    def by_product_month(self, product_id, year_month):
        return list(self.s.execute(self.q_pr_month, (product_id, year_month)))

    def last_by_product(self, product_id, year_month, n=5):
        return list(self.s.execute(self.q_pr_month_lim, (product_id, year_month, n)))

    def by_product_range(self, product_id, year_month, t_from, t_to):
        return list(self.s.execute(self.q_pr_range, (product_id, year_month, t_from, t_to)))

    def product_turnover(self, product_id, months):
        """Нетривиально: чтение нескольких партиций-бакетов и свёртка в приложении (fan-out по месяцам)."""
        result = {}
        for ym in months:
            net = 0
            for r in self.by_product_month(product_id, ym):
                if r.movement_type == "IN":
                    net += r.quantity
                elif r.movement_type == "OUT":
                    net -= r.quantity
            result[ym] = net
        return result

    # ---------- UPDATE ----------
    def update_comment(self, m: Movement, new_comment: str):
        b = BatchStatement(batch_type=BatchType.LOGGED)
        b.add(self.upd_wh, (new_comment, m.warehouse_id, m.day, m.ts, m.movement_id))
        b.add(self.upd_pr, (new_comment, m.product_id, m.year_month, m.ts, m.movement_id))
        self.s.execute(b)

    # ---------- DELETE ----------
    def delete(self, m: Movement):
        b = BatchStatement(batch_type=BatchType.LOGGED)
        b.add(self.del_wh, (m.warehouse_id, m.day, m.ts, m.movement_id))
        b.add(self.del_pr, (m.product_id, m.year_month, m.ts, m.movement_id))
        self.s.execute(b)
