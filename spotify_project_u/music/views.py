

from django.conf import settings
from django.shortcuts import redirect, render
from django.http import HttpResponse, JsonResponse
from django.db.models import Avg
from .models import Playlist, Track
import re
from django.shortcuts import render
import requests
import base64
from django.conf import settings
from django.http import JsonResponse, HttpResponse
from django.shortcuts import redirect, render
from django.db import DatabaseError
import logging
from django.views.decorators.csrf import csrf_exempt
from django.http import HttpResponseRedirect
import urllib.parse
import webbrowser
from time import time







# Initialize global variables for token and expiration
access_token = None
refresh_token = None
access_token_expiry = 0

# Spotify app credentials and redirect URI
client_id = settings.SPOTIFY_CLIENT_ID
client_secret = settings.SPOTIFY_CLIENT_SECRET
redirect_uri = 'http://localhost:8000/music/redirect'  # Ensure this matches your Spotify app settings
scope = 'playlist-modify-private playlist-modify-public'

def get_authorization_url():
    """Generate the Spotify authorization URL and open it in the browser."""
    auth_url = (
        'https://accounts.spotify.com/authorize'
        f'?client_id={client_id}'
        f'&response_type=code'
        f'&redirect_uri={urllib.parse.quote(redirect_uri)}'
        f'&scope={urllib.parse.quote(scope)}'
    )
    logger.info("Please go to the following URL and authorize the app:")
    logger.info(auth_url)
    webbrowser.open(auth_url)  # Opens the URL in the browser

def exchange_code_for_token(auth_code):
    """Exchange the authorization code for an access and refresh token."""
    global access_token, refresh_token, access_token_expiry
    token_url = 'https://accounts.spotify.com/api/token'
    auth_header = base64.b64encode(f"{client_id}:{client_secret}".encode()).decode()

    headers = {
        'Authorization': f'Basic {auth_header}',
        'Content-Type': 'application/x-www-form-urlencoded',
    }
    data = {
        'grant_type': 'authorization_code',
        'code': auth_code,
        'redirect_uri': redirect_uri,
    }
    try:
        response = requests.post(token_url, headers=headers, data=data)
        response.raise_for_status()
        token_data = response.json()
        access_token = token_data['access_token']
        refresh_token = token_data['refresh_token']
        access_token_expiry = time() + token_data['expires_in']
        logger.info("Access and refresh tokens retrieved successfully.")
        return access_token
    except requests.exceptions.RequestException as e:
        logger.error(f"Failed to exchange authorization code: {e}")
        raise Exception("Failed to retrieve tokens:", response.json())

def refresh_access_token():
    """Refresh the access token using the stored refresh token."""
    global access_token, access_token_expiry
    token_url = 'https://accounts.spotify.com/api/token'
    auth_header = base64.b64encode(f"{client_id}:{client_secret}".encode()).decode()

    headers = {
        'Authorization': f'Basic {auth_header}',
        'Content-Type': 'application/x-www-form-urlencoded',
    }
    data = {
        'grant_type': 'refresh_token',
        'refresh_token': refresh_token,
    }
    try:
        response = requests.post(token_url, headers=headers, data=data)
        response.raise_for_status()
        token_data = response.json()
        access_token = token_data['access_token']
        access_token_expiry = time() + token_data['expires_in']
        logger.info("Access token refreshed successfully.")
        return access_token
    except requests.exceptions.RequestException as e:
        logger.error(f"Failed to refresh access token: {e}")
        raise Exception("Failed to refresh access token:", response.json())

def get_spotify_token():
    """Retrieve a valid Spotify token, refreshing it if necessary."""
    global access_token, refresh_token
    try:
        # Check if the access token is missing or expired
        if access_token is None or time() >= access_token_expiry:
            # If there's a refresh token, attempt to refresh the access token
            if refresh_token:
                access_token = refresh_access_token()
            else:
                # No refresh token available; user needs to reauthorize
                logger.warning("No refresh token available. Directing user to reauthorize.")
                get_authorization_url()  # Redirects user for reauthorization
                raise Exception("User reauthorization required. Please authorize the app by following the URL.")
        return access_token
    except Exception as e:
        logger.error(f"Error retrieving Spotify token: {e}")
        raise


