"""
###### BASICS #######

The basic three major questions we're going to answer today are:
1. How many crimes have been reported to CPD from 2010 to 2014?
	1a. How many categories do these offenses fall under (THEFT, BATTERY, etc)

2. What are the top 5 categories of highest number of crimes reported in Chicago from 2010-2014?
		
3. How have the number of occurrences of the top 5 crimes changed over the years? 
	3a. Can we predict the number of occurences for 2015? Modeling the trends using basic linear regression.

We have to:
-read/process the data
-organize the entries of each crime report
-sort the entries, both by year and type
-graph the data
"""

from scipy import stats
import numpy as np
import calendar # for temperature
import parsing_module
import crime_module
import weather_module
import plotting_module

#Processing the text file

crime_file_name = '/Users/jjw036/ChicagoCrime/crimes_2001_to_present_parsed.csv'
data_list = parsing_module.read_data(crime_file_name)

#1. How many crimes have been reported from 2001 to present?
total_crimes = len(data_list)

#Organizing the data into easily ascessible structures.
#let's model the crime data with a dictionary. Each entry/line will be turned into what we define as a case

case_list = []

for entry in data_list:

	entry = entry.split(',') 
	case = {	"ID": entry[0],
				"CaseNumber": entry[1],
				"Date": entry[2],
				"Block": entry[3],
				"Type": entry[4],
				"Description": entry[5],
				"LocationType": entry[6],
				"Ward": entry[7],
				"Year": entry[8],
				"Month": entry[9],
				"Latitude": entry[10],
				"Longitude": entry[11]
			}	

	case_list.append(case)

#1a. How many categories do these offenses fall under?

offense_list = crime_module.get_unique_offenses(case_list)
print(offense_list)

#2. What are the top 5 categories?
#Organizing offenses by type.
organized_cases = crime_module.organize_cases_by_offense(case_list)

#Counting the organized structure.
offense_count = crime_module.count_offenses(organized_cases)

#Let's organize offenses by year, and then by type.

year_list = [2010,2011,2012,2013,2014]

offense_count_for_each_year = []
for year in year_list:
	yearly_case_list = crime_module.get_cases_by_year(case_list,year)
	yearly_organized_cases = crime_module.organize_cases_by_offense(yearly_case_list)
	yearly_offense_count = crime_module.count_offenses(yearly_organized_cases)
	offense_count_for_each_year.append(yearly_offense_count)

# Our top offenses seem to be burglary, criminal damage, narcotics, battery, and theft.
# Let's get the average and standard deviation and count for BURGLARY, CRIMINAL DAMAGE, NARCOTICS, BATTERY, and THEFT for each year
target_offenses = ["BURGLARY","CRIMINAL DAMAGE", "NARCOTICS", "BATTERY", "THEFT"]
means_offenses = []
stdev_offenses = []
counts_offenses = []

for offense in target_offenses:
	mean, stdev, counts = crime_module.get_stats(offense_count_for_each_year, offense)
	means_offenses.append(mean)
	stdev_offenses.append(stdev)
	counts_offenses.append(counts)

# Plotting the top 5 categories as bar graphs
save_bar_file = "top_crimes_bar.png"
plotting_module.plot_bar_graph(target_offenses,means_offenses,stdev_offenses,save_bar_file)

# 3. How have the top 5 offenses changed over time?  
save_line_file = "top_crimes_line.png"
plotting_module.plot_line_graph(target_offenses, counts_offenses,year_list,save_line_file)

# 3a. Can we predict the number of occurrences that may happen in 2015? Modeling the trends using linear regression

year_list = list(map(int,year_list))
target_year = 2015
for index,offense in enumerate(target_offenses):
	predicted, parameters = crime_module.predict_occurrences(year_list,counts_offenses[index], target_year)
	print("For the year " + str(target_year) + ", " + offense + " is predicted to have " + str(predicted) + " occurrences.")
	# y = mx + b


# Optional Project questions:

# 1. What's the correlation between temperature and offense occurrences? Is there a particular category of offense where there's a negative correlation between temperature and number of occurrences?


# Reading the temperature file:
weather_file_name = '/Users/jjw036/ChicagoCrime/weather_parsed.csv'
weather_data = parsing_module.read_data(weather_file_name)

weather_list = []

# We can read the data into a list
for entry in weather_data:

	entry = entry.split(',') 
	report = {	"Station": entry[0],
				"Location": entry[1],
				"Date": entry[2],
				"MaxTemp": entry[3],
				"Year": entry[4],
				"Month": entry[5]
			}	

	weather_list.append(report)

# Get the average temperature of each month for a 4 year period
# Get all the month names in a year.
month_list = []
for i in range(1,13):
	month_list.append(calendar.month_name[i])

average_max_temps = []
# cycle through months and years
for year in year_list:
	for month in month_list:
		mean_temp, std_temp, temps = weather_module.calculate_temp_summary_by_month(weather_list, month, year)
		average_max_temps.append(mean_temp)


# In our organized case list, we're going to get the number of occurences for each month.
monthly_offense_list =[]
total_monthly_offenses = []
for year in year_list:
	for month in month_list:
		monthly_offenses, offense_n = crime_module.get_crime_summary_by_month(organized_cases, month, year)
		monthly_offense_list.append(monthly_offenses)
		total_monthly_offenses.append(offense_n)


#Plotting the correlation between number of offenses and temperature

plotting_module.plot_correlation_graph(average_max_temps, total_monthly_offenses, "Total Monthly Offenses", "total_temp_correlation.png")

pearson_corr, p_value = stats.pearsonr(average_max_temps,total_monthly_offenses)

#There's a positive correlation between temperature and crime

#Is there an offense where there's a negative correlation?

# Organize the monthly offense list into a list of lists.
# Initialize dictionary
monthly_offense_dict = {}
for offense in offense_list:
	monthly_offense_dict[offense] = []

for month_summary in monthly_offense_list:
	for offense_tuple in month_summary:
		offense = offense_tuple[0]
		n = offense_tuple[1]
		monthly_offense_dict[offense].append(n)

tuple_list = []
for offense in monthly_offense_dict.keys():
	monthly_offense_occurence = monthly_offense_dict[offense]
	pearson_corr, p_value = stats.pearsonr(average_max_temps,monthly_offense_occurence)
	tuple_list.append((offense,pearson_corr))

tuple_list = sorted(tuple_list, key=lambda x: x[1])

# :( 


# 2. Where have these offenses occurred? We are going to write a quick extension that maps each offense onto a road map using the location of each case (longitude/latitude).

# 3. Advanced data structures. Putting the cases in a table format using a package called Pandas.