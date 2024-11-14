# # import streamlit as st
# # import requests

# # # Function to import playlists
# # def import_playlists(user_playlist_url, friend_playlist_url):
# #     response = requests.post("http://127.0.0.1:8000/import/", data={
# #         "user_playlist_url": user_playlist_url,
# #         "friend_playlist_url": friend_playlist_url
# #     })
# #     return response.status_code

# # # Function to compare playlists
# # def compare_playlists():
# #     response = requests.get("http://127.0.0.1:8000/compare/")
# #     return response.json()  # Assuming your backend returns JSON data

# # # Function to fetch playlists
# # def fetch_playlists():
# #     response = requests.get("http://127.0.0.1:8000/playlists/")
# #     return response.json()  # Assuming the backend returns a JSON list of playlists

# # # Streamlit UI
# # st.title("Spotify Playlist Comparator")

# # # Button to fetch playlists
# # if st.button("Fetch Playlists"):
# #     playlists = fetch_playlists()
# #     if playlists:
# #         st.write("Available Playlists:")
# #         for playlist in playlists:
# #             st.write(f"- {playlist['name']} (ID: {playlist['id']})")
# #     else:
# #         st.error("No playlists found or failed to fetch.")

# # # Input for user's playlist URL
# # user_playlist_url = st.text_input("Enter your playlist URL:", key="user_playlist_url")
# # friend_playlist_url = st.text_input("Enter your friend's playlist URL:", key="friend_playlist_url")

# # # Button to import playlists
# # if st.button("Import Playlists"):
# #     status_code = import_playlists(user_playlist_url, friend_playlist_url)
    
# #     if status_code == 200:
# #         st.success("Playlists imported successfully! You can now compare them.")
# #     else:
# #         st.error("Failed to import playlists. Please check the URLs and try again.")

# # # Button to compare playlists
# # if st.button("Compare Playlists"):
# #     comparison_result = compare_playlists()
    
# #     if 'error' in comparison_result:
# #         st.error(comparison_result['error'])
# #     else:
# #         # Display comparison results
# #         st.write(f"**Comparison between: {comparison_result['user_playlist_name']} and {comparison_result['friend_playlist_name']}**")
# #         st.subheader("User Playlist Metrics")
# #         st.write(comparison_result['user_avg_metrics'])
# #         st.subheader("Friend Playlist Metrics")
# #         st.write(comparison_result['friend_avg_metrics'])




# import streamlit as st
# import requests
# from streamlit_lottie import st_lottie
# import os
# import base64


# # Function to load Lottie animation from URL
# def load_lottie_url(url: str):
#     response = requests.get(url)
#     if response.status_code != 200:
#         return None
#     return response.json()

# # # # Load animation for the sidebar
# # lottie_url = "https://lottie.host/6f8de95d-9cc0-4cb9-ae70-5e6e58e316f3/EEU6wIzZPS.json"  # Replace with your desired Lottie URL
# # lottie_json = load_lottie_url(lottie_url)

# # Set page configuration
# st.set_page_config(page_title="Spotify Playlist Comparator", layout="wide")

# # API Functions for Django backend
# def import_playlists(user_playlist_url, friend_playlist_url):
#     response = requests.post("http://127.0.0.1:8000/import/", data={
#         "user_playlist_url": user_playlist_url,
#         "friend_playlist_url": friend_playlist_url
#     })
#     return response.status_code

# def compare_playlists():
#     response = requests.get("http://127.0.0.1:8000/compare/")
#     return response.json()  # Assuming your backend returns JSON data

# def fetch_playlists():
#     response = requests.get("http://127.0.0.1:8000/playlists/")
#     return response.json()  # Assuming the backend returns a JSON list of playlists

# # Custom CSS for styling
# st.markdown("""
#     <style>
#     /* Global styling for dark background */
#     .main, .block-container {
#         background-color: black;
#         color: black;
#     }
    
#     /* Sidebar styling with fallback selector */
#     [data-testid="stSidebar"] {
#         background-color: #1DB954 !important; /* Spotify green */
#         padding: 2rem;
#     }
    
