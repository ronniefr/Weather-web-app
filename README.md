
# Static Weather App

**A simple REST API + aesthetic UI for fetching (random/static) weather data. Built with FastAPI (Python backend) and HTML/CSS/JS (frontend)—great for learning API-to-UI flows. Upgrade to real-time data easily!**

## 🚩 Why use this?

- Quick GET endpoint for weather by city (simulated data for now)
- Clean, responsive UI with HTML/CSS/JS
- Modular: Backend reusable for other apps; UI fetches via JS
- Beginner-friendly: Teaches REST basics + frontend integration
- Path to production: Tips below for real APIs like OpenWeatherMap

## 🛠️ Features

- **API Endpoint:** GET `/weather/{city}` (returns random temp/condition)
- **UI:** Aesthetic display with JS fetch calls
- **Async Backend:** FastAPI for efficient handling
- **Extensible:** Add real-time data or more endpoints

## 🚀 Quickstart

1. **Backend (API):**  
    ```
    pip install fastapi uvicorn
    uvicorn app:app --reload
    ```
   - Docs: http://localhost:8000/docs

2. **Frontend (UI):**  
    Open `index.html` in browser (or deploy to Netlify/Vercel).  
    Ensure JS points to your backend URL.

3. **Full Stack:** Run backend, then load UI—JS will fetch data!

## 🔑 Upgrade to Real-Time Data

- Swap static data for a free API like OpenWeatherMap:  
  Get a key at [openweathermap.org](https://openweathermap.org).  
  In app.py:  
  ```
  import requests
  @app.get("/weather/{city}")
  async def get_weather(city: str):
      url = f"https://api.openweathermap.org/data/2.5/weather?q={city}&appid=YOUR_KEY"
      response = requests.get(url)
      return response.json()
  ```
- Test with curl: `curl http://localhost:8000/weather/london`

### ⚡ Example Output (API Response)

```
{"city": "London", "temp": 22, "condition": "Sunny"}
```

## 🤝 Contributing

- Fork and add real-time fetches, better UI animations, or auth!
- Open issues for features like multi-city support.

## 📄 License

MIT — free for all use cases!

