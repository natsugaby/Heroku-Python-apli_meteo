from distutils.util import execute
import json

with open ('apli_meteo/datameteotmp.json') as jsonFile:
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
