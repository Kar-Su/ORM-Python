from .base import BaseUtils
from databases.models import User
from sqlalchemy.orm import Session
from typing import Optional
from datetime import datetime
import pandas as pd

class UserUtils(BaseUtils):
    def __init__(self, sessionDB: Session):
        super().__init__(sessionDB, User)

    def create(self, username: str, email: str) -> User:
        new_user = User(UserName=username,
                        Email=email,
                        CreatedAt=datetime.now())

        self.db.add(new_user)
        print(f"logs: {username} ditambahkan ke session")
        return new_user

    def UpdateEmail(self, userID: int, newEmail: str) -> Optional[User]:
        user_update = self.getByID(userID)
        if user_update:
            user_update.Email = newEmail
            print(f"logs: Email dari User({userID}) Dimasukkan ke query")

    def toDataFrame(self) -> pd.DataFrame:
        all_users = self.getAll()

        if not all_users:
            return pd.DataFrame()
        
        users_data = [
            {
                "ID": user.ID,
                "Name": user.UserName,
                "Email": user.Email,
                "CreatedAt": user.CreatedAt.strftime("%Y-%m-%d %H:%M:%S") if user.CreatedAt else None
            }
            for user in all_users
        ]
        return pd.DataFrame(users_data).set_index('ID')
