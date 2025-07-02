"""
Anaya Ahaontu
18 June 2025
Creates the graphs to display on the budget calculator
"""

#import needed modules
import tkinter as tk
import numpy as np
import pandas as pd
import matplotlib.pyplot as mpl
import sys
import math
import datetime
from datetime import datetime as dt 

sys.path.append('/Users/anayaahanotu/Documents/Coding/GitHub/')

from Special_tkinter_objects import tkinterPlus2 as tk2
from other_python_docs import quick_math_operations as math2


#just to test
root = tk.Tk()
root['bg'] = 'white'


class Graphing (tk.Canvas):
    '''Make a Frame to display the different graphs'''
    
    def __init__(self, master, **kwargs):
        '''GraphFrame(args, kwargs):\n
            master: Tkinter.Frame() or Tkinter.Tk()\n
            **kwargs: tkinter.Canvas parameters -- NOT 'bg'
        '''

        if "bg" in kwargs: del kwargs["bg"] #make sure bg is not added twice

        tk.Canvas.__init__(self, master, bg='white', **kwargs) #initialize self

        #give the list of modes and set the mode
        self.charts = ['Bar Chart', 'Line plot', 'Scatter plot', 'Pie Chart']
        self.type = self.charts[0]

        #keep track of the lowest and highest x and y values plotted
        self.xLow = None
        self.xHigh = None
        self.yLow = None
        self.yHigh = None
    
    def switch_graph(self, graphType):
        '''GraphFrame.switch_graph(graphType)
        graphType: any literal in [timeline chart, bar chart, or pie chart]
        switches the graph to be displayed
        '''
        
        pass
    
    def create_graph(self, independant, dependant):
        '''GraphFrame.create_graph(graphType)
        independant: seq: x-axis values
        dependant: seq: numeric: y-axis values
        '''
        
        pass

    def make_scatterplot(self, independant, dependant, xName='', yName='',
                          title='', xAreDates=False, treatAsText =False, 
                          treatAsRange=False, timespan='1.W', pointSize=10,
                          pointColor='black'
    ):
        '''
        GraphFrame.make_scaterplot(independant, dependant, ..., pointColor='black'): void
        independant: seq: x-axis values
        dependant: numeric seq: y-axis values
        xName: str: x-axis label
        yName: str: y-axis label
        title: str: title of graph
        xAreDates: boolean: whether or not you want to look at the x axis data as a date
        treatAsText: boolean: treat all data as text, not as dates
        timespan: str: format: "<num units>.<units>"
                units: 'W' -> week, 'M' -> month (30 days), 'Y' -> year (12 months)
        pointSize: int or float: size of the point wanted (default: 10)
        pointColor: str: color of point wanted (default: 'black')
            
        '''
       
    def make_bar_graph(self, independant, dependant, xName="", yName="",
                       title="", makeHistogram=False, fillColor="black"):
        pass
    def make_line_chart(self, independant, dependant, xName='', yName='',
                          title='', xAreDates=False, treatAsText =False, 
                          treatAsRange=False, timespan='1.W', pointSize=10,
                          lineWidth=5, pointColor='black', lineColor="black"):
        pass
    def make_pie_chart(self, independant, dependant, colorcode=[]):
        pass
    def convert_to_datetime(self, dates):
        '''
        GraphFrame.convert_to_datetime(dates)
        dates: seq: str: valid dates separated by '/'
            dates must be in month/day/YYYY format
            Warning: if not in YYYY format, your dates may be off
        converts all the dates in the sequence to datetime format
        returns list: datetime.dates
        '''
        #store the dates in a new format and save it to variable
        tempIndependant = []
        for element in dates:
            #split it into a list so we can work with each unit at a time
            element = element.split("/")

            for unit in range(2):
                #make sure the month and day are in MM and DD format
                element[unit] = element[unit].zfill(2)
            
            #make sure year is in YYYY format
            element[2] = element[2].zfill(4)

            #put the properly formatted months and dates into a new string
            tempDate = "{}/{}/{}".format(*element)

            #set the format for the dates
            format = "%m/%d/%Y"

            #make the newdate in date time format
            newDate = dt.strptime(tempDate, format)

            #add it to the list of dates
            tempIndependant.append(newDate.date())

        return tempIndependant

    def show_info(self, data):

        # create an info bar on the point's 
        self.infoBar = self.create_text(
            self.winfo_width()/2,
            self.winfo_height() - 30,
            text=data,
            font=('Georgia', 15),
            fill='black'
        )

    def hide_info(self):
        self.delete(self.infoBar)

    def clean_data(self, independant, dependant):
        '''
        GraphFrame.clean_data(independant, dependant)
        independant: seq: x-axis values
        dependant: seq: y-axis values
        cleans the data by filtering out None types and null
        returns DataFrame: {'x': independant, 'y': dependant}
        '''

        data = pd.DataFrame({'x': independant, 'y': dependant})

        return data.dropna()

#### test  ####

test = Graphing(
    root,
    width = 850,
    height = 800
)

test.pack(fill='both', expand=1)
root.update()

x = np.array([
    '2/24/2023',
    '3/23/2021', 
    '2/19/1996',
    '2/17/2006',
    '9/23/1992',
    '2/9/1907',
    '3/9/2007',
    '2/8/2024',
    '9/3/2001',
    '2/3/2007'
])

x2 = np.array ([51, 85, 90, 93, -62, -25, 30, 75, 32, 53, 35])

y = np.array([-7532, 8493, -1254, 6789, -4321, 9876, -2109, 5634, -8765, 4320])
y2 = np.array([32, 93, -94, -33, 93, -29, -93, 49, 23, 94, 23])


x3 = np.array(list(((value / 1000) for value in range(-20000, 20000))))
y3 = []

y3 = list(x - math.sin(x) for x in x3)
y3.extend(list(1 - x * math.cos(x) - math.sin(x) for x in x3))


x3 = np.concatenate((x3, x3))

y3 = np.array(y3)


cleanedData = test.clean_data(x3, y3)

x3 = np.array(cleanedData['x'])
y3 = np.array(cleanedData['y'])

x4=[2]
y4=[5]

test.make_scatterplot(
    x4, y4,
    'X',
    'Y',
    'X Versus Y', 
    pointSize=3,
    pointColor='black',
    treatAsRange=True
)



root.mainloop()
