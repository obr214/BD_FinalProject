import pandas as pd
import matplotlib.pyplot as plt; plt.rcdefaults()
import numpy as np
import matplotlib.pyplot as plt
import weather_cleaner as wc
import plotly.graph_objs as go
from plotly.tools import FigureFactory as FF
import plotly as py
import pylab as pylt
import os
from scipy import stats
from datetime import datetime



py.offline.init_notebook_mode()

def round_hour(x,tt=''):
    if tt=='M':
        return pd.to_datetime(((x.astype('i8')/(1e9*60)).round()*1e9*60).astype(np.int64))
    elif tt=='H':
        return pd.to_datetime(((x.astype('i8')/(1e9*60*60)).round()*1e9*60*60).astype(np.int64))
    else:
        return pd.to_datetime(((x.astype('i8')/(1e9)).round()*1e9).astype(np.int64))

def folder_reader(path):
    names_files = os.listdir(path)
    names_files
    merged_df = 0
    for file_name in names_files:
        if file_name!= '_SUCCESS' and file_name!='.DS_Store':
            path_file = path + '/' + file_name
            data= pd.read_csv(path_file,  delimiter='\t', header=None)
            if isinstance(merged_df, pd.DataFrame):
                merged_df = pd.concat([merged_df, data], axis=0)
            else:
                merged_df = data

    return merged_df


def folder_reader_csv(path):
    names_files = os.listdir(path)
    names_files
    merged_df = 0
    for file_name in names_files:
        if file_name!= '_SUCCESS' and file_name!='.DS_Store':
            path_file = path + '/' + file_name
            data= pd.read_csv(path_file,  delimiter=',', header=None)
            if isinstance(merged_df, pd.DataFrame):
                merged_df = pd.concat([merged_df, data], axis=0)
            else:
                merged_df = data

    return merged_df



weather = wc.weather_minute()

minutes_no = weather[weather.precip_shift_no == 1].precip_shift_no.count()
minutes_low = weather[weather.precip_shift_low == 1].precip_shift_low.count()
minutes_high = weather[weather.precip_shift_high == 1].precip_shift_high.count()

minutes_no_mor = weather[(weather.datetime.dt.weekday < 5) & (weather.datetime.dt.hour < 10) & (
weather.datetime.dt.hour > 7)].precip_shift_no.count()
minutes_low_mor = weather[(weather.datetime.dt.weekday < 5) & (weather.datetime.dt.hour < 10) & (
weather.datetime.dt.hour > 7)].precip_shift_low.count()
minutes_high_mor = weather[(weather.datetime.dt.weekday < 5) & (weather.datetime.dt.hour < 10) & (
weather.datetime.dt.hour > 7)].precip_shift_high.count()

minutes_no_aft = weather[(weather.datetime.dt.weekday < 5) & (weather.datetime.dt.hour < 20) & (
weather.datetime.dt.hour > 17)].precip_shift_no.count()
minutes_low_aft = weather[(weather.datetime.dt.weekday < 5) & (weather.datetime.dt.hour < 20) & (
weather.datetime.dt.hour > 17)].precip_shift_low.count()
minutes_high_aft = weather[(weather.datetime.dt.weekday < 5) & (weather.datetime.dt.hour < 20) & (
weather.datetime.dt.hour > 17)].precip_shift_high.count()


def vectors_creator():
    weather_c = weather.copy(deep=True)

    weather_c.temperature = weather_c.temperature.astype(int)
    a = weather_c.groupby('temperature').count().reset_index().datetime

    np.save('count_temperature', a)

    weather_c.wind_speed = weather_c.wind_speed.astype(int)
    b = weather_c.groupby('wind_speed').count().reset_index().datetime

    np.save('count_wind', b)



