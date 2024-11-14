# from django.conf import settings
# from django.shortcuts import redirect, render
# from django.http import HttpResponse, JsonResponse
# from django.db.models import Avg
# from .models import Playlist, Track
# import re

# # Dummy Spotify Functions
# def get_spotify_token():
#     return "BQBCzhgGVtnYATltsr-K3ZEP6jCrvc8CivoxO7RsAKrqt_JFzZJ9yjSQcA5R8aFI1P89tiURR2a49TOMYV3v_QR1Cqc1jjZzGamNXyMiJk6lx-go7HA"

# def get_playlist_data_by_id(token, playlist_id):
#     return {
#         "playlist": {
#             "id": playlist_id,
#             "name": f"My Playlist {playlist_id}",
#             "description": "This is a sample playlist description.",
#             "owner": "user123"
#         },
#         "tracks": [
#             {"id": "track1", "name": "Song 1", "energy": 0.7, "loudness": -5.0, "key": 5, "tempo": 120.0},
#             {"id": "track2", "name": "Song 2", "energy": 0.6, "loudness": -6.0, "key": 6, "tempo": 130.0},
#         ]
#     }

# def extract_playlist_id(playlist_url):
#     match = re.search(r'playlist/([a-zA-Z0-9]+)', playlist_url)
#     if match:
#         return match.group(1)
#     return None

# def import_playlist_by_url(request):
#     if request.method == 'POST':
#         user_playlist_url = request.POST.get('user_playlist_url')
#         friend_playlist_url = request.POST.get('friend_playlist_url')

#         user_playlist_id = extract_playlist_id(user_playlist_url)
#         friend_playlist_id = extract_playlist_id(friend_playlist_url)

#         if not user_playlist_id or not friend_playlist_id:
#             return HttpResponse("Invalid playlist URLs")

#         token = get_spotify_token()

#         # Fetch and save data for the user's playlist
#         user_playlist_data = get_playlist_data_by_id(token, user_playlist_id)
#         user_playlist_info = user_playlist_data['playlist']
#         user_playlist, _ = Playlist.objects.get_or_create(
#             spotify_id=user_playlist_info['id'],
#             defaults={
#                 'name': user_playlist_info['name'],
#                 'description': user_playlist_info.get('description', ''),
#                 'owner': user_playlist_info['owner']
#             }
#         )

#         for track_data in user_playlist_data['tracks']:
#             Track.objects.get_or_create(
#                 spotify_id=track_data['id'],
#                 playlist=user_playlist,
#                 defaults={
#                     'name': track_data['name'],
#                     'energy': track_data['energy'],
#                     'loudness': track_data['loudness'],
#                     'key': track_data['key'],
#                     'tempo': track_data['tempo'],
#                 }
#             )

#         # Fetch and save data for the friend’s playlist
#         friend_playlist_data = get_playlist_data_by_id(token, friend_playlist_id)
#         friend_playlist_info = friend_playlist_data['playlist']
#         friend_playlist, _ = Playlist.objects.get_or_create(
#             spotify_id=friend_playlist_info['id'],
#             defaults={
#                 'name': friend_playlist_info['name'],
#                 'description': friend_playlist_info.get('description', ''),
#                 'owner': friend_playlist_info['owner']
#             }
#         )

#         for track_data in friend_playlist_data['tracks']:
#             Track.objects.get_or_create(
#                 spotify_id=track_data['id'],
#                 playlist=friend_playlist,
#                 defaults={
#                     'name': track_data['name'],
#                     'energy': track_data['energy'],
#                     'loudness': track_data['loudness'],
#                     'key': track_data['key'],
#                     'tempo': track_data['tempo'],
#                 }
#             )

#         # Calculate average metrics for both playlists
#         user_avg_metrics = user_playlist.tracks.aggregate(
#             avg_energy=Avg('energy'),
#             avg_loudness=Avg('loudness'),
#             avg_tempo=Avg('tempo')
#         )

#         friend_avg_metrics = friend_playlist.tracks.aggregate(
#             avg_energy=Avg('energy'),
#             avg_loudness=Avg('loudness'),
#             avg_tempo=Avg('tempo')
#         )

#         # Save the averages to the session to display in the comparison view
#         request.session['user_avg_metrics'] = user_avg_metrics
#         request.session['friend_avg_metrics'] = friend_avg_metrics
#         request.session['user_playlist_name'] = user_playlist.name
#         request.session['friend_playlist_name'] = friend_playlist.name

#         return redirect('compare_playlists')  # Redirect to comparison view

#     return render(request, 'music/import_playlist.html')

# # Fetch playlists view
# def fetch_playlists(request):
#     # Retrieve all playlists from the database
#     playlists = Playlist.objects.all().values('id', 'name', 'description', 'owner')

#     # Convert the queryset to a list
#     playlists_list = list(playlists)

#     # Return the playlists as JSON
#     return JsonResponse(playlists_list, safe=False)

# # Comparison view
# def compare_playlists(request):
#     user_avg_metrics = request.session.get('user_avg_metrics')
#     friend_avg_metrics = request.session.get('friend_avg_metrics')
#     user_playlist_name = request.session.get('user_playlist_name')
#     friend_playlist_name = request.session.get('friend_playlist_name')

#     if not user_avg_metrics or not friend_avg_metrics:
#         return JsonResponse({"error": "No playlists available for comparison"}, status=400)

#     response_data = {
#         'user_avg_metrics': user_avg_metrics,
#         'friend_avg_metrics': friend_avg_metrics,
#         'user_playlist_name': user_playlist_name,
#         'friend_playlist_name': friend_playlist_name,
#     }

#     return JsonResponse(response_data)

