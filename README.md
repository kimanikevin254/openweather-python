# py-openweathermap

A clean, Pythponic wrapper for OpenWeatherMap API.

## Features

-   Pythonic interface: Clean, intuitive API
-   Type hints: Full type annotation support
-   Error handling: Comprehensive exception handling
-   Well tested: Extensive test coverage
-   Documented: Clear docs and examples
-   Simple: Minimal deps (just `requests`)

## Installation

```bash
pip install py-openweathermap
```

Or install from source:

```bash
git clone https://github.com/kimanikevin254/py-openweathermap.git
cd py-openweathermap
pip install -e .
```

## Quick Start

```py
from py_openweathermap import OpenWeatherMapClient

# Initialize client (reads from OPENWEATHERMAP_API_KEY env var)
client = OpenWeatherMapClient()

# Or pass API key directly
client = OpenWeatherMapClient(api_key='your_api_key')

# Get current weather by coordinates
weather = client.get_current_weather_by_coords(lat=51.5074, lon=-0.1278)

# Access weather data
print(f"Temperature: {weather.main.temp}°C")
print(f"Condition: {weather.weather[0].description}")
print(f"Humidity: {weather.main.humidity}%")
```

See [examples folder](/examples/) for more examples.

## Getting an API Key

1. Sign up at [OpenWeatherMap](https://openweathermap.org/api)
2. Get your free API key
3. Set it as an environment variable:

    ```bash
    export OPENWEATHERMAP_API_KEY='your_api_key'
    ```

## License

This project is licensed under the MIT License - see the [LICENSE](/LICENSE) file for details.

## Acknowledgments

-   Weather data provided by [OpenWeatherMap](https://openweathermap.org/)
