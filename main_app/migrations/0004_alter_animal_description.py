# Generated by Django 4.0.3 on 2022-04-10 06:11

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main_app', '0003_alter_animal_description'),
    ]

    operations = [
        migrations.AlterField(
            model_name='animal',
            name='description',
            field=models.CharField(blank=True, default=1, max_length=250),
            preserve_default=False,
        ),
    ]
