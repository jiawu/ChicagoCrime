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

	### Section 2 specifics: ###
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
	
### "MAIN" section

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