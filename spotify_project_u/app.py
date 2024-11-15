


import streamlit as st
import requests
import os
import numpy as np
import pandas as pd
import altair as alt
import time

st.set_page_config(page_title="Spotify Playlist Analyzer", layout="wide")

# Utility functions for backend interaction
def create_playlist(track_name, artist_name):
    response = requests.post("http://127.0.0.1:8000/create_playlist/", data={"track_name": track_name, "artist_name": artist_name})
    if response.status_code == 201:
        st.success("Playlist created successfully!")
        playlist_data = response.json()
        st.write(f"Playlist ID: {playlist_data['playlist_id']}")
    else:
        st.error(f"Error creating playlist: {response.text}")

def import_playlists(user_playlist_url, friend_playlist_url):
    url = "http://127.0.0.1:8000/import/"
    data = {"user_playlist_url": user_playlist_url, "friend_playlist_url": friend_playlist_url}
    response = requests.post(url, data=data)
    if response.status_code == 200:
        return response.json()
    else:
        return {"error": "Failed to import playlists"}

def fetch_playlist_report_by_url(playlist_url):
    try:
        response = requests.post("http://127.0.0.1:8000/import_single_playlist/", data={"playlist_url": playlist_url})
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as e:
        return {"error": f"Failed to fetch report: {e}"}

def display_realtime_loading_graph():
    progress_bar = st.sidebar.progress(0)
    status_text = st.sidebar.empty()
    last_rows = np.random.randn(1, 1)
    chart = st.line_chart(last_rows)
    for i in range(1, 101):
        new_rows = last_rows[-1, :] + np.random.randn(5, 1).cumsum(axis=0)
        status_text.text(f"{i}% Complete")
        chart.add_rows(new_rows)
        progress_bar.progress(i)
        last_rows = new_rows
        time.sleep(0.05)
    progress_bar.empty()

def sidebar():
    st.sidebar.markdown("<div class='sidebar-title'>Spotify Playlist Analyzer</div>", unsafe_allow_html=True)
    
    st.sidebar.write("Create Your New Playlist:")
    
    # # Updated text inputs for track_name and artist_name
    # track_name = st.sidebar.text_input("Track Name:")
    # artist_name = st.sidebar.text_input("Artist Name:")

   
    
    # if st.sidebar.button("Create Playlist"):
    #     # Use track_name and artist_name for playlist creation
    #     playlist_data = create_playlist(track_name, artist_name)
        
    #     if 'playlist_id' in playlist_data:
    #         st.sidebar.success(f"Playlist created successfully with ID: {playlist_data['playlist_id']}")
    #     else:
    #         st.sidebar.error("Error creating playlist.")
    # st.sidebar.button("Go Back", on_click=set_page, args=("home",))
        
    # Updated text inputs for track_name and artist_name
    track_name = st.sidebar.text_input("Track Name:")
    artist_name = st.sidebar.text_input("Artist Name:")

    if st.sidebar.button("Create Playlist"):
        # Use track_name and artist_name for playlist creation
        playlist_data = create_playlist(track_name, artist_name)
        
        if playlist_data is not None and 'playlist_id' in playlist_data.keys():
            # Show success message with track and artist names
            st.sidebar.success(f"Playlist created successfully with ID: {playlist_data['playlist_id']}")
            st.sidebar.write(f"Track: {track_name}")
            st.sidebar.write(f"Artist: {artist_name}")
            st.sidebar.write("The playlist has been successfully created on your Spotify account!")
        else:
            st.sidebar.error("Error creating playlist.")

    st.sidebar.button("Go Back", on_click=set_page, args=("home",))


# Callback functions
def set_page(page_name):
    st.session_state.page = page_name

