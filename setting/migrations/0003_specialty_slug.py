# Generated by Django 5.0.7 on 2024-07-11 15:46

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('setting', '0002_specialty_image'),
    ]

    operations = [
        migrations.AddField(
            model_name='specialty',
            name='slug',
            field=models.SlugField(default='xxx', max_length=100, unique=True),
            preserve_default=False,
        ),
    ]