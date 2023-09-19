from app.base.resource import BaseResource
from app.users.model import User
from app.users.schemas import UserSchema


class UserResource(BaseResource):
    model = User
    schema = UserSchema()
