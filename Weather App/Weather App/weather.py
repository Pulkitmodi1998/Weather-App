from tkinter import *
from PIL import Image, ImageTk
import tkinter as tk
from geopy.geocoders import Nominatim
from tkinter import ttk, messagebox
from timezonefinder import TimezoneFinder
from datetime import datetime
import requests
import pytz

background_color = "#FFF3E0"
root = Tk()
root.title("Weather App")
root.geometry("900x500+300+200")
root.resizable(False, False)
icon_image = PhotoImage(file="images/logo.png")  # Update with your icon path
root.iconphoto(False, icon_image)
root.configure(bg=background_color)

# Create a dictionary to store weather data for multiple cities
weather_data_list = []


# Function to fetch weather data from API
def fetch_weather_data(city):
    try:
        # Use a more specific user agent
        geolocator = Nominatim(user_agent="my_unique_weather_app")
        location = geolocator.geocode(city)

        if location:
            obj = TimezoneFinder()
            result = obj.timezone_at(lng=location.longitude, lat=location.latitude)

            if result:
                home = pytz.timezone(result)
                local_time = datetime.now(home)
                current_time = local_time.strftime("%I:%M %p")

                # API call to fetch weather data
                api = f"https://api.openweathermap.org/data/2.5/weather?q={city}&appid=69bb3eb80c8ed98b3c3cac8612b4e188"
                json_data = requests.get(api).json()

                if 'weather' in json_data:
                    # Store weather data in variables
                    temp = int(json_data['main']['temp'] - 273.15)  # Kelvin to Celsius
                    condition = json_data['weather'][0]['main']
                    description = json_data['weather'][0]['description']
                    pressure = json_data['main']['pressure']
                    humidity = json_data['main']['humidity']
                    wind = json_data['wind']['speed']
                    icon_code = json_data['weather'][0]['icon']  # Get icon code (01d, 02n, etc.)

                    # Store weather data in a dictionary
                    weather_data = {
                        "city": city,
                        "temperature": temp,
                        "condition": condition,
                        "description": description,
                        "pressure": pressure,
                        "humidity": humidity,
                        "wind": wind,
                        "icon_code": icon_code,
                        "time": current_time
                    }

                    return weather_data
                else:
                    messagebox.showerror("Error", f"Error fetching weather data: {json_data.get('message', 'Unknown error')}")
            else:
                messagebox.showerror("Error", "Could not determine the timezone for the location.")
        else:
            messagebox.showerror("Error", "City not found. Please enter a valid city name.")
    except Exception as e:
        messagebox.showerror("Error", f"Failed to retrieve weather data.\nError: {e}")
    return None

# Function to fetch weather forecast data
def fetch_forecast_data(city):
    try:
        # Fetch the 5-day forecast data (every 3 hours)
        api = f"https://api.openweathermap.org/data/2.5/forecast?q={city}&appid=69bb3eb80c8ed98b3c3cac8612b4e188"
        json_data = requests.get(api).json()

        forecast_list = []
        if 'list' in json_data:
            for forecast in json_data['list'][:5]:  # Get first 5 entries (3-hour intervals)
                dt_txt = forecast['dt_txt']
                temp = int(forecast['main']['temp'] - 273.15)  # Kelvin to Celsius
                icon_code = forecast['weather'][0]['icon']

                forecast_list.append({
                    "time": dt_txt,
                    "temperature": temp,
                    "icon_code": icon_code
                })

        return forecast_list

    except Exception as e:
        messagebox.showerror("Error", f"Failed to retrieve forecast data.\nError: {e}")
    return None

# Function to display weather forecast data in the marked area
def display_forecast_data(forecast_list):
    if forecast_list:
        for idx, forecast in enumerate(forecast_list):
            # Display forecast time
            forecast_time_label = Label(root, text=forecast['time'], font=("Helvetica", 10), bg=background_color)
            forecast_time_label.place(x=650, y=50 + (idx * 70))

            # Display forecast temperature
            forecast_temp_label = Label(root, text=f"{forecast['temperature']} °C", font=("Helvetica", 12), bg=background_color)
            forecast_temp_label.place(x=780, y=50 + (idx * 70))

            # Display forecast icon
            icon_path = f"images/{forecast['icon_code']}.png"
            img = Image.open(icon_path)
            resized_img = img.resize((50, 50), Image.Resampling.LANCZOS)
            forecast_icon_image = ImageTk.PhotoImage(resized_img)
            forecast_icon_label = Label(root, image=forecast_icon_image, bg=background_color)
            forecast_icon_label.image = forecast_icon_image  # Keep a reference
            forecast_icon_label.place(x=830, y=35 + (idx * 70))


