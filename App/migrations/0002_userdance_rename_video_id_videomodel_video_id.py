# Generated by Django 4.1.3 on 2022-12-01 04:23

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('App', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='UserDance',
            fields=[
                ('video_id', models.UUIDField(primary_key=True, serialize=False)),
                ('user_id', models.UUIDField()),
                ('image_id', models.IntegerField()),
                ('image', models.TextField()),
                ('end_image', models.BooleanField(default=False)),
            ],
        ),
        migrations.RenameField(
            model_name='videomodel',
            old_name='Video_id',
            new_name='video_id',
        ),
    ]
