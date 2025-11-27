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
- **`/resources`** - List all available resources from the MCP server
- **`/resource <resource_uri>`** - Load and work with specific resources
- **`exit`**, **`quit`**, or **`q`** - Exit the application cleanly

### Available Prompts

- **Weather Comparison**: `/prompt compare_weather_prompt "London" "Paris"`
  - Generates a structured comparison between two cities
  - Provides side-by-side analysis of temperature, conditions, and wind
  - Presents results in easy-to-read tables or bullet points

### Resource Management

The assistant can load and work with external resources:

- **`/resources`** - Shows available resources like:
  - `file://delivery_log` - Access delivery log data
  - `file://index` - Access index file data
- **`/resource file://delivery_log`** - Load delivery log content
  - After loading, you can specify actions like "analyze this data" or "summarize the orders"
  - Or press Enter to just add the content to conversation memory

### Example Resource Usage

```bash
You: /resources
# Lists: file://delivery_log, file://index

You: /resource file://delivery_log
Resource loaded. What should I do with this content? 
> analyze the delivery patterns

# The assistant will analyze the loaded delivery data and provide insights
```

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

You: /resources
# Lists available resources: file://delivery_log, file://index

You: /resource file://delivery_log
Resource loaded. What should I do with this content? 
> find the most common delivery cities
# Assistant analyzes the delivery data and identifies patterns

You: What's the weather like in London?
# Natural language query for current London weather

You: exit
# Clean exit without errors
```

## Features

### Weather Capabilities
- **Current Conditions**: Real-time weather data with detailed metrics
- **48-Hour Forecasts**: Hourly weather predictions 
- **8-Day Forecasts**: Extended daily weather outlook
- **Weather Alerts**: Severe weather warnings and advisories
- **UV Index & Air Quality**: Comprehensive atmospheric data
- **Smart Comparisons**: AI-generated weather comparisons between cities

### Interactive System
- **Structured Prompts**: Pre-defined prompt templates for consistent results
- **Resource Management**: Load and analyze external data files
- **Context Memory**: Maintains conversation history and loaded resource content
- **Clean Exits**: Proper error handling for graceful shutdowns
- **Command Discovery**: Built-in help system for available commands

The assistant provides comprehensive weather information including forecasts, alerts, detailed atmospheric conditions, and structured comparisons between locations. It also features resource management capabilities for loading and analyzing external data files.

## Technical Details

### Architecture
- **MCP Server**: Handles weather API calls and resource management
- **Weather Agent**: LangGraph-based conversational AI with Google Gemini
- **Protocol**: Model Context Protocol for structured tool and resource access
- **APIs**: OpenWeatherMap One Call API 3.0 for weather data

### Resource System
- **Delivery Log**: Sample delivery data for testing resource capabilities
- **Index File**: Additional data source for resource management examples
- **Extensible**: Easy to add new resource types and data sources

### Sample Data Files

This repository includes sample data files to demonstrate the resource management system:

- **`weather_agent/delivery_log.txt`** - Contains sample delivery order data with order numbers and cities
  - Format: "Order #XXXXX: Delivered to [City Name]" 
  - Access via: `/resource file://delivery_log`
  - Use cases: Data analysis, pattern recognition, city frequency analysis
- **Sample content**: Order deliveries to various US cities including San Diego, Austin, Raleigh, etc.

These files are included in the repository and ready to use for testing the resource management features.

## Security Notes

- Never commit your `.env` file to version control
- Keep your API keys secure and don't share them
- The `.gitignore` file is configured to exclude the `.env` file