#     .sidebar-title {
#         color: white;
#         font-size: 2.0rem;
#         font-weight: bold;
#         text-align: center;
#         margin-bottom: 1rem;
#     }
    
#     /* Buttons styling */
#     .button {
#         margin-top: 1rem;
#         width: 100%;
#         background-color: #ff7f50;
#         color: white;
#         font-weight: bold;
#         font-size: 1.1rem;
#         border: none;
#         border-radius: 8px;
#         padding: 0.75rem;
#         transition: background-color 0.3s ease;
#     }
#     .button:hover {
#         background-color: #ff6347;
#         cursor: pointer;
#     }
#     /* Transparent container for Lottie animation */
#     .logo-container {
#         background-color: black; /* Make the background transparent */
#         display: flex;
#         width: 50px;
#         height: 50px;
#         justify-content: center;
#         align-items: center;
#         margin-top: 1rem;
#     }
#     /* Welcome message styling */
#     .welcome-container {
#         display: flex;
#         justify-content: center;
#         align-items: center;
#         margin-bottom: 35rem;
#         font-size: 3rem;
#         font-weight: bold;
#         color: white;
#         animation: fadeIn 2s ease-in-out;
#     }
#     # /* Buttons styling */
#     # .import-button, .compare-button {
#     #     width: 150px; /* Fixed width for buttons */
#     #     background-color: #ff7f50;
#     #     color: white;
#     #     font-weight: bold;
#     #     font-size: 1.1rem;
#     #     border: none;
#     #     border-radius: 8px;
#     #     padding: 0.75rem;
#     #     transition: background-color 0.3s ease;
#     #     cursor: pointer;
#     # }
#     # .import-button:hover, .compare-button:hover {
#     #     background-color: #ff6347;
#     # }
#     # /* Album artwork styling */
#     # .album-art {
#     #     display: flex;
#     #     justify-content: center;
#     #     flex-wrap: wrap;
#     #     margin-top: 1rem;
#     # }
#     # .album-art img {
#     #     width: 100px; /* Adjust size as needed */
#     #     height: 100px; /* Adjust size as needed */
#     #     margin: 0.5rem;
#     #     border-radius: 8px;
#     # }
#      /* Video background styling */
#     .video-background {
#         position: relative;
#         width: 100%;
#         height: 500px;
#         overflow: hidden;
#     }

#    /* Fullscreen video background styling */
#     .video-background {
#         position: fixed;
#         top: 0;
#         left: 0;
#         width: 100%;
#         height: 100%;
#         z-index: -1;
#         overflow: hidden;
#     }

#     .video-background video {
#         position: absolute;
#         top: 50%;
#         left: 50%;
#         width: auto;
#         height: auto;
#         min-width: 100%;
#         min-height: 100%;
#         transform: translate(-50%, -50%);
#         object-fit: cover;
#         opacity: 0.5; /* Adjust transparency as needed */
#     }

#     /* Content container to layer over the video */
#     .content {
#         position: relative;
#         z-index: 1;
#     }

#     </style>
#     """, unsafe_allow_html=True)


# # if lottie_json:
# #     st.markdown("<div class='lottie-container'>", unsafe_allow_html=True)
# #     st_lottie(lottie_json, height=200, key="spotify_animation")
# #     st.markdown("</div>", unsafe_allow_html=True)
    
# # Sidebar layout
# st.sidebar.markdown("<div class='sidebar-title'>Spotify Playlists</div>", unsafe_allow_html=True)



# # Sidebar input and fetch button
# st.sidebar.write("Enter URLs for Spotify playlists below:")
# user_playlist_url = st.sidebar.text_input("Your playlist URL:")
# friend_playlist_url = st.sidebar.text_input("Friend's playlist URL:")

