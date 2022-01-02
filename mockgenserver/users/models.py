from django.conf import settings
from django.contrib.auth.models import AbstractUser
from django.db import models
from django.urls import reverse
from django.utils.translation import gettext_lazy as _
from django.core.validators import validate_email


class Company(models.Model):
    name = models.CharField(max_length=50)

    def __str__(self):
        return self.name


class User(AbstractUser):
    """Default user for MockGenServer."""

    #: First and last name do not cover name patterns around the globe

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = []

    name = models.CharField(_("Name of User"), blank=True, max_length=255)
    first_name = None  # type: ignore
    last_name = None  # type: ignore

    added_by = models.ForeignKey(
        settings.AUTH_USER_MODEL, null=True, blank=True, on_delete=models.SET_NULL
    )
    email = models.CharField(
        _("email"),
        max_length=150,
        unique=True,
        validators=[validate_email],
        error_messages={
            "unique": _("This email address is already registered to an account."),
        },
    )
    company = models.ForeignKey(
        Company, related_name="users", on_delete=models.CASCADE, blank=True, null=True
    )

    def get_absolute_url(self):
        """Get url for user's detail view.

        Returns:
            str: URL for user detail.

        """
        return reverse("users:detail", kwargs={"username": self.username})
