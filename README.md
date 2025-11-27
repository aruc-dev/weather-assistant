# Weather Assistant

A weather assistant application using MCP (Model Context Protocol) with Google Gemini AI and OpenWeatherMap One Call API 3.0.

## Important: API Requirements

This application now uses **OpenWeatherMap One Call API 3.0** which provides comprehensive weather data including:
- Current weather conditions
- 48-hour hourly forecasts
- 8-day daily forecasts
- Weather alerts
- UV index and air quality data

**⚠️ Subscription Required**: One Call API 3.0 requires a separate "One Call by Call" subscription (includes 1,000 free calls per day).

## Project Structure

- `mcp_server/` - Contains the MCP server that provides weather data tools
- `weather_agent/` - Contains the client/agent code that interacts with the MCP server
- `.env` - Environment variables file (create from `.env.example`)
- `.env.example` - Template for environment variables

## Setup

1. **Python Requirements:**
   - Python 3.10 or higher is required
   - This project has been tested with Python 3.11.14

2. **Create a virtual environment (recommended):**
   ```bash
   python3.11 -m venv .venv
   source .venv/bin/activate  # On macOS/Linux
   # or
   .venv\Scripts\activate     # On Windows
   ```

3. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

4. **Configure environment variables:**
   ```bash
   # Copy the example environment file
   cp .env.example .env
   
   # Edit .env and add your actual API keys
   ```

3. **Get API Keys:**
   - **OpenWeatherMap One Call API 3.0**: 
     - Sign up at https://openweathermap.org/api
     - **Important**: Subscribe to "One Call by Call" plan (includes 1,000 calls/day free)
     - This is a separate subscription from the basic Current Weather API
     - Get your API key from the API keys section
   - **Google Gemini API**: Get your key from https://makersuite.google.com/app/apikey

4. **Update .env file:**
   ```
   OPENWEATHERMAP_API_KEY=your_actual_openweathermap_key
   GOOGLE_GEMINI_API_KEY=your_actual_gemini_key
   ```

## Running the Application

1. **Start the MCP Server:**
   ```bash
   cd mcp_server
   python main.py
   ```

2. **Start the Weather Agent (in a separate terminal):**
   ```bash
   cd weather_agent
   python main.py
   ```

## Usage

Once both components are running, you can interact with the weather assistant by typing natural language queries about weather information for different locations.

### Interactive Commands

The weather assistant now supports interactive commands for enhanced functionality:

- **`/prompts`** - List all available structured prompts and their usage
- **`/prompt <prompt_name> "arg1" "arg2"`** - Execute a specific prompt with arguments
- **`exit`**, **`quit`**, or **`q`** - Exit the application cleanly

### Available Prompts

- **Weather Comparison**: `/prompt compare_weather_prompt "London" "Paris"`
  - Generates a structured comparison between two cities
  - Provides side-by-side analysis of temperature, conditions, and wind
  - Presents results in easy-to-read tables or bullet points

### Natural Language Queries

**Enhanced capabilities with One Call API 3.0:**
- "What's the weather in New York?" - Get current conditions
- "What's the hourly forecast for London?" - Get detailed hourly data  
- "Will it rain in Tokyo this week?" - Get 8-day forecast
- "Are there any weather alerts for Miami?" - Get weather warnings
- "What's the UV index in Sydney?" - Get UV and air quality data
- "Compare the weather between Seattle and Portland" - Get AI-generated comparison

### Example Usage

```bash
You: /prompts
# Lists all available prompts

You: /prompt compare_weather_prompt "New York" "Los Angeles"
# Generates structured weather comparison between NYC and LA

You: What's the weather like in London?
# Natural language query for current London weather

You: exit
# Clean exit without errors
```

The assistant provides comprehensive weather information including forecasts, alerts, detailed atmospheric conditions, and structured comparisons between locations.

## Security Notes

- Never commit your `.env` file to version control
- Keep your API keys secure and don't share them
- The `.gitignore` file is configured to exclude the `.env` file