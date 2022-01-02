from django.contrib.auth import get_user_model
from rest_framework import serializers

from mockgenserver.users.models import Company

User = get_user_model()


class UserSerializer(serializers.ModelSerializer):

    username = serializers.CharField()
    email = serializers.CharField()
    password = serializers.CharField(write_only=True)
    company = serializers.PrimaryKeyRelatedField(queryset=Company.objects.all())

    def create(self, validated_data):
        user = super().create(validated_data)
        user.set_password(validated_data["password"])
        user.save()
        return user

    class Meta:
        model = User
        fields = ["id", "username", "email", "password", "company"]

        extra_kwargs = {
            "url": {"view_name": "api:user-detail", "lookup_field": "username"}
        }


class LoginRequestSerializer(serializers.Serializer):
    email = serializers.EmailField()
    password = serializers.CharField()
