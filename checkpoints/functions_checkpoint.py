import statistics

#Let's ask a few questions of our data.
#1. How much crime has occurred in Chicago since 2010?
#2. What are the top 5 most frequent offenses?
#3. How much do those contribute to the total crime each year?

#The first question should follow directly from where we left off
def read_data(file_name):
	"""Functions should have docstrings explaining their use succinctly."""
	file_object = open(file_name,"r")
	file_data = file_object.readlines()
	header_list = file_data.pop(0).strip().split(",")
	data_list = []
	for data in file_data:
		data_list.append(data.strip().split(","))
	return((header_list,data_list))

case_list = []
for i in range(6):
	headers, cases = read_data("./crimes_201"+str(i)+".csv")
	for case in cases:
		case = dict(zip(headers,case))
		case_list.append(case)

#The length of the case_list should be the total number of crimes committed:
total_crimes = len(case_list)

#Onward! We'll need a few things for question 2.
#A list of offenses that can occur.
#Some sort of array that organizes case_list by offense
#Counts for each offense
#A sorted version of that array so we can pick the top 5.
#We'll start at the beginning, finding the complete set of offenses:
def get_unique_offenses(case_list):
	"""Returns an exhaustive set of offenses from a list of dictionaries"""
	unique_offenses = []
	for case in case_list:
		offense = case["Primary Type"]
		if offense not in unique_offenses:
			unique_offenses.append(offense)
	return(unique_offenses)

#Excellent, now we need to organize case_list into another array by offense type
def get_organized_cases_offense(case_list):
	"""Returns a dictionary of lists of dictionaries given a list of dictionaries"""
	unique_offenses = get_unique_offenses(case_list) #See how easy that was!
	#First we'll create a shell of this dictionary
	offense_dictionary = {}
	for offense in unique_offenses:
		offense_dictionary[offense] = []

	#Then will the shell with crime-flavored filling!
	for case in case_list:
		offense = case["Primary Type"]
		offense_dictionary[offense].append(case)
	return(offense_dictionary)

#Now, we need to find out what offenses are the top 5. To do this, let's simplify
#our data a little bit. All we really need are the offenses, and the number associated right?
def count_offenses(offense_dictionary):
	"""Returns a list of tuples with a category and the size of that category"""
	offenses = offense_dictionary.keys()
	numbers_list = []
	for offense, offense_list in offense_dictionary.items():
		numbers_list.append((offense,len(offense_list)))
	return(numbers_list)

#Once we have our list of offenses and their totals since 2010 we can sort that list by
#the number associated with that offense. We didn't cover sorting before, but Python handles
#this internally.
random = [2,5,1,-3,5,0]
print(sorted(random))
print(sorted(random,reverse=True))
random_tuples = [(2,1),(3,-4),(0,1),(7,3),(-5,0),(0,9)]
print(sorted(random_tuples))
#We'll need a way to pick that second part of the tuple!
def my_key(random_tuple):
	"""Returns the second element in a two-count tuple"""
	return(random_tuple[1])
#Perfect
print(sorted(random_tuples, key=my_key))

sorted_offense_list = sorted(count_offenses(get_organized_cases_offense(case_list)))
print(sorted_offense_list[:5])

#Finallly, we'll need to separately organize these crimes by year, and then offense if we
#want to see the contribution of each 'major' offense to the total each year.

def get_organized_cases_year(case_list):
	"""Returns a dictionary of dictionaries given a list of dictionaries"""
	#First we'll create a shell of this dictionary
	year_dictionary = {2010:[],2011:[],2012:[],2013:[],2014:[],2015:[]}
	#Then will the shell with crime-flavored filling!
	for case in case_list:
		year = int(case["Year"])
		year_dictionary[year].append(case)
	#Let's also simplify our efforts, we'll need to get the result of count_offenses()
	#for each year as well:
	for year in year_dictionary.keys():
		offenses = get_organized_cases_offense(year_dictionary[year])
		numbers = count_offenses(offenses)
		year_dictionary[year] = dict(sorted(numbers, key=my_key))
	return(year_dictionary)

years_of_crime = get_organized_cases_year(case_list)
print(years_of_crime[2010])
#Now that we have the year_dictionary, let's get some statistics.
#Let's say we want the percent of crimes that were BURGLARY in each year:

def get_stats(dictionary_list, target_offense):
	"""Returns useful statistics (mean, stdev, contribution) for a target offense"""
	values = []
	contributions = []
	for year, offenses in dictionary_list.items():
		total_offenses = sum(offenses.values())
		offense_list = offenses.keys()
		if offense in offense_list:
			value = offenses[target_offense]
			values.append(value)
			contributions.append(float(value)/float(total_offenses))
		else:
			values.append(0.0)
			contributions.append(0.0)
	mean = statistics.mean(values)
	stdev = statistics.stdev(values)
	return([mean,stdev,contributions])

unique_offenses = get_unique_offenses(case_list)
print(unique_offenses)
for offense in unique_offenses:
	stats = get_stats(years_of_crime,offense)
	mean, stdev, conts = stats
	print(offense, mean, stdev, conts)
