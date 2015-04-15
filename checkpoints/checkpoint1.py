crime_file_name = '/Users/jjw036/ChicagoCrime/crimes_2001_to_present_parsed.csv'
file_object = open(filename, 'r')

#read the file line-by-line
data_list = []
for line in file_object:
	#get rid of \n newspace
	new_line = line.strip()
	data_list.append(new_line)

#first line is the header, remove that from the data and save it
data_header = data_list.pop(0)

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

	

#Writing your first function:
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
	
data_list = read_data(crime_file_name)