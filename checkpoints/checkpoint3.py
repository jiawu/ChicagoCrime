def read_data(filename):
	"""Returns a list of all the lines in the file, minus the header"""
	file_object = open(filename, 'r')

	#read the file line-by-line
	data_list = []
	for line in file_object:
		#get rid of \n newspace
		new_line = line.strip()
		data_list.append(new_line)

	#first line is the header, remove that from the data and save it
	data_header = data_list.pop(0)
	return(data_list)

def get_unique_offenses(case_list):
	"""Return a list of unique offenses, given a list of case dicts"""

	unique_offenses = []
	for case in case_list:
		offense = case['Type']
		if offense not in unique_offenses:
			unique_offenses.append(offense)

	unique_offense_n = len(unique_offenses)
	print("There are " + str(unique_offense_n) + " unique offenses.")
	return(unique_offenses)
	

def organize_cases_by_offense(case_list):
	""" Organizes cases by the offense and returns a dictionary
	Input: a LIST of DICTS (cases) for example:[ case1, case2, case3 ]
	Output: a DICT of LISTs. The lists are lists of cases. 
	for example:
	{"offense1" : list_of_cases_in_offense1, 
	 "offense2" : list_of_cases_in_offense2 
	}
	"""
	unique_offenses = get_unique_offenses(case_list)
	#initialize a dictionary
	organized_cases = {}
	for item in unique_offenses:
		organized_cases[item] = []
	#now go through each case and append the cases to the matching list.
	for case in case_list:
		case_offense = case['Type']
		organized_cases[case_offense].append(case)

	return(organized_cases)
	
def count_offenses(organized_case_dict):
	"""Return a list of tuples indicating the offense and the number of offenses in the organized case dict, given an organized case dict"""
	tuple_list = []
	for key in organized_case_dict.keys():
		offense = key
		case_n = len(organized_case_dict[key])
		offense_tuple = (offense, case_n)
		tuple_list.append(offense_tuple)

	
	#anyone know how to sort without using lambda?
	return(tuple_list)

def get_stats(tuple_list, target_offense):
	"""Returns the mean and standard deviation of an offense given a target offense and an organized case dict"""
	values_list = []
	for year in tuple_list:
		for offense_tuple in year:
			if offense_tuple[0] == target_offense:
				values_list.append(offense_tuple[1])
	mean = statistics.mean(values_list)
	stdev = statistics.stdev(values_list)
	return(mean,stdev,values_list)

	### Section 3 specifics: ###
def predict_occurrences(year_list,counts_per_year, target_year):
	"""Returns the predicted number of offenses for a given year and the parameters for the linear regression used to fit"""
	slope, intercept, r_value, p_value, std_err = stats.linregress(year_list, counts_per_year)
	# y = mx + b
	predicted = slope * int(target_year) + intercept
	parameters = {  "slope": slope,
					"intercept": intercept,
					"r_value": r_value,
					"p_value": p_value,
					"std_error": std_err
	}
	return(predicted,parameters)
	
def plot_bar_graph(target_offenses, means_offenses, stdev_offenses, filename):
	"""Plots and saves a bar graph"""
	fig, ax = plt.subplots()
	bar_width = 0.8
	index = np.arange(len(target_offenses))
	bar_graph = plt.bar(index, means_offenses, width=bar_width, yerr=stdev_offenses)

	plt.xlabel('Offenses')
	plt.ylabel('Average Occurences Per Year')
	plt.title('Average Occurrences Per Year 2010-2014')
	ax.set_xticklabels(target_offenses)
	ax.xaxis.set(ticks=np.arange(bar_width/2, len(target_offenses)), ticklabels=target_offenses)
	plt.tight_layout()
	plt.savefig(filename,format="png")
	plt.show()
	

def plot_line_graph(target_offenses, counts, year_list, filename):
	"""Plots and saves a line graph """
	#this is to demonstrate line graphs but the data is categorical so you should actually be using bar graphs
	fig, ax = plt.subplots()
	colors = ["blue","red","orange","green","yellow","purple"]
	for index,offense in enumerate(target_offenses):
		plt.plot(year_list, counts[index], color=colors[index], marker= 'o', label=offense)
	ax.get_xaxis().get_major_formatter().set_useOffset(False)	
	plt.xlabel('Year')
	plt.ylabel('Number of offenses')
	plt.legend()
	plt.savefig(filename,format="png")
	plt.show()

### Main execution script ###
crime_file_name = '/Users/jjw036/ChicagoCrime/crimes_2001_to_present_parsed.csv'
data_list = read_data(crime_file_name)

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

### Section 2 specifics: ###
organized_cases = organize_cases_by_offense(case_list)
offense_list = get_unique_offenses(case_list)
print(offense_list)
offense_count = count_offenses(organized_cases)

#Let's organize offenses by year, and then by type.

year_list = [2010,2011,2012,2013,2014]

offense_count_for_each_year = []
for year in year_list:
	yearly_case_list = get_cases_by_year(case_list,year)
	yearly_organized_cases = organize_cases_by_offense(yearly_case_list)
	yearly_offense_count = count_offenses(yearly_organized_cases)
	offense_count_for_each_year.append(yearly_offense_count)

# Our top offenses seem to be burglary, criminal damage, narcotics, battery, and theft.
# Let's get the average and standard deviation and count for BURGLARY, CRIMINAL DAMAGE, NARCOTICS, BATTERY, and THEFT for each year
target_offenses = ["BURGLARY","CRIMINAL DAMAGE", "NARCOTICS", "BATTERY", "THEFT"]
means_offenses = []
stdev_offenses = []
counts_offenses = []

for offense in target_offenses:
	mean, stdev, counts = get_stats(offense_count_for_each_year, offense)
	means_offenses.append(mean)
	stdev_offenses.append(stdev)
	counts_offenses.append(counts)
	
# Plotting the top 5 categories as bar graphs
save_bar_file = "top_crimes_bar.png"
plot_bar_graph(target_offenses,means_offenses,stdev_offenses,save_bar_file)

# 3. How have the top 5 offenses changed over time?  
save_line_file = "top_crimes_line.png"
plot_line_graph(target_offenses, counts_offenses,year_list,save_line_file)

# 3a. Can we predict the number of occurrences that may happen in 2015? Modeling the trends using linear regression

year_list = list(map(int,year_list))
target_year = 2015
for index,offense in enumerate(target_offenses):
	predicted, parameters = predict_occurrences(year_list,counts_offenses[index], target_year)
	print("For the year " + str(target_year) + ", " + offense + " is predicted to have " + str(predicted) + " occurrences.")
	# y = mx + b