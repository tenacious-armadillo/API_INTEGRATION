import requests
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# Replace 'your_api_key' with your actual OpenWeatherMap API key
API_KEY = 'e19210cde1680010d287838a69dead8f'
CITY = 'Vizianagaram'
URL = f"http://api.openweathermap.org/data/2.5/forecast?q={CITY}&appid={API_KEY}"

def fetch_weather_data(url):
    response = requests.get(url)
    if response.status_code == 200:
        return response.json()
    else:
        print("Status Code:", response.status_code)
        print("Response Text:", response.text)
        raise Exception("Error fetching data from OpenWeatherMap API")

def parse_weather_data(data):
    forecast_list = data['list']
    parsed_data = []
    for forecast in forecast_list:
        date_time = forecast['dt_txt']
        temperature = forecast['main']['temp'] - 273.15  # Convert from Kelvin to Celsius
        humidity = forecast['main']['humidity']
        weather = forecast['weather'][0]['description']
        parsed_data.append([date_time, temperature, humidity, weather])
    return parsed_data

def create_dataframe(parsed_data):
    df = pd.DataFrame(parsed_data, columns=['DateTime', 'Temperature(C)', 'Humidity(%)', 'Weather'])
    df['DateTime'] = pd.to_datetime(df['DateTime'])
    print("DataFrame Info:\n", df.info())  # Debug print
    print("DataFrame Head:\n", df.head())  # Debug print
    return df

def visualize_data(df):
    plt.figure(figsize=(12, 6))
    
    plt.subplot(2, 1, 1)
    sns.lineplot(x='DateTime', y='Temperature(C)', data=df)
    plt.title(f'Temperature Forecast for {CITY}')
    plt.xlabel('DateTime')
    plt.ylabel('Temperature (C)')
    plt.xticks(rotation=45)

    plt.subplot(2, 1, 2)
    sns.lineplot(x='DateTime', y='Humidity(%)', data=df)
    plt.title(f'Humidity Forecast for {CITY}')
    plt.xlabel('DateTime')
    plt.ylabel('Humidity (%)')
    plt.xticks(rotation=45)

    plt.tight_layout()
    plt.show()

if __name__ == "__main__":
    weather_data = fetch_weather_data(URL)
    parsed_data = parse_weather_data(weather_data)
    df = create_dataframe(parsed_data)
    visualize_data(df)