def spotify_redirect(request):
    """Handles the redirect after Spotify authorization and exchanges the code for tokens."""
    auth_code = request.GET.get('code')
    
    if auth_code:
        try:
            # Exchange the authorization code for access and refresh tokens
            access_token = exchange_code_for_token(auth_code)
            
            # Log the successful exchange
            logger.info(f"Successfully exchanged auth code for access token: {access_token}")
            
            # Return the success message with the access token
            return JsonResponse({'message': 'Authorization successful', 'access_token': access_token})
        except Exception as e:
            # Log the error
            logger.error(f"Error during token exchange: {str(e)}")
            return JsonResponse({'error': str(e)}, status=500)
    else:
        return JsonResponse({'error': 'Authorization code not found'}, status=400)


    
def get_playlist_data_by_id(token, playlist_id):
    # Step 1: Fetch playlist metadata and tracks
    url = f'https://api.spotify.com/v1/playlists/{playlist_id}'
    headers = {'Authorization': f'Bearer {token}'}
    response = requests.get(url, headers=headers)

    if response.status_code != 200:
        logger.error(f"Error fetching playlist data: {response.status_code}, {response.text}")
        return None

    data = response.json()
    playlist = {
        "id": playlist_id,
        "name": data['name'],
        "description": data.get('description', ''),
        "owner": data['owner']['id']
    }

    # Step 2: Prepare track data list and fetch audio features separately
    tracks = []
    for item in data['tracks']['items']:
        track = item['track']
        track_id = track['id']
        track_name = track['name']

        # Make an additional request for each track's audio features
        audio_features_url = f'https://api.spotify.com/v1/audio-features/{track_id}'
        audio_features_response = requests.get(audio_features_url, headers=headers)
        
        if audio_features_response.status_code == 200:
            audio_features = audio_features_response.json()
            track_data = {
                "id": track_id,
                "name": track_name,
                "energy": audio_features.get('energy', 0.0),
                "loudness": audio_features.get('loudness', 0.0),
                "key": audio_features.get('key', 0),
                "tempo": audio_features.get('tempo', 0.0),
                "danceability": audio_features.get('danceability', 0.0)

            }
        else:
            logger.warning(f"Could not fetch audio features for track {track_id}")
            track_data = {
                "id": track_id,
                "name": track_name,
                "energy": 0.0,
                "loudness": 0.0,
                "key": 0,
                "tempo": 0.0,
                "danceability": 0.0

            }

        tracks.append(track_data)
        print(tracks)
    return {"playlist": playlist, "tracks": tracks}

def extract_playlist_id(playlist_url):
    # Handle URLs with extra query parameters or special formatting
    match = re.search(r'playlist/([a-zA-Z0-9]+)', playlist_url)
    if match:
        return match.group(1)
    print(f"Could not extract playlist ID from: {playlist_url}")
    return None




logger = logging.getLogger(__name__)

@csrf_exempt
def import_single_playlist(request):
    if request.method == 'POST':
        try:
            playlist_url = request.POST.get('playlist_url')

            # Extract playlist ID from the URL
            playlist_id = extract_playlist_id(playlist_url)
            if not playlist_id:
                return JsonResponse({'error': 'Invalid playlist URL'}, status=400)

            # Get Spotify token
            token = get_spotify_token()

            # Fetch playlist data from Spotify
            playlist_data = get_playlist_data_by_id(token, playlist_id)
            if not playlist_data:
                return JsonResponse({'error': 'Error retrieving playlist data'}, status=500)

            playlist_info = playlist_data['playlist']

            # Save playlist data to the database
            try:
                playlist, _ = Playlist.objects.get_or_create(
                    spotify_id=playlist_info['id'],
                    defaults={
                        'name': playlist_info['name'],
                        'description': playlist_info.get('description', ''),
                        'owner': playlist_info['owner']
                    }
                )
                playlist.tracks.all().delete()

                # Save tracks
                for track_data in playlist_data['tracks']:
                    Track.objects.update_or_create(
                        spotify_id=track_data['id'],
                        playlist=playlist,
                        defaults={
                            'name': track_data['name'],
                            'energy': track_data['energy'],
                            'loudness': track_data['loudness'],
                            'key': track_data['key'],
                            'tempo': track_data['tempo'],
                            'danceability': track_data['danceability']
                        }
                    )
            except DatabaseError as db_err:
                logger.error(f"Database error: {db_err}")
                return JsonResponse({'error': 'Database error while saving playlist data'}, status=500)

            # Calculate average metrics for the playlist
            avg_metrics = playlist.tracks.aggregate(
                avg_energy=Avg('energy'),
                avg_loudness=Avg('loudness'),
                avg_tempo=Avg('tempo'),
                avg_danceability=Avg('danceability')
            )

            # Return the average metrics as a JSON response
            return JsonResponse({
                'playlist_name': playlist.name,
                'avg_energy': avg_metrics['avg_energy'],
                'avg_loudness': avg_metrics['avg_loudness'],
                'avg_tempo': avg_metrics['avg_tempo'],
                'avg_danceability': avg_metrics['avg_danceability']
            })

        except Exception as e:
            logger.exception(f"Unexpected error: {e}")
            return JsonResponse({'error': 'An unexpected error occurred'}, status=500)

    return JsonResponse({'error': 'Invalid request method'}, status=405)


