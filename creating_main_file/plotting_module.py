import matplotlib.pyplot as plt
import numpy as np

def plot_bar_graph(target_offenses, means_offenses, stdev_offenses, name_offenses, filename):
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