# Generated by Django 4.2.5 on 2023-09-26 13:28

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('ilmoweb', '0002_alter_user_student_id'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='labgroups',
            name='is_visible',
        ),
        migrations.AddField(
            model_name='labgroups',
            name='status',
            field=models.IntegerField(default=0),
        ),
    ]
