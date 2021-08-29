from sqlalchemy.orm import Session

from . import models, schemas
from .schemas import ItemCreate

def create_item(db: Session, item: ItemCreate):
    db_item = models.Item(**item.dict())
    db.add(db_item)
    db.commit()
    db.refresh(db_item)
    return db_item