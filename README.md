# WeatherSocket
The source code for the WeatherSocket system I've created for NeosVR

Hello and welcome to the server side of WeatherSocket. The code I have provided is perfect for running your own instance of WeatherSocket in your own world without having to rely on external servers or API limitations. Before I tell you how to work it, let me get the boring license out of the way:

These scripts and the materials inside the "WeatherSocket" public folder by user "Kodufan" (hereby called "materials") are subject to the CC BY-NC 4.0 license, meaning you are free to take, modify, build upon, or remix either the source code or materials as long as credit is provided and that the use is non commercial. 

Here's how to get it working...

## Step 0: Installing Python

This tool runs entirely on Python. If you don't have it, head over to https://www.python.org/ and grab yourself the latest stable copy.

## Step 1: Getting your own API key

API keys are a tool used by the developers of Application Program Interfaces to control or monitor who uses their API, how often, for what purposes, etc. This also allows APIs to be monetizable quite easily. The API I am using is "OpenWeatherMap". They have a free API plan that requires no payment information. Head over to https://openweathermap.org/price, click "Get API key" under the free category, create an account, and paste the key inside the quotes of the "api_key" variables inside the code. This API key is super secret and only for you, so don't share it! The free plan has restrictions, but they should never be a problem for individual use. There are two types of API calls this code takes advantage of, current calls and "onecall" calls. WeatherSocket App and WeatherSocket Combine use one of each API call for every time "Pull API" is called, aka each time "Get Weather" is pressed on the GUI in Neos. 

Current calls have two stipulations: 
- No more than 60 calls every minute
- No more than 1 million calls per month

One Call calls have one stipulation:
- No more than 1,000 calls per day

I've done the math, and to max out the million calls per month limit, you must make a call roughly every 2.6 seconds 24/7 for a 31 day month. For One Call, you must make a call every 1.44 minutes. If you exceed the API call limit, you will be contacted by OpenWeatherMap requesting payment. If this happens, consider adding some wait periods to using the GUI with pulse delays. If you know for sure you didn't make that many calls, change your API key as someone else may have guessed or stolen it. 

## Step 2: Choosing which program to use

Now this is simple, use WeatherSocket Live (with your API key!) if you wish to only use the world integration feature of Weathersocket. Use WeatherSocket App if you wish to host the GUI version of WeatherSocket. Use WeatherSocket Combine if you wish to use both!

## Step 3: Networking

Haha, just kidding. Sorry if that worried you. WeatherSocket GUI and the world integration make all Websocket requests through the specified user (which you should assign to yourself), so you don't have to do any networking! In fact, you don't even run these servers publically, so there's no risk of anyone hacking you unless they hack Neos first. You can host these publically, however by default, It Just Works™.

You now have the server side of WeatherSocket setup to your liking. You'll notice that when you run it, a window will pop up. This is your diagnostic terminal. This shows you every time your server is contacted and some other information. You can use this to see what your websocket is doing. You can also see what users have entered into the WeatherSocket app if you're using it (My favorite is "Batman", which apparently is a real city).

## Step 4: Setting it up in Neos

All you need to do to get your instance working is click "Show logix" on either the world integration demo or the weather app (or both). Enter your username where it says "You!". For the app, you will have to click "Connect to WeatherSocket" to get it working, but after that, you're golden! You can disable the "Show Logix" button and then save a copy for yourself. For the demo, simply plug in your name, city, and how often you want it to check into the appropriate inputs that're neatly organized above the outputs. You are also able to change how often it checks for new weather information. I wouldn't recommend setting it lower than 3 seconds if you plan to run it 24/7.

You're done! There are some extra things you can do now, however everything is already set up for most use cases.

## Bonus:
WeatherSocket has some more customization, too! By changing the ip waaaaaay at the bottom of each script from "localhost" to your interal IP and port forwarding the port lets you allow anyone to use your API key to make requests from their own world. This is similar to how my MMC version can be used by anyone, not just myself. However, if you let someone else use your API key, they must change the username from yours to theirs for it to work. This (should) also work on things like avatars, too! Remember: The pulse to "Websocket message sender" must also be yours, and I've taken care of that for the public folder version. Keep that in mind if you customize it. This isn't all you can change, though... All the information sent to the app or world integration is customizable. If you want to see all the information it returns, have it print onecallJSON (if using the App script) to the diagnostic panel and use a JSON viewer to make sense of it. You can add or remove things to your liking. If you add more to the world integration than my Logix string parser can handle, simply copy the pattern the parser follows until you have enough outputs. Woo to modularity!

If you have any questions, or your diagnostic panel gets mad and throws out a long scary traceback, send me a message on Discord at Kodufan#7558 and I'll do my best to fix it. (If you modify the source code or Logix, please explain what you've done)


This is my first public coding project, and as such, there are likely many optimizations I could make. I am aware of this. 
This is also my first public use of GitHub, so I am not familiar with traditional standards. I am aware of this.