def rain_gender(path, graph='rain_gender'):
    rain_gender = folder_reader(path)
    rain_gender.columns = ['key', 'value']

    high_f = int(rain_gender[rain_gender.key == "highf"].value)
    high_m = int(rain_gender[rain_gender.key == "highm"].value)
    high_o = int(rain_gender[rain_gender.key == "higho"].value)
    low_f = int(rain_gender[rain_gender.key == "lowf"].value)
    low_m = int(rain_gender[rain_gender.key == "lowm"].value)
    low_o = int(rain_gender[rain_gender.key == "lowo"].value)
    no_f = int(rain_gender[rain_gender.key == "nof"].value)
    no_m = int(rain_gender[rain_gender.key == "nom"].value)
    no_o = int(rain_gender[rain_gender.key == "noo"].value)



    if graph=='rain_gender_complete':
        fig = {
            "data": [
                {
                    "values": [high_f + high_m + high_o, low_f + low_m + low_o, no_f + no_m + no_o],
                    "labels": [
                        'high rain', 'low rain', 'no rain'
                    ],
                    "domain": {"x": [0, .48]},
                    "name": "Total Trips by weather",
                    "hoverinfo": "label+percent+name",
                    "hole": .4,
                    "type": "pie"
                },
                {
                    "values": [(high_f + high_m + high_o) / minutes_high, (low_f + low_m + low_o) / minutes_low,
                               (no_f + no_m + no_o) / minutes_no],
                    "labels": [
                        'high rain', 'low rain', 'no rain'
                    ],
                    "text": "CO2",
                    "textposition": "inside",
                    "domain": {"x": [.52, 1]},
                    "name": "Trips per minute by weather",
                    "hoverinfo": "label+percent+name",
                    "hole": .4,
                    "type": "pie"
                },
            ],
            "layout": {
                "title": "City Bike trips by raining condition",
                "annotations": [
                    {
                        "font": {
                            "size": 20
                        },
                        "showarrow": False,
                        "text": "Total",
                        "x": 0.20,
                        "y": 0.5
                    },
                    {
                        "font": {
                            "size": 20
                        },
                        "showarrow": False,
                        "text": "Normalized",
                        "x": 0.83,
                        "y": 0.5
                    }
                ]
            }
        }

        url = py.offline.iplot(fig)

    if graph=='rain_gender':

        labels = 'high rain', 'low rain', 'no rain'
        sizes = [high_f + high_m + high_o, low_f + low_m + low_o, no_f + no_m + no_o]
        colors = ['gold', 'yellowgreen', 'lightcoral']
        explode = (0.2, 0.1, 0)  # explode 1st slice

        # Plot
        plt.pie(sizes, explode=explode, labels=labels, colors=colors,
                autopct='%1.1f%%', shadow=True, startangle=140)

        plt.axis('equal')
        plt.show()



    if graph=='rain_gender_norm':
        labels = 'high rain', 'low rain', 'no rain'
        sizes = [(high_f + high_m + high_o) / minutes_high, (low_f + low_m + low_o) / minutes_low,
                 (no_f + no_m + no_o) / minutes_no]
        colors = ['gold', 'yellowgreen', 'lightcoral']
        explode = (0.2, 0.1, 0)  # explode 1st slice

        # Plot
        plt.pie(sizes, explode=explode, labels=labels, colors=colors,
                autopct='%1.1f%%', shadow=True, startangle=140)

        plt.axis('equal')

        plt.show()

    if graph == 'rain_gender_bars':

        objects = ('high rain', 'low rain', 'no rain')
        y_pos = np.arange(len(objects))
        performance = [(high_f + high_m + high_o) / minutes_high, (low_f + low_m + low_o) / minutes_low,
                       (no_f + no_m + no_o) / minutes_no]

        plt.bar(y_pos, performance, align='center', alpha=0.5)
        plt.xticks(y_pos, objects)
        plt.ylabel('Number of trips')
        plt.title('Amount of trips per minute')

        plt.show()

    if graph == 'rain_gender_bars_hor':

        data = [
            go.Bar(
                x=[(high_f + high_m + high_o) / minutes_high, (low_f + low_m + low_o) / minutes_low,
                   (no_f + no_m + no_o) / minutes_no],
                y=['high rain', 'low rain', 'no rain'],
                orientation='h',
            )
        ]
        plot_url = py.offline.iplot(data)

    if graph == 'gender_rain_complete':
        fig = {
            "data": [
                {
                    "values": [no_f, no_m],
                    "labels": [
                        'female', 'male'
                    ],
                    "domain": {"x": [0, .48]},
                    "name": "Total Trips by weather",
                    "hoverinfo": "label+percent+name",
                    "hole": .4,
                    "type": "pie"
                },
                {
                    "values": [low_f + high_f, low_m + high_m],
                    "labels": [
                        'female', 'male'
                    ],
                    "text": "CO2",
                    "textposition": "inside",
                    "domain": {"x": [.52, 1]},
                    "name": "Trips per minute by weather",
                    "hoverinfo": "label+percent+name",
                    "hole": .4,
                    "type": "pie"
                },
            ],
            "layout": {
                "title": "Gender trip proportion by raining condition",
                "annotations": [
                    {
                        "font": {
                            "size": 20
                        },
                        "showarrow": False,
                        "text": "No Rain",
                        "x": 0.20,
                        "y": 0.5
                    },
                    {
                        "font": {
                            "size": 20
                        },
                        "showarrow": False,
                        "text": "Rain",
                        "x": 0.79,
                        "y": 0.5
                    }
                ]
            }
        }

        url = py.offline.iplot(fig)


    if graph=='gender_rain_no':
        labels = 'female trips with no rain', 'male trips with no rain'
        sizes = [no_f, no_m]
        colors = ['red', 'blue']
        explode = (0.2, 0.1)  # explode 1st slice

        # Plot
        plt.pie(sizes, explode=explode, labels=labels, colors=colors,
                autopct='%1.1f%%', shadow=True, startangle=140)

        plt.axis('equal')
        plt.show()

    if graph=='gender_rain_yes':
        labels = 'female trips with rain', 'male trips with rain'
        sizes = [low_f + high_f, low_m + high_m]
        colors = ['red', 'blue']
        explode = (0.2, 0.1)  # explode 1st slice

        # Plot
        plt.pie(sizes, explode=explode, labels=labels, colors=colors,
                autopct='%1.1f%%', shadow=True, startangle=140)

        plt.axis('equal')
        plt.show()


