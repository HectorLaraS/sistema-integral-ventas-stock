from dataclasses import asdict
from fastapi import APIRouter, HTTPException
from src.services.product_service import ProductService
from src.domain.product import Product
from src.api.schemas.product_schema import (
    ProductCreateRequest,
    ProductResponse,
    ProductUpdateRequest
)


router = APIRouter(
    prefix="/products",
    tags=["Products"]
)


@router.get("")
def list_products():
    service = ProductService()
    products = service.list_products()

    return [asdict(product) for product in products]

@router.post("", response_model=ProductResponse)
def create_product(request: ProductCreateRequest):
    service = ProductService()

    product = Product(
        sku=request.sku,
        product_name=request.product_name,
        description=request.description,
        category=request.category,
        unit=request.unit,
        is_active=True
    )

    created_product = service.create_product(product)

    return ProductResponse(
        product_id=created_product.product_id,
        sku=created_product.sku,
        product_name=created_product.product_name,
        description=created_product.description,
        category=created_product.category,
        unit=created_product.unit,
        is_active=created_product.is_active
    )

@router.get("/{product_id}", response_model=ProductResponse)
def get_product_by_id(product_id: int):
    service = ProductService()
    product = service.get_product_by_id(product_id)

    if product is None:
        raise HTTPException(
            status_code=404,
            detail="Product not found"
        )

    return ProductResponse(
        product_id=product.product_id,
        sku=product.sku,
        product_name=product.product_name,
        description=product.description,
        category=product.category,
        unit=product.unit,
        is_active=product.is_active
    )

@router.put("/{product_id}", response_model=ProductResponse)
def update_product(
    product_id: int,
    request: ProductUpdateRequest
):
    service = ProductService()

    product = Product(
        sku=request.sku,
        product_name=request.product_name,
        description=request.description,
        category=request.category,
        unit=request.unit,
        is_active=request.is_active
    )

    updated_product = service.update_product(
        product_id,
        product
    )

    if updated_product is None:
        raise HTTPException(
            status_code=404,
            detail="Product not found"
        )

    return ProductResponse(
        product_id=updated_product.product_id,
        sku=updated_product.sku,
        product_name=updated_product.product_name,
        description=updated_product.description,
        category=updated_product.category,
        unit=updated_product.unit,
        is_active=updated_product.is_active
    )

@router.delete("/{product_id}")
def delete_product(product_id: int):
    service = ProductService()

    deleted = service.delete_product(product_id)

    if not deleted:
        raise HTTPException(
            status_code=404,
            detail="Product not found"
        )

    return {
        "message": "Product deactivated successfully"
    }

@router.patch("/{product_id}/reactivate")
def reactivate_product(product_id: int):
    service = ProductService()

    reactivated = service.reactivate_product(product_id)

    if not reactivated:
        raise HTTPException(
            status_code=404,
            detail="Product not found"
        )

    return {
        "message": "Product reactivated successfully"
    }