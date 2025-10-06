import pytest
from unittest.mock import Mock, patch
from py_openweathermap import OpenWeatherMapClient, CurrentWeather
from py_openweathermap.exceptions import (
    AuthenticationError, InvalidParameterError
)

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

    @patch('os.environ', {'OPENWEATHERMAP_API_KEY': 'test_api_key'})
    def test_init_from_env_var(self):
        """Test client reads API key from environment"""
        client = OpenWeatherMapClient()
        assert client.api_key == 'test_api_key'