from django.http import JsonResponse

@csrf_exempt
def import_playlist_by_url(request):
    if request.method == 'POST':
        try:
            user_playlist_url = request.POST.get('user_playlist_url')
            friend_playlist_url = request.POST.get('friend_playlist_url')

            user_playlist_id = extract_playlist_id(user_playlist_url)
            friend_playlist_id = extract_playlist_id(friend_playlist_url)

            if not user_playlist_id or not friend_playlist_id:
                logger.warning("Invalid playlist URLs provided.")
                return JsonResponse({"error": "Invalid playlist URLs"}, status=400)

            token = get_spotify_token()

            # Fetch and save data for the user's playlist
            try:
                user_playlist_data = get_playlist_data_by_id(token, user_playlist_id)
                user_playlist_info = user_playlist_data['playlist']
            except KeyError:
                logger.error("User playlist data could not be retrieved from Spotify.")
                return JsonResponse({"error": "Error retrieving user playlist data."}, status=500)

            # Database operation for user's playlist
            try:
                user_playlist, _ = Playlist.objects.get_or_create(
                    spotify_id=user_playlist_info['id'],
                    defaults={
                        'name': user_playlist_info['name'],
                        'description': user_playlist_info.get('description', ''),
                        'owner': user_playlist_info['owner']
                    }
                )
                user_playlist.tracks.all().delete()
            except DatabaseError as db_err:
                logger.error("Database error while saving user playlist: %s", db_err)
                return JsonResponse({"error": "Database error while saving user playlist data."}, status=500)

            # Save user playlist tracks
            for track_data in user_playlist_data['tracks']:
                Track.objects.update_or_create(
                    spotify_id=track_data['id'],
                    playlist=user_playlist,
                    defaults={
                        'name': track_data['name'],
                        'energy': track_data['energy'],
                        'loudness': track_data['loudness'],
                        'key': track_data['key'],
                        'tempo': track_data['tempo'],
                        'danceability': track_data['danceability']
                    }
                )

            # Fetch and save data for the friend’s playlist
            try:
                friend_playlist_data = get_playlist_data_by_id(token, friend_playlist_id)
                friend_playlist_info = friend_playlist_data['playlist']
            except KeyError:
                logger.error("Friend playlist data could not be retrieved from Spotify.")
                return JsonResponse({"error": "Error retrieving friend playlist data."}, status=500)

            # Database operation for friend's playlist
            try:
                friend_playlist, _ = Playlist.objects.get_or_create(
                    spotify_id=friend_playlist_info['id'],
                    defaults={
                        'name': friend_playlist_info['name'],
                        'description': friend_playlist_info.get('description', ''),
                        'owner': friend_playlist_info['owner']
                    }
                )
                friend_playlist.tracks.all().delete()
            except DatabaseError as db_err:
                logger.error("Database error while saving friend playlist: %s", db_err)
                return JsonResponse({"error": "Database error while saving friend playlist data."}, status=500)

            # Save friend playlist tracks
            for track_data in friend_playlist_data['tracks']:
                Track.objects.update_or_create(
                    spotify_id=track_data['id'],
                    playlist=friend_playlist,
                    defaults={
                        'name': track_data['name'],
                        'energy': track_data['energy'],
                        'loudness': track_data['loudness'],
                        'key': track_data['key'],
                        'tempo': track_data['tempo'],
                        'danceability': track_data['danceability']
                    }
                )

            # Calculate average metrics for both playlists
            user_avg_metrics = user_playlist.tracks.aggregate(
                avg_energy=Avg('energy'),
                avg_loudness=Avg('loudness'),
                avg_tempo=Avg('tempo'),
                avg_danceability=Avg('danceability')
            )
            friend_avg_metrics = friend_playlist.tracks.aggregate(
                avg_energy=Avg('energy'),
                avg_loudness=Avg('loudness'),
                avg_tempo=Avg('tempo'),
                avg_danceability=Avg('danceability')
            )

            # Return the average metrics as a JSON response
            return JsonResponse({
                "user_playlist_name": user_playlist.name,
                "friend_playlist_name": friend_playlist.name,
                "user_avg_metrics": user_avg_metrics,
                "friend_avg_metrics": friend_avg_metrics
            }, status=200)

        except Exception as e:
            logger.exception("Unexpected error during playlist import: %s", e)
            return JsonResponse({"error": "An unexpected error occurred. Please try again."}, status=500)

    return JsonResponse({"error": "Invalid request method."}, status=405)

