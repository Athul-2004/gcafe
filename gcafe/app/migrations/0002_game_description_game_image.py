# Generated by Django 5.1.2 on 2024-10-24 07:44

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='game',
            name='description',
            field=models.CharField(default='placeholder description', max_length=200),
        ),
        migrations.AddField(
            model_name='game',
            name='image',
            field=models.URLField(default='https://via.placeholder.com/400'),
        ),
    ]