import pandas as pd
import numpy as np
from datetime import datetime, timedelta
from pytz import timezone
from scipy import stats


def data_sampler_renamer_parser(path='weather-data.txt'):

    # Take columns that are useful, rename them, parse the timestamp string

    data = pd.read_csv(path, delimiter=r"\s+")
    data_useful = data[
        ['YR--MODAHRMN', 'DIR', 'SPD', 'CLG', 'SKC', 'VSB', 'MW', 'AW', 'AW.1', 'TEMP', 'DEWP', 'SLP', 'ALT', 'MAX',
         'MIN', 'PCP01', 'PCP06', 'PCP24', 'PCPXX', 'SD']]
    data_useful.rename(
        columns={'YR--MODAHRMN': 'timestamp', 'DIR': 'wind_direction', 'SPD': 'wind_speed', 'CLG': 'cloud_ceiling',
                 'SKC': 'sky_cover', 'VSB': 'visibility_miles', 'MW': 'manual_weather', 'AW': 'auto_weather',
                 'AW.1': 'auto_weather1', 'TEMP': 'temprature', 'DEWP': 'dew_point', 'SLP': 'sea_level',
                 'ALT': 'altimeter', 'MAX': 'max_temp', 'MIN': 'min_temp', 'PCP01': '1hour_precip',
                 'PCP06': '6hour_precip', 'PCP24': '24hour_precip', 'PCPXX': '3hour_precip', 'SD': 'snow_depth'},
        inplace=True)
    data_useful.timestamp = data_useful.timestamp.astype(str)
    data_useful['year'] = data_useful.timestamp.str[0:4]
    data_useful['month'] = data_useful.timestamp.str[4:6]
    data_useful['day'] = data_useful.timestamp.str[6:8]
    data_useful['hour'] = data_useful.timestamp.str[8:10]
    data_useful['minutes'] = data_useful.timestamp.str[10:12]
    data_useful.minutes = data_useful.minutes.astype(int)
    data_useful.year = data_useful.year.astype(int)
    data_useful.month = data_useful.month.astype(int)
    data_useful.day = data_useful.day.astype(int)
    data_useful.hour = data_useful.hour.astype(int)

    return data_useful


def days_fixer(dataframe):

    # Unify times to have observations at every hour. Fix all the dates/times based on this criteria

    df = dataframe
    df.loc[(df['minutes'].values < 31) & (df['minutes'].values != 0), 'minutes'] = 0
    df.loc[(df['minutes'].values > 30) & (df['minutes'].values != 0), 'hour'] = df[(df.minutes != 0) & (
    df.minutes > 30)].hour + 1
    df.loc[(df['minutes'].values > 30) & (df['minutes'].values != 0), 'minutes'] = 0
    df.loc[(df['hour'].values == 24), 'day'] = df[df.hour == 24].day + 1
    df.loc[(df['hour'].values == 24), 'hour'] = 0
    df.loc[(df['day'].values == 32), 'month'] = df[df.day == 32].month + 1
    df.loc[(df['day'].values == 32), 'day'] = 1
    df.loc[(df['day'].values == 29) & (df['month'].values == 2), ['month', 'day']] = 3, 1
    df.loc[(df['day'].values == 31) & (df['month'].values == 4), ['month', 'day']] = 5, 1
    df.loc[(df['day'].values == 31) & (df['month'].values == 6), ['month', 'day']] = 7, 1
    df.loc[(df['day'].values == 31) & (df['month'].values == 9), ['month', 'day']] = 10, 1
    df.loc[(df['day'].values == 31) & (df['month'].values == 11), ['month', 'day']] = 12, 1
    df.loc[(df['day'].values == 1) & (df['month'].values == 13), ['month', 'day', 'year']] = 1, 1, 2016

    df.hour = df.hour.map("{:02}".format)
    df['datetime'] = pd.to_datetime(
        df.year.astype(str) + ' ' + df.month.astype(str) + ' ' + df.day.astype(str) + ' ' + df.hour.astype(str),
        format='%Y %m %d %H')

    return df


def grouper(dataframe):

    # Take a subset of colums and group them by time stamp. Afterwards take the mean/mode of the values depending on dataype

    sub_df = dataframe[
        ['wind_direction', 'wind_speed', 'cloud_ceiling', 'sky_cover', 'visibility_miles', 'temprature', 'dew_point',
         'sea_level', 'altimeter', '1hour_precip', 'datetime']]
    sub_df = sub_df.convert_objects(convert_numeric=True)

    f = {'wind_direction': ['mean'], 'wind_speed': ['mean'], 'cloud_ceiling': ['mean'], 'visibility_miles': ['mean'],
         'temprature': ['mean'], 'dew_point': ['mean'], 'sea_level': ['mean'], 'altimeter': ['mean'],
         '1hour_precip': ['mean']}
    grouped = sub_df.groupby('datetime').agg(f)
    grouped.columns = grouped.columns.droplevel(-1)

    grouped2 = sub_df[['sky_cover', 'datetime']]
    grouped2.loc[(grouped2['sky_cover'].values == '***'), 'sky_cover'] = np.nan
    grouped3 = grouped2.groupby(['datetime']).agg(lambda x: stats.mode(x)[0][0])
    grouped3.loc[(grouped3['sky_cover'].values == 0), 'sky_cover'] = np.nan

    data_full = grouped.merge(grouped3, how='left', on=None, left_on=None, right_on=None, left_index=True,
                              right_index=True)

    data_full.reset_index(inplace=True)

    data_full['1hour_precip'].fillna(0, inplace=True)

    data_full.loc[data_full[data_full['1hour_precip'] > 0.049].index, 'precip'] = 'high'
    data_full.loc[data_full[data_full['1hour_precip'] <= 0.049].index, 'precip'] = 'low'
    data_full.loc[data_full[data_full['1hour_precip'] == 0].index, 'precip'] = 'no'

    data_full['precip_shift'] = data_full.precip.shift(-1)
    data_full = pd.get_dummies(data_full, prefix=None, columns=['precip_shift'], sparse=False, drop_first=False)

    data_full = data_full.fillna(method='bfill', axis=0, inplace=False, limit=None, downcast=None)

    return data_full


