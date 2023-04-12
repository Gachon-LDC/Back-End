# Generated by Django 4.1.7 on 2023-04-12 06:56

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("App", "0001_initial"),
    ]

    operations = [
        migrations.CreateModel(
            name="VideoAngleModel",
            fields=[
                ("angle_id", models.UUIDField(primary_key=True, serialize=False)),
                ("embeds", models.TextField()),
                ("video_id", models.UUIDField()),
            ],
        ),
        migrations.RemoveField(
            model_name="videomodel",
            name="embeds",
        ),
        migrations.RemoveField(
            model_name="videomodel",
            name="file_path",
        ),
        migrations.AddField(
            model_name="usermodel",
            name="salt",
            field=models.TextField(default=""),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name="videomodel",
            name="content",
            field=models.TextField(default=""),
        ),
        migrations.AddField(
            model_name="videomodel",
            name="title",
            field=models.TextField(default=""),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name="videomodel",
            name="uploader_id",
            field=models.UUIDField(),
        ),
    ]