import pandas as pd
import numpy as np
from scipy import stats



def data_sampler_renamer_parser(path='weather-data.txt'):

    #Take columns that are useful, rename them, parse the timestamp string

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

    #Take a subset of colums and group them by time stamp. Afterwards take the mean/mode of the values depending on dataype

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

    return data_full

def weather_cleaner(path='weather-data.txt'):
    dataframe = data_sampler_renamer_parser(path)
    dataframe = days_fixer(dataframe)
    dataframe = grouper(dataframe)
    return dataframe
