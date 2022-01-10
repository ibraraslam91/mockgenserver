from rest_framework import serializers

from mockgenserver.mock_gen.models import Project, Screen, Layer
from mockgenserver.users.api.serializers import UserSerializer
from mockgenserver.users.models import User


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
    layers_count = serializers.SerializerMethodField()

    def get_layers_count(self, obj):
        return obj.layers.count()

    class Meta:
        model = Screen
        fields = ["id", "name", "layers_count"]


class ProjectSerializer(serializers.ModelSerializer):
    added_by = serializers.PrimaryKeyRelatedField(read_only=True)
    users = serializers.PrimaryKeyRelatedField(queryset=User.objects.all(), many=True)
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
