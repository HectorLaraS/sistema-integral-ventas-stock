from fastapi import APIRouter, HTTPException
from src.domain.inventory_movement import InventoryMovement
from src.services.inventory_service import InventoryService
from src.api.schemas.inventory_schema import (
    InventoryInRequest,
    InventoryOutRequest,
    InventoryMovementResponse,
)


router = APIRouter(
    prefix="/movements",
    tags=["Inventory Movements"]
)


@router.post("/in", response_model=InventoryMovementResponse)
def register_inventory_in(request: InventoryInRequest):
    service = InventoryService()

    movement = InventoryMovement(
        product_id=request.product_id,
        quantity=request.quantity,
        reference_text=request.reference_text,
        notes=request.notes,
        created_by=request.created_by,
    )

    try:
        result = service.register_in(movement)
    except ValueError as error:
        raise HTTPException(
            status_code=400,
            detail=str(error)
        )

    return InventoryMovementResponse(
        movement_id=result.movement_id,
        product_id=result.product_id,
        movement_type=result.movement_type,
        quantity=result.quantity,
        reference_text=result.reference_text,
        notes=result.notes,
        created_by=result.created_by,
        created_at=result.created_at,
    )

@router.post("/out", response_model=InventoryMovementResponse)
def register_inventory_out(request: InventoryOutRequest):
    service = InventoryService()

    movement = InventoryMovement(
        product_id=request.product_id,
        quantity=request.quantity,
        reference_text=request.reference_text,
        notes=request.notes,
        created_by=request.created_by,
    )

    try:
        result = service.register_out(movement)
    except ValueError as error:
        raise HTTPException(
            status_code=400,
            detail=str(error)
        )

    return InventoryMovementResponse(
        movement_id=result.movement_id,
        product_id=result.product_id,
        movement_type=result.movement_type,
        quantity=result.quantity,
        reference_text=result.reference_text,
        notes=result.notes,
        created_by=result.created_by,
        created_at=result.created_at,
    )