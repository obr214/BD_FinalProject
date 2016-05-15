
from __future__ import print_function

import sys
from datetime import datetime
from pytz import timezone
from pyspark import SparkContext


if __name__ == "__main__":

    # Create SparkContext
    sc = SparkContext(appName="MergeCitiBikeWeather")

    def format_string_to_date(string_date):
        stripped_date = string_date.split(' ')
        date_section = stripped_date[0].split('/')
        month = date_section[0].zfill(2)
        day = date_section[1].zfill(2)
        year = date_section[2]
        time = stripped_date[1].split(':')
        hour = time[0].zfill(2)
        minutes = time[1].zfill(2)
        string_date = month + ' ' + day + ' ' + year + ' ' + hour + ':' + minutes
        date_obj = datetime.strptime(string_date, '%m %d %Y %H:%M')
        return date_obj


    def transform_dates(x_list):
        x_list[3] = format_string_to_date(x_list[3])
        x_list[4] = format_string_to_date(x_list[4])
        return x_list


    def format_date_to_gtm(date_obj):
        try:
            eastern_tz = timezone('US/Eastern')
            gmt = timezone('GMT')
            date_obj = eastern_tz.localize(date_obj)
            date_gmt = date_obj.astimezone(gmt)
            date_str = date_gmt.strftime('%Y-%m-%d %H:%M:00')
            return date_str
        except IndexError:
            return ''


    def add_gmt_time_columns(x_list):
        x_list.append(format_date_to_gtm(x_list[3]))
        x_list.append(format_date_to_gtm(x_list[4]))
        return x_list


    def datetime_to_str(x_list):
        x_list[3] = x_list[3].strftime('%Y-%m-%d %H:%M:00')
        x_list[4] = x_list[4].strftime('%Y-%m-%d %H:%M:00')
        return x_list


    def lists_to_string(x_1, x_2):
        first = ''
        second = ''
        if x_1:
            first = ','.join(x_1).encode('utf 8')
        if x_2:
            second = ','.join(x_2).encode('utf 8')
        return first + ',' + second

    # citibike = sc.textFile('cityBike.csv')
    citibike = sc.textFile(sys.argv[1], 1)

    header = citibike.first()
    citibike = citibike.filter(lambda x: x != header)
    citibike_splitted = citibike.map(lambda x: x.strip().split(','))
    citibike_test = citibike_splitted.map(lambda x: map(lambda x: x[1:-1], x))
    citibike_dates = citibike_test.map(lambda x: transform_dates(x))
    citibike_gmt_dates = citibike_dates.map(lambda x: add_gmt_time_columns(x))
    citibike_gmt_dates = citibike_gmt_dates.map(lambda x: datetime_to_str(x))

    citibike_key = citibike_gmt_dates.map(lambda x: (x[-2], x))

    # weather = sc.textFile('weather_ready_join')
    weather = sc.textFile(sys.argv[2], 1)
    w_header = weather.first()
    weather = weather.filter(lambda x: x != w_header)
    weather = weather.map(lambda x: x.strip().split(','))
    weather_key = weather.map(lambda x: (x[0].encode('utf 8'), x))

    citybike_weather = citibike_key.leftOuterJoin(weather_key)
    citybike_weather_clean = citybike_weather.filter(lambda x: x[1][1] != None)
    weather_final = citybike_weather_clean.map(lambda x: lists_to_string(x[1][0], x[1][1]))
    weather_final.coalesce(1).saveAsTextFile('citibike_weather')

    sc.stop()
