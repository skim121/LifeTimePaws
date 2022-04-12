# Generated by Django 4.0.3 on 2022-04-12 03:42

from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main_app', '0009_alter_animal_due_date'),
    ]

    operations = [
        migrations.AlterField(
            model_name='animal',
            name='favorites',
            field=models.ManyToManyField(blank=True, default=None, related_name='animal', to=settings.AUTH_USER_MODEL),
        ),
    ]