def compare_playlists_callback():
    user_playlist_url = st.session_state.user_playlist_url_key
    friend_playlist_url = st.session_state.friend_playlist_url_key
    response_data = import_playlists(user_playlist_url, friend_playlist_url)
    if response_data and "user_playlist_name" in response_data and "friend_playlist_name" in response_data:
        st.success("Playlists imported successfully! You can now compare them.")
        st.write(f"*Comparison between: {response_data['user_playlist_name']} and {response_data['friend_playlist_name']}*")
        col1, col2 = st.columns(2)
        with col1:
            st.subheader("User Playlist Metrics")
            st.write(response_data['user_avg_metrics'])
            user_data = pd.DataFrame({
                'Metric': ['Energy', 'Loudness', 'Tempo', 'Danceability'],
                'Value': [response_data['user_avg_metrics'].get(metric, 0) for metric in ['avg_energy', 'avg_loudness', 'avg_tempo', 'avg_danceability']]
            })
            user_chart = alt.Chart(user_data).mark_bar(color='blue').encode(
                x=alt.X('Metric:N', title=None),
                y=alt.Y('Value:Q', title="Value")
            ).properties(
                title="User Playlist Metrics",
                width=150,
                height=300
            )
            st.altair_chart(user_chart, use_container_width=True)
        with col2:
            st.subheader("Friend Playlist Metrics")
            st.write(response_data['friend_avg_metrics'])
            friend_data = pd.DataFrame({
                'Metric': ['Energy', 'Loudness', 'Tempo', 'Danceability'],
                'Value': [response_data['friend_avg_metrics'].get(metric, 0) for metric in ['avg_energy', 'avg_loudness', 'avg_tempo', 'avg_danceability']]
            })
            friend_chart = alt.Chart(friend_data).mark_bar(color='green').encode(
                x=alt.X('Metric:N', title=None),
                y=alt.Y('Value:Q', title="Value")
            ).properties(
                title="Friend Playlist Metrics",
                width=150,
                height=300
            )
            st.altair_chart(friend_chart, use_container_width=True)
    else:
        st.error("Failed to import playlists. Please check the URLs and try again.")

def analyze_playlist_callback():
    playlist_url = st.session_state.single_playlist_url
    if playlist_url:
        display_realtime_loading_graph()
        report_data = fetch_playlist_report_by_url(playlist_url)
        if 'error' not in report_data:
            st.subheader(f"Report for Playlist: {report_data['playlist_name']}")
            st.write(f"Danceability (Avg): {report_data['avg_danceability']}")
            st.write(f"Energy (Avg): {report_data['avg_energy']}")
            st.write(f"Tempo (Avg): {report_data['avg_tempo']}")
            st.write(f"Loudness (Avg): {report_data['avg_loudness']}")
            metrics = ['Danceability', 'Energy', 'Tempo', 'Loudness']
            values = [report_data['avg_danceability'], report_data['avg_energy'], report_data['avg_tempo'], report_data['avg_loudness']]
            df = pd.DataFrame({'Metric': metrics, 'Value': values})
            chart = alt.Chart(df).mark_bar().encode(
                x='Metric:N',
                y='Value:Q',
                color='Metric:N',
                tooltip=['Metric', 'Value']
            ).properties(width=300, height=300)
            st.altair_chart(chart, use_container_width=True)
        else:
            st.error(report_data['error'])

# CSS for UI customization
st.markdown("""
<style>
.main, .block-container {
    background-color: #121212;
    color: white;
    min-height: 100vh;
}
[data-testid="stSidebar"] {
    background-color: #1DB954;
    padding: 2rem;
}
.sidebar-title {
    color: white;
    font-size: 2rem;
    font-weight: bold;
    text-align: center;
    margin-bottom: 1rem;
}
.stButton>button {
    background-color: #1DB954;
    color: white;
    font-weight: bold;
    font-size: 1.1rem;
    border: none;
    
    border-radius: 8px;
    padding: 0.75rem;
    width: 100%;
}
.home-buttons-container {
    display: flex;
    justify-content: space-between;
    margin-top: auto;
}
</style>
""", unsafe_allow_html=True)

# Initialize session state
if 'page' not in st.session_state:
    st.session_state.page = 'home'

# Page navigation logic
if st.session_state.page == 'home':
    sidebar()
    st.image("spotify1.png", width=150)
    st.markdown("<div style='font-size: 5rem; font-weight: bold; color: white; text-align: center;'>Welcome to the Spotify Playlist Analyzer</div>", unsafe_allow_html=True)
    col1, col2 = st.columns(2)
    with col1:
        st.button("Compare + Import", on_click=set_page, args=("compare_import",))
    with col2:
        st.button("Single Playlist Evaluation", on_click=set_page, args=("single_playlist_eval",))

elif st.session_state.page == 'compare_import':
    sidebar()
    st.text_input("Your playlist URL:", key="user_playlist_url_key")
    st.text_input("Friend's playlist URL:", key="friend_playlist_url_key")
    st.button("Compare", on_click=compare_playlists_callback)

elif st.session_state.page == 'single_playlist_eval':
    sidebar()
    st.text_input("Enter Playlist URL for detailed report:", key="single_playlist_url")
    st.button("Analyze", on_click=analyze_playlist_callback)