def trips_customer(path, rain='no'):
    trips_customer = folder_reader(path)
    trips_customer.columns = ['key', 'value']

    if rain == 'no':
        labels = 'Customers no rain', 'Suscribers no rain'
        sizes = [int(trips_customer[trips_customer.key == 'cusno'].value),
                 int(trips_customer[trips_customer.key == 'susno'].value)]
        colors = ['lightyellow', 'orange']
        explode = (0.2, 0.1)  # explode 1st slice

        # Plot
        plt.pie(sizes, explode=explode, labels=labels, colors=colors,
                autopct='%1.1f%%', shadow=True, startangle=140)

        plt.axis('equal')
        plt.show()

    if rain == 'yes':
        labels = 'Customers no rain', 'Suscribers no rain'
        sizes = [int(trips_customer[trips_customer.key == 'cuslow'].value) + int(
            trips_customer[trips_customer.key == 'cushigh'].value),
                 int(trips_customer[trips_customer.key == 'suslow'].value) + int(
                     trips_customer[trips_customer.key == 'sushigh'].value)]
        colors = ['lightyellow', 'orange']
        explode = (0.2, 0.1)  # explode 1st slice

        # Plot
        plt.pie(sizes, explode=explode, labels=labels, colors=colors,
                autopct='%1.1f%%', shadow=True, startangle=140)

        plt.axis('equal')
        plt.show()

    if rain=='complete':
        fig = {
            "data": [
                {
                    "values": [int(trips_customer[trips_customer.key == 'cusno'].value),
                               int(trips_customer[trips_customer.key == 'susno'].value)],
                    "labels": [
                        'Customers', 'Suscribers'
                    ],
                    "domain": {"x": [0, .48]},
                     'marker': {'colors': ['rgb(177, 127, 38)',
                                  'rgb(205, 152, 36)']},
                    "name": "Customer type proportion by weather condition",
                    "hoverinfo": "label+percent+name",
                    "hole": .4,
                    "type": "pie"
                },
                {
                    "values": [int(trips_customer[trips_customer.key == 'cuslow'].value) + int(
                        trips_customer[trips_customer.key == 'cushigh'].value),
                               int(trips_customer[trips_customer.key == 'suslow'].value) + int(
                                   trips_customer[trips_customer.key == 'sushigh'].value)],
                    "labels": [
                        'Customers', 'Suscribers'
                    ],
                    "text": "CO2",
                    "textposition": "inside",
                    "domain": {"x": [.52, 1]},
                    'marker': {'colors': ['rgb(177, 127, 38)',
                                  'rgb(205, 152, 36)']},
                    "name": "Customer type proportion by weather condition",
                    "hoverinfo": "label+percent+name",
                    "hole": .4,
                    "type": "pie"
                },
            ],
            "layout": {
                "title": "Customer type proportion by weather condition",
                "annotations": [
                    {
                        "font": {
                            "size": 20
                        },
                        "showarrow": False,
                        "text": "No Rain",
                        "x": 0.20,
                        "y": 0.5
                    },
                    {
                        "font": {
                            "size": 20
                        },
                        "showarrow": False,
                        "text": "Rain",
                        "x": 0.79,
                        "y": 0.5
                    }
                ]
            }
        }

        url = py.offline.iplot(fig)


def avg_trip(path):
    avg_trip = folder_reader(path)
    avg_trip.columns = ['key', 'value']

    objects = ('high rain', 'low rain', 'no rain')
    y_pos = np.arange(len(objects))
    performance = [int(avg_trip[avg_trip.key == 'high'].value), int(avg_trip[avg_trip.key == 'low'].value),
                   int(avg_trip[avg_trip.key == 'no'].value)]

    plt.bar(y_pos, performance, align='center', alpha=0.5)
    plt.xticks(y_pos, objects)
    plt.ylabel('Time')
    plt.title('Average time of a trip')

    plt.show()

def avg_dist(path):
    avg_dist = folder_reader(path)
    avg_dist.columns = ['key', 'value']
    objects = ('high rain', 'low rain', 'no rain')
    y_pos = np.arange(len(objects))
    performance = [int(avg_dist[avg_dist.key == 'high'].value * 10000),
                   int(avg_dist[avg_dist.key == 'low'].value * 10000),
                   int(avg_dist[avg_dist.key == 'no'].value * 10000)]

    plt.bar(y_pos, performance, align='center', alpha=0.5)
    plt.xticks(y_pos, objects)
    plt.ylabel('Distance Proxy')
    plt.title('Average distance of a trip')

    plt.show()



def dist_vs_trip(path1, path2):
    avg_trip = folder_reader(path1)
    avg_trip.columns = ['key', 'value']
    avg_dist = folder_reader(path2)
    avg_dist.columns = ['key', 'value']

    trace1 = go.Bar(
        x=['high rain', 'low rain', 'no rain'],
        y=[int(avg_trip[avg_trip.key == 'high'].value), int(avg_trip[avg_trip.key == 'low'].value),
           int(avg_trip[avg_trip.key == 'no'].value)],
        marker=dict(
            color=['rgba(145,191,219, 0.8)', 'rgba(145,191,219, 0.6)', 'rgba(145,191,219, 0.4)']),
        name='Travel Time',
    )
    trace2 = go.Scatter(
        x=['high rain', 'low rain', 'no rain'],
        y=[int(avg_dist[avg_dist.key == 'high'].value * 100000), int(avg_dist[avg_dist.key == 'low'].value * 100000),
           int(avg_dist[avg_dist.key == 'no'].value * 100000)],
        name='Travel Distance',
        yaxis='y2'
    )
    data = [trace1, trace2]
    layout = go.Layout(
        legend=dict(
            x=0.1,
            y=1.1
        ),
        title='Average Travel distance vs. Time',
        yaxis=dict(
            domain=[0, 1000],
            title='Average travel time in seconds'
        ),
        yaxis2=dict(
            title='Average L2 travel Distance',
            range=[0, 2000],
            titlefont=dict(
                color='rgb(148, 103, 189)'
            ),
            tickfont=dict(
                color='rgb(148, 103, 189)'
            ),
            overlaying='y',
            side='right'

        )
    )
    fig = go.Figure(data=data, layout=layout)
    plot_url = py.offline.iplot(fig, )


