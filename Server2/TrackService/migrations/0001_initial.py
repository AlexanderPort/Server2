# Generated by Django 3.1.7 on 2021-05-03 09:55

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Album',
            fields=[
                ('id', models.UUIDField(auto_created=True, primary_key=True, serialize=False)),
                ('title', models.CharField(max_length=1024)),
            ],
        ),
        migrations.CreateModel(
            name='Artist',
            fields=[
                ('id', models.UUIDField(auto_created=True, primary_key=True, serialize=False)),
                ('name', models.CharField(max_length=1024)),
            ],
        ),
        migrations.CreateModel(
            name='Track',
            fields=[
                ('id', models.UUIDField(auto_created=True, primary_key=True, serialize=False)),
                ('title', models.CharField(max_length=1024)),
                ('description', models.CharField(max_length=1024)),
                ('track', models.FilePathField()),
                ('thumbnail', models.FilePathField()),
                ('views', models.PositiveIntegerField(default=0)),
                ('url', models.URLField(max_length=1024)),
                ('album', models.ForeignKey(null=True, on_delete=django.db.models.deletion.PROTECT, to='TrackService.album')),
                ('author', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='TrackService.artist')),
            ],
        ),
        migrations.CreateModel(
            name='User',
            fields=[
                ('id', models.UUIDField(auto_created=True, primary_key=True, serialize=False)),
                ('name', models.CharField(max_length=1024)),
                ('lastname', models.CharField(max_length=1024)),
                ('albums', models.ManyToManyField(to='TrackService.Album')),
                ('artists', models.ManyToManyField(to='TrackService.Artist')),
                ('tracks', models.ManyToManyField(to='TrackService.Track')),
            ],
        ),
        migrations.AddField(
            model_name='album',
            name='author',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.PROTECT, to='TrackService.artist'),
        ),
    ]
