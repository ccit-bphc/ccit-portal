# Generated by Django 2.2.4 on 2019-09-06 08:49

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('complaints', '0012_auto_20190904_0002'),
    ]

    operations = [
        migrations.AddField(
            model_name='unblockrequest',
            name='domain',
            field=models.CharField(blank=True, max_length=200),
        ),
    ]
