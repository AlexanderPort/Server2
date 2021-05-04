"""MediaPlayerServer URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from TrackService import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/tracks/', views.post_track),
    path('api/tracks/meta/<str:id>', views.get_track_meta_by_id),
    path('api/tracks/data/<str:id>', views.get_track_data_by_id),
    path('api/tracks/random/<int:k>', views.get_random_tracks),
    path('api/tracks/thumbnail/<str:id>', views.get_thumbnail_by_id),
]