# if st.sidebar.button("Fetch Playlists", key="fetch"):
#     playlists = fetch_playlists()
#     if playlists:
#         st.sidebar.write("Available Playlists:")
#         for playlist in playlists:
#             st.sidebar.write(f"- {playlist['name']} (ID: {playlist['id']})")
#             # Optionally display album artwork
#             if 'album_image_url' in playlist:  # Adjust according to your API response
#                 st.sidebar.image(playlist['album_image_url'], width=50)
#     else:
#         st.sidebar.error("No playlists found or failed to fetch.")


# # # Load and display the local PNG image within a styled div
# # image_path = "spotify1.png"  # Replace with the path to your local PNG file
# # if os.path.exists(image_path):
# #     # Using a div to wrap the image with CSS styling
# #     st.markdown(f"""
# #         <div>
# #             <img src='data:image/png;base64,{st.image(image_path, )}' style='max-width: 50%; height: 50%;' />
# #         </div>
# #     """, unsafe_allow_html=True)
# # else:
# #     st.error("Image not found. Please check the file path.")
    
# # Horizontal Welcome message animation
# welcome_text = "Welcome to Spotify Playlist Comparator"
# st.markdown(f"<div class='welcome-container'>{''.join(welcome_text)}</div>", unsafe_allow_html=True)


# # Embed the background video directly below the welcome message
# video_path = "/home/ali-hassan/Desktop/Spotify_Project/spotify_project/static/vidbgc.mp4"  # Adjust path as necessary

# # Check if the video file exists
# if os.path.exists(video_path):
#     st.markdown(f"""
#         <style>
#             /* Ensure video fills the entire screen and stays fixed */
#             .video-background {{
#                 position: fixed;
#                 top: 0;
#                 left: 0;
#                 width: 100%;
#                 height: 100%;
#                 z-index: -1;  /* Place the video behind other content */
#             }}
#             /* Ensure the video itself covers the entire screen */
#             .video-background video {{
#                 object-fit: cover;
#                 width: 100%;
#                 height: 100%;
#                 opacity: 0.6;  /* Set video opacity to 60% */
#             }}
#             /* Optional: Add a semi-transparent overlay for additional visibility control */
#             .overlay {{
#                 position: absolute;
#                 top: 0;
#                 left: 0;
#                 width: 100%;
#                 height: 100%;
#                 background: rgba(0, 0, 0, 0.4);  /* Semi-transparent black overlay (40% opacity) */
#                 z-index: 0;
#             }}
#         </style>

#         <div class="video-background">
#             <video autoplay loop muted playsinline>
#                 <source src="{video_path}" type="video/mp4">
#             </video>
#         </div>
#         <!-- Optional: Add overlay for visibility -->
#         <div class="overlay"></div>
#     """, unsafe_allow_html=True)
# else:
#     st.error("Video file not found. Please check the path.")

# import streamlit as st

# # Create a container to hold the buttons
# with st.container():
#     col1, col2, col3 = st.columns([1, 2, 5])  # Adjust column widths as needed

#     # Add custom CSS for button styling
#     st.markdown("""
#         <style>
#         /* Sidebar button styling */
#         .css-1d391kg button {
#             background-color: black;
#             color: black;
#             font-weight: bold;
#         }

#         /* Import and Compare button styling */
#         .stButton > button {
#             background-color: #1DB954;  /* Light green background */
#             color: black;
#             border-radius: 5px;
#             font-weight: bold;
#         }
#         </style>
#     """, unsafe_allow_html=True)
    
#     # Button 1
#     with col1:
#         st.write("                                                                                     ")
#         if st.button("Import Playlists", key="import"):
#             status_code = import_playlists(user_playlist_url, friend_playlist_url)
#             if status_code == 200:
#                 st.success("Playlists imported successfully! You can now compare them.")
#             else:
#                 st.error("Failed to import playlists. Please check the URLs and try again.")

#     # Button 2
#     with col2:
#         st.write("                                                                                      ")

