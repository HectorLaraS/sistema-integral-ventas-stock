from src.repositories.stock_psql import StockPSQL
from src.domain.stock import Stock


class StockService:
    def __init__(self):
        self._repository = StockPSQL()

    def list_stock(self) -> list[Stock]:
        return self._repository.list_stock()