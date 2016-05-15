import sys
import pandas as pd
import random
from datetime import datetime, timedelta


# This function creates x number of hex colors
def create_color(num_colors):
    list_colors = []
    for i in range(num_colors):
        r = lambda: random.randint(0,255)
        color = '#%02X%02X%02X' % (r(),r(),r())
        list_colors.append(color)
    return list_colors


# Function that creates a list of date strings per hour
def create_datetimes_delta(start_date, end_date, delta_hour):
    all_dates = []
    one_hour = timedelta(hours=delta_hour)
    current_date = start_date
    while current_date < end_date:
        all_dates.append(current_date.strftime('%Y-%m-%d %H:%M:00'))
        current_date =  current_date + one_hour
    return all_dates


def creates_hourly_files(citibike_df, hourly_dates, station_catalogue, dest_folder):
    for i, h_date in enumerate(hourly_dates):
        if i + 1 < len(hourly_dates):
            start_date_hour = hourly_dates[i]
            end_date_hour = hourly_dates[i+1]
            # Filters the dataframe by the corresponding hour
            trips_hour = citibike_df[(citibike_df['start_time_east'] > start_date_hour )
                                     & (citibike_df['start_time_east'] < end_date_hour )]

            # Number of Trips Going Out.
            start_stations = trips_hour.groupby(['start_station']).count()
            start_stations = start_stations[['start_time_east']]
            start_stations = start_stations.reset_index()
            start_stations.columns = ['start_station', 'bikes_out']
            #print "Out Trips", len(start_stations.index)

            # Number of Trips Going In
            end_stations = trips_hour.groupby(['end_station']).count()
            end_stations = end_stations[['start_time_east']]
            end_stations = end_stations.reset_index()
            end_stations.columns = ['end_station', 'bikes_in']
            # print "In Trips", len(end_stations.index)

            # From the dataframe obtains the unique stations
            start_stations_uniques = sorted(trips_hour.start_station.unique())
            end_stations_uniques = sorted(trips_hour.end_station.unique())
            list_stations = sorted(list(set(start_stations_uniques + end_stations_uniques)))

            # Creates the transp matrix filled with zeros
            transp_matrix = pd.DataFrame(index=list_stations, columns=list_stations)
            transp_matrix = transp_matrix.fillna(0)

            # Fills the transp matrix with the trips
            for index, row in trips_hour.iterrows():
                try:
                    transp_matrix.loc[row.start_station, row.end_station] += 1
                except IndexError:
                    print "IndexError", row.start_station, row.end_station

            # Creates the ratios
            total_trips = trips_hour.shape[0]
            trans_matrix_ratios = transp_matrix.divide(total_trips)

            # Filter the stations from the catalogue, to get the names
            filtered_stations = station_catalogue.loc[list_stations,:]
            filtered_stations = filtered_stations.reset_index()

            # Joins the station catalogue with the In/Out trips
            filtered_stations = filtered_stations.merge(start_stations, how='left',
                                                        left_on='station_id',
                                                        right_on='start_station')
            filtered_stations = filtered_stations.merge(end_stations, how='left',
                                                        left_on='station_id',
                                                        right_on='end_station')
            filtered_stations = filtered_stations.fillna(0)
            filtered_stations = filtered_stations[['station_id','name','lat','lon','bikes_out','bikes_in']]
            filtered_stations[['bikes_out','bikes_in']] = filtered_stations[['bikes_out','bikes_in']].astype(int)
            # print len(filtered_stations)

            # Creates a diferent color for each station
            n_colors = filtered_stations.shape[0]
            list_colors = create_color(n_colors)
            filtered_stations['color'] = list_colors

            # Creates a name for the files (the json and the csv)
            file_name = start_date_hour.replace(' ','_')
            file_name_catalogue = file_name+'_catalogue.csv'
            file_name_graph = file_name+'_gmap.csv'
            file_name_matrix_json = file_name+'_matrix_ratios.json'

            # Directios Graph for Google Maps
            trips_graph = trips_hour[['start_station','start_lat', 'start_lon',
                                      'end_station', 'end_lat', 'end_lon']]
            # trips_graph.drop_duplicates(inplace=True)

            # Saves the json and the csvs
            trans_matrix_ratios.to_json(dest_folder+'/'+file_name_matrix_json, orient='values')
            filtered_stations.to_csv(dest_folder+'/'+file_name_catalogue, index=False)
            trips_graph.to_csv(dest_folder+'/'+file_name_graph, index=False)

            print "Files Saved:", file_name_catalogue, file_name_matrix_json


if __name__ == '__main__':
    # sys.argv[1] = "Merged citibike weather"
    # sys.argv[2] = "Stations List"
    # sys.argv[3] = "Init Date"
    # sys.argv[4] = "End Date"
    # sys.argv[5] = "Destination Folder"

    # Loads the merged dataset
    citibike_merged = pd.read_csv(sys.argv[1], header=None, index_col=False)
    # Filters just the needed columns
    citibike_merged_reduced = citibike_merged.iloc[:, [3, 4, 5, 7, 8, 9, 11, 12]]
    citibike_merged_reduced.columns = ['start_time_east', 'end_time_east',
                                       'start_station', 'start_lat', 'start_lon',
                                       'end_station', 'end_lat', 'end_lon']

    # Loads the file with the stations. This is used to create the file with the names of the stations and colors.
    station_catalogue = pd.read_csv(sys.argv[2], index_col=[0])

    # Converts from string to datetime object
    s_date = sys.argv[3]
    e_date = sys.argv[4]
    first_date = datetime.strptime(s_date, '%Y-%m-%d %H:%M:%S')
    last_date = datetime.strptime(e_date, '%Y-%m-%d %H:%M:%S')

    hourly_dates = create_datetimes_delta(first_date, last_date, 1)

    destination = sys.argv[5]

    creates_hourly_files(citibike_merged_reduced, hourly_dates, station_catalogue, destination)