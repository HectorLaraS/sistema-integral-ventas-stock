from datetime import datetime
from pydantic import BaseModel


class InventoryInRequest(BaseModel):
    product_id: int
    quantity: int
    reference_text: str | None = None
    notes: str | None = None
    created_by: int | None = None


class InventoryMovementResponse(BaseModel):
    movement_id: int
    product_id: int
    movement_type: str
    quantity: int
    reference_text: str | None = None
    notes: str | None = None
    created_by: int | None = None
    created_at: datetime