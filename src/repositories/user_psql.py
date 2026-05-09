from src.config.db_connection import DBConnection
from src.domain.user import User


class UserPSQL:
    def __init__(self):
        self._db_connection = DBConnection()

    def create_user(self, user: User) -> User:
        query = """
            INSERT INTO inventario.users (
                username,
                password_hash,
                role
            )
            VALUES (%s, %s, %s)
            RETURNING
                user_id,
                username,
                password_hash,
                role,
                is_active,
                created_at;
        """

        with self._db_connection.get_conn() as conn:
            with conn.cursor() as cur:
                cur.execute(
                    query,
                    (
                        user.username,
                        user.password_hash,
                        user.role,
                    )
                )

                row = cur.fetchone()

            conn.commit()

        return User(
            user_id=row[0],
            username=row[1],
            password_hash=row[2],
            role=row[3],
            is_active=row[4],
            created_at=row[5],
        )

    def get_user_by_username(
        self,
        username: str
    ) -> User | None:

        query = """
            SELECT
                user_id,
                username,
                password_hash,
                role,
                is_active,
                created_at
            FROM inventario.users
            WHERE username = %s;
        """

        with self._db_connection.get_conn() as conn:
            with conn.cursor() as cur:
                cur.execute(query, (username,))
                row = cur.fetchone()

        if row is None:
            return None

        return User(
            user_id=row[0],
            username=row[1],
            password_hash=row[2],
            role=row[3],
            is_active=row[4],
            created_at=row[5],
        )