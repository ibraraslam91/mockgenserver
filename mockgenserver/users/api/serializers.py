from django.contrib.auth import get_user_model
from django.contrib.auth.models import Group
from rest_framework import serializers

from mockgenserver.users.models import Company

User = get_user_model()


class UserSerializer(serializers.ModelSerializer):

    username = serializers.CharField()
    email = serializers.CharField()
    password = serializers.CharField(write_only=True)
    company = serializers.PrimaryKeyRelatedField(queryset=Company.objects.all())
    groups = serializers.PrimaryKeyRelatedField(
        write_only=True, many=True, queryset=Group.objects.all()
    )

    def create(self, validated_data):
        user = super().create(validated_data)
        user.set_password(validated_data["password"])
        user.save()
        return user

    def to_representation(self, instance):
        data = super().to_representation(instance)
        data.update({"groups": instance.groups.values_list("name", flat=True)})
        return data

    class Meta:
        model = User
        fields = ["id", "username", "email", "password", "company", "groups"]

        extra_kwargs = {
            "url": {"view_name": "api:user-detail", "lookup_field": "username"}
        }

class GroupSerializer(serializers.ModelSerializer):

    class Meta:
        model = Group
        fields = ["id", "name"]


class LoginRequestSerializer(serializers.Serializer):
    email = serializers.EmailField()
    password = serializers.CharField()