@csrf_exempt
def compare_playlists(request):
    logger.debug("Request method: %s", request.method)
    
    # if request.method != 'GET':
    #     return JsonResponse({"error": "Invalid request method"}, status=400)
    user_avg_metrics = request.session.get('user_avg_metrics')
    friend_avg_metrics = request.session.get('friend_avg_metrics')
    user_playlist_name = request.session.get('user_playlist_name')
    friend_playlist_name = request.session.get('friend_playlist_name')

    print(f'1. {user_avg_metrics}')
    print(f'2. {friend_avg_metrics}')
    print(f'3. {user_playlist_name}')
    print(f'4. {friend_playlist_name}')


    # Log session data for debugging
    logger.debug(f"Session Data: {request.session.items()}")

    if not user_avg_metrics or not friend_avg_metrics:
        return JsonResponse({"error": "No playlists available for comparison"}, status=400)

    response_data = {
        'user_playlist': {
            'name': user_playlist_name,
            'avg_metrics': {
                'energy': user_avg_metrics.get('avg_energy', 0.0),
                'loudness': user_avg_metrics.get('avg_loudness', 0.0),
                'tempo': user_avg_metrics.get('avg_tempo', 0.0)
            }
        },
        'friend_playlist': {
            'name': friend_playlist_name,
            'avg_metrics': {
                'energy': friend_avg_metrics.get('avg_energy', 0.0),
                'loudness': friend_avg_metrics.get('avg_loudness', 0.0),
                'tempo': friend_avg_metrics.get('avg_tempo', 0.0)
            }
        }
    }

    return JsonResponse(response_data)


from urllib.parse import quote_plus

import urllib.parse


def search_tracks_by_params(token, track_name=None, artist_name=None):
    """Search for tracks based on parameters."""
    # Initialize the search query
    search_query = ''

    # Check if track_name or artist_name is provided and build the query
    if track_name:
        search_query += f'track:{track_name} '
    if artist_name:
        search_query += f'artist:{artist_name}'

    # If neither is provided, search for all tracks (no filters)
    if not search_query:
        search_query = '*'

    # URL encode the query parameters to ensure they are properly formatted
    search_query = urllib.parse.quote(search_query.strip())

    # Construct the search URL with a more robust query string
    search_url = f'https://api.spotify.com/v1/search?q={search_query}&type=track&market=ES&limit=5&offset=0&include_external=audio'
    headers = {'Authorization': f'Bearer {token}'}

    print(f"Search URL: {search_url}")  # Debugging step

    # Make the request to the Spotify API
    response = requests.get(search_url, headers=headers)

    if response.status_code == 200:
        # Extract track data from the response
        tracks = response.json().get('tracks', {}).get('items', [])
        
        if not tracks:
            print("No tracks found for the given parameters.")
            return None
        
        # Prepare a list of track details
        track_list = []
        for track in tracks:
            track_list.append({
                'id': track['id'],
                'name': track['name'],
                'uri': track['uri'],
                'artist': ', '.join([artist['name'] for artist in track['artists']]),  # Include artist(s)
            })
        return track_list
    else:
        # Log the error if the request fails
        print(f"Error: {response.status_code} - {response.json()}")
        return None


