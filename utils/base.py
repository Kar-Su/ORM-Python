from sqlalchemy.orm import Session
from typing import List, Optional, Type, TypeVar
from databases.basemodel import base as BaseModel

T = TypeVar('T', bound=BaseModel)

# utilitas dasar yang dapat diwariskan dan digunakan oleh kelas turunannya
class BaseUtils:
    def __init__(self, sessionDB: Session, model: Type[T]):
        self.db = sessionDB
        self.model = model

    def getByID(self, itemID: int) -> Optional[T]:
        return self.db.query(self.model).filter(self.model.ID == itemID).first()

    def getAll(self) -> List[T]:
        return self.db.query(self.model).all()

    def delete(self, itemID: int) -> bool:
        try:
            item_deleted = self.getByID(itemID)
            if not item_deleted:
                print(f"logs: Item ID {itemID} tidak ditemukan")
                return False
            
            self.db.delete(item_deleted)
            print(f"logs: Item ID {itemID} dari tabel {self.model.__tablename__} berhasil dihapus")
            return True
        except Exception as e:
            print(f"Error deleting item: {e}")
            return False
