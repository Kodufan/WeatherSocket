import os
import asyncio
import websockets
import requests 
import json
from datetime import datetime
import time

async def echo(websocket, path):
    def get_time():
        time = datetime.now().strftime("[%d/%m/%Y %H:%M:%S]:")
        return time
    print (get_time(),"User connected")
    try:
        async for message in websocket:
            command = message.split(";")[0]
            city_name = message.split(";")[1]
            units = message.split(";")[2]
            if command == "World Weather":
                api_key = "Enter API Key here"
                base_url = "http://api.openweathermap.org/data/2.5/weather?"
                complete_url = base_url + "id=524901&" + "appid=" + api_key + "&q=" + city_name + "&units=imperial"
                # Despite being in imperial, the units can be changed to Metric with simple logix ingame.

                response = requests.get(complete_url)
                currentJSON = response.json()
                print (get_time(),"World weather called at",city_name)
                try:
                    city = currentJSON["name"]
                except:
                    await websocket.send(";32;Invalid city;0;0;0;0;0")
                    continue
                weather_description = currentJSON["weather"][0]["description"]
                temp = currentJSON["main"]["temp"]
                temp_feels = currentJSON["main"]["feels_like"]
                humidity = currentJSON["main"]["humidity"]
                wind_speed = currentJSON["wind"]["speed"]
                wind_angle = currentJSON["wind"]["deg"]
                sunrise = currentJSON["sys"]["sunrise"]
                sunset = currentJSON["sys"]["sunset"]
                await websocket.send(weather_description + ";" + str(temp) + ";" + city + ";" + str(humidity) + ";" + str(wind_speed) + ";" + str(wind_angle) + ";" + str(sunrise) + ";" + str(sunset))
                # Description;Temp;Feel like temp;Humidity;wind speed;wind angle;sunrise;sunset

                time.sleep(3)
                # This is a measure to keep your API key from being called too many times.
    except websockets.exceptions.ConnectionClosedError:
        print(get_time(),"User disconnected")

asyncio.get_event_loop().run_until_complete(
    websockets.serve(echo, 'localhost', 8765))
asyncio.get_event_loop().run_forever()