import os
from dotenv import find_dotenv, load_dotenv
from flask import Flask, render_template

app = Flask(__name__)

load_dotenv(find_dotenv())

@app.route('/')
def homepage():
    return render_template('index.html')

app.run(
    host = os.getenv("IP", "0.0.0.0"),
    port = int(os.getenv("PORT", 8080)),
    debug = True)