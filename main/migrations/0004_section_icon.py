# Generated by Django 2.0.5 on 2018-06-04 09:06

from django.db import migrations, models
import main.models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0003_auto_20180525_1933'),
    ]

    operations = [
        migrations.AddField(
            model_name='section',
            name='icon',
            field=models.ImageField(default='default_pictures/section_default.png', upload_to=main.models.Section.section_icon_path),
        ),
    ]
