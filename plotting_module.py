# pyplot module import
import matplotlib.pyplot as plt
# basemap import
from mpl_toolkits.basemap import Basemap
# Numpy import
import numpy as np


def plot_bar_graph(target_offenses, means_offenses, stdev_offenses, filename):
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

### Optional Method for project extension 1 ###
def plot_correlation_graph(temps, offense_counts,label, filename):
	#this is to demonstrate line graphs but the data is categorical so you should actually be using bar graphs
	fig, ax = plt.subplots()


	plt.scatter(temps, offense_counts, color="blue", marker= 'o', label=label)
	
	plt.xlabel('Temperature (Celsius)')
	plt.ylabel('Number of offenses')
	plt.legend()
	plt.savefig(filename,format="png")
	plt.show()

### Optional Method for project extension 2 ###

def plot_crime_map(offense_list, filename):
	""" Plots all the locations of a given offense list. Saves the figure.
	"""
	lons = []
	lats = []
	# get list of longitudes
	# get list of latitudes
	for offense in offense_list:
		if offense['Latitude'] and offense['Longitude']:
			lats.append(float(offense['Latitude']))
			lons.append(float(offense['Longitude']))

	m = Basemap(llcrnrlon=-88.03512, llcrnrlat=41.62194, urcrnrlon=-87.49499, urcrnrlat=42.15477, projection='lcc', lat_1=33, lat_2=45, lon_0=-95, resolution='h', area_thresh=10000)
	m.drawmapboundary()
	m.drawcoastlines()
	m.fillcontinents()
	m.readshapefile('/Users/jjw036/ChicagoCrime/shapes/CTA_RailLines','CTA')
	m.readshapefile('/Users/jjw036/ChicagoCrime/shapes/Neighborhoods','neighborhoods')

	x,y =m(lons, lats)
	m.plot(x,y,'bo', markersize=2)
	plt.savefig(filename,format="png")

	plt.show()


	