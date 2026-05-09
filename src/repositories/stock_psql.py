from src.config.db_connection import DBConnection
from src.domain.stock import Stock


class StockPSQL:
    def __init__(self):
        self._db_connection = DBConnection()

    def list_stock(self) -> list[Stock]:
        query = """
            SELECT
                p.product_id,
                p.sku,
                p.product_name,
                p.category,
                p.unit,
                COALESCE(s.quantity_on_hand, 0) AS quantity_on_hand
            FROM inventario.products p
            LEFT JOIN inventario.inventory_stock s
                ON p.product_id = s.product_id
            WHERE p.is_active = TRUE
            ORDER BY p.product_id;
        """

        stock_items: list[Stock] = []

        with self._db_connection.get_conn() as conn:
            with conn.cursor() as cur:
                cur.execute(query)
                rows = cur.fetchall()

        for row in rows:
            stock_items.append(
                Stock(
                    product_id=row[0],
                    sku=row[1],
                    product_name=row[2],
                    category=row[3],
                    unit=row[4],
                    quantity_on_hand=row[5],
                )
            )

        return stock_items