import pytest
from unittest.mock import Mock, patch
from py_openweathermap import OpenWeatherMapClient, CurrentWeather
from py_openweathermap.exceptions import (
    AuthenticationError, InvalidParameterError
)
from py_openweathermap.constants import CURRENT_WEATHER_ENDPOINT

class TestClientInitialization:
    """Tests for client initialization"""
    def test_init_with_api_key(self):
        """Test client initializes with API key"""
        client = OpenWeatherMapClient(api_key='test_api_key')
        assert client.api_key == 'test_api_key'
        assert client.units == 'metric'
        assert client.timeout == 10

    def test_init_without_api_key_raises_errors(self):
        """Test client raises error when no API key is provided"""
        with pytest.raises(AuthenticationError):
            OpenWeatherMapClient()

    def test_init_with_invalid_units_raises_errors(self):
        """Test client raises error for invalid units"""
        with pytest.raises(InvalidParameterError):
            OpenWeatherMapClient(api_key='test_api_key', units='invalid')

    @patch.dict('os.environ', {'OPENWEATHERMAP_API_KEY': 'test_api_key'})
    def test_init_from_env_var(self):
        """Test client reads API key from environment"""
        client = OpenWeatherMapClient()
        assert client.api_key == 'test_api_key'

class TestCurrentWeatherByCoords:
    """Tests for get_current_weather_by_coords method"""
    @pytest.fixture
    def mock_api_response(self):
        """Sample response matching OpenWeatherMap structure"""
        return {
            "coord": {"lon": -0.13, "lat": 51.51},
            "weather": [
                {
                    "id": 300,
                    "main": "Drizzle",
                    "description": "light intensity drizzle",
                    "icon": "09d"
                }
            ],
            "base": "stations",
            "main": {
                "temp": 280.32,
                "feels_like": 278.43,
                "temp_min": 279.15,
                "temp_max": 281.15,
                "pressure": 1012,
                "humidity": 81,
                "sea_level": 1012,
                "grnd_level": 1010
            },
            "visibility": 10000,
            "wind": {
                "speed": 4.1,
                "deg": 80,
                "gust": 6.2
            },
            "clouds": {"all": 90},
            "dt": 1485789600,
            "sys": {
                "type": 1,
                "id": 5091,
                "country": "GB",
                "sunrise": 1485762037,
                "sunset": 1485794875
            },
            "timezone": 0,
            "id": 2643743,
            "name": "London",
            "cod": 200
        }
    
    @patch('py_openweathermap.client.OpenWeatherMapClient._make_request')
    def test_get_current_weather_by_coords(self, mock_make_request, mock_api_response):
        """Test successful weather retrieval by coordinates"""
        mock_make_request.return_value = mock_api_response

        # Make request
        client = OpenWeatherMapClient(api_key='test-api-key')
        weather = client.get_current_weather_by_coords(lat=51.51, lon=-0.13)

        # Verify make request was called correctly
        mock_make_request.assert_called_once_with(
            CURRENT_WEATHER_ENDPOINT,
            {
                'lat': 51.51,
                'lon': -0.13,
                'units': client.units
            }
        )

        # Assertions
        assert isinstance(weather, CurrentWeather)
        assert weather.name == "London"
        assert weather.coord.lat == 51.51
        assert weather.coord.lon == -0.13
        assert weather.main.temp == 280.32
        assert weather.weather[0].description == "light intensity drizzle"
        assert weather.sys.country == "GB"
