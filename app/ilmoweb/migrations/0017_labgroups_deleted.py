# Generated by Django 4.2.5 on 2023-10-31 12:12

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('ilmoweb', '0016_alter_report_filename'),
    ]

    operations = [
        migrations.AddField(
            model_name='labgroups',
            name='deleted',
            field=models.BooleanField(default=0),
        ),
    ]