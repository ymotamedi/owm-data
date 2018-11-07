import pyowm
import pandas as pd
import os
from datetime import datetime, time, date
from apscheduler.schedulers.blocking import BlockingScheduler


# if a data file has not been created, make one

if not os.path.isfile('weather.csv'):

    # create empty data frame to fill and save it
    weather_df = pd.DataFrame(columns=['date', 'time', 'location', 'humidity', 'cloud_cover', 'rain',
        'pressure', 'tempC'])

    weather_df.to_csv('weather.csv', index=False)



def is_time_between(begin_time, end_time):

    """
    Function to check whether current time falls withing a certain
    boundary.

    """

    # If check time is not given, default to current UTC time
    check_time = datetime.now().time()

    if begin_time < end_time:

        return check_time >= begin_time and check_time <= end_time

    else: # crosses midnight
        return check_time >= begin_time or check_time <= end_time



def get_weather(loc):


    currentDate = date.today().strftime('%d-%m-%y')
    currentTime = datetime.now().time().strftime('%H:%M:%S')

    # open csv file
    weather_df = pd.read_csv('weather.csv')

    # input API key
    owm = pyowm.OWM('ced36762b224bdb49060ba275e76d3fc')

    # get weather at loc
    observation = owm.weather_at_place(loc)
    w = observation.get_weather()

    # get weather variables
    humidity = w.get_humidity()
    cloud_cover = w.get_clouds()
    rain = int(w.get_rain()!={})
    pressure = w.get_pressure()['press']
    temp = w.get_temperature('celsius')['temp']

    weather_dict = {'humidity': humidity,
    'cloud_cover': cloud_cover,
    'rain':rain,
    'pressure': pressure,
    'tempC': temp,
    'date': currentDate,
    'time': currentTime,
    'location': loc}

    weather_df = weather_df.append(weather_dict, ignore_index=True)

    weather_df.to_csv('weather.csv', index=False)


def get_weather_commuter(locWork, locHome):

    """
    Function to get weather data from Open Weather Map for a commuter.

    """

    loc = ''

    day = datetime.today().weekday()


    if day < 4 and is_time_between(time(8,0), time(18,0)):

        loc = locWork

    else:

        loc = locHome

    get_weather(loc)




#### run

sched = BlockingScheduler()
sched.add_job(get_weather_commuter, 'interval', ['London,GB', 'Cambridge,GB'], hours=3,
    start_date = '2018-10-30 12:10:00', id='my_job')
sched.start()
