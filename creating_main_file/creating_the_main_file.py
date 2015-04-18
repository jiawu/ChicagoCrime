'''The basic overview of our project execution is in three parts
	1. Read file inputs
	2. Analyze the imported data
	3. Plot outcomes of our analysis

	We will therefore make 3 modules to assisst in the organization of this
	project
'''
# Make a file called "main.py"
''' There will be 4 main sections of this project '''

# 1. Import statements. In python, these are almost always at the top
	# We'll add to this as we make our modules
from parsing_module import read_data
import analysis_module as am
import plotting_module as pm

# 2. Data input section. We will read the files and parse data here

case_list = []
for i in range(6):
    headers, cases = read_data("./crimes_201"+str(i)+".csv")
    for case in cases:
        case = dict(zip(headers,case))
        case_list.append(case)

total_crimes = len(case_list)

# 3. Data analysis section
unique_offenses = am.get_unique_offenses(case_list)

# Sort the offenses
sorted_offense_list = sorted(am.count_offenses(am.get_organized_cases_offense(case_list)), key=am.my_key)

years_of_crime = am.get_organized_cases_year(case_list)

for offense in unique_offenses:
    stats = am.get_stats(years_of_crime,offense)
    mean, stdev, conts = stats
    #print(offense, mean, stdev, conts)

# 4. Data output and plotting section
target_offenses = sorted_offense_list[-5:]

# we know out top 5
print(target_offenses)

# re-use the same logic from earlier
means_offenses = []
stdev_offenses = []
name_offenses = []
cont_offenses = []

for offense, _ in target_offenses:
    my_stats = am.get_stats(years_of_crime, offense)
    mean, stdev, cont = my_stats
    name_offenses.append(offense)
    means_offenses.append(mean)
    stdev_offenses.append(stdev)
    cont_offenses.append(cont) 

save_bar_file = "top_crimes_bar.png"
pm.plot_bar_graph(target_offenses,means_offenses,stdev_offenses, name_offenses, save_bar_file)
'''May need to add name_offenses to the arguments'''

year_list = list(years_of_crime.keys())

save_line_file = "top_crimes_line.png"
pm.plot_line_graph(name_offenses, cont_offenses, year_list, save_line_file)

''' Lastly, predicting future occurrences seems like it should be in the 
analysis module. Let's put it there'''

target_year = 2015

for index,offense in enumerate(name_offenses):
    predicted, parameters = am.predict_occurrences(year_list[:-1],cont_offenses[index][:-1], target_year)
    print("For the year " + str(target_year) + ", " + offense + " is predicted to contribute " + str(predicted) + " percent.")
    # y = mx + b

''' If we compare this to the original project script, it is much more easily 
understood. Each section carries out a specific task and is supported by a
module of functions. These could easily be reused in a different project.
Overall our project is easier to read and therefore easier to debug! '''


