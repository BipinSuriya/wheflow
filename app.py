import os
import requests
import streamlit as st
from datetime import datetime

st.set_page_config(page_title="Wheflow | Weather Music", page_icon="🎧", layout="wide")

WEATHER_URL = "https://api.openweathermap.org/data/2.5/weather"
ITUNES_URL = "https://itunes.apple.com/search"

# Weather/time combinations mapped to artists, then filtered by the selected genre.
ARTISTS = {
    "Clear_Day": {
        "Pop": ["Dua Lipa", "Taylor Swift", "Ariana Grande"],
        "Rock": ["Imagine Dragons", "OneRepublic", "Maroon 5"],
        "Lo-fi": ["idealism", "Kina", "Powfu"],
        "Hip-Hop": ["Drake", "Post Malone", "Kendrick Lamar"],
        "Romantic": ["Ed Sheeran", "Shawn Mendes", "Adele"],
        "Tamil": ["Anirudh Ravichander", "A R Rahman", "Sid Sriram"],
    },
    "Clear_Night": {
        "Pop": ["The Weeknd", "Dua Lipa", "Ariana Grande"],
        "Rock": ["Coldplay", "OneRepublic", "Imagine Dragons"],
        "Lo-fi": ["Kina", "Joji", "idealism"],
        "Hip-Hop": ["Drake", "Travis Scott", "Post Malone"],
        "Romantic": ["The Weeknd", "Adele", "Arijit Singh"],
        "Tamil": ["Anirudh Ravichander", "Sid Sriram", "A R Rahman"],
    },
    "Rain_Day": {
        "Pop": ["Ed Sheeran", "Taylor Swift", "Adele"],
        "Rock": ["Coldplay", "The Script", "OneRepublic"],
        "Lo-fi": ["Powfu", "Kina", "idealism"],
        "Hip-Hop": ["Drake", "Post Malone", "Juice WRLD"],
        "Romantic": ["Ed Sheeran", "Arijit Singh", "Shreya Ghoshal"],
        "Tamil": ["Sid Sriram", "A R Rahman", "Anirudh Ravichander"],
    },
    "Rain_Night": {
        "Pop": ["Billie Eilish", "The Weeknd", "Lana Del Rey"],
        "Rock": ["Coldplay", "Radiohead", "The Neighbourhood"],
        "Lo-fi": ["Joji", "Kina", "Powfu"],
        "Hip-Hop": ["Juice WRLD", "Drake", "Post Malone"],
        "Romantic": ["Adele", "Billie Eilish", "Arijit Singh"],
        "Tamil": ["A R Rahman", "Sid Sriram", "Anirudh Ravichander"],
    },
    "Clouds": {
        "Pop": ["Coldplay", "OneRepublic", "Maroon 5"],
        "Rock": ["Coldplay", "Imagine Dragons", "The Script"],
        "Lo-fi": ["idealism", "Kina", "Joji"],
        "Hip-Hop": ["Drake", "Post Malone", "Kendrick Lamar"],
        "Romantic": ["Ed Sheeran", "Adele", "Arijit Singh"],
        "Tamil": ["A R Rahman", "Anirudh Ravichander", "Sid Sriram"],
    },
    "Other": {
        "Pop": ["Dua Lipa", "The Weeknd", "Taylor Swift"],
        "Rock": ["Coldplay", "Imagine Dragons", "OneRepublic"],
        "Lo-fi": ["Kina", "Powfu", "idealism"],
        "Hip-Hop": ["Drake", "Post Malone", "Kendrick Lamar"],
        "Romantic": ["Ed Sheeran", "Adele", "Arijit Singh"],
        "Tamil": ["Anirudh Ravichander", "A R Rahman", "Sid Sriram"],
    },
}

GENRES = ["Pop", "Rock", "Lo-fi", "Hip-Hop", "Romantic", "Tamil"]


def get_current_location():
    """Get an approximate city name from the user's IP address."""
    try:
        response = requests.get("https://ipinfo.io/json", timeout=8)
        response.raise_for_status()
        return response.json().get("city", "")
    except requests.RequestException:
        return ""


def get_weather(city, api_key):
    params = {"q": city, "appid": api_key, "units": "metric"}
    response = requests.get(WEATHER_URL, params=params, timeout=12)
    response.raise_for_status()
    return response.json()


def map_weather_to_music(weather):
    condition = weather["weather"][0]["main"].lower()
    is_day = 6 <= datetime.now().hour < 18

    if condition == "clear":
        return "Clear_Day" if is_day else "Clear_Night"
    if condition in ("rain", "drizzle", "thunderstorm"):
        return "Rain_Day" if is_day else "Rain_Night"
    if condition in ("clouds", "mist", "fog", "haze", "smoke", "dust", "sand"):
        return "Clouds"
    return "Other"


