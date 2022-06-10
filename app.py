
from crypt import methods
from lib2to3.pgen2 import driver
import re
from distutils.util import execute
import json
from unittest import removeResult
from flask import Flask, request, render_template 
import psycopg2
import os, requests
import imp
app = Flask(__name__)
@app.route('/')
def my_form():
    return render_template('index.html')

@app.route('/', methods=['POST', 'GET'])
def home():
    import json
    text = request.form['text']
    processed_text = text.upper()
    r_weather = requests.get('https://api.openweathermap.org/data/2.5/weather?q='+ processed_text + '&appid=beb97c1ce62559bba4e81e28de8be095')
    data = r_weather.json()
    processed_data = json.dumps(data)
    with open("datameteotmp.json", "w") as f:
        f.write(str(processed_data))
    return render_template('index.html',Location = "Location  ", Locationdata = str(data['name'])+'  ', country_code = "country_code  ", country_codedata = str(data['sys']['country'])+'  ', coordinate = "coordinates  ", coordinatedata = str(data['coord']['lon']) + ' ' + str(data['coord']['lat'])+'  ', temp = "temperature  ", tempdata = str(round(data['main']['temp']-273.15)) + '°C'+'  ', pressure = "pressure  ", pressuredata = str(data['main']['pressure'])+' hPa', humidity = "humidity  ", humiditydata = str(data['main']['humidity'])+'% ', Sky = "Sky  ", Skydata = str(data['weather'][0]['description'])+'  ', Wind = "Wind  ", Winddata = str(data['wind']['speed'])+' m/s')
if __name__ == "__main__":
    app.run(port = 8000,debug=True)


@app.route('/about/')
def about():
    return render_template('about.html')
    
@app.route('/comments/')
def comments():
    comments = ['This is the first comment.',
                'This is the second comment.',
                'This is the third comment.',
                'This is the fourth comment.'
                ]

    return render_template('comments.html', comments=comments)
@app.route('/save/', methods = ['POST', 'GET'])
def save():
    if request.method == 'POST':
        if request.form.get('save_buton1') == 'Save':
            with open ('/home/gabriel/Documents/python-exo/apli_meteo/datameteotmp.json') as jsonFile:
                data = json.load(jsonFile)

            locationdata = str(data['name'])
            country_codedata = str(data['sys']['country'])
            coordinatedata = str(data['coord']['lon']) + ' ' + str(data['coord']['lat'])
            tempdata = str(round(data['main']['temp']-273.15)) + '°C'
            pressuredata = str(data['main']['pressure'])+' hPa'
            humiditydata = str(data['main']['humidity'])+'% '
            Skydata = str(data['weather'][0]['description'])
            Winddata = str(data['wind']['speed'])+' m/s'

            import psycopg2
            conn = psycopg2.connect(
            database="ma_base",
            user='gabriel', 
            password='Kqa1btd?',
            host='localhost',
            port='5432'
            )
            savecursor = conn.cursor()
            savecursor.execute('INSERT INTO save (location, country_code, coordinates, temperature, pressure, humidity, sky, wind) VALUES (%s, %s, %s, %s, %s, %s, %s ,%s)', (locationdata, country_codedata, coordinatedata, tempdata, pressuredata, humiditydata, Skydata, Winddata))

            conn.commit()
            conn.close()

        else:
            pass # unknown
    elif request.method == 'GET':
        return render_template('save.html', save='bruh')
    return render_template('index.html', message = 'saved!')