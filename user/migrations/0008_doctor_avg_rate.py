# Generated by Django 5.0.7 on 2024-07-14 09:40

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('user', '0007_account_image'),
    ]

    operations = [
        migrations.AddField(
            model_name='doctor',
            name='avg_rate',
            field=models.FloatField(default=0),
        ),
    ]