def get_itunes_tracks(artists, limit=10):
    """Search iTunes for tracks from the selected artists."""
    tracks = []
    seen = set()

    for artist in artists:
        try:
            params = {
                "term": artist,
                "entity": "song",
                "limit": 8,
                "country": "IN",
            }
            response = requests.get(ITUNES_URL, params=params, timeout=12)
            response.raise_for_status()

            for item in response.json().get("results", []):
                track_id = item.get("trackId")
                preview = item.get("previewUrl")
                if not track_id or track_id in seen:
                    continue
                seen.add(track_id)
                tracks.append({
                    "name": item.get("trackName", "Unknown track"),
                    "artist": item.get("artistName", artist),
                    "album": item.get("collectionName", ""),
                    "artwork": item.get("artworkUrl100", "").replace("100x100", "300x300"),
                    "preview": preview,
                    "link": item.get("trackViewUrl", ""),
                })
                if len(tracks) >= limit:
                    return tracks
        except requests.RequestException:
            continue

    return tracks[:limit]


st.title("🎧 Wheflow")
st.subheader("Music that matches your weather")
st.write("Enter a city or use approximate IP-based location to get weather-inspired music.")

with st.sidebar:
    st.header("Settings")
    api_key = st.text_input(
        "OpenWeatherMap API key",
        value=os.getenv("bea8c83ea8fd937b2de8885a3acaac72", ""),
        type="password",
        help="Get a free API key from openweathermap.org",
    )
    genre = st.selectbox("Choose a music genre", GENRES)
    if st.button("Use my approximate location"):
        detected = get_current_location()
        if detected:
            st.session_state["city"] = detected
            st.success(f"Detected city: {detected}")
        else:
            st.warning("Could not detect your city. Please enter it manually.")

city = st.text_input("City", value=st.session_state.get("city", "Coimbatore"), placeholder="e.g. Coimbatore")

if st.button("Get my weather & music", type="primary"):
    if not api_key:
        st.error("Enter your OpenWeatherMap API key in the sidebar.")
    elif not city.strip():
        st.error("Enter a city name.")
    else:
        try:
            with st.spinner("Checking the weather..."):
                weather = get_weather(city.strip(), api_key)
            weather_type = map_weather_to_music(weather)
            artists = ARTISTS[weather_type][genre]

            st.session_state["weather"] = weather
            st.session_state["weather_type"] = weather_type
            st.session_state["genre"] = genre
            st.session_state["artists"] = artists
            st.session_state["tracks"] = get_itunes_tracks(artists, limit=10)
        except requests.HTTPError as exc:
            if exc.response is not None and exc.response.status_code == 404:
                st.error("City not found. Check the spelling and try again.")
            elif exc.response is not None and exc.response.status_code == 401:
                st.error("The OpenWeatherMap API key is invalid or not active yet.")
            else:
                st.error(f"Weather API error: {exc}")
        except requests.RequestException as exc:
            st.error(f"Network error: {exc}")

if "weather" in st.session_state:
    weather = st.session_state["weather"]
    current = weather["main"]
    wind = weather.get("wind", {}).get("speed", 0)
    description = weather["weather"][0]["description"].title()

    st.markdown("---")
    st.header(f"Weather in {weather.get('name', city)}")
    c1, c2, c3, c4 = st.columns(4)
    c1.metric("Temperature", f"{current.get('temp', 0):.1f} °C")
    c2.metric("Feels like", f"{current.get('feels_like', 0):.1f} °C")
    c3.metric("Humidity", f"{current.get('humidity', 0)}%")
    c4.metric("Wind speed", f"{wind} m/s")
    st.caption(f"Condition: {description} | Music mood: {st.session_state['weather_type']} | Genre: {st.session_state['genre']}")

    st.header("Your music recommendations")
    tracks = st.session_state.get("tracks", [])
    if not tracks:
        st.info("No tracks were returned by iTunes for these artists. Try another genre.")
    else:
        for start in range(0, len(tracks), 2):
            cols = st.columns(2)
            for col, track in zip(cols, tracks[start:start + 2]):
                with col:
                    if track["artwork"]:
                        st.image(track["artwork"], width=150)
                    st.markdown(f"**{track['name']}**")
                    st.write(track["artist"])
                    if track["album"]:
                        st.caption(track["album"])
                    if track["preview"]:
                        st.audio(track["preview"])
                    if track["link"]:
                        st.link_button("Open in Apple Music / iTunes", track["link"])
                    st.markdown("---")
else:
    st.info("Add your OpenWeatherMap API key, choose a genre, enter a city, and click **Get my weather & music**.")

st.caption("Weather data: OpenWeatherMap · Music metadata and previews: iTunes Search API")
