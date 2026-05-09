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
    
    def register_out(self, movement: InventoryMovement) -> InventoryMovement:
        get_stock_query = """
            SELECT quantity_on_hand
            FROM inventario.inventory_stock
            WHERE product_id = %s
            FOR UPDATE;
        """

        insert_movement_query = """
            INSERT INTO inventario.inventory_movements (
                product_id,
                movement_type,
                quantity,
                reference_text,
                notes,
                created_by
            )
            VALUES (%s, 'OUT', %s, %s, %s, %s)
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

        update_stock_query = """
            UPDATE inventario.inventory_stock
            SET
                quantity_on_hand = quantity_on_hand - %s,
                updated_at = NOW()
            WHERE product_id = %s;
        """

        with self._db_connection.get_conn() as conn:
            with conn.cursor() as cur:
                cur.execute(get_stock_query, (movement.product_id,))
                stock_row = cur.fetchone()

                if stock_row is None:
                    raise ValueError("Product has no stock record")

                current_stock = stock_row[0]

                if current_stock < movement.quantity:
                    raise ValueError("Not enough stock available")

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
                    update_stock_query,
                    (
                        movement.quantity,
                        movement.product_id,
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