from app.base.resource import BaseResource
from app.users.model import User
from app.users.schemas import UserSchema
from app.base.models import save


class UserResource(BaseResource):
    model = User
    schema = UserSchema()

    def register_sms_user(self, user_data):
        errors = self.schema.validate(user_data)
        if errors:
            return {"error": True, "errors": str(errors)}, 400
        item = self.model(**user_data)

        try:
            save(item)
            return self.schema.dump(item), 201
        except Exception as e:
            return {"error": e.args}, 500
