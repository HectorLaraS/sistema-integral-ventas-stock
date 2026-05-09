from src.domain.inventory_movement import InventoryMovement
from src.repositories.inventory_psql import InventoryPSQL


class InventoryService:
    def __init__(self):
        self._repository = InventoryPSQL()

    def register_in(self, movement: InventoryMovement) -> InventoryMovement:
        if movement.quantity is None or movement.quantity <= 0:
            raise ValueError("Quantity must be greater than zero")

        return self._repository.register_in(movement)
    
    def register_out(self, movement: InventoryMovement) -> InventoryMovement:
        if movement.quantity is None or movement.quantity <= 0:
            raise ValueError("Quantity must be greater than zero")

        return self._repository.register_out(movement)
    
    def list_movements(self) -> list[InventoryMovement]:
        return self._repository.list_movements()
    
    def get_movement_by_id(self,movement_id: int) -> InventoryMovement | None:
        return self._repository.get_movement_by_id(movement_id)