from fastapi import Depends, APIRouter, HTTPException
from ..tiny_database.db import DBHandler


router = APIRouter()


def get_db_handler():
    """Placeholder for the actual DBHandler."""
    raise NotImplementedError("Dependency not provided!")


@router.get("/")
async def order_detail_check(
    order_id: str,
    secret_key: str | None = None,
    db_handler: DBHandler = Depends(get_db_handler),
):
    order = db_handler.get_order(order_id)
    if not order:
        raise HTTPException(status_code=404, detail="Order not found")

    return order
