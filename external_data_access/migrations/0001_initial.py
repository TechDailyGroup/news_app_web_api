# Generated by Django 2.0.5 on 2018-05-15 07:20

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('main', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='ArticleText',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('text', models.TextField(null=True)),
                ('article', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to='main.Article')),
            ],
        ),
    ]
