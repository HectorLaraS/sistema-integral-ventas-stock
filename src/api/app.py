from fastapi import FastAPI
from src.config.settings import settings
from src.config.db_connection import DBConnection
from src.api.routes.product_routes import router as product_router
from src.api.routes.stock_routes import router as stock_router
from src.api.routes.inventory_routes import router as inventory_router


app = FastAPI(
    title=settings.APP_NAME,
    version=settings.APP_VERSION
)

app.include_router(product_router)
app.include_router(stock_router)
app.include_router(inventory_router)


@app.get("/health")
def health_check():
    return {
        "status": "ok",
        "app": settings.APP_NAME,
        "version": settings.APP_VERSION
    }


@app.get("/health/db")
def health_check_db():
    db = DBConnection()

    with db.get_conn() as conn:
        with conn.cursor() as cur:
            cur.execute("SELECT NOW();")
            result = cur.fetchone()

    return {
        "status": "ok",
        "database": "connected",
        "server_time": str(result[0])
    }