#         if st.button("Compare Playlists", key="compare"):
#             comparison_result = compare_playlists()
#             if 'error' in comparison_result:
#                 st.error(comparison_result['error'])
#             else:
#                 # Display comparison results
#                 st.write(f"**Comparison between: {comparison_result['user_playlist_name']} and {comparison_result['friend_playlist_name']}**")
#                 st.subheader("User Playlist Metrics")
#                 st.write(comparison_result['user_avg_metrics'])
#                 st.subheader("Friend Playlist Metrics")
#                 st.write(comparison_result['friend_avg_metrics'])
                
#     # Empty column to create space between the buttons
#     with col3:
#         st.write("            ")

# # # Display Spotify playlist album pictures below the fetch button
# # if st.sidebar.button("Show Album Art", key="show_album_art"):
# #     # Simulating fetched playlist album images
# #     album_images = [
# #         "https://via.placeholder.com/100",  # Replace with actual URLs from your API
# #         "https://via.placeholder.com/100",
# #         "https://via.placeholder.com/100"
# #     ]
# #     st.sidebar.markdown("<div class='album-art'>", unsafe_allow_html=True)
# #     for image in album_images:
# #         st.sidebar.image(image, use_column_width='auto')
# #     st.sidebar.markdown("</div>", unsafe_allow_html=True)




# # import streamlit as st
# # import requests
# # import os

# # # Set page configuration
# # st.set_page_config(page_title="Spotify Playlist Comparator", layout="wide")

# # # API Functions for Django backend
# # def import_playlists(user_playlist_url, friend_playlist_url):
# #     response = requests.post("http://127.0.0.1:8000/import/", data={
# #         "user_playlist_url": user_playlist_url,
# #         "friend_playlist_url": friend_playlist_url
# #     })
# #     return response.status_code

# # def compare_playlists():
# #     response = requests.get("http://127.0.0.1:8000/compare/")
# #     return response.json()  # Assuming your backend returns JSON data

# # def fetch_playlists():
# #     response = requests.get("http://127.0.0.1:8000/playlists/")
# #     return response.json()  # Assuming the backend returns a JSON list of playlists

# # # Custom CSS for styling
# # st.markdown("""
# #     <style>
# #     /* Make the main content fill the screen */
# #     .main, .block-container {
# #         position: relative;
# #         z-index: 2;
# #         background-color: black;
# #         color: white;
# #         min-height: 100vh; /* Full screen height */
# #     }
   
# #     /* Sidebar styling */
# #     [data-testid="stSidebar"] {
# #         background-color: #1DB954 !important;
# #         padding: 2rem;
# #     }

# #     .sidebar-title {
# #         color: white;
# #         font-size: 2.0rem;
# #         font-weight: bold;
# #         text-align: center;
# #         margin-bottom: 1rem;
# #     }

# #     /* Welcome message styling */
# #     .welcome-container {
# #         display: flex;
# #         justify-content: center;
# #         align-items: center;
# #         margin-bottom: 2rem;
# #         font-size: 3rem;
# #         font-weight: bold;
# #         color: white;
# #         animation: fadeIn 2s ease-in-out;
# #     }

# #     /* Fullscreen video background styling */
# #     .video-background {
# #     position: fixed;
# #     top: 0;
# #     left: 0;
# #     width: calc(100% - 150px); /* Adjust width based on sidebar width */
# #     height: 100%;
# #     margin-left: 300px; /* Shift video to start after sidebar */
# #     z-index: -1;
# #     overflow: hidden;
# #     background-color: black; /* Black background if video doesn't load */
# #     }

# #     .video-background video {
# #         position: absolute;
# #         top: 50%;
# #         left: 50%;
# #         width: auto;
# #         height: auto;
# #         min-width: 100%;
# #         min-height: 100%;
# #         transform: translate(-50%, -50%);
# #         object-fit: cover;
# #         opacity: 0.5; /* 50% transparency */
# #     }

# #     /* Keyframes for fade-in animation */
# #     @keyframes fadeIn {
# #         from { opacity: 0; }
# #         to { opacity: 1; }
# #     }
# #     </style>
# #     """, unsafe_allow_html=True)

