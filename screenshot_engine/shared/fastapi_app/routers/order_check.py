import fastapi
import pydantic
from shared.database.db import DBHandler

router = fastapi.APIRouter()


class OrderCheck(pydantic.BaseModel):
    order_id: str
    secret_key: str | None = None


@router.get("/")
async def order_detail_check(order_check: OrderCheck):
    order = DBHandler.get_order(order_check.order_id)
    if not order:
        raise fastapi.HTTPException(status_code=404, detail="Order not found")
    
    return order