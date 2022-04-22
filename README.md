# Rently
## Overview of Rently:
This is a full stack web application which uses the inputted location and returns available items users could rent/checkout and users can also loan their own item for other people to rent out.

<h2> SWE Final Project </h2>

<h3> Team Members </h3>
- Abdullah Shehata   <br>
- Chihumeya Eresia-Eke   <br>
- Chaudhary Danial   <br>
- Shams Sikder  <br>

<br>

Sprint 2 Heroku URL: https://rently2-mads.herokuapp.com/

<br>

Sprint 1 Heroku URL: https://rently-mads.herokuapp.com/login?next=%2F


## Framework Used: <a href="https://flask.palletsprojects.com/en/2.0.x/"> Flask </a>
## APIs Used: <a href = "https://openweathermap.org/api"> Open Weater API </a>

## Requirements (Packages Needed): 
1. `pip3 install flask` 
2. `pip install python-dotenv`
3. `pip install requests`
4. `pip3 install pylint`
5. `pip3 install psycopg2-binary`
6. `pip3 install Flask-SQLAlchemy`

## To run this project locally
1. Clone this repository 
2. Create an account on Open Weather API : https://openweathermap.org/api
3. Register for an API Key
4. Create a `.env` file in the same directory as your project and store the API key such as WeatherAPI_KEY = "Your Key"
5. Create a heroku account fom "https://id.heroku.com/login"
6. Go through the following commands to create an app for the database: 
-    `heroku login -i` : connect your heroku account to your local computer  
-    `heroku create` : creates a heroku app 
-    `heroku addons:create heroku-postgresql:hobby-dev -a {your-app-name}` : adds a new database to your heroku app 
7. Then run `heroku config`, copy the value then add the `DATABASE_URL` to your `.env` file  such as DATABASE_URL = ""
8. If the url starts with postgres: change it to postgresql: in your `.env` file
9. Add a <b>SECRET_KEY</b> to your `.env` file such as SECRET_KEY = "{write-in-your-secret-key}"

## Not Necessay to run the code but useful 
1. Create a `.gitignore` file and store files such as `.env` which we don't want to be pushed to github 

## Run `python3 app.py` to run the application 
