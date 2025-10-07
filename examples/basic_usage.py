"""
Basic usage example

Before running:
1. Get your API key from https://openweathermap.org/api
2. Set it as env var: export OPENWEATHERMAP_API_KEY='your-key'
    OR pass it directly to the client
"""
from py_openweathermap import OpenWeatherMapClient
from py_openweathermap.exceptions import (
    AuthenticationError, WrongLatitudeOrLongitude, RateLimitError, PyOpenWeatherMapError
)

def example_basic_usage():
    """Basic weather lookup by coordinates"""
    print('='*60)
    print('Example 1: Basic Usage')
    print('='*60)

    try:
        client = OpenWeatherMapClient()

        # Get wetaher for London coordinates
        weather = client.get_current_weather_by_coords(lat=51.5074, lon=0.1278)

        # Simple output
        print(f'\n{weather}')

        # Detailed output
        print(f"\nLocation: {weather.name}, {weather.sys.country}")
        print(f"Temperature: {weather.main.temp}°")
        print(f"Feels like: {weather.main.feels_like}°")
        print(f"Condition: {weather.weather[0].description}")
        print(f"Humidity: {weather.main.humidity}%")
        print(f"Wind: {weather.wind.speed} m/s, {weather.wind.deg}°")
        print(f"Cloudiness: {weather.clouds.all}%")

    except AuthenticationError:
        print('Error: Invalid or missing API key')
    except Exception as e:
        print(f'Error: {str(e)}')

def example_with_units():
    """Using different temperature units."""
    print("\n" + "=" * 60)
    print("Example 2: Different Units")
    print("=" * 60)
    
    # Coordinates for New York City
    lat, lon = 40.7128, -74.0060
    
    # Metric (Celsius, m/s)
    client_metric = OpenWeatherMapClient(units='metric')
    weather_metric = client_metric.get_current_weather_by_coords(lat, lon)
    print(f"\nMetric: {weather_metric.main.temp}°C")
    
    # Imperial (Fahrenheit, mph)
    client_imperial = OpenWeatherMapClient(units='imperial')
    weather_imperial = client_imperial.get_current_weather_by_coords(lat, lon)
    print(f"Imperial: {weather_imperial.main.temp}°F")
    
    # Standard (Kelvin)
    client_standard = OpenWeatherMapClient(units='standard')
    weather_standard = client_standard.get_current_weather_by_coords(lat, lon)
    print(f"Standard: {weather_standard.main.temp}K")

def example_multiple_cities():
    """Check weather for multiple cities."""
    print("\n" + "=" * 60)
    print("Example 3: Multiple Cities")
    print("=" * 60)
    
    cities = {
        "London": (51.5074, -0.1278),
        "Paris": (48.8566, 2.3522),
        "Tokyo": (35.6762, 139.6503),
        "New York": (40.7128, -74.0060),
        "Sydney": (-33.8688, 151.2093),
    }
    
    client = OpenWeatherMapClient()
    
    print(f"\n{'City':<15} {'Temp':<8} {'Condition':<25} {'Humidity'}")
    print("-" * 60)
    
    for city_name, (lat, lon) in cities.items():
        try:
            weather = client.get_current_weather_by_coords(lat, lon)
            print(
                f"{city_name:<15} "
                f"{weather.main.temp}°{'':<4} "
                f"{weather.weather[0].description:<25} "
                f"{weather.main.humidity}%"
            )
        except Exception as e:
            print(f"{city_name:<15} Error: {e}")

def example_error_handling():
    """Demonstrate proper error handling."""
    print("\n" + "=" * 60)
    print("Example 4: Error Handling")
    print("=" * 60)
    
    client = OpenWeatherMapClient()
    
    # Invalid coordinates (out of range)
    print("\nTrying invalid coordinates...")
    try:
        weather = client.get_current_weather_by_coords(lat=999, lon=999)
    except WrongLatitudeOrLongitude as e:
        print(f"Caught WrongLatitudeOrLongitude: {e}")
    
    # Test with invalid API key
    print("\nTrying invalid API key...")
    try:
        bad_client = OpenWeatherMapClient(api_key='invalid_key_12345')
        weather = bad_client.get_current_weather_by_coords(51.5074, -0.1278)
    except AuthenticationError as e:
        print(f"Caught AuthenticationError: {e}")
    
    # General error handling pattern
    print("\nRecommended error handling pattern:")
    try:
        weather = client.get_current_weather_by_coords(51.5074, -0.1278)
        print(f"Success: {weather}")
    except AuthenticationError:
        print("Please check your API key")
    except RateLimitError:
        print("Rate limit exceeded, try again later")
    except PyOpenWeatherMapError as e:
        print(f"API error: {e}")

if __name__ == "__main__":
    example_basic_usage()
    example_with_units()
    example_multiple_cities()
    example_error_handling()