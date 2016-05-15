# DS-GA-1004_Final-Project

Authors
-------
- Sebastian Brarda (sb5518@nyu.edu)
- Osvaldo Bulos Ramirez (obr214@nyu.edu)
- Ali Josue Limon (ajl649@nyu.edu)


What is it?
-----------
This GIT HUB repository includes all the code necessary to reproduce the analysis conducted for the Final Project of the course "Big Data", DS-GA-1004, Spring 2016, New York University.

The PDF of the analysis is included in the GIT HUB repository. In order to reproduce the analysis, all the code was included here, but some of the data needs to be downloaded from the internet.


Installation instructions
-------------------------

The Following Python packages are required to run the code:

- Pandas
- Numpy 
- Plotly
- Matplotlib
- Scipy
- Os
- Pytz
- Time
- Datetime
- Pylab


Data Download
-------------

Two Datasets are Required to conduct the analysis and run the code.

- The first one, weather data from NOAA is included in the Repository
- The second one, Citi Bike trips information from 2015 is open and must be downloaded from their webpage.
You can find them at https://www.citibikenyc.com/system-data

Weather Data Preprocessing
--------------------------
To pre-process the weather data, just run the weather_minute() function inside the weather_cleaner.py script located in the root directory. It returns a DataFrame that is ready to Join with the Citi Bike data.

Citi Bike Data Integration with SPARK
-------------------------

Once the CitiBike and Weather Datasets are preprocessed, they are ready to be merged.
For this task, a PySpark script was coded.
The pyspark script is named: citibike_weather_spark_merger.py

Requirements:
    pytz module installed.

To do the merge the following line should be executed:
>> spark-submit citibike_weather_spark_merger.py cityBike.csv weather_ready_join
Where the first parameter is the pyspark script, followed by the citibike dataset and finally the weather dataset

The final output will be saved in a folder named: "citibike_weather"

How to run the charts for the analysis
--------------------------------------

1) Conduct the join of the tables as mentioned in the previous step.
2) Once the main table is stored in the main directory, proceed to run the map-reduce tasks:
        - Tasks can be run on Local Hadoop, or in a Hadoop cluster. We run them in AWS, Amazon Cloud Services.
	- Each map and reduce task has a number (ie. 1,2,3,4...)
	- Each map tasks should be run with the respective reduce task over the main datafile, except map7.py that has no reducer (it should be run alone).
        - The result of each map reduce should be stored in a folder with the same number of the respective map.py and reduce.py (ie. map1.py and reduce1.py output should be store in a folder called "1")
        - All the output folders should be store in the main root of the repository
        - Any number of reducers will be fine for the process, we used 2 as a reference.
3) Once all the map reduce tasks were conducted, open the Plot.ipynb and Plot 2.ipynb with Jupyter Notebook and execute all the lines.
4) Once this is done, all the charts shown in the PDF of the report should be displayed. Otherwise, please contact us by e-mail

Visualization Files
--------------------------------------
The visualization needs a series of hourly files from where the information is obtained.
This approach was selected due the limitation that no server can be used to make requests to a database.
The files generated are small in size. It is not recommended to load a large size file into a web browser since the user experience can be affected in a negative way.
To create said files, a range of dates can be provided and the amount of files generated will be the number of hours between the given dates.

For one hour of a day, three files are generated:
- A CSV containing the active stations during that hour with their locations, and number of trips in and out. File used for the Chord Plot and Google Map.
- A JSON with the transport matrix. File used for the Chord Plot.
- A CSV containing the interactions between stations (). File used for the Google Map.


To generate those files, the script visualization_hourly_files.py should be run.
It receives as parameters:
    - The name of the citibike_weather file (The merge produced by the PySpark script).
    - The name of the stations_list file (Provided - final_station_list.csv. It includes the names, ids and locations of each station).
    - The Start Date with hour in the format "YYYY-MM-DD HH:MM:SS"
    - The End Data with hour in the format "YYYY-MM-DD HH:MM:SS"
    - The name of the folder where the files will be stored. (It should be created before the execution of the script)

Example:
>> python visualization_hourly_files.py citibike_weather.csv final_station_list.csv '2015-12-01 05:00:00' '2015-12-01 08:00:00' hourly_files

Directories, Files and Modules
------------------------------

	/BD_FinalProject
        - README.txt
    - citibike_weather_spark_merger.py
	- weather_cleaner.py
	- plot_functions.py
	- weather-data.txt
        - Plots.ipynb
        - Plots 2.ipynb
        - final_project.pdf

	
	/BD_FinalProject/weather_cleaning
	- weather_cleaner.py
	- Police_Stations.csv
        - weather_grouped

	/BD_FinalProject/mappers
	- map1.py
        - map2.py
        - map3.py
        - map4.py
        - map5.py
        - map6.py
        - map7.py
        - map8.py
        - map9.py
        - map10.py


	/BD_FinalProject/reducers
	- reduce1.py
        - reduce2.py
        - reduce3.py
        - reduce4.py
        - reduce5.py
        - reduce6.py
        - reduce8.py
        - reduce9.py
        - reduce10.py





Copyright and licencing information:
------------------------------------

- No code was reused from other sources.
- The charts created with Plot.ly were mainly based on examples provided in their webpage.
- The visualization uses a Free Distribution Bootstrap Template created by Almsaeed Studio. (Copyright © 2014-2015 Almsaeed Studio. All rights reserved.)

Other considerations
--------------------
