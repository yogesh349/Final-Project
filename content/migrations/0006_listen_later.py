# Generated by Django 4.0.3 on 2022-05-23 04:56

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('content', '0005_alter_song_song'),
    ]

    operations = [
        migrations.CreateModel(
            name='Listen_Later',
            fields=[
                ('watch_id', models.AutoField(primary_key=True, serialize=False)),
                ('video_id', models.CharField(default='', max_length=100000)),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]