import uuid
from dataclasses import dataclass, field
from datetime import datetime, date

MOVEMENT_TYPES = ("IN", "OUT", "TRANSFER", "ADJUST")


def month_bucket(ts: datetime) -> str:
    """Бакет партиции истории товара: 'YYYY-MM'."""
    return ts.strftime("%Y-%m")


@dataclass
class Movement:
    warehouse_id: str
    product_id: str
    movement_type: str
    quantity: int
    ts: datetime
    operator: str = "system"
    doc_ref: str = ""
    comment: str = ""
    movement_id: uuid.UUID = field(default_factory=uuid.uuid4)

    def __post_init__(self):
        if self.movement_type not in MOVEMENT_TYPES:
            raise ValueError(f"movement_type must be one of {MOVEMENT_TYPES}")
        if self.quantity <= 0:
            raise ValueError("quantity must be positive")

    @property
    def day(self) -> date:
        return self.ts.date()

    @property
    def year_month(self) -> str:
        return month_bucket(self.ts)
