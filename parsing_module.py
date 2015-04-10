def read_data(filename):
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