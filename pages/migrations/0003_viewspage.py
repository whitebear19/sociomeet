# Generated by Django 3.1.2 on 2020-11-11 06:49

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('pages', '0002_likepage'),
    ]

    operations = [
        migrations.CreateModel(
            name='ViewsPage',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('user_id', models.IntegerField(default='', null=True)),
                ('page_id', models.IntegerField(default='', null=True)),
                ('created_at', models.DateTimeField(auto_now_add=True, null=True)),
            ],
            options={
                'db_table': 'viewspage',
            },
        ),
    ]
