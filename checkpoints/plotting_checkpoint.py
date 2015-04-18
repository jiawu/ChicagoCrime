
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

sorted_offense_list = sorted(count_offenses(get_organized_cases_offense(case_list)), key=my_key)
print(sorted_offense_list[-5:])


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
import statistics

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
            contributions.append(float(value)/float(total_offenses)*100)
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

################################ things I need, in case ############################################

target_offenses = sorted_offense_list[-5:]

############################################################################

# test imports

import numpy as np
import matplotlib.pyplot as plt
from scipy import stats

# target_offenses is the list of top 5 offenses
# plot average contribution to total crime per year for the top 5 offenses
# for bar plot - we need data, std dev, x-labels

################this could be done earlier#############################

# we know out top 5
print(target_offenses)

# re-use the same logic from earlier
means_offenses = []
stdev_offenses = []
name_offenses = []
cont_offenses = []

for offense, _ in target_offenses:
    my_stats = get_stats(years_of_crime, offense)
    mean, stdev, cont = my_stats
    name_offenses.append(offense)
    means_offenses.append(mean)
    stdev_offenses.append(stdev)
    cont_offenses.append(cont) 

#################################################################################

# so now we have:

# already have x-axis labels = name_offenses
print(name_offenses)

# plot data = means_offenses
print(means_offenses)

# error bars = stdev_offenses
print(stdev_offenses)

# file name for plot?
save_bar_file = "top_crimes_bar.png"

# We haven't seen this before - let's check - docs tell us it's position on x-axis of left side of bar
print(np.arange(len(name_offenses)))

# We need some logic to ensure our labels line up with the tick marks
bar_width = 0.8
print(np.arange(bar_width/2, len(name_offenses)))

#We'll make this a function
def plot_bar_graph(target_offenses, means_offenses, stdev_offenses, filename):
    """Plots and saves a bar graph"""   
    bar_width = 0.8
    index = np.arange(len(name_offenses))
    plt.bar(index, means_offenses, width=bar_width, yerr=stdev_offenses)

    plt.xlabel('Offenses')
    plt.ylabel('Average Occurences Per Year')
    plt.title('Average Occurrences Per Year 2010-Present')
    plt.xticks(np.arange(bar_width/2, len(name_offenses)), name_offenses)
    
    plt.savefig(filename,format="png")
    plt.show()
    
    
# Try running it
plot_bar_graph(target_offenses,means_offenses,stdev_offenses,save_bar_file)

# 3. How has the contribution of the top 5 offenses to overall crime changed over time?  
# Use a line plot
# we have all the data we need except the years - list(view()) - new python3
year_list = list(years_of_crime.keys())
print(year_list)

# we'll be plotting our yearly contributions, let's just inspect that data 
print(cont_offenses)

def plot_line_graph(target_offenses, conts, year_list, filename):
    """Plots and saves a line graph """
    # each line should be a different color
    colors = ["blue","red","orange","green","yellow","purple"]
    
    #add each line's data to plot
    for index,offense in enumerate(target_offenses):
        plt.plot(year_list, conts[index], color=colors[index], marker= 'o', label=offense)
    
    # turn off scientific notation/formatting in general for x-axis 
    ax = plt.gca()
    ax.get_xaxis().get_major_formatter().set_useOffset(False)    
    
    plt.xlabel('Year')
    plt.ylabel('Percent contribution')
    plt.legend()
    
    plt.savefig(filename,format="png")
    plt.show()



save_line_file = "top_crimes_line.png"
plot_line_graph(name_offenses, cont_offenses, year_list, save_line_file)

# 3a. Can we predict the contribution for these crimes that may happen by then end 2015? Modeling the trends using linear regression

from scipy import stats

target_year = 2015

def predict_occurrences(year_list,cont_per_year, target_year):
    """Returns the predicted number of offenses for a given year and the parameters for the linear regression used to fit"""
    slope, intercept, r_value, p_value, std_err = stats.linregress(year_list, cont_per_year)
    # y = mx + b
    predicted = slope * int(target_year) + intercept
    parameters = {  "slope": slope,
                    "intercept": intercept,
                    "r_value": r_value,
                    "p_value": p_value,
                    "std_error": std_err
    }
    return(predicted,parameters)

for index,offense in enumerate(name_offenses):
    predicted, parameters = predict_occurrences(year_list[:-1],cont_offenses[index][:-1], target_year)
    print("For the year " + str(target_year) + ", " + offense + " is predicted to contribute " + str(predicted) + " percent.")
    # y = mx + b