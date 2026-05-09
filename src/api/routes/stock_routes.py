from dataclasses import asdict
from fastapi import APIRouter, HTTPException, Depends
from src.services.stock_service import StockService
from src.api.schemas.stock_schema import StockResponse
from src.domain.user import User
from src.api.dependencies.security import get_current_user

router = APIRouter(
    prefix="/stock",
    tags=["Stock"]
)


@router.get("", response_model=list[StockResponse])
def list_stock(current_user: User = Depends(get_current_user)):
    service = StockService()
    stock_items = service.list_stock()

    return [asdict(item) for item in stock_items]