# Function to display weather data on GUI
def display_weather_data(weather_data):
    # Update GUI with fetched weather data
    if weather_data:
        t.config(text=f"{weather_data['temperature']} °C")
        c.config(text=f"{weather_data['condition']} | FEELS LIKE {weather_data['temperature']} °C")
        w.config(text=weather_data['wind'])
        h.config(text=weather_data['humidity'])
        d.config(text=weather_data['description'])
        p.config(text=weather_data['pressure'])
        clock.config(text=weather_data['time'])
        name.config(text="CURRENT WEATHER")

        # Display weather icon
        icon_path = f"images/{weather_data['icon_code']}.png"
        img = Image.open(icon_path)
        resized_img = img.resize((250, 250), Image.Resampling.LANCZOS)  # Resize the image to 250x250 pixels
        weather_image = ImageTk.PhotoImage(resized_img)
        logo.config(image=weather_image, bg=background_color)
        logo.image = weather_image  # Keep a reference to avoid garbage collection

# Function to get weather for multiple cities
def getWeather():
    city = textfield.get()

    if city:
        # Fetch weather data for entered city and display it
        weather_data = fetch_weather_data(city)
        if weather_data:
            weather_data_list.append(weather_data)  # Add to the list of weather data for multiple cities
            display_weather_data(weather_data)

        # Fetch and display forecast data for the entered city
        forecast_data = fetch_forecast_data(city)
        if forecast_data:
            display_forecast_data(forecast_data)
    else:
        messagebox.showerror("Input Error", "Please enter a city name.")


# Search Box
Search_image = PhotoImage(file="images/search.png")
myimage=Label(image=Search_image, bg="#FFF3E0")
myimage.place(x=20,y=20)

textfield=tk.Entry(root, justify="center", width=17, font=("poppins", 25, "bold"), bg="#43403C", border=0, fg="white")
textfield.place(x=50,y=40)

Search_icon=PhotoImage(file="images/search_icon.png")
myimage_icon=Button(image=Search_icon, borderwidth=0, cursor="hand2", bg="#43403C", command=getWeather)
myimage_icon.place(x=400, y=34)

# Logo
Logo_image=PhotoImage(file="images/logo.png")
logo=Label(image=Logo_image, bg=background_color)
logo.place(x=150,y=100)

# Time
name= Label(root, font=("arial", 15,"bold"), bg=background_color)
name.place(x=30, y=100)
clock=Label(root, font=("Helvetica", 20), bg=background_color)
clock.place(x=30, y=130)

# Bottom Box
Frame_image=PhotoImage(file="images/box.png")
frame_myimage=Label(image=Frame_image, bg=background_color)
frame_myimage.pack(padx=5, pady=5, side=BOTTOM)

# Weather info labels
label1=Label(root,text="WIND",font=("Helvetica", 15, "bold"), fg="white", bg="#1CB5ED")
label1.place(x=120, y=400)

label2=Label(root,text="HUMIDITY",font=("Helvetica", 15, "bold"), fg="white", bg="#1CB5ED")
label2.place(x=250, y=400)

label3=Label(root,text="DESCRIPTION",font=("Helvetica", 15, "bold"), fg="white", bg="#1CB5ED")
label3.place(x=430, y=400)

label4=Label(root,text="PRESSURE",font=("Helvetica", 15, "bold"), fg="white", bg="#1CB5ED")
label4.place(x=650, y=400)

t=Label(font=("arial", 70, "bold"), fg="#ee666d", bg=background_color)
t.place(x=400, y=150)
c=Label(font=("arial", 15, "bold"), bg=background_color)
c.place(x=400, y=250)

w=Label(text="...", font=("arial", 20, "bold"), bg="#1CB5ED")
w.place(x=124,y=430)

h=Label(text="...", font=("arial", 20, "bold"), bg="#1CB5ED")
h.place(x=254,y=430)

d=Label(text="...", font=("arial", 20, "bold"), bg="#1CB5ED")
d.place(x=435,y=430)

p=Label(text="...", font=("arial", 20, "bold"), bg="#1CB5ED")
p.place(x=655,y=430)

root.mainloop()