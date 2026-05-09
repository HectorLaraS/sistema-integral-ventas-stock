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

@router.get("", response_model=list[InventoryMovementResponse])
def list_movements():
    service = InventoryService()
    movements = service.list_movements()

    return [
        InventoryMovementResponse(
            movement_id=item.movement_id,
            product_id=item.product_id,
            movement_type=item.movement_type,
            quantity=item.quantity,
            reference_text=item.reference_text,
            notes=item.notes,
            created_by=item.created_by,
            created_at=item.created_at,
        )
        for item in movements
    ]

@router.get("/{movement_id}",response_model=InventoryMovementResponse)
def get_movement_by_id(movement_id: int):
    service = InventoryService()

    movement = service.get_movement_by_id(
        movement_id
    )

    if movement is None:
        raise HTTPException(
            status_code=404,
            detail="Movement not found"
        )

    return InventoryMovementResponse(
        movement_id=movement.movement_id,
        product_id=movement.product_id,
        movement_type=movement.movement_type,
        quantity=movement.quantity,
        reference_text=movement.reference_text,
        notes=movement.notes,
        created_by=movement.created_by,
        created_at=movement.created_at,
    )