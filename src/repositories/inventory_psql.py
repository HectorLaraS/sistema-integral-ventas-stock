from src.config.db_connection import DBConnection
from src.domain.inventory_movement import InventoryMovement


class InventoryPSQL:
    def __init__(self):
        self._db_connection = DBConnection()

    def register_in(self, movement: InventoryMovement) -> InventoryMovement:
        insert_movement_query = """
            INSERT INTO inventario.inventory_movements (
                product_id,
                movement_type,
                quantity,
                reference_text,
                notes,
                created_by
            )
            VALUES (%s, 'IN', %s, %s, %s, %s)
            RETURNING
                movement_id,
                product_id,
                movement_type,
                quantity,
                reference_text,
                notes,
                created_by,
                created_at;
        """

        upsert_stock_query = """
            INSERT INTO inventario.inventory_stock (
                product_id,
                quantity_on_hand
            )
            VALUES (%s, %s)
            ON CONFLICT (product_id)
            DO UPDATE SET
                quantity_on_hand = inventario.inventory_stock.quantity_on_hand + EXCLUDED.quantity_on_hand,
                updated_at = NOW();
        """

        with self._db_connection.get_conn() as conn:
            with conn.cursor() as cur:
                cur.execute(
                    insert_movement_query,
                    (
                        movement.product_id,
                        movement.quantity,
                        movement.reference_text,
                        movement.notes,
                        movement.created_by,
                    )
                )

                row = cur.fetchone()

                cur.execute(
                    upsert_stock_query,
                    (
                        movement.product_id,
                        movement.quantity,
                    )
                )

            conn.commit()

        return InventoryMovement(
            movement_id=row[0],
            product_id=row[1],
            movement_type=row[2],
            quantity=row[3],
            reference_text=row[4],
            notes=row[5],
            created_by=row[6],
            created_at=row[7],
        )