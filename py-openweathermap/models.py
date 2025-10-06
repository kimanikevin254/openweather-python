"""Data models for API responses"""
from dataclasses import dataclass
from datetime import datetime
from typing import Optional, List

@dataclass
class Coordinates:
    """
    Geographic coordinates
    
    Attributes:
      lat: Latitude of the location
      lon: Longitude of the location
    """
    lat: float
    lon: float

    def __str__(self) -> str:
        return f"({self.lat}, {self.lon})"

@dataclass
class Weather:
    """
    Weather condition details

    Attributes:
        id: Weather condition id
        main: Group of weather parameters (Rain, Snow, Clouds etc.)
        description: Weather condition description
        icon: Weather icon id
    """
    id: int
    main: str
    description: str
    icon: str

    def __str__(self):
        return f"{self.main}: {self.description}"

@dataclass
class Main:
    """
    Main weather params

    Attributes:
      temp: current temperature
      feels_like: human perception of temperature
      temp_min: minimum temperature at the moment
      temp_max: maximum temperature at the moment
      pressure: atmospheric pressure (hPa)
      humidity: humidity percentage
      sea_level: atm pressure at sea level (hPa)
      grnd_level: atm pressure at ground level (hPa)
    """
    temp: float
    feels_like: float
    temp_min: float
    temp_max: float
    pressure: int
    humidity: int
    sea_level: int
    grnd_level: int

    def __str__(self):
        return f"{self.temp}° (feels like {self.feels_like}°)"
    
@dataclass
class Wind:
    """
    Wind information

    Attributes:
      speed: wind speed
      deg: wind direction in degrees
      gust: winf gust
    """
    speed: float
    deg: int
    gust: float

    def __str__(self):
        return self.speed

@dataclass
class Clouds:
    """
    Cloud information

    Attributes:
      all: cloudiness percentage
    """
    all: int

    def __str__(self):
        return f'{self.all}% clouds'

@dataclass
class Rain:
    """
    Rainfall information

    Attrs:
      one_h: rain precipitation for the last 1 hour in mm (optional)
    """
    one_h: Optional[float] = None

    def __str__(self):
        if self.one_h:
            return f"{self.one_h}mm (1h)"
        return "No rain data"
    
@dataclass
class Snow:
    """
    Snow information

    Attrs:
      one_h: snow precipitation for the last 1 hour in mm (optional)
    """
    one_h: Optional[float] = None

    def __str__(self):
        if self.one_h:
            return f"{self.one_h}mm (1h)"
        return "No snow data"
    
@dataclass
class Sys:
    """
    System information

    Attrs:
      type: Internal parameter
      id: Internal parameter
      country: Country code (GB, JP etc.)
      sunrise: Sunrise time, unix, UTC
      sunset: Sunset time, unix, UTC
    """
    type: int
    id: int
    country: str
    sunrise: int
    sunset: int

    def get_sunrise_time(self) -> datetime:
        """Convert sunrise timestamp to datetime."""
        return datetime.fromtimestamp(self.sunrise)
    
    def get_sunset_time(self) -> datetime:
        """Convert sunset timestamp to datetime."""
        return datetime.fromtimestamp(self.sunset)

    def __str__(self) -> str:
        sunrise_str = self.get_sunrise_time().strftime("%H:%M")
        sunset_str = self.get_sunset_time().strftime("%H:%M")
        return f"Sunrise: {sunrise_str}, Sunset: {sunset_str}"

@dataclass
class CurrentWeather:
    """Current weather data for a location"""
    coord: Coordinates
    weather: List[Weather]
    base: str
    main: Main
    visibility: int
    wind: Wind
    clouds: Clouds
    rain: Optional[Rain] = None
    snow: Optional[Snow] = None
    dt: int # Time of data calculation (unix timestamp)
    sys: Sys
    timezone: int # Shift in secs from UTC
    id: int # City ID
    name: str # City name
    cod: int # Internal param (response code)

    def get_timestamp(self) -> datetime:
        """Convert dt to datetime object"""    
        return datetime.fromtimestamp(self.dt)
    
    def __str__(self):
        """Human readable weather summary"""
        return (
            f"{self.name}, {self.sys.country}: {self.main.temp}°, "
            f"{self.weather[0].description}"
        )
    
    def __repr__(self):
        """Developer friendly representation"""
        return f"CurrentWeather(name='{self.name}', temp={self.main.temp})"
    
    