#!/usr/bin/env python3
"""
Test script to verify OpenWeatherMap One Call API 3.0 key
"""
import os
import requests
from dotenv import load_dotenv

def test_geocoding_api():
    """Test the Geocoding API first"""
    load_dotenv()
    api_key = os.getenv('OPENWEATHERMAP_API_KEY')
    
    print("🗺️  Testing Geocoding API...")
    
    url = 'http://api.openweathermap.org/geo/1.0/direct'
    params = {
        'q': 'London',
        'limit': 1,
        'appid': api_key
    }
    
    try:
        response = requests.get(url, params=params, timeout=10)
        
        if response.status_code == 200:
            data = response.json()
            if data:
                print(f"✅ Geocoding API working! Found: {data[0]['name']}, {data[0].get('country', '')}")
                return data[0]['lat'], data[0]['lon']
            else:
                print("❌ No location data returned")
                return None, None
        else:
            print(f"❌ Geocoding API error: {response.status_code} - {response.text}")
            return None, None
            
    except Exception as e:
        print(f"❌ Geocoding API error: {e}")
        return None, None

def test_onecall_api(lat, lon):
    """Test the One Call API 3.0"""
    load_dotenv()
    api_key = os.getenv('OPENWEATHERMAP_API_KEY')
    
    print("🌤️  Testing One Call API 3.0...")
    
    url = 'https://api.openweathermap.org/data/3.0/onecall'
    params = {
        'lat': lat,
        'lon': lon,
        'exclude': 'minutely,hourly,daily,alerts',  # Only get current weather for testing
        'units': 'metric',
        'appid': api_key
    }
    
    try:
        response = requests.get(url, params=params, timeout=10)
        
        if response.status_code == 200:
            data = response.json()
            current = data['current']
            print("✅ One Call API 3.0 is working!")
            print(f"🌡️  Temperature: {current['temp']}°C")
            print(f"🌤️  Weather: {current['weather'][0]['description']}")
            return True
        elif response.status_code == 401:
            print("❌ Unauthorized: Invalid API key")
            return False
        elif response.status_code == 402:
            print("❌ Payment Required: You need to subscribe to 'One Call by Call' plan")
            print("💡 Go to: https://openweathermap.org/price#onecall")
            return False
        elif response.status_code == 429:
            print("❌ Too Many Requests: Rate limit exceeded")
            return False
        else:
            print(f"❌ API error: {response.status_code} - {response.text}")
            return False
            
    except Exception as e:
        print(f"❌ One Call API error: {e}")
        return False

def test_api_key():
    """Main test function"""
    load_dotenv()
    api_key = os.getenv('OPENWEATHERMAP_API_KEY')
    
    if not api_key:
        print("❌ No API key found in environment variables!")
        return False
    
    print(f"🔑 Testing API key: {api_key}")
    
    # Test geocoding first
    lat, lon = test_geocoding_api()
    if lat is None or lon is None:
        return False
    
    # Test One Call API
    return test_onecall_api(lat, lon)

if __name__ == "__main__":
    print("🧪 OpenWeatherMap One Call API 3.0 Validator")
    print("=" * 50)
    
    success = test_api_key()
    
    if not success:
        print("\n🔄 Next steps:")
        print("1. Ensure you have a valid OpenWeatherMap account")
        print("2. Subscribe to 'One Call by Call' plan at: https://openweathermap.org/price#onecall")
        print("3. Get your API key from: https://home.openweathermap.org/api_keys")
        print("4. Update your .env file with the correct key")
        print("5. Wait a few minutes for the subscription to activate")
    else:
        print("\n🎉 Your API key is working perfectly with One Call API 3.0!")
        print("You can now run the weather assistant.")