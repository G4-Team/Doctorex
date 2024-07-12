# Generated by Django 5.0.7 on 2024-07-12 13:40

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('setting', '0004_alter_specialty_image'),
        ('user', '0005_doctor_balance'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='doctor',
            name='balance',
        ),
        migrations.RemoveField(
            model_name='patient',
            name='balance',
        ),
        migrations.AddField(
            model_name='account',
            name='balance',
            field=models.IntegerField(default=0),
        ),
        migrations.AddField(
            model_name='account',
            name='is_doctor',
            field=models.BooleanField(default=False),
        ),
        migrations.AlterField(
            model_name='doctor',
            name='account',
            field=models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
        migrations.AlterField(
            model_name='doctor',
            name='specialty',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='doctors', to='setting.specialty'),
        ),
        migrations.AlterField(
            model_name='patient',
            name='account',
            field=models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
    ]