def rain_dist(path, graph='matplotlib'):

    rain_dist = folder_reader(path)
    rain_dist.columns = ['rain', 'age', 'count']
    no = rain_dist[rain_dist.rain == 'no'][['age', 'count']].set_index('age').sort()
    low = rain_dist[rain_dist.rain == 'low'][['age', 'count']].set_index('age').sort()
    high = rain_dist[rain_dist.rain == 'high'][['age', 'count']].set_index('age').sort()

    if graph == 'matplotlib':
        pylt.figure(figsize=(13, 9))

        pylt.plot((high / rain_dist[rain_dist.rain == 'high']['count'].sum()), label='high rain')
        pylt.plot((low / rain_dist[rain_dist.rain == 'low']['count'].sum()), label='low rain')
        pylt.plot((no / rain_dist[rain_dist.rain == 'no']['count'].sum()), label='no rain')
        pylt.legend(loc='upper right')
        pylt.xlabel('age')
        pylt.ylabel('% of population')
        pylt.grid()
        pylt.show()

    if graph == 'plotly':
        l = low.reset_index()
        h = high.reset_index()
        n = no.reset_index()

        l = l[l.age < 81]
        h = h[h.age < 81]
        n = n[n.age < 81]

        n['count'] = (n['count'] / 1000).astype(int)
        l['count'] = (l['count'] / 10).astype(int)
        h['count'] = (h['count'] / 10).astype(int)

        low_hist = np.repeat(l.age.values, l['count'])
        high_hist = np.repeat(h.age.values, h['count'])
        no_hist = np.repeat(n.age.values, n['count'])

        hist_data = [low_hist]

        group_labels = ['low rain']

        colors = ['rgb(0, 0, 100)']

        # Create distplot with custom bin_size
        fig = FF.create_distplot(hist_data, group_labels, bin_size=1, colors=colors)

        # Plot!
        py.offline.iplot(fig)

        # Add histogram data
        # Group data together
        hist_data = [high_hist]

        group_labels = ['high rain']

        colors = ['rgb(0, 200, 200)']

        # Create distplot with custom bin_size
        fig = FF.create_distplot(hist_data, group_labels, bin_size=1, colors=colors)

        # Plot!
        py.offline.iplot(fig)

        # Add histogram data
        # Group data together
        hist_data = [no_hist]

        group_labels = ['no rain']

        colors = ['rgb(0, 100, 100)']
        # Create distplot with custom bin_size
        fig = FF.create_distplot(hist_data, group_labels, bin_size=1, colors=colors)

        # Plot!
        py.offline.iplot(fig)

        hist_data = [low_hist, high_hist, no_hist]

        group_labels = ['low rain', 'high_rain', 'no rain']

        # Create distplot with custom bin_size
        fig = FF.create_distplot(hist_data, group_labels, bin_size=1)

        # Plot!
        py.offline.iplot(fig)

