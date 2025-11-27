import os
import requests
from mcp.server.fastmcp import FastMCP
from dotenv import load_dotenv
import pathlib

# Load environment variables from the parent directory's .env file
env_path = pathlib.Path(__file__).parent.parent / '.env'
load_dotenv(env_path)

OPENWEATHERMAP_API_KEY = os.getenv("OPENWEATHERMAP_API_KEY")

if not OPENWEATHERMAP_API_KEY:
    print("Warning: OPENWEATHERMAP_API_KEY environment variable is not set!")
    print("Please set your OpenWeatherMap API key in the .env file.")

# Initialize the FastMCP server
mcp = FastMCP("WeatherAssistant")

@mcp.tool()
def list_available_tools() -> dict:
    """
    Lists all available tools in this MCP server.
    
    Returns:
        A dictionary containing information about all available tools.
    """
    return {
        "available_tools": [
            {
                "name": "get_weather",
                "description": "Fetches comprehensive weather data using OpenWeatherMap One Call API 3.0",
                "parameters": {
                    "location": "City name with optional country code (e.g., 'London,uk')"
                },
                "features": [
                    "Current weather conditions",
                    "48-hour hourly forecast", 
                    "8-day daily forecast",
                    "Weather alerts and warnings",
                    "UV index and visibility data"
                ]
            },
            {
                "name": "list_available_tools",
                "description": "Lists all available tools in this MCP server",
                "parameters": "None",
                "features": ["Tool discovery", "API documentation"]
            }
        ],
        "server_info": {
            "name": "WeatherAssistant",
            "api_version": "One Call API 3.0",
            "total_tools": 2
        }
    }

@mcp.tool()
def get_weather(location: str) -> dict:
    """
    Fetches comprehensive weather data for a specified location using OpenWeatherMap One Call API 3.0.
    
    This includes current weather, hourly forecast (48h), daily forecast (8 days), and weather alerts.

    Args:
        location: The city name and optional country code (e.g., "London,uk").

    Returns:
        A dictionary containing comprehensive weather information or an error message.
    """
    if not OPENWEATHERMAP_API_KEY:
        return {"error": "OpenWeatherMap API key is not configured on the server."}

    try:
        # Step 1: Get coordinates from location name using Geocoding API
        geocoding_url = "http://api.openweathermap.org/geo/1.0/direct"
        geocoding_params = {
            "q": location,
            "limit": 1,
            "appid": OPENWEATHERMAP_API_KEY
        }
        
        geo_response = requests.get(geocoding_url, params=geocoding_params)
        geo_response.raise_for_status()
        geo_data = geo_response.json()
        
        if not geo_data:
            return {"error": f"Could not find coordinates for '{location}'. Please check the location name."}
        
        lat = geo_data[0]["lat"]
        lon = geo_data[0]["lon"]
        city_name = geo_data[0]["name"]
        country = geo_data[0].get("country", "")
        
        # Step 2: Get weather data using One Call API 3.0
        onecall_url = "https://api.openweathermap.org/data/3.0/onecall"
        onecall_params = {
            "lat": lat,
            "lon": lon,
            "exclude": "minutely",  # Exclude minutely data to reduce response size
            "units": "metric",
            "appid": OPENWEATHERMAP_API_KEY
        }
        
        weather_response = requests.get(onecall_url, params=onecall_params)
        weather_response.raise_for_status()
        weather_data = weather_response.json()
        
        # Extract and format the relevant weather information
        current = weather_data["current"]
        daily = weather_data.get("daily", [])
        alerts = weather_data.get("alerts", [])
        
        # Format current weather
        formatted_data = {
            "location": f"{city_name}, {country}" if country else city_name,
            "coordinates": {"latitude": lat, "longitude": lon},
            "current_weather": {
                "description": current["weather"][0]["description"],
                "temperature_celsius": f"{current['temp']}°C",
                "feels_like_celsius": f"{current['feels_like']}°C",
                "humidity": f"{current['humidity']}%",
                "pressure": f"{current['pressure']} hPa",
                "wind_speed_mps": f"{current['wind_speed']} m/s",
                "wind_direction": f"{current.get('wind_deg', 'N/A')}°",
                "clouds": f"{current['clouds']}%",
                "uv_index": current['uvi'],
                "visibility": f"{current.get('visibility', 'N/A')} m"
            }
        }
        
        # Add today's forecast
        if daily:
            today = daily[0]
            formatted_data["today_forecast"] = {
                "summary": today.get("summary", "No summary available"),
                "min_temp": f"{today['temp']['min']}°C",
                "max_temp": f"{today['temp']['max']}°C",
                "morning_temp": f"{today['temp']['morn']}°C",
                "evening_temp": f"{today['temp']['eve']}°C",
                "precipitation_probability": f"{int(today['pop'] * 100)}%",
                "sunrise": f"Unix timestamp: {today['sunrise']}",
                "sunset": f"Unix timestamp: {today['sunset']}"
            }
        
        # Add next 3 days forecast
        if len(daily) > 1:
            formatted_data["3_day_forecast"] = []
            for day in daily[1:4]:  # Next 3 days
                formatted_data["3_day_forecast"].append({
                    "date": f"Unix timestamp: {day['dt']}",
                    "summary": day.get("summary", "No summary available"),
                    "min_temp": f"{day['temp']['min']}°C",
                    "max_temp": f"{day['temp']['max']}°C",
                    "weather": day["weather"][0]["description"],
                    "precipitation_probability": f"{int(day['pop'] * 100)}%"
                })
        
        # Add weather alerts if any
        if alerts:
            formatted_data["alerts"] = []
            for alert in alerts[:3]:  # Limit to 3 alerts
                formatted_data["alerts"].append({
                    "event": alert["event"],
                    "description": alert["description"][:200] + "..." if len(alert["description"]) > 200 else alert["description"],
                    "start": f"Unix timestamp: {alert['start']}",
                    "end": f"Unix timestamp: {alert['end']}"
                })
        
        return formatted_data

    except requests.exceptions.HTTPError as http_err:
        # Check which response caused the error
        if 'geo_response' in locals():
            status_code = geo_response.status_code
            if status_code == 401:
                return {"error": "Authentication failed. Please check your OpenWeatherMap API key."}
            elif status_code == 404:
                return {"error": f"Could not find location '{location}'. Please check the location name."}
            else:
                return {"error": f"Geocoding API error: {http_err}"}
        elif 'weather_response' in locals():
            status_code = weather_response.status_code
            if status_code == 401:
                return {"error": "Authentication failed. Please check your API key and ensure you're subscribed to One Call API 3.0."}
            elif status_code == 402:
                return {"error": "Subscription required. One Call API 3.0 requires a separate 'One Call by Call' subscription."}
            elif status_code == 429:
                return {"error": "API rate limit exceeded. Please try again later."}
            else:
                return {"error": f"Weather API error: {http_err}"}
        else:
            return {"error": f"HTTP error occurred: {http_err}"}
    except requests.exceptions.RequestException as req_err:
        return {"error": f"Network error occurred: {req_err}"}
    except KeyError as key_err:
        return {"error": f"Unexpected data format from weather API: missing field {key_err}"}
    except Exception as e:
        return {"error": f"An unexpected error occurred: {e}"}


if __name__ == "__main__":
    # The server will run and listen for requests from the client over stdio
    mcp.run(transport="stdio")