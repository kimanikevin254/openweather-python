import pytest
import requests
from unittest.mock import Mock, patch
from py_openweathermap import OpenWeatherMapClient, CurrentWeather
from py_openweathermap.exceptions import (
    AuthenticationError, InvalidParameterError, NotFoundError, 
    RateLimitError, PyOpenWeatherMapError
)
from py_openweathermap.constants import CURRENT_WEATHER_ENDPOINT, BASE_URL

class TestClientInitialization:
    """Tests for client initialization"""
    def test_init_with_api_key(self):
        """Test client initializes with API key"""
        client = OpenWeatherMapClient(api_key='test_api_key')
        assert client.api_key == 'test_api_key'
        assert client.units == 'metric'
        assert client.timeout == 10

    @patch.dict('os.environ', {}, clear=True)
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

class TestMakeResult:
    """Tests for _make_request private method"""
    
    @pytest.fixture
    def client(self):
        """Create a test client"""
        return OpenWeatherMapClient(api_key='test-api-key')
    
    @pytest.fixture
    def mock_success_response(self):
        """Mock a successful response"""
        mock_resp = Mock()
        mock_resp.status_code = 200
        mock_resp.json.return_value = {'test': 'data'}
        return mock_resp
    
    @patch('py_openweathermap.client.requests.get')
    def test_make_request_success(self, mock_get, client, mock_success_response):
        """Test successful API request"""
        mock_get.return_value = mock_success_response

        result = client._make_request('/test', {'q': 'London'})

        # Verify request was made successfully
        mock_get.assert_called_once_with(
            url=f"{BASE_URL}/test",
            params={'q': 'London', 'appid': 'test-api-key'},
            timeout=10
        )
        
        assert result == {'test': 'data'}

    @patch('py_openweathermap.client.requests.get')
    def test_make_request_adds_api_key(self, mock_get, client, mock_success_response):
        """Test API key is automatically added to params"""
        mock_get.return_value = mock_success_response

        client._make_request('/test', {'q': 'London'})

        call_params = mock_get.call_args[1]['params']
        assert 'appid' in call_params
        assert call_params['appid'] == 'test-api-key'

    @patch('py_openweathermap.client.requests.get')
    def test_make_request_uses_custom_timeout(self, mock_get, mock_success_response):
        """Test custom timeout is used"""
        client = OpenWeatherMapClient(api_key='test_api_key', timeout=25)
        mock_get.return_value = mock_success_response

        client._make_request('/test', {'q': 'London'})

        timeout = mock_get.call_args[1]['timeout']
        assert timeout == 25

    @patch('py_openweathermap.client.requests.get')
    def test_make_request_401_raises_authentication_error(self, mock_get, client):
        """Test 401 status code raise AuthenticationError"""
        mock_resp = Mock()
        mock_resp.status_code = 401
        mock_get.return_value = mock_resp

        with pytest.raises(AuthenticationError, match='Invalid API key'):
            client._make_request('/test', {})

    @patch('py_openweathermap.client.requests.get')
    def test_make_request_404_raises_not_found_error(self, mock_get, client):
        "Test 404 status raise NotFoundError"
        mock_resp = Mock()
        mock_resp.status_code = 404
        mock_get.return_value = mock_resp

        with pytest.raises(NotFoundError, match='Location not found'):
            client._make_request('/test', {})

    @patch('py_openweathermap.client.requests.get')
    def test_make_request_429_raises_rate_limit_error(self, mock_get, client):
        "Test 429 status raises RateLimitError"
        mock_resp = Mock()
        mock_resp.status_code = 429
        mock_get.return_value = mock_resp

        with pytest.raises(RateLimitError, match='API rate limit exceeded'):
            client._make_request('/test', {})

    @patch('py_openweathermap.client.requests.get')
    def test_make_request_500_raises_api_error(self, mock_get, client):
        """Test 5xx status code raises PyOpenWeatherMapError"""
        mock_resp = Mock()
        mock_resp.status_code = 500
        mock_get.return_value = mock_resp

        with pytest.raises(PyOpenWeatherMapError, match='API error'):
            client._make_request('/test', {})

    @patch('py_openweathermap.client.requests.get')
    def test_make_request_timeout_raises_error(self, mock_get, client):
        """Test request timeout is handled"""
        mock_get.side_effect = requests.exceptions.Timeout()

        with pytest.raises(PyOpenWeatherMapError, match='Request timed out'):
            client._make_request('/test', {})

    @patch('py_openweathermap.client.requests.get')
    def test_make_request_generic_request_exception(self, mock_get, client):
        """Test generic request exceptions are handled"""
        mock_get.side_effect = requests.exceptions.RequestException('Unknown error')

        with pytest.raises(PyOpenWeatherMapError, match='Request failed'):
            client._make_request('/test', {})


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
