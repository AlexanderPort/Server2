from django.db import models


class User(models.Model):
    id = models.UUIDField(primary_key=True, auto_created=True)
    name = models.CharField(max_length=1024)
    lastname = models.CharField(max_length=1024)
    tracks = models.ManyToManyField(to='Track')
    artists = models.ManyToManyField(to='Artist')
    albums = models.ManyToManyField(to='Album')

    def __str__(self):
        return f'Artist(name={self.name}, surname={self.lastname})'


class Artist(models.Model):
    id = models.UUIDField(primary_key=True, auto_created=True)
    name = models.CharField(max_length=1024)

    def __str__(self):
        return f'Artist(name={self.name}, surname={self.lastname})'


class Track(models.Model):
    id = models.UUIDField(primary_key=True, auto_created=True)
    album = models.ForeignKey(to='Album', null=True, on_delete=models.PROTECT)
    author = models.ForeignKey(to='Artist', on_delete=models.CASCADE)
    title = models.CharField(max_length=1024)
    description = models.CharField(max_length=1024)
    track = models.FilePathField()
    thumbnail = models.FilePathField()
    views = models.PositiveIntegerField(default=0)
    url = models.URLField(max_length=1024)

    def __str__(self):
        return f'Track(name={self.name})'


class Album(models.Model):
    id = models.UUIDField(primary_key=True, auto_created=True)
    title = models.CharField(max_length=1024)
    author = models.ForeignKey(to='Artist', null=True, on_delete=models.PROTECT)

