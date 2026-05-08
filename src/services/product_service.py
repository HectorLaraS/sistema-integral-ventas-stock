from src.repositories.product_psql import ProductPSQL
from src.domain.product import Product


class ProductService:
    def __init__(self):
        self._repository = ProductPSQL()

    def list_products(self) -> list[Product]:
        return self._repository.list_products()
    
    def create_product(self, product: Product) -> Product:
        return self._repository.create_product(product)
    
    def get_product_by_id(self, product_id: int) -> Product | None:
        return self._repository.get_product_by_id(product_id)
    
    def update_product(
        self,
        product_id: int,
        product: Product
    ) -> Product | None:

        return self._repository.update_product(
            product_id,
            product
        )   

    def delete_product(self, product_id: int) -> bool:
        return self._repository.delete_product(product_id)
    
    def reactivate_product(self, product_id: int) -> bool:
        return self._repository.reactivate_product(product_id)