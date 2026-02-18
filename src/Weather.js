import React, { useState } from "react";
import "./App.css";

function Weather() {
  const [city, setCity] = useState("");
  const [weatherData, setWeatherData] = useState([]);
  const [error, setError] = useState("");

  const apiKey = "419a2079613692a5f479d935c8288b7f"; // Replace with new key

  // Fetch 5-day forecast
  const fetchForecast = async (cityName) => {
    const response = await fetch(
      `https://api.openweathermap.org/data/2.5/forecast?q=${cityName}&appid=${apiKey}&units=metric`
    );
    const data = await response.json();
    return data;
  };

  const fetchWeather = async () => {
    if (city.trim() === "") {
      setError("Please enter city name");
      return;
    }

    setError("");
    setWeatherData([]);

    const cityList = city.split(",");

    for (let c of cityList) {
      try {
        const response = await fetch(
          `https://api.openweathermap.org/data/2.5/weather?q=${c.trim()}&appid=${apiKey}&units=metric`
        );

        const currentData = await response.json();

        if (currentData.cod === 200) {
          const forecastData = await fetchForecast(c.trim());

          // Filter one forecast per day (12:00:00)
          const dailyForecast = forecastData.list.filter(item =>
            item.dt_txt.includes("12:00:00")
          );

          setWeatherData((prev) => [
            ...prev,
            {
              current: currentData,
              forecast: dailyForecast
            }
          ]);
        } else {
          setError(`City not found: ${c.trim()}`);
        }

      } catch (err) {
        setError("Something went wrong");
      }
    }

    setCity("");
  };

  return (
    <div className="container">
      <h1>Weather Forecast App</h1>

      <input
        type="text"
        placeholder="Enter cities separated by comma"
        value={city}
        onChange={(e) => setCity(e.target.value)}
      />

      <button onClick={fetchWeather}>Get Weather</button>

      {error && <p className="error">{error}</p>}

      {weatherData.map((cityWeather, index) => (
        <div key={index} className="weather-card">
          <h2>{cityWeather.current.name}</h2>
          <p><strong>Current Temperature:</strong> {cityWeather.current.main.temp}°C</p>
          <p><strong>Humidity:</strong> {cityWeather.current.main.humidity}%</p>
          <p><strong>Description:</strong> {cityWeather.current.weather[0].description}</p>

          <img
            src={`https://openweathermap.org/img/wn/${cityWeather.current.weather[0].icon}@2x.png`}
            alt="weather icon"
          />

          <h3>5-Day Forecast</h3>

          <div className="forecast-container">
            {cityWeather.forecast.map((item, i) => (
              <div key={i} className="forecast-card">
                <p><strong>Date:</strong> {item.dt_txt.split(" ")[0]}</p>
                <p>Temp: {item.main.temp}°C</p>
                <p>Humidity: {item.main.humidity}%</p>
                <p>{item.weather[0].description}</p>

                <img
                  src={`https://openweathermap.org/img/wn/${item.weather[0].icon}@2x.png`}
                  alt="forecast icon"
                />
              </div>
            ))}
          </div>
        </div>
      ))}
    </div>
  );
}

export default Weather;
