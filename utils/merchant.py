from databases.models import Merchant
from .base import BaseUtils
from sqlalchemy.orm import Session
import pandas as pd

class MerchantUtils(BaseUtils):
    def __init__(self, db_session: Session):
        super().__init__(db_session, Merchant)

    def create(self, admin_id: int, location_id: int) -> Merchant:
        new_merchant = Merchant(AdminID=admin_id, LocationID=location_id)
        self.db.add(new_merchant)
        print(f"->logs: Merchant untuk Admin ID {admin_id} ditambahkan ke session.")
        return new_merchant
    
    def toDataFrame(self, admin_id: int, location_id: int) -> pd.DataFrame:
        all_merchants = self.getAll()

        if not all_merchants:
            return pd.DataFrame()
        
        merchants_data = [
            {
                "ID": merchant.ID,
                "LocationID": merchant.LocationID,
                "AdminID": merchant.AdminID
            }
            for merchant in all_merchants
        ]
        return pd.DataFrame(merchants_data).set_index("ID")

