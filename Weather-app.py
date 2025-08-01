#!/usr/bin/env python3
"""
Weather API using FastAPI

A simple REST API for fetching weather data with async support and basic UI.
"""

from fastapi import FastAPI, HTTPException, Request
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel
from typing import Optional, Dict, Any
import asyncio
import random
from datetime import datetime


app = FastAPI(
    title="Weather API",
    description="A simple API for fetching weather information",
    version="1.0.0"
)


class WeatherData(BaseModel):
    """Model for weather data response."""
    city: str
    temperature: float
    description: str
    humidity: int
    pressure: int
    wind_speed: float
    timestamp: str


class WeatherService:
    """Service class for handling weather data operations."""
    
    @staticmethod
    async def fetch_weather_data(city: str) -> Dict[str, Any]:
        """
        Fetch or simulate weather data for a given city.
        
        Args:
            city: Name of the city to get weather for
            
        Returns:
            Dictionary containing weather data
            
        Raises:
            HTTPException: If city is not found or API error occurs
        """
        # Normalize city name
        normalized_city = city.strip().title()
        
        # Simulate API delay
        await asyncio.sleep(0.1)
        
        # Generate realistic weather data based on city name
        weather_descriptions = [
            "Sunny", "Partly Cloudy", "Cloudy", "Rainy", "Thunderstorm",
            "Snowy", "Foggy", "Windy", "Clear", "Overcast"
        ]
        
        # Simple city-based temperature simulation
        base_temp = 20.0  # Base temperature in Celsius
        if "north" in normalized_city.lower() or "northern" in normalized_city.lower():
            base_temp -= 10
        elif "south" in normalized_city.lower() or "southern" in normalized_city.lower():
            base_temp += 10
        elif "east" in normalized_city.lower():
            base_temp += 2
        elif "west" in normalized_city.lower():
            base_temp -= 2
            
        # Add some randomness
        temperature = round(base_temp + random.uniform(-5, 5), 1)
        description = random.choice(weather_descriptions)
        humidity = random.randint(30, 90)
        pressure = random.randint(980, 1040)
        wind_speed = round(random.uniform(0, 20), 1)
        timestamp = datetime.now().isoformat()
        
        return {
            "city": normalized_city,
            "temperature": temperature,
            "description": description,
            "humidity": humidity,
            "pressure": pressure,
            "wind_speed": wind_speed,
            "timestamp": timestamp
        }


