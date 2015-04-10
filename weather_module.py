import statistics
from scipy import stats

def calculate_temp_summary_by_month(weather_list, month, year):
	""" Returns mean , standard deviation, and list of values of the temperature (Celsius) of a given month and year.
	"""
	values_list = []
	for report in weather_list:
		if report['Month'] == month and int(report['Year']) == int(year):
			values_list.append(float(report['MaxTemp'])*0.1 )
	mean = statistics.mean(values_list)
	stdev = statistics.stdev(values_list)
	return(mean,stdev,values_list)