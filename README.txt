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

OSVALD

- Finally place the dataset with the name "XXXXXXX" in the root directory of the repository

How to run the charts for the analysis
--------------------------------------

1) Conduct the join of the tables as mentioned in the previous step.
2) Once the main table is stored in the main directory, proceed to run the map-reduce tasks:
	- Each map and reduce task has a number (ie. 1,2,3,4...)
	- Each map tasks should be run with the respective reduce task over the main datafile, except map7.py that has no reducer (it should be run alone).
        - The result of each map reduce should be stored in a folder with the same number of the respective map.py and reduce.py (ie. map1.py and reduce1.py output should be store in a folder called "1")
        - All the output folders should be store in the main root of the repository
        - Any number of reducers will be fine for the process, we used 2 as a reference.
3) Once all the map reduce tasks were conducted, open the Plot.ipynb and Plot 2.ipynb with Jupyter Notebook and execute all the lines.
4) Once this is done, all the charts shown in the PDF of the report should be displayed. Otherwise, please contact us by e-mail

Directories, Files and Modules
------------------------------

	/BD_FinalProject
        - README.txt
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


Other considerations
--------------------
OSVALD