def start_end_stations(path, graph='all'):
    cum_station_hour = folder_reader(path)
    cum_station_hour.columns = ['rain', 'start_end', 'time', 'station', 'count']

    merged_commute_morning_h = cum_station_hour[
        (cum_station_hour.time == 'morning') & (cum_station_hour.start_end == 'start') & (
        cum_station_hour.rain == 'high')].merge(cum_station_hour[(cum_station_hour.time == 'morning') & (
    cum_station_hour.start_end == 'end') & (cum_station_hour.rain == 'high')], how='outer', left_on=['station'],
                                                right_on=['station'])
    merged_commute_afternoon_h = cum_station_hour[
        (cum_station_hour.time == 'afternoon') & (cum_station_hour.start_end == 'start') & (
        cum_station_hour.rain == 'high')].merge(cum_station_hour[(cum_station_hour.time == 'afternoon') & (
    cum_station_hour.start_end == 'end') & (cum_station_hour.rain == 'high')], how='outer', left_on=['station'],
                                                right_on=['station'])

    merged_commute_morning_n = cum_station_hour[
        (cum_station_hour.time == 'morning') & (cum_station_hour.start_end == 'start') & (
        cum_station_hour.rain == 'no')].merge(cum_station_hour[(cum_station_hour.time == 'morning') & (
    cum_station_hour.start_end == 'end') & (cum_station_hour.rain == 'no')], how='outer', left_on=['station'],
                                              right_on=['station'])
    merged_commute_afternoon_n = cum_station_hour[
        (cum_station_hour.time == 'afternoon') & (cum_station_hour.start_end == 'start') & (
        cum_station_hour.rain == 'no')].merge(cum_station_hour[(cum_station_hour.time == 'afternoon') & (
    cum_station_hour.start_end == 'end') & (cum_station_hour.rain == 'no')], how='outer', left_on=['station'],
                                              right_on=['station'])

    merged_commute_morning_l = cum_station_hour[
        (cum_station_hour.time == 'morning') & (cum_station_hour.start_end == 'start') & (
        cum_station_hour.rain == 'low')].merge(cum_station_hour[(cum_station_hour.time == 'morning') & (
    cum_station_hour.start_end == 'end') & (cum_station_hour.rain == 'low')], how='outer', left_on=['station'],
                                               right_on=['station'])
    merged_commute_afternoon_l = cum_station_hour[
        (cum_station_hour.time == 'afternoon') & (cum_station_hour.start_end == 'start') & (
        cum_station_hour.rain == 'low')].merge(cum_station_hour[(cum_station_hour.time == 'afternoon') & (
    cum_station_hour.start_end == 'end') & (cum_station_hour.rain == 'low')], how='outer', left_on=['station'],
                                               right_on=['station'])

    merged_commute_morning_h['start/end'] = merged_commute_morning_h.count_x / (
    merged_commute_morning_h.count_y + merged_commute_morning_h.count_x)
    merged_commute_morning_h['end/start'] = 1 - merged_commute_morning_h['start/end']
    merged_commute_afternoon_h['start/end'] = merged_commute_afternoon_h.count_x / (
    merged_commute_afternoon_h.count_y + merged_commute_afternoon_h.count_x)
    merged_commute_afternoon_h['end/start'] = 1 - merged_commute_afternoon_h['start/end']

    merged_commute_morning_n['start/end'] = merged_commute_morning_n.count_x / (
    merged_commute_morning_n.count_y + merged_commute_morning_n.count_x)
    merged_commute_morning_n['end/start'] = 1 - merged_commute_morning_n['start/end']
    merged_commute_afternoon_n['start/end'] = merged_commute_afternoon_n.count_x / (
    merged_commute_afternoon_n.count_y + merged_commute_afternoon_n.count_x)
    merged_commute_afternoon_n['end/start'] = 1 - merged_commute_afternoon_n['start/end']

    merged_commute_morning_l['start/end'] = merged_commute_morning_l.count_x / (
    merged_commute_morning_l.count_y + merged_commute_morning_l.count_x)
    merged_commute_morning_l['end/start'] = 1 - merged_commute_morning_l['start/end']
    merged_commute_afternoon_l['start/end'] = merged_commute_afternoon_l.count_x / (
    merged_commute_afternoon_l.count_y + merged_commute_afternoon_l.count_x)
    merged_commute_afternoon_l['end/start'] = 1 - merged_commute_afternoon_l['start/end']

    merged_commute_morning_h = merged_commute_morning_h[['station', 'count_x', 'count_y', 'start/end', 'end/start']]
    merged_commute_morning_h.columns = ['station', 'start_count', 'end_count', 'start/end', 'end/start']
    merged_commute_morning_h['start_count'] = merged_commute_morning_h['start_count'] / (minutes_high_mor / 60)
    merged_commute_morning_h['end_count'] = merged_commute_morning_h['end_count'] / (minutes_high_mor / 60)

    merged_commute_afternoon_h = merged_commute_afternoon_h[['station', 'count_x', 'count_y', 'start/end', 'end/start']]
    merged_commute_afternoon_h.columns = ['station', 'start_count', 'end_count', 'start/end', 'end/start']
    merged_commute_afternoon_h['start_count'] = merged_commute_afternoon_h['start_count'] / (minutes_high_aft / 60)
    merged_commute_afternoon_h['end_count'] = merged_commute_afternoon_h['end_count'] / (minutes_high_aft / 60)

    merged_commute_morning_l = merged_commute_morning_l[['station', 'count_x', 'count_y', 'start/end', 'end/start']]
    merged_commute_morning_l.columns = ['station', 'start_count', 'end_count', 'start/end', 'end/start']
    merged_commute_morning_l['start_count'] = merged_commute_morning_l['start_count'] / (minutes_low_mor / 60)
    merged_commute_morning_l['end_count'] = merged_commute_morning_l['end_count'] / (minutes_low_mor / 60)

    merged_commute_afternoon_l = merged_commute_afternoon_l[['station', 'count_x', 'count_y', 'start/end', 'end/start']]
    merged_commute_afternoon_l.columns = ['station', 'start_count', 'end_count', 'start/end', 'end/start']
    merged_commute_afternoon_l['start_count'] = merged_commute_afternoon_l['start_count'] / (minutes_low_aft / 60)
    merged_commute_afternoon_l['end_count'] = merged_commute_afternoon_l['end_count'] / (minutes_low_aft / 60)

    merged_commute_morning_n = merged_commute_morning_n[['station', 'count_x', 'count_y', 'start/end', 'end/start']]
    merged_commute_morning_n.columns = ['station', 'start_count', 'end_count', 'start/end', 'end/start']
    merged_commute_morning_n['start_count'] = merged_commute_morning_n['start_count'] / (minutes_no_mor / 60)
    merged_commute_morning_n['end_count'] = merged_commute_morning_n['end_count'] / (minutes_no_mor / 60)

    merged_commute_afternoon_n = merged_commute_afternoon_n[['station', 'count_x', 'count_y', 'start/end', 'end/start']]
    merged_commute_afternoon_n.columns = ['station', 'start_count', 'end_count', 'start/end', 'end/start']
    merged_commute_afternoon_n['start_count'] = merged_commute_afternoon_n['start_count'] / (minutes_no_aft / 60)
    merged_commute_afternoon_n['end_count'] = merged_commute_afternoon_n['end_count'] / (minutes_no_aft / 60)

    merged_commute_morning = merged_commute_morning_h.merge(merged_commute_morning_n, how='inner', left_on=['station'],
                                                            right_on=['station'], suffixes=('_h', '_n'))
    merged_commute_afternoon = merged_commute_afternoon_h.merge(merged_commute_afternoon_n, how='inner',
                                                                left_on=['station'], right_on=['station'],
                                                                suffixes=('_h', '_n'))

    mcm = merged_commute_morning

    mcm['diff'] = mcm['start/end_h'] - mcm['start/end_n']
    mcm2 = mcm.sort('start/end_n', ascending=False)

    mca = merged_commute_afternoon

    mca['diff'] = mca['start/end_h'] - mca['start/end_n']
    mcm3 = mca.sort('end/start_n', ascending=False)

    morning_starters = list(mcm[mcm['start/end_n'] > 0.8].station)
    day_sleeping_stations = list(mca[(mca['end/start_n'] > 0.8) & (mca.station.isin(morning_starters))].station)

    mcm_days = mcm[mcm.station.isin(day_sleeping_stations)].sort(['station'])
    mca_days = mca[mca.station.isin(day_sleeping_stations)].sort(['station'])

    if graph == 'all':

        data = [
            go.Bar(
                x=mcm2['station'],  # assign x as the dataframe column 'x'
                y=mcm2['start/end_n'],
                name='% of Trips Started',
                marker=dict(
                    color='rgb(400, 83,40)')
            ),
            go.Bar(
                x=mcm2['station'],
                y=mcm2['end/start_n'],
                name='% of Trips Ended',
                marker=dict(
                    color='rgb(0, 150, 200)')
            )

        ]

        layout = go.Layout(
            barmode='group',
            title='% of Started and Ended Trips in Morning Commute'
        )

        fig = go.Figure(data=data, layout=layout)

        url = py.offline.iplot(fig)

        data = [
            go.Bar(
                x=mcm3['station'],  # assign x as the dataframe column 'x'
                y=mcm3['end/start_n'],
                name='% of Trips Ended'
            ),
            go.Bar(
                x=mcm3['station'],
                y=mcm3['start/end_n'],
                name='% of Trips Started'
            )

        ]

        layout = go.Layout(
            barmode='group',
            title='% of Started and Ended Trips in Afternoon Commute'
        )

        fig = go.Figure(data=data, layout=layout)

        # IPython notebook
        # py.iplot(fig, filename='pandas-bar-chart-layout')

        url = py.offline.iplot(fig)

    if graph == "top_day_starters":



        data = [
            go.Bar(
                x=mcm_days['station'],  # assign x as the dataframe column 'x'
                y=mcm_days['end/start_n'],
                name='% of Trips Ended',
                marker=dict(
                    color='rgb(0, 150, 200)')
            ),
            go.Bar(
                x=mcm_days['station'],
                y=mcm_days['start/end_n'],
                name='% of Trips Started',
                marker=dict(
                    color='rgb(400, 83,40)')
            )

        ]

        layout = go.Layout(
            barmode='group',
            title='% of Started and Ended Trips in Morning Commute for Top "Day Starters"'
        )

        fig = go.Figure(data=data, layout=layout)

        url = py.offline.iplot(fig)



        data = [
            go.Bar(
                x=mca_days['station'],  # assign x as the dataframe column 'x'
                y=mca_days['end/start_n'],
                name='% of Trips Ended'
            ),
            go.Bar(
                x=mca_days['station'],
                y=mca_days['start/end_n'],
                name='% of Trips Started'
            )

        ]

        layout = go.Layout(
            barmode='group',
            title='% of Started and Ended Trips in Afternoon Commute for Top "Day Starters"'
        )

        fig = go.Figure(data=data, layout=layout)

        # IPython notebook
        # py.iplot(fig, filename='pandas-bar-chart-layout')

        url = py.offline.iplot(fig)

    if graph == "correlation":
        mca_merge = mca[['station', 'start/end_n', 'start_count_n', 'end_count_n']]
        mcm_merge = mcm[['station', 'start/end_n', 'start_count_n', 'end_count_n']]
        mca_merge.columns = ['station', 'start_end_aft', 'start_count_aft', 'end_count_aft']
        mcm_merge.columns = ['station', 'start_end_mor', 'start_count_mor', 'end_count_mor']

        merged_corr = mcm_merge.merge(mca_merge, how='inner', left_on=['station'], right_on=['station'],
                                      suffixes=('_m', '_a'))


        xi = np.array(merged_corr.start_end_mor)

        # (Almost) linear sequence
        y = np.array(merged_corr.start_end_aft)

        # Generated linear fit
        slope, intercept, r_value, p_value, std_err = stats.linregress(xi, y)
        line = slope * xi + intercept

        # Creating the dataset, and generating the plot
        trace1 = go.Scatter(
            x=xi,
            y=y,
            mode='markers',
            marker=go.Marker(color='rgb(255, 127, 14)'),
            name='Data'
        )

        trace2 = go.Scatter(
            x=xi,
            y=line,
            mode='lines',
            marker=go.Marker(color='rgb(31, 119, 180)'),
            name='Fit'
        )

        annotation = go.Annotation(
            x=3.5,
            y=23.5,
            showarrow=False,
            font=go.Font(size=16)
        )
        layout = go.Layout(
            title='Correlation between % of started trips in the morning and % of started trips in the afternoon, No rain',
            plot_bgcolor='rgb(229, 229, 229)',
            # xaxis=go.XAxis(zerolinecolor='rgb(255,255,255)', gridcolor='rgb(255,255,255)'),
            # yaxis=go.YAxis(zerolinecolor='rgb(255,255,255)', gridcolor='rgb(255,255,255)'),
            xaxis=dict(range=[0, 1]),
            yaxis=dict(range=[0, 1]))

        data = [trace1, trace2]
        fig = go.Figure(data=data, layout=layout)

        py.offline.iplot(fig)

        print("r-squared:", r_value ** 2)

    if graph == "correlation_high":
        mca_merge = mca[['station', 'start/end_h', 'start_count_h', 'end_count_h']]
        mcm_merge = mcm[['station', 'start/end_h', 'start_count_h', 'end_count_h']]
        mca_merge.columns = ['station', 'start_end_aft', 'start_count_aft', 'end_count_aft']
        mcm_merge.columns = ['station', 'start_end_mor', 'start_count_mor', 'end_count_mor']

        merged_corr = mcm_merge.merge(mca_merge, how='inner', left_on=['station'], right_on=['station'],
                                      suffixes=('_m', '_a'))

        xi = np.array(merged_corr.start_end_mor)

        # (Almost) linear sequence
        y = np.array(merged_corr.start_end_aft)

        # Generated linear fit
        slope, intercept, r_value, p_value, std_err = stats.linregress(xi, y)
        line = slope * xi + intercept

        # Creating the dataset, and generating the plot
        trace1 = go.Scatter(
            x=xi,
            y=y,
            mode='markers',
            marker=go.Marker(color='rgb(255, 127, 14)'),
            name='Data'
        )

        trace2 = go.Scatter(
            x=xi,
            y=line,
            mode='lines',
            marker=go.Marker(color='rgb(31, 119, 180)'),
            name='Fit'
        )

        annotation = go.Annotation(
            x=3.5,
            y=23.5,
            showarrow=False,
            font=go.Font(size=16)
        )
        layout = go.Layout(
            title='Correlation between % of started trips in the morning and % of started trips in the afternoon, High rain',
            plot_bgcolor='rgb(229, 229, 229)',
            # xaxis=go.XAxis(zerolinecolor='rgb(255,255,255)', gridcolor='rgb(255,255,255)'),
            # yaxis=go.YAxis(zerolinecolor='rgb(255,255,255)', gridcolor='rgb(255,255,255)'),
            xaxis=dict(range=[0, 1]),
            yaxis=dict(range=[0, 1]))

        data = [trace1, trace2]
        fig = go.Figure(data=data, layout=layout)

        py.offline.iplot(fig)

        print("r-squared:", r_value ** 2)

    if graph=="top_day_starters_quant":
        data = [
            go.Bar(
                x=mcm_days['station'],  # assign x as the dataframe column 'x'
                y=mcm_days['end_count_n'],
                name='AVG No. of Trips Ended per minute',
                marker=dict(
                    color='rgb(0, 150, 200)')
            ),
            go.Bar(
                x=mcm_days['station'],
                y=mcm_days['start_count_n'],
                name='AVG No. of Trips Started per minute',
                marker=dict(
                    color='rgb(400, 83,40)')
            )

        ]

        layout = go.Layout(
            barmode='group',
            title=' Number of Started and Ended Trips in Morning Commute for Top "Day Starters with No Rain"'
        )

        fig = go.Figure(data=data, layout=layout)

        url = py.offline.iplot(fig)

        data = [
            go.Bar(
                x=mca_days['station'],  # assign x as the dataframe column 'x'
                y=mca_days['end_count_n'],
                name='AVG No. of Trips Ended per minute'
            ),
            go.Bar(
                x=mca_days['station'],
                y=mca_days['start_count_n'],
                name='AVG No. of Trips Started per minute'
            )

        ]

        layout = go.Layout(
            barmode='group',
            title='Number  of Started and Ended Trips in Afternoon Commute for Top "Day Starters" with No Rain'
        )

        fig = go.Figure(data=data, layout=layout)

        # IPython notebook
        # py.iplot(fig, filename='pandas-bar-chart-layout')

        url = py.offline.iplot(fig)

    if graph == "end_quant_weather":
        data = [
            go.Bar(
                x=mca_days['station'],  # assign x as the dataframe column 'x'
                y=mca_days['end_count_n'],
                name='AVG No. of Trips Ended per minute with no Rain',
                marker=dict(
                    color='rgb(400, 83,400)')
            ),
            go.Bar(
                x=mca_days['station'],
                y=mca_days['end_count_h'],
                name='AVG No. of Trips Ended per minute with High Rain',
                marker=dict(
                    color='rgb(0, 150, 0)')
            )

        ]

        layout = go.Layout(
            barmode='group',
            title=' AVG Number of Ended Trips in the Afternoon by weather'
        )

        fig = go.Figure(data=data, layout=layout)

        url = py.offline.iplot(fig)

