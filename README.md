# Wheflow — Weather-Based Music Recommendation System

Wheflow recommends music based on the current weather, time of day, and selected genre.

## Features
- Current weather, temperature, humidity, feels-like temperature, and wind speed
- Weather/time-based music mood selection
- Pop, Rock, Lo-fi, Hip-Hop, Romantic, and Tamil genres
- Up to 10 iTunes song results with artwork, audio previews, and Apple Music/iTunes links
- Optional approximate city detection using IP information

## Project files
- `app.py` — Streamlit application
- `requirements.txt` — Python dependencies

## Run locally
1. Install Python 3.9 or newer.
2. Open a terminal in this folder.
3. Install dependencies:

   ```bash
   pip install -r requirements.txt
   ```

4. Get an API key from https://openweathermap.org/api.
5. Run:

   ```bash
   streamlit run app.py
   ```

6. Enter your OpenWeatherMap API key in the sidebar and search for a city.

You can also set the key as an environment variable named `OPENWEATHER_API_KEY`.

## Deploy on Streamlit Community Cloud
1. Push this folder to a GitHub repository.
2. Create a new app in Streamlit Community Cloud.
3. Set the main file path to `app.py`.
4. Add `OPENWEATHER_API_KEY` under the app's Secrets settings, or enter it in the app sidebar.

## APIs
- OpenWeatherMap Current Weather API
- Apple/iTunes Search API

Note: This is a reconstructed, clean version based on the project details available from the previous discussion. It may not be byte-for-byte identical to the original files.
