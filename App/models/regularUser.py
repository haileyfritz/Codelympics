from App.models import User
from App.database import db

class RegularUser(User):
    __tablename__ = 'regular_user'