# HTML template for the UI
HTML_TEMPLATE = """
<!DOCTYPE html>
<html>
<head>
    <title>Weather App</title>
    <meta charset="utf-8">
    <meta name="viewport" content="width=device-width, initial-scale=1">
    <style>
        * {
            box-sizing: border-box;
            margin: 0;
            padding: 0;
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
        }
        body {
            background: linear-gradient(135deg, #74b9ff, #0984e3);
            min-height: 100vh;
            display: flex;
            justify-content: center;
            align-items: center;
            padding: 20px;
        }
        .container {
            background-color: rgba(255, 255, 255, 0.9);
            border-radius: 15px;
            box-shadow: 0 10px 30px rgba(0, 0, 0, 0.2);
            width: 100%;
            max-width: 500px;
            padding: 30px;
        }
        h1 {
            color: #2d3436;
            text-align: center;
            margin-bottom: 25px;
            font-size: 2.2rem;
        }
        .form-group {
            margin-bottom: 20px;
        }
        label {
            display: block;
            margin-bottom: 8px;
            font-weight: 600;
            color: #2d3436;
        }
        input[type="text"] {
            width: 100%;
            padding: 15px;
            border: 2px solid #ddd;
            border-radius: 8px;
            font-size: 16px;
            transition: border-color 0.3s;
        }
        input[type="text"]:focus {
            border-color: #74b9ff;
            outline: none;
            box-shadow: 0 0 0 2px rgba(116, 185, 255, 0.2);
        }
        button {
            background: linear-gradient(to right, #74b9ff, #0984e3);
            color: white;
            border: none;
            padding: 15px;
            width: 100%;
            border-radius: 8px;
            font-size: 16px;
            font-weight: 600;
            cursor: pointer;
            transition: transform 0.2s, box-shadow 0.2s;
        }
        button:hover {
            transform: translateY(-2px);
            box-shadow: 0 5px 15px rgba(0, 0, 0, 0.1);
        }
        button:active {
            transform: translateY(0);
        }
        .result {
            margin-top: 25px;
            padding: 20px;
            border-radius: 8px;
            background-color: #f8f9fa;
            display: none;
        }
        .result h2 {
            color: #2d3436;
            margin-bottom: 15px;
            text-align: center;
        }
        .weather-info {
            display: grid;
            grid-template-columns: 1fr 1fr;
            gap: 15px;
        }
        .info-item {
            background-color: white;
            padding: 15px;
            border-radius: 8px;
            box-shadow: 0 2px 5px rgba(0, 0, 0, 0.05);
        }
        .info-label {
            font-weight: 600;
            color: #636e72;
            font-size: 14px;
            margin-bottom: 5px;
        }
        .info-value {
            font-size: 18px;
            color: #2d3436;
            font-weight: 700;
        }
        .error {
            color: #d63031;
            background-color: #ffeaa7;
            padding: 15px;
            border-radius: 8px;
            margin-top: 20px;
            display: none;
        }
        .loading {
            text-align: center;
            display: none;
        }
        .spinner {
            border: 4px solid rgba(0, 0, 0, 0.1);
            border-radius: 50%;
            border-top: 4px solid #74b9ff;
            width: 30px;
            height: 30px;
            animation: spin 1s linear infinite;
            margin: 0 auto 15px;
        }
        @keyframes spin {
            0% { transform: rotate(0deg); }
            100% { transform: rotate(360deg); }
        }
        @media (max-width: 480px) {
            .container {
                padding: 20px;
            }
            h1 {
                font-size: 1.8rem;
            }
            .weather-info {
                grid-template-columns: 1fr;
            }
        }
    </style>
</head>
<body>
    <div class="container">
        <h1>🌤️ Weather Forecast</h1>
        <form id="weatherForm">
            <div class="form-group">
                <label for="city">Enter City Name</label>
                <input type="text" id="city" name="city" placeholder="e.g., London, New York, Tokyo" required>
            </div>
            <button type="submit">Get Weather</button>
        </form>
        
        <div class="loading" id="loading">
            <div class="spinner"></div>
            <p>Fetching weather data...</p>
        </div>
        
        <div class="error" id="error"></div>
        
        <div class="result" id="result">
            <h2 id="resultCity">Weather in <span id="cityName">City</span></h2>
            <div class="weather-info">
                <div class="info-item">
                    <div class="info-label">Temperature</div>
                    <div class="info-value"><span id="temperature">--</span>°C</div>
                </div>
                <div class="info-item">
                    <div class="info-label">Condition</div>
                    <div class="info-value" id="description">--</div>
                </div>
                <div class="info-item">
                    <div class="info-label">Humidity</div>
                    <div class="info-value"><span id="humidity">--</span>%</div>
                </div>
                <div class="info-item">
                    <div class="info-label">Wind Speed</div>
                    <div class="info-value"><span id="windSpeed">--</span> m/s</div>
                </div>
                <div class="info-item">
                    <div class="info-label">Pressure</div>
                    <div class="info-value"><span id="pressure">--</span> hPa</div>
                </div>
                <div class="info-item">
                    <div class="info-label">Last Updated</div>
                    <div class="info-value" id="timestamp">--</div>
                </div>
            </div>
        </div>
    </div>

    <script>
        document.getElementById('weatherForm').addEventListener('submit', async function(e) {
            e.preventDefault();
            
            const city = document.getElementById('city').value.trim();
            if (!city) return;
            
            // Show loading, hide result and error
            document.getElementById('loading').style.display = 'block';
            document.getElementById('result').style.display = 'none';
            document.getElementById('error').style.display = 'none';
            
            try {
                const response = await fetch(`/weather/${encodeURIComponent(city)}`);
                
                if (!response.ok) {
                    const errorData = await response.json();
                    throw new Error(errorData.detail || 'Failed to fetch weather data');
                }
                
                const data = await response.json();
                
                // Update UI with weather data
                document.getElementById('cityName').textContent = data.city;
                document.getElementById('temperature').textContent = data.temperature;
                document.getElementById('description').textContent = data.description;
                document.getElementById('humidity').textContent = data.humidity;
                document.getElementById('pressure').textContent = data.pressure;
                document.getElementById('windSpeed').textContent = data.wind_speed;
                document.getElementById('timestamp').textContent = new Date(data.timestamp).toLocaleString();
                
                // Show result, hide loading
                document.getElementById('loading').style.display = 'none';
                document.getElementById('result').style.display = 'block';
            } catch (error) {
                // Show error, hide loading
                document.getElementById('loading').style.display = 'none';
                document.getElementById('error').textContent = error.message;
                document.getElementById('error').style.display = 'block';
            }
        });
    </script>
</body>
</html>
"""


@app.get("/", response_class=HTMLResponse)
async def root():
    """
    Serve the main HTML page with weather UI.
    
    Returns:
        HTML content for the weather application
    """
    return HTML_TEMPLATE


@app.get(
    "/weather/{city}",
    response_model=WeatherData,
    summary="Get weather data for a city",
    description="Retrieve current weather information for a specified city"
)
async def get_weather(city: str) -> WeatherData:
    """
    Get weather data for a specific city.
    
    Args:
        city: Name of the city to get weather for
        
    Returns:
        WeatherData object containing weather information
        
    Raises:
        HTTPException: If city parameter is invalid
    """
    if not city or not city.strip():
        raise HTTPException(
            status_code=400,
            detail="City name cannot be empty"
        )
    
    try:
        weather_service = WeatherService()
        weather_data = await weather_service.fetch_weather_data(city)
        return WeatherData(**weather_data)
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Error fetching weather data: {str(e)}"
        )


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)