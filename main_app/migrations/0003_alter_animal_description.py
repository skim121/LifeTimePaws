# Generated by Django 4.0.3 on 2022-04-10 05:53

import ckeditor.fields
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('main_app', '0002_alter_animal_description_alter_animal_due_date'),
    ]

    operations = [
        migrations.AlterField(
            model_name='animal',
            name='description',
            field=ckeditor.fields.RichTextField(blank=True, null=True),
        ),
    ]