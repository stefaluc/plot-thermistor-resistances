#! /usr/bin/env python2.7
import numpy as np
from dateutil.parser import parse
import datetime, csv, matplotlib
import matplotlib.pyplot as plt

matplotlib.rc('font', family='Arial') # For displaying the sigma unicode
# Sequence to display plots in
color_sequence = [('blue','grey'),
                  ('grey','blue'),
                  ('green','yellow'),
                  ('yellow','green'),
                  ('black','white'),
                  ('white','black'),
                  ('red','black'),
                  ('black','red')]

# Temperatures of corresponding colors
color_temps = {
    'grey': 360,
    'red': 337,
    'green': 323,
    'yellow': 288,
    'blue': 254,
    'white': 233,
    'black': 222
}

# Graph resistances over time for each CAL%d.csv file
for idx,color in enumerate(color_sequence, start=1):
    times = []
    resvals = [[]*8 for i in xrange(8)]
    # Extract time and resistances data from .csv file
    with open('./cals/CAL0%d.csv' % idx, 'rb') as fp:
        reader = csv.reader(fp)
        for row in reader:
            # Time values
            times.append(row[0])
            # Resistance values for channels 0-3
            resvals[0].append(row[4]); resvals[1].append(row[9]); resvals[2].append(row[14]); resvals[3].append(row[19])
            # Resistance values for channels 4-7
            resvals[4].append(row[24]); resvals[5].append(row[29]); resvals[6].append(row[34]); resvals[7].append(row[39])

    # Parse time to datetime objects
    for i,time in enumerate(times):
        times[i] = parse(time)

    # Calculate standard deviation
    resvals = np.array(resvals) # Convert to numpy array
    resvals = resvals.astype(float) # Convert values from string to float

    # Calculate standard deviations for each CAL
    sigma=[]
    for chan in resvals:
        sigma.append(np.std(chan))
    
    # Begin plotting values
    # Instantiate matplotlib figure
    fig = plt.figure() 
    # Add subplots
    ax1 = fig.add_subplot(211)
    ax2 = fig.add_subplot(212, sharex=ax1)
    # Add plotting styles
    linestyles = [':','--','-',':']
    markers = ['^','x','s','o']
    # Plot data for channels 0-3
    for i,marker in enumerate(markers):
        ax1.plot(times, resvals[i], marker=marker)
    # Plot data for channels 4-7
    for i,marker in enumerate(markers, start=4):
        ax2.plot(times, resvals[i], marker=marker)
    # Label axises
    ax1.set_xlabel('Time'); ax2.set_xlabel('Time')
    ax1.set_ylabel('Resistance (Ohms)'); ax2.set_ylabel('Resistance (Ohms)')
    # Remove scientific notation from y-label
    y_formatter = matplotlib.ticker.ScalarFormatter(useOffset=False)
    ax1.yaxis.set_major_formatter(y_formatter)
    ax2.yaxis.set_major_formatter(y_formatter)
    # Title graph
    fig.suptitle('CAL0%d Resistances Over Time' % idx, fontsize=20, fontweight='bold')
    ax1.set_title('%s Channels 0-3 (%dK)' % (color[0].capitalize(), color_temps[color[0]]), fontsize=14)
    ax2.set_title('%s Channels 4-7 (%dK)' % (color[1].capitalize(), color_temps[color[1]]), fontsize=14)
    # Add legend
    channels = ['Channel 0\n'+u'\u03C3 = %.2f' % sigma[0], 'Channel 1\n'+u'\u03C3 = %.2f' % sigma[1], 
                'Channel 2\n'+u'\u03C3 = %.2f' % sigma[2], 'Channel 3\n'+u'\u03C3 = %.2f' % sigma[3],
                'Channel 4\n'+u'\u03C3 = %.2f' % sigma[4], 'Channel 5\n'+u'\u03C3 = %.2f' % sigma[5], 
                'Channel 6\n'+u'\u03C3 = %.2f' % sigma[6], 'Channel 7\n'+u'\u03C3 = %.2f' % sigma[7]]
    ax1.legend(channels[:4]);ax2.legend(channels[4:])
    # Size plots
    fig = matplotlib.pyplot.gcf()
    fig.set_size_inches(18.5, 10.5)
    # Save figure to ./plots/
    plt.savefig('./plots/CAL%d.png' % idx, bbox_inches='tight')
