# Generated by Django 3.2.10 on 2021-12-19 15:11

from django.conf import settings
import django.core.validators
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='added_by',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to=settings.AUTH_USER_MODEL),
        ),
        migrations.AlterField(
            model_name='user',
            name='email',
            field=models.CharField(error_messages={'unique': 'This email address is already registered to an account.'}, max_length=150, unique=True, validators=[django.core.validators.EmailValidator()], verbose_name='email'),
        ),
    ]