def penn_station(path):

    penn_station = folder_reader_csv(path)
    penn_station.columns = ['', '', '', 'start_time', 'end_time', '', 'start_station', '', '', '', 'end_station', '', '','', '', '', '', '', '', '', '', '', '', '', '', '', '', '', 'rain', '', '', '']
    rain_gender2 = penn_station[['start_time', 'end_time', 'start_station', 'end_station', 'rain']]

    rain_gender2.start_time = pd.to_datetime(rain_gender2.start_time)
    rain_gender2.end_time = pd.to_datetime(rain_gender2.end_time)
    rain_pen_start = rain_gender2[rain_gender2.start_station == 'Penn Station Valet']
    rain_pen_end = rain_gender2[rain_gender2.end_station == 'Penn Station Valet']

    rain_pen_start['rounded_hour'] = round_hour(rain_pen_start.start_time, 'H')
    rain_pen_end['rounded_hour'] = round_hour(rain_pen_end.end_time, 'H')

    test1 = rain_pen_start.groupby('rounded_hour').count().start_time.reset_index()
    test2 = rain_pen_end.groupby('rounded_hour').count().end_time.reset_index()


    trace1 = go.Scatter(x=test1.rounded_hour,
                        y=test1.start_time)

    trace2 = go.Scatter(x=test2.rounded_hour,
                        y=test2.end_time)

    data = [trace1, trace2]

    layout = dict(
        title='Time series with range slider and selectors for Penn Station Trips',
        xaxis=dict(
            rangeselector=dict(
                buttons=list([
                    dict(count=1,
                         label='1m',
                         step='month',
                         stepmode='backward'),
                    dict(count=6,
                         label='6m',
                         step='month',
                         stepmode='backward'),
                    dict(count=1,
                         label='YTD',
                         step='year',
                         stepmode='todate'),
                    dict(count=1,
                         label='1y',
                         step='year',
                         stepmode='backward'),
                    dict(step='all')
                ])
            ),
            rangeslider=dict(),
            type='date'
        )
    )

    fig = dict(data=data, layout=layout)
    py.offline.iplot(fig)