# # # Sidebar layout
# # st.sidebar.markdown("<div class='sidebar-title'>Spotify Playlists</div>", unsafe_allow_html=True)

# # # Sidebar input and fetch button
# # st.sidebar.write("Enter URLs for Spotify playlists below:")
# # user_playlist_url = st.sidebar.text_input("Your playlist URL:")
# # friend_playlist_url = st.sidebar.text_input("Friend's playlist URL:")

# # if st.sidebar.button("Fetch Playlists", key="fetch"):
# #     playlists = fetch_playlists()
# #     if playlists:
# #         st.sidebar.write("Available Playlists:")
# #         for playlist in playlists:
# #             st.sidebar.write(f"- {playlist['name']} (ID: {playlist['id']})")
# #             if 'album_image_url' in playlist:
# #                 st.sidebar.image(playlist['album_image_url'], width=50)
# #     else:
# #         st.sidebar.error("No playlists found or failed to fetch.")
# # # Welcome message animation
# # welcome_text = "Welcome to Spotify Playlist Comparator"
# # st.markdown(f"<div class='welcome-container'>{welcome_text}</div>", unsafe_allow_html=True)

# # # Background video setup
# # video_path = "vidbgc.mp4"
# # # st.video(video_path, format="video/mp4", start_time=0)

# # # Video path
# # # video_path = "Spotify_video_bg2.mp4"

# # # Check if the video exists and display it manually with HTML
# # if os.path.exists(video_path):
# #     st.markdown(f"""
# #         <div class="video-background">
# #             <video autoplay loop muted playsinline>
# #                 <source src="{video_path}" type="video/mp4">
# #                 Your browser does not support the video tag.
# #             </video>
# #         </div>
# #     """, unsafe_allow_html=True)
# # else:
# #     st.error("Video file not found. Please check the file path.")

# # # Create a container to hold the buttons
# # with st.container():
# #     col1, col2, col3 = st.columns([1, 2, 5])  # Adjust column widths as needed

# #     # Button 1
# #     with col1:
# #         if st.button("Import Playlists", key="import"):
# #             status_code = import_playlists(user_playlist_url, friend_playlist_url)
# #             if status_code == 200:
# #                 st.success("Playlists imported successfully! You can now compare them.")
# #             else:
# #                 st.error("Failed to import playlists. Please check the URLs and try again.")

# #     # Button 2
# #     with col2:
# #         if st.button("Compare Playlists", key="compare"):
# #             comparison_result = compare_playlists()
# #             if 'error' in comparison_result:
# #                 st.error(comparison_result['error'])
# #             else:
# #                 # Display comparison results
# #                 st.write(f"**Comparison between: {comparison_result['user_playlist_name']} and {comparison_result['friend_playlist_name']}**")
# #                 st.subheader("User Playlist Metrics")
# #                 st.write(comparison_result['user_avg_metrics'])
# #                 st.subheader("Friend Playlist Metrics")
# #                 st.write(comparison_result['friend_avg_metrics'])
                
# #     # Empty column to create space between the buttons
# #     with col3:
# #         st.write(" ")


import streamlit as st
import requests
import os

# Function to load Lottie animation from a URL
def load_lottie_url(url: str):
    try:
        response = requests.get(url)
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as e:
        st.error(f"Error loading Lottie animation: {e}")
        return None

# Set up Streamlit page configuration
st.set_page_config(page_title="Spotify Playlist Comparator", layout="wide")

# Functions to interact with Django backend API
def import_playlists(user_playlist_url, friend_playlist_url=None):
    response = requests.post("http://127.0.0.1:8000/import/", data={
        "user_playlist_url": user_playlist_url,
        "friend_playlist_url": friend_playlist_url if friend_playlist_url else ""
    })
    return response.status_code

def compare_playlists():
    response = requests.get("http://127.0.0.1:8000/compare/")
    return response.json()

