# Generated by Django 5.1.2 on 2024-10-24 09:49

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0003_alter_game_image'),
    ]

    operations = [
        migrations.AlterField(
            model_name='booking',
            name='bill_amount',
            field=models.DecimalField(blank=True, decimal_places=2, max_digits=6, null=True),
        ),
    ]
