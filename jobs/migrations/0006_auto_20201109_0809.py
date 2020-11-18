# Generated by Django 3.1.2 on 2020-11-09 08:09

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('jobs', '0005_auto_20201109_0758'),
    ]

    operations = [
        migrations.AlterField(
            model_name='jobs',
            name='benefits',
            field=models.TextField(blank=True, default='', max_length=1000, null=True),
        ),
        migrations.AlterField(
            model_name='jobs',
            name='client',
            field=models.CharField(blank=True, default='', max_length=250, null=True),
        ),
        migrations.AlterField(
            model_name='jobs',
            name='email',
            field=models.CharField(blank=True, default='', max_length=250, null=True),
        ),
        migrations.AlterField(
            model_name='jobs',
            name='job_city',
            field=models.CharField(blank=True, default='', max_length=50, null=True),
        ),
        migrations.AlterField(
            model_name='jobs',
            name='job_country',
            field=models.CharField(blank=True, default='', max_length=50, null=True),
        ),
        migrations.AlterField(
            model_name='jobs',
            name='job_state',
            field=models.CharField(blank=True, default='', max_length=50, null=True),
        ),
        migrations.AlterField(
            model_name='jobs',
            name='job_zip',
            field=models.CharField(blank=True, default='', max_length=10, null=True),
        ),
        migrations.AlterField(
            model_name='jobs',
            name='jobtype',
            field=models.CharField(blank=True, default='', max_length=250, null=True),
        ),
        migrations.AlterField(
            model_name='jobs',
            name='lat',
            field=models.CharField(blank=True, default='', max_length=250, null=True),
        ),
        migrations.AlterField(
            model_name='jobs',
            name='lng',
            field=models.CharField(blank=True, default='', max_length=250, null=True),
        ),
        migrations.AlterField(
            model_name='jobs',
            name='location',
            field=models.CharField(blank=True, default='', max_length=50, null=True),
        ),
        migrations.AlterField(
            model_name='jobs',
            name='period',
            field=models.CharField(blank=True, default='', max_length=250, null=True),
        ),
        migrations.AlterField(
            model_name='jobs',
            name='phone',
            field=models.CharField(blank=True, default='', max_length=250, null=True),
        ),
        migrations.AlterField(
            model_name='jobs',
            name='remote',
            field=models.CharField(blank=True, default='', max_length=250, null=True),
        ),
        migrations.AlterField(
            model_name='jobs',
            name='reply',
            field=models.CharField(blank=True, default='', max_length=1, null=True),
        ),
        migrations.AlterField(
            model_name='jobs',
            name='salary',
            field=models.CharField(blank=True, default='', max_length=250, null=True),
        ),
        migrations.AlterField(
            model_name='jobs',
            name='status',
            field=models.CharField(blank=True, default='1', max_length=1, null=True),
        ),
        migrations.AlterField(
            model_name='jobs',
            name='travel',
            field=models.CharField(blank=True, default='', max_length=250, null=True),
        ),
        migrations.AlterField(
            model_name='jobs',
            name='url',
            field=models.CharField(blank=True, default='', max_length=250, null=True),
        ),
        migrations.AlterField(
            model_name='jobs',
            name='workauth',
            field=models.TextField(blank=True, default='', max_length=1000, null=True),
        ),
    ]
