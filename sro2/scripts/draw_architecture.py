python scripts/init_schema.pyimport pathlib
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.patches import FancyBboxPatch

fig, ax = plt.subplots(figsize=(11, 5.5)); ax.axis("off"); ax.set_xlim(0, 11); ax.set_ylim(0, 5.5)

def box(x, y, w, h, text, c):
    ax.add_patch(FancyBboxPatch((x, y), w, h, boxstyle="round,pad=0.05", fc=c, ec="#333"))
    ax.text(x + w / 2, y + h / 2, text, ha="center", va="center", fontsize=9)

def arrow(x1, y1, x2, y2):
    ax.annotate("", xy=(x2, y2), xytext=(x1, y1), arrowprops=dict(arrowstyle="->", lw=1.4))

box(0.2, 2.2, 2.0, 1.1, "Scripts\nseed.py / run_queries.py", "#e8f0fe")
box(3.0, 2.2, 2.4, 1.1, "MovementRepository\n(Python, cassandra-driver)", "#fff3cd")
box(6.4, 3.4, 4.2, 1.3, "movements_by_warehouse_day\nPK ((warehouse_id, day), ts DESC)\nAP1-AP4", "#d4edda")
box(6.4, 0.8, 4.2, 1.3, "movements_by_product\nPK ((product_id, year_month), ts DESC)\nAP5-AP8", "#d4edda")
ax.text(8.5, 5.1, "Apache Cassandra 4.1 (keyspace warehouse)", ha="center", fontsize=10, weight="bold")
arrow(2.2, 2.75, 3.0, 2.75)
arrow(5.4, 2.9, 6.4, 3.9); arrow(5.4, 2.6, 6.4, 1.5)
ax.text(0.2, 0.3, "Write: LOGGED BATCH into both tables | Read: from the table built for the Access Pattern", fontsize=9)
out = pathlib.Path(__file__).resolve().parent.parent / "docs" / "architecture.png"
plt.savefig(out, dpi=150, bbox_inches="tight")
