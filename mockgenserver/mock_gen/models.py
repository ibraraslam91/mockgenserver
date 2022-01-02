from django.db import models
from django.contrib.auth import get_user_model
from django.contrib.postgres.fields import JSONField

# Create your models here.

User = get_user_model()


class CreateUpdateMixin(models.Model):
    created_at = models.DateTimeField(auto_now_add=True, editable=False, null=True)
    last_updated_at = models.DateTimeField(auto_now=True, editable=False, null=True)

    class Meta:
        abstract = True


class Project(CreateUpdateMixin):
    name = models.CharField(max_length=255)
    added_by = models.ForeignKey(User, related_name="created_projects", on_delete=models.CASCADE)
    users = models.ManyToManyField(User, related_name="properties", blank=True)
    description = models.TextField()

    def __str__(self):
        return self.name


class Screen(CreateUpdateMixin):
    project = models.ForeignKey(
        Project, related_name="screens", on_delete=models.CASCADE
    )
    name = models.CharField(max_length=255)

    def __str__(self):
        return f"{self.name} - {self.project.name}"


class Layer(CreateUpdateMixin):
    screen = models.ForeignKey(Screen, related_name="layers", on_delete=models.CASCADE)
    mock = JSONField(default=list)

    def __str__(self):
        return f"{self.id} - {self.screen.name}"