def plot_Gender(path, feature, type_):
    feature = pd.DataFrame(feature)
    feature = feature.reset_index()
    data = folder_reader(path)
    data.columns = ['temperature', 'wind', 'gender', 'total']
    aux = data[data.gender == 1]
    aux = aux.groupby(type_)['total'].sum()
    aux = aux.reset_index()
    aux = pd.merge(aux, feature, how='left', left_index=type_, right_index="index")
    number = aux[aux.columns[1]] * 100 / aux[aux.columns[3]]
    Temp_1 = np.repeat(aux[aux.columns[0]].values, number.round(0).astype(int))

    aux = data[data.gender == 2]
    aux = aux.groupby(type_)['total'].sum()
    aux = aux.reset_index()
    aux = pd.merge(aux, feature, how='left', left_index=type_, right_index="index")
    number = aux[aux.columns[1]] / aux[aux.columns[3]]
    Temp_2 = np.repeat(aux[aux.columns[0]].values, number.round(0).astype(int))

    hist_data = [Temp_1, Temp_2]
    group_labels = ['Man', 'Woman']
    colors = ['rgb(0, 0, 100)', 'rgb(0, 200, 200)']
    fig = FF.create_distplot(hist_data, group_labels, colors=colors)
    plot_url = py.offline.plot(fig)

