
from db.models import User
from api.crud import CRUDBase
from api.schemas import UserUpdate, UserCreate


class CRUDUser(CRUDBase[User, UserCreate, UserUpdate]):
    ...


user = CRUDUser(User)
