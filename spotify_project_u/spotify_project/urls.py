"""
URL configuration for spotify_project project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.1/topics/http/urls/
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

# spotify_project/urls.py
from django.contrib import admin
from django.urls import path
from music import views  # Import views from the music app

urlpatterns = [
    path('admin/', admin.site.urls),
    path('import/', views.import_playlist_by_url, name='import_playlist_by_url'),  # Import two playlists
    path('compare/', views.compare_playlists, name='compare_playlists'),  # Display comparison results
    path('import_single_playlist/', views.import_single_playlist, name='import_single_playlist'),  # API for single playlist import
    # path('music/redirect', views.spotify_redirect, name='spotify_redirect'),  # New route for handling redirect
    path('create_playlist/', views.create_playlist, name='create_playlist'),  # Create a new playlist
    path('music/redirect', views.spotify_redirect, name='spotify_redirect'),  # Add this line
    # path('user/playlists/', views.get_user_playlists, name='get_user_playlists'),


    # path('report/', views.get_playlist_data_by_id, name='get_playlist_data_by_id'),  # Display report

    # path('check_session/', views.check_session, name='check_session'),  # Add this line

]
