from src.config.db_connection import DBConnection
from src.domain.product import Product


class ProductPSQL:
    def __init__(self):
        self._db_connection = DBConnection()

    def list_products(self) -> list[Product]:
        query = """
            SELECT 
                product_id,
                sku,
                product_name,
                description,
                category,
                unit,
                is_active
            FROM inventario.products
            WHERE is_active = TRUE
            ORDER BY product_id;
        """

        products: list[Product] = []

        with self._db_connection.get_conn() as conn:
            with conn.cursor() as cur:
                cur.execute(query)
                rows = cur.fetchall()

        for row in rows:
            product = Product(
                product_id=row[0],
                sku=row[1],
                product_name=row[2],
                description=row[3],
                category=row[4],
                unit=row[5],
                is_active=row[6],
            )
            products.append(product)

        return products
    
    def create_product(self, product: Product) -> Product:
        query = """
            INSERT INTO inventario.products (
                sku,
                product_name,
                description,
                category,
                unit
            )
            VALUES (%s, %s, %s, %s, %s)
            RETURNING
                product_id,
                sku,
                product_name,
                description,
                category,
                unit,
                is_active;
        """

        with self._db_connection.get_conn() as conn:
            with conn.cursor() as cur:
                cur.execute(
                    query,
                    (
                        product.sku,
                        product.product_name,
                        product.description,
                        product.category,
                        product.unit
                    )
                )

                row = cur.fetchone()

            conn.commit()

        return Product(
            product_id=row[0],
            sku=row[1],
            product_name=row[2],
            description=row[3],
            category=row[4],
            unit=row[5],
            is_active=row[6]
        )
    
    def get_product_by_id(self, product_id: int) -> Product | None:
        query = """
            SELECT 
                product_id,
                sku,
                product_name,
                description,
                category,
                unit,
                is_active
            FROM inventario.products
            WHERE product_id = %s;
        """

        with self._db_connection.get_conn() as conn:
            with conn.cursor() as cur:
                cur.execute(query, (product_id,))
                row = cur.fetchone()

        if row is None:
            return None

        return Product(
            product_id=row[0],
            sku=row[1],
            product_name=row[2],
            description=row[3],
            category=row[4],
            unit=row[5],
            is_active=row[6]
        )
    
    def update_product(
        self,
        product_id: int,
        product: Product
    ) -> Product | None:

        query = """
            UPDATE inventario.products
            SET
                sku = %s,
                product_name = %s,
                description = %s,
                category = %s,
                unit = %s,
                is_active = %s,
                updated_at = NOW()
            WHERE product_id = %s
            RETURNING
                product_id,
                sku,
                product_name,
                description,
                category,
                unit,
                is_active;
        """

        with self._db_connection.get_conn() as conn:
            with conn.cursor() as cur:
                cur.execute(
                    query,
                    (
                        product.sku,
                        product.product_name,
                        product.description,
                        product.category,
                        product.unit,
                        product.is_active,
                        product_id
                    )
                )

                row = cur.fetchone()

            conn.commit()

        if row is None:
            return None

        return Product(
            product_id=row[0],
            sku=row[1],
            product_name=row[2],
            description=row[3],
            category=row[4],
            unit=row[5],
            is_active=row[6]
        )
    
    def delete_product(self, product_id: int) -> bool:
        query = """
            UPDATE inventario.products
            SET
                is_active = FALSE,
                updated_at = NOW()
            WHERE product_id = %s;
        """

        with self._db_connection.get_conn() as conn:
            with conn.cursor() as cur:
                cur.execute(query, (product_id,))

                affected_rows = cur.rowcount

            conn.commit()

        return affected_rows > 0
    
    def reactivate_product(self, product_id: int) -> bool:
        query = """
            UPDATE inventario.products
            SET
                is_active = TRUE,
                updated_at = NOW()
            WHERE product_id = %s;
        """

        with self._db_connection.get_conn() as conn:
            with conn.cursor() as cur:
                cur.execute(query, (product_id,))
                affected_rows = cur.rowcount

            conn.commit()

        return affected_rows > 0