from rest_framework.serializers import ModelSerializer
from .models import AppUser


class UserSerializer(ModelSerializer):

    class Meta:
        model = AppUser
        fields = "__all__"

    def create(self, data):
        new_user = AppUser(**data)
        new_user.is_staff = False
        new_user.is_superuser = False
        new_user.set_password(data.get("password"))
        new_user.full_clean()
        new_user.save()
        return new_user
