from pydantic import BaseModel


class StockResponse(BaseModel):
    product_id: int
    sku: str
    product_name: str
    category: str | None = None
    unit: str
    quantity_on_hand: int