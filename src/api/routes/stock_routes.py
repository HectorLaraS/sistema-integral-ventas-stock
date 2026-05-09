from dataclasses import asdict
from fastapi import APIRouter
from src.services.stock_service import StockService
from src.api.schemas.stock_schema import StockResponse


router = APIRouter(
    prefix="/stock",
    tags=["Stock"]
)


@router.get("", response_model=list[StockResponse])
def list_stock():
    service = StockService()
    stock_items = service.list_stock()

    return [asdict(item) for item in stock_items]