# Apply custom CSS styling
st.markdown("""
    <style>
    .main, .block-container { background-color: black; color: white; }
    
    /* Sidebar styling */
    [data-testid="stSidebar"] { 
        background-color: #1DB954; 
        padding: 2rem; 
    }
    
    /* Sidebar title styling */
    .sidebar-title { 
        color: white; 
        font-size: 2.0rem; 
        font-weight: bold; 
        text-align: center; 
        margin-bottom: 1rem; 
    }
    
    /* General button styling */
    .button { 
        margin-top: 1rem; 
        width: 100%; 
        background-color: #1DB954;  /* Same as sidebar */ color: black;  /* Black text */
        font-weight: bold; 
        font-size: 1.1rem; 
        border: none; 
        border-radius: 8px; 
        padding: 0.75rem; 
        transition: background-color 0.3s ease; 
    }
    
    /* Button hover effect */
    .button:hover { 
        background-color: #1DB954; 
        cursor: pointer; 
    }
    
    /* Welcome container styling */
    .welcome-container { 
        display: flex; 
        justify-content: center; 
        align-items: center; 
        margin-bottom: 35rem; 
        font-size: 3rem; 
        font-weight: bold; 
        color: white; 
        animation: fadeIn 2s ease-in-out; 
    }
    
    /* Video background styling */
    .video-background { 
        position: fixed; 
        top: 0; 
        left: 0; 
        width: 100%; 
        height: 100%; 
        z-index: -1; 
        overflow: hidden; 
    }
    
    .video-background video { 
        object-fit: cover; 
        width: 100%; 
        height: 100%; 
        opacity: 0.6; 
    }
    
    /* Adjust button margins and alignment */
    .container .button {
        margin-top: 1rem;
    }
    
    /* Make sure buttons are aligned without gaps */
    .container {
        display: flex;
        justify-content: center; /* Center both buttons */
        gap: 10px; /* Adjust the gap between buttons */
    }
    
    .container button {
        width: 48%;  /* Ensures buttons take up equal space without gaps */
    }
    </style>
    """, unsafe_allow_html=True)

# Sidebar layout
st.sidebar.markdown("<div class='sidebar-title'>Spotify Playlists</div>", unsafe_allow_html=True)
user_playlist_url = st.sidebar.text_input("Your playlist URL:")
friend_playlist_url = st.sidebar.text_input("Friend's playlist URL:")

# Welcome message animation
st.markdown("<div class='welcome-container'>Welcome to Spotify Playlist Comparator</div>", unsafe_allow_html=True)

# Background video setup
video_path = "/home/ali-hassan/Desktop/Spotify_Project/spotify_project/vidbgc.mp4"
if os.path.exists(video_path):
    st.markdown(f"""
        <div class="video-background">
            <video autoplay loop muted playsinline>
                <source src="{video_path}" type="video/mp4">
            </video>
        </div>
    """, unsafe_allow_html=True)
else:
    st.error("Video file not found. Please check the path.")

# Main content with import and compare buttons
with st.container():
    col1, col2 = st.columns([1, 1])  # Adjusted to make sure buttons are side by side
    
    with col1:
        if st.button("Import Playlists", key="import_playlists"):
            if user_playlist_url:
                status_code = import_playlists(user_playlist_url, friend_playlist_url)
                if status_code == 200:
                    st.success("Playlists imported successfully! You can now compare them.")
                else:
                    st.error("Failed to import playlists. Please check the URLs and try again.")
            else:
                st.error("Please provide your playlist URL to import.")

    with col2:
        if st.button("Compare Playlists", key="compare_playlists"):
            if user_playlist_url and friend_playlist_url:
                comparison_result = compare_playlists()
                if 'error' in comparison_result:
                    st.error(comparison_result['error'])
                else:
                    st.write(f"**Comparison between: {comparison_result['user_playlist_name']} and {comparison_result['friend_playlist_name']}**")
                    st.subheader("User  Playlist Metrics")
                    st.write(comparison_result['user_avg_metrics'])
                    st.subheader("Friend Playlist Metrics")
                    st.write(comparison_result['friend_avg_metrics'])
            else:
                st.error("Both user and friend playlist URLs are required to compare.")
