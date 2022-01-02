import requests
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated
from rest_framework.views import Response, status
from rest_framework.viewsets import ModelViewSet
from rest_framework_extensions.mixins import NestedViewSetMixin

from mockgenserver.mock_gen.api.serializers import ProjectSerializer, ScreenSerializer
from mockgenserver.mock_gen.models import Project, Screen, Layer
from mockgenserver.mock_gen.api.utils import transform_mocks


class ProjectViewSet(NestedViewSetMixin, ModelViewSet):

    permission_classes = (IsAuthenticated,)
    serializer_class = ProjectSerializer

    def get_queryset(self):
        return Project.objects.filter(users__in=[self.request.user])

    def create(self, request, *args, **kwargs):
        request_data = request.data
        request_data["added_by"] = request.user.id
        return super().create(request)


class ScreenViewSet(NestedViewSetMixin, ModelViewSet):
    base_url = "https://8f82-35-196-217-243.ngrok.io"
    url = f"{base_url}/mock_gen"

    queryset = Screen.objects.all()

    serializer_class = ScreenSerializer

    def create(self, request, *args, **kwargs):
        request_data = request.data
        request_data["project"] = kwargs.get("parent_lookup_project")
        return super().create(request)

    @action(detail=True, methods=["POST"])
    def add_layer(self, request, pk=None, *args, **kwargs):
        file = request.FILES["img"].file
        # with open("image.png", "wb") as out_file:
        #     out_file.write(file.read())
        # file.seek(0)
        files = {"file": ("image.jpg", file.read())}
        r = requests.post(self.url, files=files)
        mocks = r.json()
        transformed_mocks = transform_mocks(mocks)
        if transformed_mocks:
            Layer.objects.create(screen_id=pk, mock=transformed_mocks)
        print("#"*40)
        print(transformed_mocks)
        print("#" * 40)
        return Response(data=transformed_mocks, status=status.HTTP_200_OK)


#[{'score': 0.9840945601463318, 'element': 'textarea', 'bbox': [667, 145, 245, 99]},
# {'score': 0.8314349055290222, 'element': 'image', 'bbox': [681, 280, 104, 81]}]
