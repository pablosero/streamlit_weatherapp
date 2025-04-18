import streamlit as st
import requests

st.set_page_config(page_title="Weather App", layout="centered")

# ------------------ Styling ------------------
st.markdown("""
    <style>
        .big-label {
            font-size: 40px;
            font-style: italic;
            font-family: Calibri, sans-serif;
            text-align: center;
        }
        .city-input input {
            font-size: 40px !important;
            text-align: center;
            font-family: Calibri, sans-serif;
        }
        .weather-button button {
            font-size: 30px !important;
            font-weight: bold;
            font-family: Calibri, sans-serif;
        }
        .temp-display {
            font-size: 75px;
            text-align: center;
            font-family: Calibri, sans-serif;
        }
        .emoji-display {
            font-size: 100px;
            font-family: 'Segoe UI Emoji', Calibri, sans-serif;
            text-align: center;
        }
        .desc-display {
            font-size: 50px;
            font-family: Calibri, sans-serif;
            text-align: center;
        }
    </style>
""", unsafe_allow_html=True)

# ------------------ Input ------------------
st.markdown('<div class="big-label">Enter City Name:</div>', unsafe_allow_html=True)
city = st.text_input("", key="city_input", label_visibility="collapsed", placeholder="e.g. Berlin")

# ------------------ Platzhalter vorbereiten ------------------
temp_display = st.empty()
emoji_display = st.empty()
desc_display = st.empty()

# ------------------ Wetter-Emoji ------------------
def get_weather_emoji(weather_id):
    if 200 <= weather_id <= 232:
        return "⛈️"
    elif 300 <= weather_id <= 321:
        return "🌦️"
    elif 500 <= weather_id <= 531:
        return "🌧️"
    elif 600 <= weather_id <= 622:
        return "❄️"
    elif 701 <= weather_id <= 741:
        return "🌫️"
    elif weather_id == 762:
        return "🌋"
    elif weather_id == 771:
        return "💨"
    elif weather_id == 781:
        return "🌪️"
    elif weather_id == 800:
        return "☀️"
    elif weather_id == 801:
        return "🌤️"
    elif weather_id == 802:
        return "⛅"
    elif weather_id == 803:
        return "🌥️"
    elif weather_id == 804:
        return "☁️"
    else:
        return ""

# ------------------ Fehleranzeige ------------------
def show_error(msg):
    temp_display.markdown(f'<div class="temp-display" style="font-size:20px;">{msg}</div>', unsafe_allow_html=True)
    emoji_display.empty()
    desc_display.empty()

# ------------------ API-Anfrage ------------------
def fetch_weather(city):
    api_key = "a18f098c4ae3d1d803e1241f434e8a1e"
    url = f"https://api.openweathermap.org/data/2.5/weather?q={city}&appid={api_key}&units=metric&lang=en"

    try:
        response = requests.get(url)
        response.raise_for_status()
        data = response.json()

        if data["cod"] == 200:
            temp_c = data["main"]["temp"]
            desc = data["weather"][0]["description"]
            weather_id = data["weather"][0]["id"]

            temp_display.markdown(f'<div class="temp-display">{temp_c:.1f}°C</div>', unsafe_allow_html=True)
            emoji_display.markdown(f'<div class="emoji-display">{get_weather_emoji(weather_id)}</div>', unsafe_allow_html=True)
            desc_display.markdown(f'<div class="desc-display">{desc.capitalize()}</div>', unsafe_allow_html=True)
        else:
            show_error("Unknown error – maybe city not found?")

    except requests.exceptions.HTTPError as http_error:
        match response.status_code:
            case 400: msg = "Bad request: Please check your input"
            case 401: msg = "Unauthorized: Invalid API key"
            case 403: msg = "Forbidden: Access denied"
            case 404: msg = "City not found"
            case 500: msg = "Internal server error – try again later"
            case 502: msg = "Bad Gateway: Invalid server response"
            case 503: msg = "Server unavailable"
            case 504: msg = "Gateway Timeout: No response from server"
            case _:   msg = f"HTTP error occurred: {http_error}"
        show_error(msg)

    except requests.exceptions.ConnectionError:
        show_error("Connection error: Check your internet")
    except requests.exceptions.Timeout:
        show_error("Timeout: The request took too long")
    except requests.exceptions.RequestException as e:
        show_error(f"Request error: {e}")

# ------------------ Ausführung ------------------
if city:
    fetch_weather(city)

if st.button("Get Weather"):
    fetch_weather(city)