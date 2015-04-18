import statistics
from scipy import stats

def get_unique_offenses(case_list):
    """Returns an exhaustive set of offenses from a list of dictionaries"""
    unique_offenses = []
    for case in case_list:
        offense = case["Primary Type"]
        if offense not in unique_offenses:
            unique_offenses.append(offense)
    return(unique_offenses)

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

def count_offenses(offense_dictionary):
    """Returns a list of tuples with a category and the size of that category"""
    offenses = offense_dictionary.keys()
    numbers_list = []
    for offense, offense_list in offense_dictionary.items():
        numbers_list.append((offense,len(offense_list)))
    return(numbers_list)

def my_key(random_tuple):
    """Returns the second element in a two-count tuple"""
    return(random_tuple[1])

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

def get_stats(dictionary_list, target_offense):
    """Returns useful statistics (mean, stdev, contribution) for a target offense"""
    values = []
    contributions = []
    for year, offenses in dictionary_list.items():
        total_offenses = sum(offenses.values())
        offense_list = offenses.keys()
        if target_offense in offense_list:
            value = offenses[target_offense]
            values.append(value)
            contributions.append(float(value)/float(total_offenses)*100)
        else:
            values.append(0.0)
            contributions.append(0.0)
    mean = statistics.mean(values)
    stdev = statistics.stdev(values)
    return([mean,stdev,contributions])

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