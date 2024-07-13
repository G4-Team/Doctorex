# Generated by Django 5.0.7 on 2024-07-12 22:47

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('reservation', '0001_initial'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Comment',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('score', models.IntegerField(choices=[(1, 'very bad'), (2, 'bad'), (3, 'not bad'), (4, 'good'), (5, 'very good')], default=3)),
                ('title', models.CharField(max_length=50)),
                ('text', models.CharField(max_length=1000)),
                ('author', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='comments', to=settings.AUTH_USER_MODEL)),
                ('reply_to', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='replies', to='reservation.comment')),
                ('reservation', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='comments', to='reservation.reservation')),
            ],
        ),
    ]