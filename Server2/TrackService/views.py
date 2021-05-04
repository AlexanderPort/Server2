from django.shortcuts import render
from rest_framework.response import Response
from rest_framework.decorators import api_view
from rest_framework import status

from django.http import JsonResponse, FileResponse
from . import models, serializers
from django.conf import settings
import requests
import os
import uuid
import random

import youtube_dl

EXTENSIONS = ['.jpg', '.jpeg', '.png', '.webp']
RESOURCES = f'{settings.BASE_DIR}/resources'
MAX = 281474976710655  # 2 ** 48 - 1


@api_view(['POST'])
def post_track(request):
    if request.method == 'POST':
        if 'url' in request.data:
            url = request.data.get('url')
            if models.Track.objects.filter(url=url).exists():
                return JsonResponse({'status': False})

            ID = uuid.uuid1(random.randint(0, MAX))
            directory = f'{RESOURCES}/tracks/{ID}'
            options = {
                'format': 'bestaudio/best',
                'outtmpl': f'{directory}/track.mp3'
            }
            ydl = youtube_dl.YoutubeDL(options)
            info = ydl.extract_info(url)
            tags = info.get('tags')
            title = info.get('title')
            album = info.get('album')
            artist = info.get('artist')
            formats = info.get('formats')
            categories = info.get('categories')
            thumbnails = info.get('thumbnails')
            description = info.get('description')

            artists = models.Artist.objects.filter(name=artist)
            if artists.exists():
                artist = artists[0]
            else:
                id = uuid.uuid1(random.randint(0, MAX))
                artist = models.Artist(id=id, name=artist)
                artist.save()
            albums = models.Album.objects.filter(title=album)
            if albums.exists():
                album = albums[0]
            else:
                id = uuid.uuid1(random.randint(0, MAX))
                album = models.Album(id=id, title=album, author=artist)
                album.save()

            track = models.Track(
                description=description,
                author=artist, album=album,
                id=ID, title=title, url=url,
                track=f'{directory}/track.mp3',
                thumbnail=f'{directory}/thumbnails')
            track.save()

            if not os.path.exists(directory):
                os.mkdir(directory)
            directory = f'{directory}/thumbnails'
            if not os.path.exists(directory):
                os.mkdir(directory)

            for thumbnail in thumbnails:
                filename = False
                url = thumbnail.get('url')
                resolution = thumbnail.get('resolution')
                for extension in EXTENSIONS:
                    if extension in url:
                        filename = f'thumbnail{resolution}{extension}'

                if filename:
                    response = requests.get(url)
                    filename = f'{directory}/{filename}'
                    with open(filename, mode='wb') as file:
                        file.write(response.content)

    return JsonResponse({'status': False})


@api_view(['GET'])
def get_track_meta_by_id(request, id):
    if request.method == 'GET':
        track = models.Track.objects.get(id=id)
        data = {
            'id': track.id,
            'title': track.title,
        }
        return JsonResponse(data)
    return JsonResponse({'status': False})


@api_view(['GET'])
def get_track_data_by_id(request, id):
    if request.method == 'GET':
        id = id.replace('-', '')
        id = f'{id[0:8]}-{id[8:12]}-{id[12:16]}-{id[16:20]}-{id[20:]}'
        directory = f'{RESOURCES}/tracks/{id}'.replace('\\', '/')
        track = f'{directory}/track.mp3'
        return FileResponse(open(track, 'rb'))
    return JsonResponse({'status': False})


@api_view(['GET'])
def get_thumbnail_by_id(request, id, mode="small"):
    if request.method == 'GET':
        id = id.replace('-', '')
        id = f'{id[0:8]}-{id[8:12]}-{id[12:16]}-{id[16:20]}-{id[20:]}'
        directory = f'{RESOURCES}/tracks/{id}'.replace('\\', '/')
        if mode == "small": thumbnail = "thumbnail336x188.jpg"
        elif mode == "big": thumbnail = "thumbnail1920x1080.webp"
        else: thumbnail = "thumbnail336x188.jpg"
        thumbnail = f'{directory}/thumbnails/{thumbnail}'
        return FileResponse(open(thumbnail, 'rb'))
    return JsonResponse({'status': False})


@api_view(['GET'])
def get_random_tracks(request, k=1):
    if request.method == 'GET':
        tracks = models.Track.objects.all()
        tracks = random.choices(tracks, k=k)
        data = {'tracks': [], 'status': True}
        for track in tracks:
            author = models.Artist.objects.get(id=track.author_id)
            album = models.Album.objects.get(id=track.album_id)
            data['tracks'].append({
                'id': track.id,
                'title': track.title,
                'author': {
                    'id': author.id,
                    'name': author.name,
                },
                'album': {
                    'id': album.id,
                    'title': album.title,
                }
            })
        return JsonResponse(data)
    return JsonResponse({'status': False})