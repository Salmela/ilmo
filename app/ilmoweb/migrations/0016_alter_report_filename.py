from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('ilmoweb', '0015_alter_report_filename'),
    ]

    operations = [
        migrations.AlterField(
            model_name='report',
            name='filename',
            field=models.FileField(null=True, upload_to='ilmoweb/static/upload/'),
        ),
    ]
