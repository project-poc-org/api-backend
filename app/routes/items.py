from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from ..auth import get_current_user
from ..db import get_db
from ..logging_config import configure_logging
from ..models import ItemDB
from ..schemas import Item, ItemCreate, Items


router = APIRouter(prefix="/items", tags=["items"])
logger = configure_logging("api-backend")


@router.post("", response_model=Item)
def create_item(
    item: ItemCreate,
    db: Session = Depends(get_db),
    current_user: str = Depends(get_current_user),
):
    db_item = ItemDB(name=item.name, description=item.description)
    db.add(db_item)
    db.commit()
    db.refresh(db_item)
    logger.info("/items created", extra={"user": current_user, "item_id": db_item.id})
    return Item(id=db_item.id, name=db_item.name, description=db_item.description)


@router.get("", response_model=Items)
def list_items(
    db: Session = Depends(get_db),
    current_user: str = Depends(get_current_user),
):
    items = db.query(ItemDB).all()
    logger.info("/items listed", extra={"user": current_user, "count": len(items)})
    return [Item(id=i.id, name=i.name, description=i.description) for i in items]
