from dataclasses import dataclass
from datetime import datetime


@dataclass(frozen=True)
class InventoryMovement:
    movement_id: int | None = None
    product_id: int | None = None
    movement_type: str | None = None
    quantity: int | None = None
    reference_text: str | None = None
    notes: str | None = None
    created_by: int | None = None
    created_at: datetime | None = None