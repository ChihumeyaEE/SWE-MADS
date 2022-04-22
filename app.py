import requests
from flask import request
import flask
import os

app = flask.Flask(__name__)
from dotenv import load_dotenv, find_dotenv
load_dotenv(find_dotenv())


api_key = os.getenv("api_key")
@app.route('/')
def index():

    return flask.render_template('weather.html')

@app.route('/weather', methods=['POST'])
def temp():
    
    zipcode = request.form['zip']
    url = requests.get('http://api.openweathermap.org/data/2.5/weather?zip='+zipcode+',us&appid='+api_key)
    

    weather = url.json() 

    #Down below is temperature in kelin.
    temperatureKelvin = float(weather['main']['temp'])
    humid = float(weather['main']['humidity'])
    condition = str(weather['weather'][0]['description'])
    icon = str(weather['weather'][0]['icon'])
    cityname = str(weather['name'])
    

    #Formula to change temeprature from kelvin to fahrenheit
    temperaturefahrenheit = round(temperatureKelvin - 273.15) * 1.8 + 32
  
    return flask.render_template('weather.html', temp=temperaturefahrenheit , humidity=humid, cond=condition, city = cityname, icon = icon)
   
    
    

app.run(
    host=os.getenv("IP", "0.0.0.0"),
    port=int(os.getenv("PORT", 8080)),
    debug=True,
)