from pydantic import BaseModel


class ProductCreateRequest(BaseModel):
    sku: str
    product_name: str
    description: str | None = None
    category: str | None = None
    unit: str = "pieza"


class ProductResponse(BaseModel):
    product_id: int
    sku: str
    product_name: str
    description: str | None = None
    category: str | None = None
    unit: str
    is_active: bool

class ProductUpdateRequest(BaseModel):
    sku: str
    product_name: str
    description: str | None = None
    category: str | None = None
    unit: str = "pieza"
    is_active: bool = True