# Generated by Django 2.2.4 on 2019-09-09 16:36

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('complaints', '0013_unblockrequest_domain'),
    ]

    operations = [
        migrations.AddField(
            model_name='complaint',
            name='image',
            field=models.ImageField(blank=True, null=True, upload_to=''),
        ),
    ]
