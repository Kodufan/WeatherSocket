import os
import asyncio
import websockets
import sys
import requests 
import json
from datetime import date
import time
import random
from _datetime import datetime

wind_direction = ""
currentJSON = ""
onecallJSON = ""
city_name = ""

def convertSpeedToKMPH(speed):
    speed = speed * 1.609344
    return speed
def convertTempToCelsius(temp):
    temp = (temp - 32) * (5/9)
    return temp
async def echo(websocket, path):
    def get_time():
        time = datetime.now().strftime("[%d/%m/%Y %H:%M:%S]:")
        return time
    def getWindDir(wind_angle): 
        # The API gives the wind direction as an angle, and writes the cardinal direction to wind_direction
        if wind_angle >= 0 and wind_angle <= 22.5:
            wind_direction = "North"
        elif wind_angle > 22.5 and wind_angle <= 67.5:
            wind_direction = "North East"
        elif wind_angle > 67.5 and wind_angle <= 112.5:
            wind_direction = "East"
        elif wind_angle > 112.5 and wind_angle <= 157.5:
            wind_direction = "South East"
        elif wind_angle > 157.5 and wind_angle <= 202.5:
            wind_direction = "West"
        elif wind_angle > 202.5 and wind_angle <= 247.5:
            wind_direction = "South West"
        elif wind_angle > 247.5 and wind_angle <= 292.5:
            wind_direction = "West"
        elif wind_angle > 292.5 and wind_angle <= 337.5:
            wind_direction = "North West"
        elif wind_angle > 337.5 and wind_angle <= 360:
            wind_direction = "North"
        return wind_direction
    def pullAPI(city_name):
        api_key = "Enter API key here"
        base_url = "http://api.openweathermap.org/data/2.5/weather?"
        complete_url = base_url + "id=524901&" + "appid=" + api_key + "&q=" + city_name + "&units=imperial"
        response = requests.get(complete_url)
        currentJSON = response.json()
        if currentJSON["cod"] != "404":
            lat = currentJSON["coord"]["lat"]
            lon = currentJSON["coord"]["lon"]
            base_url_onecall = "https://api.openweathermap.org/data/2.5/onecall?"
            complete_url_onecall = base_url_onecall + "lat=" + str(lat) + "&lon=" + str(lon) + "&exclude=minutely,alerts,hourly" + "&units=imperial" + "&appid=" + api_key
            response = requests.get(complete_url_onecall) 
            onecallJSON = response.json()
            city = currentJSON["name"]
            onecallJSON.update({"city":city})
            return onecallJSON
        else: 
            return "Invalid city"
    day_count = 0
    print (get_time(),"User connected")
    try:
        async for message in websocket:
            command = message.split(";")[0]
            city_name = message.split(";")[1]
            units = message.split(";")[2]
            if command == "Current Forecast":
                print (get_time(),"Current Forecast called at",city_name,"with",units,"units")
                try:
                    # Grabs all desired data and assigns them to variables. If you want to add or take from the forecast, this is where you do it
                    current_temperature = onecallJSON["current"]["temp"]
                    current_humidiy = onecallJSON["current"]["humidity"] 
                    weather_description = onecallJSON["current"]["weather"][0]["description"] 
                    wind_speed = onecallJSON["current"]["wind_speed"]
                    wind_angle = onecallJSON["current"]["wind_deg"]
                    city = onecallJSON["city"]
                except:
                    await websocket.send("You didn't click \"Get Weather!\" first. Please click \"Get Weather!\"")
                    print (get_time(),"Get Weather wasn't pushed first! This won't work until then")
                    continue
                


                if(units == "Metric"):
                    current_temperature = convertTempToCelsius(current_temperature)
                    wind_speed = convertSpeedToKMPH(wind_speed)
                    wind_measurement = "km/h"
                    temp_measurement = "C"
                else:
                    wind_measurement = "mph"
                    temp_measurement = "F"

                wind_direction = getWindDir(wind_angle)

                await websocket.send(city + "'s Current Weather\nTemp: "+ str(round(current_temperature, 1)) + " °" + temp_measurement + "\nHumidity: " + str(current_humidiy) + "%\nWind speed: " + str(round(wind_speed, 1)) + wind_measurement + "\nWind direction: " + wind_direction + "\nDescription: " + weather_description)
            elif command == "7 Day Forecast":
                print (get_time(),"7 Day Forecast called at",city_name,"with",units,"units")

                day_count = 0

                try:
                    current_day = date.fromtimestamp(onecallJSON["current"]["dt"]).strftime("%A")
                    # The UNIX epoch time code is provided inside each day, so this code returns the day of the week you see ingame.
                except:
                    await websocket.send("You didn't click \"Get Weather!\" first. Please click \"Get Weather!\"")
                    print (get_time(),"Get Weather wasn't pushed first! This won't work until then")
                    continue

                temp = onecallJSON["daily"][0]["temp"]
                temp_day = temp["day"]
                temp_min = temp["min"]
                temp_max = temp["max"]

                temp_feels = onecallJSON["daily"][0]["feels_like"]["day"]
                humidity = onecallJSON["daily"][0]["humidity"]
                wind_speed = onecallJSON["daily"][0]["wind_speed"]
                wind_angle = onecallJSON["daily"][0]["wind_deg"]
                weather_description = onecallJSON["daily"][0]["weather"][0]["description"]
                city = onecallJSON["city"]

                if(units == "Metric"):
                    wind_speed = convertSpeedToKMPH(wind_speed)
                    temp_day = convertTempToCelsius(temp_day)
                    temp_max = convertTempToCelsius(temp_max)
                    temp_min = convertTempToCelsius(temp_min)
                    temp_feels = convertTempToCelsius(temp_feels)
                    wind_measurement = "km/h"
                    temp_measurement = "C"
                else:
                    wind_measurement = "mph"
                    temp_measurement = "F"

                wind_direction = getWindDir(wind_angle)

                await websocket.send(current_day + "\nCity: " + city + "\nDaily temp: " + str(round(temp_day,1)) + " °" + temp_measurement + "\nFeels like: " + str(round(temp_feels)) + " °" + temp_measurement + "\nMin: " + str(round(temp_min,1)) + " °" + temp_measurement + "\nMax: " + str(round(temp_max,1)) + " °" + temp_measurement + "\nHumidity: " + str(humidity) + "%\nWind speed: " + str(round(wind_speed,1)) + wind_measurement + "\nDirection: " + wind_direction + "\nCondition: " + weather_description + "\n")
            elif command == "Next Day":
                try:
                    if day_count == 7:
                        continue
                    else:
                        day_count += 1
                    dailyJSON = onecallJSON["daily"][day_count]
                    current_day_UNIX = dailyJSON["dt"]
                    current_day = date.fromtimestamp(current_day_UNIX).strftime("%A")
                except:
                    await websocket.send("You didn't click \"Get Weather!\" first. Please click \"Get Weather!\"")
                    print (get_time(),"Get Weather wasn't pushed first! This won't work until then")
                    day_count = 0
                    continue

                print (get_time(),"Next Day called at",city_name,"with",units,"units")

                temp = onecallJSON["daily"][day_count]["temp"]
                temp_day = temp["day"]
                temp_min = temp["min"]
                temp_max = temp["max"]

                temp_feels = onecallJSON["daily"][day_count]["feels_like"]["day"]
                humidity = onecallJSON["daily"][day_count]["humidity"]
                wind_speed = onecallJSON["daily"][day_count]["wind_speed"]
                wind_angle = onecallJSON["daily"][day_count]["wind_deg"]
                weather_description = onecallJSON["daily"][day_count]["weather"][0]["description"]
                city = onecallJSON["city"]

                if(units == "Metric"):
                    wind_speed = convertSpeedToKMPH(wind_speed)
                    temp_day = convertTempToCelsius(temp_day)
                    temp_max = convertTempToCelsius(temp_max)
                    temp_min = convertTempToCelsius(temp_min)
                    temp_feels = convertTempToCelsius(temp_feels)
                    wind_measurement = "km/h"
                    temp_measurement = "C"
                else:
                    wind_measurement = "mph"
                    temp_measurement = "F"

                wind_direction = getWindDir(wind_angle)
                await websocket.send(current_day + "\nCity: " + city + "\nDaily temp: " + str(round(temp_day,1)) + " °" + temp_measurement + "\nFeels like: " + str(round(temp_feels)) + " °" + temp_measurement + "\nMin: " + str(round(temp_min,1)) + " °" + temp_measurement + "\nMax: " + str(round(temp_max,1)) + " °" + temp_measurement + "\nHumidity: " + str(humidity) + "%\nWind speed: " + str(round(wind_speed,1)) + wind_measurement + "\nDirection: " + wind_direction + "\nCondition: " + weather_description + "\n")
            elif command == "Previous Day":
                try:
                    if day_count == 0:
                        continue
                    else:
                        day_count -= 1
                    dailyJSON = onecallJSON["daily"][day_count]
                    current_day_UNIX = dailyJSON["dt"]
                    current_day = date.fromtimestamp(current_day_UNIX).strftime("%A")
                except:
                    await websocket.send("You didn't click \"Get Weather!\" first. Please click \"Get Weather!\"")
                    print (get_time(),"Get Weather wasn't pushed first! This won't work until then")
                    day_count = 0
                    continue
                
                print (get_time(),"Next Day called at",city_name,"with",units,"units")

                temp = onecallJSON["daily"][day_count]["temp"]
                temp_day = temp["day"]
                temp_min = temp["min"]
                temp_max = temp["max"]

                temp_feels = onecallJSON["daily"][day_count]["feels_like"]["day"]
                humidity = onecallJSON["daily"][day_count]["humidity"]
                wind_speed = onecallJSON["daily"][day_count]["wind_speed"]
                wind_angle = onecallJSON["daily"][day_count]["wind_deg"]
                weather_description = onecallJSON["daily"][day_count]["weather"][0]["description"]
                city = onecallJSON["city"]

                if(units == "Metric"):
                    wind_speed = convertSpeedToKMPH(wind_speed)
                    temp_day = convertTempToCelsius(temp_day)
                    temp_max = convertTempToCelsius(temp_max)
                    temp_min = convertTempToCelsius(temp_min)
                    temp_feels = convertTempToCelsius(temp_feels)
                    wind_measurement = "km/h"
                    temp_measurement = "C"
                else:
                    wind_measurement = "mph"
                    temp_measurement = "F"

                wind_direction = getWindDir(wind_angle)

                await websocket.send(current_day + "\nCity: " + city + "\nDaily temp: " + str(round(temp_day,1)) + " °" + temp_measurement + "\nFeels like: " + str(round(temp_feels)) + " °" + temp_measurement + "\nMin: " + str(round(temp_min,1)) + " °" + temp_measurement + "\nMax: " + str(round(temp_max,1)) + " °" + temp_measurement + "\nHumidity: " + str(humidity) + "%\nWind speed: " + str(round(wind_speed,1)) + wind_measurement + "\nDirection: " + wind_direction + "\nCondition: " + weather_description + "\n")
                
            elif command == "Pull API":
                print (get_time(),"Pulling weather information at \"" + city_name + "\" from API...")

                result = pullAPI(city_name)
                if (result != "Invalid city"):
                    print(get_time(),"Success!")
                    onecallJSON = result
                    await websocket.send("Loading accurate weather data...")
                    for i in range(random.randint(3,7)):
                        time.sleep(1)
                else: 
                    await websocket.send("Invalid city.\nPlease enter a city name in the style City,State/Province (optional),Country. Ex: Sacramento,California,United States / Sacramento,ca,us")
                    print(get_time(),"Failure, invalid city")
                    onecallJSON = {}
    except websockets.exceptions.ConnectionClosedError: 
        print(get_time(),"User disconnected")

asyncio.get_event_loop().run_until_complete(
    websockets.serve(echo, 'localhost', 8765))
asyncio.get_event_loop().run_forever()