def convert_gmt_to_easttime(string_date):
    """
    :param string_date: GMT date
    :return: Date converted to eastern time
    """
    # Converts the string to datetime object
    string_date = str(string_date)
    try:
        gtm = timezone('GMT')
        eastern_tz = timezone('US/Eastern')

        date_obj = datetime.strptime(string_date, '%Y-%m-%d %H:%M:%S')
        date_obj = date_obj.replace(tzinfo=gtm)
        date_eastern = date_obj.astimezone(eastern_tz)
        date_str = date_eastern.strftime('%Y-%m-%d %H:%M:%S')
        return date_str

    except IndexError:
        return ''


def add_easterntime_column(dataframe):
    """
    :param dataframe: Weather dataframe
    :return: dataframe with easter time column
    """
    dataframe['est_datetime'] = dataframe['datetime'].apply(convert_gmt_to_easttime)
    dataframe['est_datetime'] = pd.to_datetime(dataframe['est_datetime'])
    return dataframe

#Set

#Interpolation
### 5 functions:
### ToTimestamp(d) from date to number
### toStringDate(d) from number to Date
### RepeatLast() interpolate by the last number
### toMinute() from hours to minutes
### Inter() Interpolate the dataset of weather

def toTimestamp(d):
    return mktime(utc.localize(d).utctimetuple())


def toStringDate(d):
    return datetime.fromtimestamp(d)


def repeatLast(left,right, values):
    right= pd.concat((pd.DataFrame(right),pd.DataFrame(values)),axis=1)
    right.columns=['first','second']
    left.columns=['first']
    inter = left.merge(right, how='left', on='first')
    return inter.fillna(method='ffill')


def toMinute(datatime):
    date_aux = datatime[0]
    minute_dates = []
    while (date_aux <= datatime[len(datatime)-1]): 
        minute_dates.append(toTimestamp(date_aux))
        date_aux +=timedelta(minutes=1) # days, seconds, then other fields.
    return minute_dates


def inter(weather):
    datatime = pd.to_datetime(weather['datetime'])
    datatime = datatime.apply(toTimestamp)
    minute_dates=toMinute(weather['datetime'])
    wind = np.interp(minute_dates, datatime, weather['wind_speed'])
    dew = np.interp(minute_dates, datatime, weather['dew_point'])
    visibility= np.interp(minute_dates, datatime, weather['visibility_miles'])
    wind_dir= np.interp(minute_dates, datatime, weather['wind_direction'])
    sea_level= np.interp(minute_dates, datatime, weather['sea_level'])
    altimeter =  np.interp(minute_dates, datatime, weather['altimeter'])
    temprature = np.interp(minute_dates, datatime, weather['temprature'])
    precip=repeatLast(pd.DataFrame(minute_dates),datatime, weather[ 'precip'])
    precip_shift_high=repeatLast(pd.DataFrame(minute_dates),datatime, weather[ 'precip_shift_high'])
    precip_shift_low=repeatLast(pd.DataFrame(minute_dates),datatime, weather[ 'precip_shift_low'])
    precip_shift_no=repeatLast(pd.DataFrame(minute_dates),datatime, weather[ 'precip_shift_no']) 
    interDf = pd.concat((pd.DataFrame(minute_dates),pd.DataFrame(wind), 
                      pd.DataFrame(dew),pd.DataFrame(visibility), 
                      pd.DataFrame(wind_dir),pd.DataFrame(sea_level),
                      pd.DataFrame(altimeter),pd.DataFrame(temprature),
                         precip['second'],precip_shift_high['second'],
                         precip_shift_low['second'], precip_shift_no['second'],
                     ),axis=1)
    interDf.columns=['datetime', 'wind_speed', 'dew_point', 'visibility_miles',
                    'wind_direction', 'sea_level', 'altimeter', 'temperature',
                    'precip', 'precip_shift_high','precip_shift_low', 'precip_shift_no']
    interDf['datetime']=interDf['datetime'].apply(toStringDate)
    return interDf    

def weather_cleaner(path='weather-data.txt'):
    dataframe = data_sampler_renamer_parser(path)
    dataframe = days_fixer(dataframe)
    dataframe = grouper(dataframe)
    dataframe = add_easterntime_column(dataframe)
    return dataframe
    
def weather_minute():
    hour_weather=weather_cleaner()
    min_weather=inter(hour_weather)

