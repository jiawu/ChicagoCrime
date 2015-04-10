import statistics
from scipy import stats

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

def get_cases_by_year(case_list, desired_year=2015):
	"""Return the list of relevant cases, given a list of case dicts and the target year"""
	relevant_cases = []
	for case in case_list:
		case_year = int(case['Year'])
		if case_year == desired_year:
			relevant_cases.append(case)
	return(relevant_cases)


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

#let's count the number of cases for each offense
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

def predict_occurrences(year_list,counts_per_year, target_year):
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

### Optional function for project extension 1 ###
def get_crime_summary_by_month(organized_case_dict, month, year):
	"""Returns for each category, the number of occurrences at a given month/year
	"""
	overall = []
	monthly_organized_case_dict = {}
	for key in organized_case_dict.keys():
		cases = []
		for case in organized_case_dict[key]:
			if case['Month'] == month and int(case['Year']) == int(year):
				cases.append(case)
				overall.append(case)				
		monthly_organized_case_dict[key] = cases
	monthly_tuples = count_offenses(monthly_organized_case_dict)
	crime_n = len(overall)
	return(monthly_tuples, crime_n)
