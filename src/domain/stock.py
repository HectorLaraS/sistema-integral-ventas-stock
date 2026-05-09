from dataclasses import dataclass


@dataclass(frozen=True)
class Stock:
    product_id: int
    sku: str
    product_name: str
    category: str | None
    unit: str
    quantity_on_hand: int