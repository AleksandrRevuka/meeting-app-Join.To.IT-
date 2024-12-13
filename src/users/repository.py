from src.adapters.repository import AsyncRepository
from src.users.orm import User
from src.users.schemas import PrivateUser


class UsersRepository(AsyncRepository[User, PrivateUser]):
    model = User
    schema = PrivateUser