from django.conf import settings
from django.shortcuts import redirect, render
from django.http import HttpResponse, JsonResponse
from django.db.models import Avg
from .models import Playlist, Track
import re
from django.shortcuts import render
from django.http import HttpResponseForbidden
from django.views.decorators.csrf import csrf_protect
import requests
import base64
from django.conf import settings

def get_spotify_token():
    token_url = "https://accounts.spotify.com/api/token"
    client_id = settings.SPOTIFY_CLIENT_ID
    client_secret = settings.SPOTIFY_CLIENT_SECRET
    data = {
        'grant_type': 'client_credentials'
    }
    headers = {
        'Authorization': f'Basic {base64.b64encode(f"{client_id}:{client_secret}".encode()).decode()}'
    }
    response = requests.post(token_url, data=data, headers=headers)
    
    if response.status_code == 200:
        token_data = response.json()
        print(token_data)
        return token_data['access_token']
        
    else:
        raise Exception("Failed to retrieve Spotify token")


def get_playlist_data_by_id(token, playlist_id):
    # Simulate fetching playlist data from Spotify
    return {
        "playlist": {
            "id": playlist_id,
            "name": f"My Playlist {playlist_id}",
            "description": "This is a sample playlist description.",
            "owner": "user123"
        },
        "tracks": [
            {"id": "track1", "name": "Song 1", "energy": 0.7, "loudness": -5.0, "key": 5, "tempo": 120.0},
            {"id": "track2", "name": "Song 2", "energy": 0.6, "loudness": -6.0, "key": 6, "tempo": 130.0},
        ]
    }

def extract_playlist_id(playlist_url):
    match = re.search(r'playlist/([a-zA-Z0-9]+)', playlist_url)
    if match:
        return match.group(1)
    return None

@csrf_protect  # This decorator ensures that CSRF protection is applied to this view
def import_playlist_by_url(request):
    if request.method == 'POST':
        user_playlist_url = request.POST.get('user_playlist_url')
        friend_playlist_url = request.POST.get('friend_playlist_url')

        user_playlist_id = extract_playlist_id(user_playlist_url)
        friend_playlist_id = extract_playlist_id(friend_playlist_url)

        if not user_playlist_id or not friend_playlist_id:
            return HttpResponse("Invalid playlist URLs")

        token = get_spotify_token()

        # Fetch and save data for the user's playlist
        user_playlist_data = get_playlist_data_by_id(token, user_playlist_id)
        user_playlist_info = user_playlist_data['playlist']
        user_playlist, _ = Playlist.objects.get_or_create(
            spotify_id=user_playlist_info['id'],
            defaults={
                'name': user_playlist_info['name'],
                'description': user_playlist_info.get('description', ''),
                'owner': user_playlist_info['owner']
            }
        )

        # Remove any existing tracks for the playlist to avoid duplicates
        user_playlist.tracks.all().delete()

        for track_data in user_playlist_data['tracks']:
            Track.objects.get_or_create(
                spotify_id=track_data['id'],
                playlist=user_playlist,
                defaults={
                    'name': track_data['name'],
                    'energy': track_data['energy'],
                    'loudness': track_data['loudness'],
                    'key': track_data['key'],
                    'tempo': track_data['tempo'],
                }
            )

        # Fetch and save data for the friend’s playlist
        friend_playlist_data = get_playlist_data_by_id(token, friend_playlist_id)
        friend_playlist_info = friend_playlist_data['playlist']
        friend_playlist, _ = Playlist.objects.get_or_create(
            spotify_id=friend_playlist_info['id'],
            defaults={
                'name': friend_playlist_info['name'],
                'description': friend_playlist_info.get('description', ''),
                'owner': friend_playlist_info['owner']
            }
        )

        # Remove any existing tracks for the playlist to avoid duplicates
        friend_playlist.tracks.all().delete()

        for track_data in friend_playlist_data['tracks']:
            Track.objects.get_or_create(
                spotify_id=track_data['id'],
                playlist=friend_playlist,
                defaults={
                    'name': track_data['name'],
                    'energy': track_data['energy'],
                    'loudness': track_data['loudness'],
                    'key': track_data['key'],
                    'tempo': track_data['tempo'],
                }
            )

        # Calculate average metrics for both playlists
        user_avg_metrics = user_playlist.tracks.aggregate(
            avg_energy=Avg('energy'),
            avg_loudness=Avg('loudness'),
            avg_tempo=Avg('tempo')
        )

        friend_avg_metrics = friend_playlist.tracks.aggregate(
            avg_energy=Avg('energy'),
            avg_loudness=Avg('loudness'),
            avg_tempo=Avg('tempo')
        )

        # Save the averages to the session to display in the comparison view
        request.session['user_avg_metrics'] = user_avg_metrics
        request.session['friend_avg_metrics'] = friend_avg_metrics
        request.session['user_playlist_name'] = user_playlist.name
        request.session['friend_playlist_name'] = friend_playlist.name

        return redirect('compare_playlists')  # Redirect to comparison view
    return render(request, 'playlist.html')

# Comparison view
def compare_playlists(request):
    user_avg_metrics = request.session.get('user_avg_metrics')
    friend_avg_metrics = request.session.get('friend_avg_metrics')
    user_playlist_name = request.session.get('user_playlist_name')
    friend_playlist_name = request.session.get('friend_playlist_name')

    if not user_avg_metrics or not friend_avg_metrics:
        return JsonResponse({"error": "No playlists available for comparison"}, status=400)

    response_data = {
        'user_avg_metrics': user_avg_metrics,
        'friend_avg_metrics': friend_avg_metrics,
        'user_playlist_name': user_playlist_name,
        'friend_playlist_name': friend_playlist_name,
    }

    return JsonResponse(response_data)
