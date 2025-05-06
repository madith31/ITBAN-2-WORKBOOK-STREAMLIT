import streamlit as st
import requests
import pandas as pd
import altair as alt

st.title("🌤️ Weather Dashboard - Philippines Only")

# List of allowed Philippine cities (full names)
philippine_cities = [
    "Manila", "Quezon City", "Davao City", "Cebu City", "Zamboanga City", "Baguio City",
    "Iloilo City", "General Santos City", "Tagum City", "Cagayan de Oro City", "Butuan City",
    "Tacloban City", "Bacolod City", "Puerto Princesa City", "Legazpi City", "Pagadian City",
    "Cotabato City", "Naga City", "Dumaguete City", "San Fernando City"
]

# Fallback city in case the city is not found
fallback_city = "Davao City"

# Text input for city name
city = st.text_input("Enter a city in the Philippines:", "Davao City")

# Normalize input (e.g., "davao city" → "Davao City")
normalized_city = city.strip().title()

# Function to get weather data for a city
def get_weather_data(city_name):
    api_key = "dd66b7ef57014edc71bae97301470c1f"  # Use your actual API key
    url = f"http://api.openweathermap.org/data/2.5/weather?q={city_name},PH&appid={api_key}&units=metric"
    response = requests.get(url)

    if response.status_code == 200:
        return response.json()
    else:
        return None

# If the city is in the allowed list, fetch weather data
if normalized_city:
    if normalized_city in philippine_cities:
        data = get_weather_data(normalized_city)
        if data:
            weather_data = {
                "City": normalized_city,
                "Temperature (°C)": data['main']['temp'],
                "Weather": data['weather'][0]['description'].title(),
                "Humidity (%)": data['main']['humidity'],
                "Wind Speed (m/s)": data['wind']['speed']
            }

            df = pd.DataFrame([weather_data])
            st.subheader(f"📍 Weather Information for {normalized_city}")
            st.dataframe(df, use_container_width=True)

            # CSV download
            csv = df.to_csv(index=False).encode('utf-8')
            st.download_button(
                label="⬇️ Download as CSV",
                data=csv,
                file_name=f"{normalized_city}_weather.csv",
                mime="text/csv"
            )

            # Sample weekly forecast (dummy data)
            forecast_data = pd.DataFrame({
                'Day': ['Mon', 'Tue', 'Wed', 'Thu', 'Fri'],
                'Temperature': [29, 30, 31, 32, 30]
            })

            chart = alt.Chart(forecast_data).mark_line(point=True).encode(
                x='Day',
                y='Temperature'
            ).properties(title='📈 Sample Weekly Forecast')

            st.altair_chart(chart, use_container_width=True)

        else:
            st.error(f"⚠️ Weather data could not be retrieved for {normalized_city}. Showing data for fallback city.")
            # Use fallback city
            data = get_weather_data(fallback_city)
            if data:
                weather_data = {
                    "City": fallback_city,
                    "Temperature (°C)": data['main']['temp'],
                    "Weather": data['weather'][0]['description'].title(),
                    "Humidity (%)": data['main']['humidity'],
                    "Wind Speed (m/s)": data['wind']['speed']
                }

                df = pd.DataFrame([weather_data])
                st.subheader(f"📍 Weather Information for {fallback_city}")
                st.dataframe(df, use_container_width=True)
            else:
                st.error("⚠️ Weather data could not be retrieved for fallback city either. Please try again later.")

    else:
        st.error("❌ City not found in the Philippines list. Please enter a valid city.")
