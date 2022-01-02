from rest_framework import serializers

from mockgenserver.mock_gen.models import Project, Screen, Layer
from mockgenserver.users.models import User
from mockgenserver.users.api.serializers import UserSerializer


class LayerSerializer(serializers.ModelSerializer):
    mock = serializers.JSONField()

    class Meta:
        model = Layer
        fields = ["id", "mock"]


class ScreenSerializer(serializers.ModelSerializer):
    project = serializers.PrimaryKeyRelatedField(queryset=Project.objects.all())
    layers = LayerSerializer(many=True, read_only=True)

    class Meta:
        model = Screen
        fields = "__all__"


class ScreenListSerializer(serializers.ModelSerializer):
    name = serializers.CharField()
    id = serializers.IntegerField()

    class Meta:
        model = Screen
        fields = ["id", "name"]


class ProjectSerializer(serializers.ModelSerializer):
    added_by = serializers.PrimaryKeyRelatedField(queryset=User.objects.all())
    users = serializers.PrimaryKeyRelatedField(read_only=True, many=True)
    screens = ScreenListSerializer(many=True, read_only=True)

    class Meta:
        model = Project
        fields = "__all__"

    def create(self, validated_data):
        project = super(ProjectSerializer, self).create(validated_data)
        project.users.add(project.added_by)
        return project

    def to_representation(self, instance):
        data = super().to_representation(instance)
        data.update(
            {"added_by": UserSerializer(User.objects.get(id=instance.added_by.id)).data}
        )
        return data
