# Generated by Django 3.1.2 on 2020-11-11 07:45

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0005_views'),
    ]

    operations = [
        migrations.AddField(
            model_name='posts',
            name='page_id',
            field=models.IntegerField(default='0'),
        ),
    ]
