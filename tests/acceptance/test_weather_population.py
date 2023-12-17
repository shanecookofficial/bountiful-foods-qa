import os
import requests
from datetime import datetime, timedelta
import unittest
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from dotenv import load_dotenv
from pages.home import HomePage

class WeatherPopulationAcceptanceTest(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        # Load environment variables from .env file
        load_dotenv()

        # Set up Chrome options for WebDriver (optional, for headless mode, etc.)
        chrome_options = Options()
        # chrome_options.add_argument("--headless")  # Uncomment for headless mode

        # Initialize WebDriver
        cls.driver = webdriver.Chrome(options=chrome_options)

    def setUp(self):
        # Set up instance-specific components if needed
        self.home_page = HomePage(self.driver)

    def get_weather_data(self):
        api_key = os.environ.get('OPENWEATHER_API_KEY')
        weather_data = {}

        # Current Weather Data Call
        url = f'https://api.openweathermap.org/data/2.5/weather?lat=33.158092&lon=-117.350594&appid={api_key}'
        response = requests.get(url)
        if response.status_code == 200:
            raw_weather_data = response.json()
            weather_data = {
                'CURRENT_CONDITION': raw_weather_data['weather']['main'],
                'HUMIDITY': raw_weather_data['main']['humidity'],
                'CURRENT_TEMP': self.convert_kelvin_to_fahrenheit(raw_weather_data["main"]['temp']),
                'TODAY_LOW': self.convert_kelvin_to_fahrenheit(raw_weather_data["main"]['temp_min']),
                'TODAY_HIGH': self.convert_kelvin_to_fahrenheit(raw_weather_data["main"]['temp_max']),
            }
        else:
            # Handle errors or bad responses
            return None
        
        # 5 Day Weather Forecast Data Call
        url = f'api.openweathermap.org/data/2.5/forecast?lat=33.158092&lon=-117.350594&appid={api_key}'
        data9AM = self.get_data_9AM(url)
        weather_data['DAY_1_TEMP'] = self.convert_kelvin_to_fahrenheit(data9AM[0]['main']['temp'])
        weather_data['DAY_2_TEMP'] = self.convert_kelvin_to_fahrenheit(data9AM[1]['main']['temp'])
        weather_data['DAY_3_TEMP'] = self.convert_kelvin_to_fahrenheit(data9AM[2]['main']['temp'])

        return weather_data

    def convert_kelvin_to_fahrenheit(self, kelvin):
        return kelvin * (9/5) - 459.
    
    def get_data_9AM(self, url):
        response = requests.get(url)
        data_9AM = []
        if response.status_code == 200:
            raw_forecast_data = response.json()
            next_three_days = [datetime.now().date() + timedelta(days=i) for i in range(1, 4)]
            formatted_next_three_days_with_time = [date.strftime("%Y-%m-%d 9:00:00") for date in next_three_days]
            forecast_list = raw_forecast_data["list"]
            for forecast in forecast_list:
                if forecast['td_txt'] in formatted_next_three_days_with_time:
                    data_9AM.append(forecast['td_txt'] in formatted_next_three_days_with_time)
            return data_9AM
        else:
            # Handle errors or bad responses
            return None

    def test_weather_population(self):
        self.home_page.go_to_home_page()
        weather_data = self.get_weather_data()
        if HomePage.CURRENT_CONDITION.text != weather_data['CURRENT_CONDITION']:
            print(f'Verify Failed: Current Condition text is not {weather_data["CURRENT_CONDITION"]}')
        if HomePage.HUMIDITY.text != weather_data['HUMIDITY']:
            print(f'Verify Failed: Current Condition text is not {weather_data["HUMIDITY"]}')
        if HomePage.CURRENT_TEMP.text != weather_data['CURRENT_TEMP']:
            print(f'Verify Failed: Current Condition text is not {weather_data["CURRENT_TEMP"]}')
        # TODAY LOW
        # TODAY HIGH
        if HomePage.DAY_1_TEMP.text != weather_data['DAY_1_TEMP']:
            print(f'Verify Failed: Current Condition text is not {weather_data["DAY_1_TEMP"]}')
        if HomePage.DAY_2_TEMP.text != weather_data['DAY_2_TEMP']:
            print(f'Verify Failed: Current Condition text is not {weather_data["DAY_2_TEMP"]}')
        if HomePage.DAY_3_TEMP.text != weather_data['DAY_3_TEMP']:
            print(f'Verify Failed: Current Condition text is not {weather_data["DAY_3_TEMP"]}')
        
    @classmethod
    def tearDownClass(cls):
        cls.driver.close()  # Close the browser window

if __name__ == "__main__":
    unittest.main()
