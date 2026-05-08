from dataclasses import dataclass


@dataclass(frozen=True)
class Product:
    product_id: int | None = None
    sku: str | None = None
    product_name: str | None = None
    description: str | None = None
    category: str | None = None
    unit: str | None = None
    is_active: bool | None = None