def create_spotify_playlist(token, user_id, playlist_name, track_uris):
    """Create a new playlist on Spotify."""
    url = f"https://api.spotify.com/v1/users/{user_id}/playlists"
    headers = {'Authorization': f'Bearer {token}', 'Content-Type': 'application/json'}
    data = {
        'name': playlist_name,
        'description': 'A playlist created from Spotify Playlist Analyzer',
        'public': True  # Set to True if you want to make it public
    }

    # Create the playlist first
    response = requests.post(url, headers=headers, json=data)

    if response.status_code == 201:
        playlist_id = response.json().get('id')

        # Now add tracks to the playlist
        add_tracks_url = f"https://api.spotify.com/v1/playlists/{playlist_id}/tracks"
        add_tracks_data = {
            'uris': track_uris
        }
        add_tracks_response = requests.post(add_tracks_url, headers=headers, json=add_tracks_data)

        if add_tracks_response.status_code == 201:
            return playlist_id
        else:
            print(f"Error adding tracks to playlist: {add_tracks_response.json()}")
            return None
    else:
        print(f"Error creating playlist: {response.json()}")
        return None

def get_user_id_from_token(token):
    """Retrieve the user ID from the Spotify access token."""
    url = 'https://api.spotify.com/v1/me'
    headers = {
        'Authorization': f'Bearer {token}',
    }

    response = requests.get(url, headers=headers)
    
    # Log the full response for debugging
    print("Response Status Code:", response.status_code)
    print("Response Content:", response.content)

    if response.status_code == 200:
        user_data = response.json()
        print("User data from Spotify API:", user_data)
        if 'id' in user_data:
            return user_data['id']
        else:
            print("ID not found in the response.")
            return None
    else:
        print(f"Error: {response.status_code}")
        return None
    
def get_audio_features(user_spotify_token, track_id):
    """Fetch the audio features of a track from Spotify."""
    url = f"https://api.spotify.com/v1/audio-features/{track_id}"
    headers = {
        'Authorization': f'Bearer {user_spotify_token}'
    }
    response = requests.get(url, headers=headers)

    if response.status_code == 200:
        return response.json()
    else:
        # Handle error or return a default value
        return {}


@csrf_exempt
def create_playlist(request):
    """Create a playlist based on user parameters (track name, artist name)."""
    if request.method == 'POST':
        try:
            # Step 1: Retrieve a valid Spotify access token
            user_spotify_token = get_spotify_token()  # This function should retrieve the token from session or database
            print("Token is Here:")
            print(user_spotify_token)

            # Extract track and artist names from the request
            track_name = request.POST.get('track_name', '')
            artist_name = request.POST.get('artist_name', '')

            # Step 2: Get the user ID
            user_id = get_user_id_from_token(user_spotify_token)
            print("My ID: ")
            print(user_id)

            # Step 3: Search for tracks based on provided parameters
            tracks = search_tracks_by_params(user_spotify_token, track_name, artist_name)
            if not tracks:
                return JsonResponse({'error': 'No tracks found based on the search parameters.'}, status=400)

            # Collect track URIs for playlist creation
            track_uris = [track['uri'] for track in tracks]

            # Step 4: Create the playlist on Spotify
            playlist_name = f"{track_name} Playlist" if track_name else "Custom Playlist"
            playlist_id = create_spotify_playlist(user_spotify_token, user_id, playlist_name, track_uris)

            if not playlist_id:
                return JsonResponse({'error': 'Failed to create playlist on Spotify.'}, status=500)

            # Step 5: Save the playlist and tracks in your Django database
            playlist, created = Playlist.objects.get_or_create(
                spotify_id=playlist_id,
                defaults={'name': playlist_name, 'owner': user_id}
            )

            # Step 6: Save each track to the database, including danceability
            for track in tracks:
                # Get the track's audio features (including danceability)
                track_audio_features = get_audio_features(user_spotify_token, track['id'])

                # Check if danceability exists, otherwise set a default value
                danceability = track_audio_features.get('danceability', 0.5)  # Default to 0.5 if not found

                Track.objects.update_or_create(
                    spotify_id=track['id'],
                    playlist=playlist,
                    defaults={
                        'name': track['name'],
                        'danceability': danceability,  # Add danceability to the track
                        # Add other necessary fields like popularity, energy, etc.
                    }
                )

            # Step 7: Return the newly created playlist information
            return JsonResponse({'message': 'Playlist created successfully', 'playlist_id': playlist_id}, status=201)

        except Exception as e:
            # Handle exceptions by returning an error response
            return JsonResponse({'error': str(e)}, status=500)

    # Return error if the request method is not POST
    return JsonResponse({'error': 'Invalid request method'}, status=405)

