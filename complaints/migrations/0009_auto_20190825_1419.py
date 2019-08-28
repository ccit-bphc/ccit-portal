# Generated by Django 2.2.4 on 2019-08-25 08:49

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('complaints', '0008_auto_20190824_1940'),
    ]

    operations = [
        migrations.AlterField(
            model_name='unblockrequest',
            name='url',
            field=models.TextField(error_messages={'unique': 'This url is already under consideration'}, unique=True, validators=[django.core.validators.RegexValidator(message='This is not a valid URL.', regex='^(([^:/?#]+):)?(//([^/?#]*))?([^?#]*)(\\?([^#]*))?(#(.*))?')]),
        ),
    ]