from databases.models import Location
from .base import BaseUtils
from sqlalchemy.orm import Session

class LocationUtils(BaseUtils):
    def __init__(self, db_session: Session):
        super().__init__(db_session, Location)

    def create(self, city: str, province: str, zipcode: str) -> Location:
        new_location = Location(City=city, Province=province, ZipCode=zipcode)
        self.db.add(new_location)
        print(f"->logs: Lokasi '{city}' ditambahkan ke session.")
        return new_location