def plot_Age(path, feature, type_):
    feature = pd.DataFrame(feature)
    feature = feature.reset_index()
    data = folder_reader(path)
    data.columns = ['temperature', 'wind', 'age', 'total']
    aux = data[data.age < 1950]
    aux = aux.groupby(type_)['total'].sum()
    aux = aux.reset_index()
    aux = pd.merge(aux, feature, how='left', left_index=type_, right_index="index")
    number = aux[aux.columns[1]] * 100 / aux[aux.columns[3]]
    Temp_1 = np.repeat(aux[aux.columns[0]].values, number.round(0).astype(int))

    aux = data[data.age >= 1950]
    aux = aux[aux.age < 1985]
    aux = aux.groupby(type_)['total'].sum()
    aux = aux.reset_index()
    aux = pd.merge(aux, feature, how='left', left_index=type_, right_index="index")
    number = aux[aux.columns[1]] * 100 / aux[aux.columns[3]]
    Temp_2 = np.repeat(aux[aux.columns[0]].values, number.round(0).astype(int))

    aux = data[data.age >= 1985]
    aux = aux.groupby(type_)['total'].sum()
    aux = aux.reset_index()
    aux = pd.merge(aux, feature, how='left', left_index="wind", right_index="index")
    number = aux[aux.columns[1]] * 100 / aux[aux.columns[3]]
    Temp_3 = np.repeat(aux[aux.columns[0]].values, number.round(0).astype(int))

    hist_data = [Temp_1, Temp_2, Temp_3]
    group_labels = ['Older than 65', 'Betwen 30-65', 'Younger than 30']
    colors = ['rgb(0, 0, 100)', 'rgb(0, 200, 200)', 'rgb(0, 300, 300)']
    fig = FF.create_distplot(hist_data, group_labels, colors=colors)
    plot_url = py.offline.plot(fig)


def box_Plot(path):
    data = folder_reader(path)
    data.columns = ['temperature', 'wind', 'time', 'total']
    aux = data[data.temperature < 10]
    aux.time = aux.time / 60
    aux = aux[aux.time < 60]
    number = aux[aux.columns[3]]
    Temp_0 = np.repeat(aux[aux.columns[2]].values, number.round(0).astype(int))

    aux = data[data.temperature < 30]
    aux = aux[aux.temperature >= 10]
    aux.time = aux.time / 60
    aux = aux[aux.time < 60]
    number = aux[aux.columns[3]]
    Temp_1 = np.repeat(aux[aux.columns[2]].values, number.round(0).astype(int))

    aux = data[data.temperature < 50]
    aux = aux[aux.temperature >= 30]
    aux.time = aux.time / 60
    aux = aux[aux.time < 60]
    number = aux[aux.columns[3]]
    Temp_2 = np.repeat(aux[aux.columns[2]].values, number.round(0).astype(int))

    aux = data[data.temperature < 70]
    aux = aux[aux.temperature >= 50]
    aux.time = aux.time / 60
    aux = aux[aux.time < 60]
    number = aux[aux.columns[3]]
    Temp_3 = np.repeat(aux[aux.columns[2]].values, number.round(0).astype(int))

    aux = data[data.temperature < 90]
    aux = aux[aux.temperature >= 70]
    aux.time = aux.time / 60
    aux = aux[aux.time < 60]
    number = aux[aux.columns[3]]
    Temp_4 = np.repeat(aux[aux.columns[2]].values, number.round(0).astype(int))

    trace0 = go.Box(
        y=Temp_0,
        name='0 to 10'
    )
    trace1 = go.Box(
        y=Temp_1,
        name='10 to 30'
    )
    trace2 = go.Box(
        y=Temp_2,
        name='30 to 50'
    )
    trace3 = go.Box(
        y=Temp_3,
        name='50 to 70'
    )
    trace4 = go.Box(
        y=Temp_4,
        name='70 to 90'
    )

    data = [trace0, trace1, trace2, trace3, trace4]
    plot_url = py.offline.plot(data)

def box_Plot_wind(path):
    data = folder_reader(path)
    data.columns = ['temperature', 'wind', 'time', 'total']
    aux = data[data.wind < 10]
    aux.time = aux.time / 60
    aux = aux[aux.time < 60]
    number = aux[aux.columns[3]]
    Temp_0 = np.repeat(aux[aux.columns[2]].values, number.round(0).astype(int))

    aux = data[data.wind < 20]
    aux = aux[aux.wind >= 10]
    aux.time = aux.time / 60
    aux = aux[aux.time < 60]
    number = aux[aux.columns[3]]
    Temp_1 = np.repeat(aux[aux.columns[2]].values, number.round(0).astype(int))

    aux = data[data.wind >= 20]
    aux.time = aux.time / 60
    aux = aux[aux.time < 60]
    number = aux[aux.columns[3]]
    Temp_2 = np.repeat(aux[aux.columns[2]].values, number.round(0).astype(int))

    trace0 = go.Box(
        y=Temp_0,
        name='0 to 10'
    )
    trace1 = go.Box(
        y=Temp_1,
        name='10 to 30'
    )
    trace2 = go.Box(
        y=Temp_2,
        name='30 to 50'
    )

    data = [trace0, trace1, trace2]
    plot_url = py.offline.plot(data)


