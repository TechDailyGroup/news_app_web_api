# Generated by Django 2.0.5 on 2018-09-02 12:21

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('external_data_access', '0003_auto_20180531_1728'),
    ]

    operations = [
        migrations.AlterField(
            model_name='articletext',
            name='indexed_by_es',
            field=models.BooleanField(db_index=True, default=False),
        ),
        migrations.AlterField(
            model_name='articletext',
            name='indexed_by_solr',
            field=models.BooleanField(db_index=True, default=False),
        ),
    ]
