import tkinter as tk
import numpy as np
import pandas as pd
import sys
import math
sys.path.append( '/Users/anayaahanotu/Documents/Coding/GitHub/')

from Special_tkinter_objects import tkinterPlus2 as tk2

from other_python_docs import quick_math_operations as math2
import datetime
from datetime import datetime as dt 

root = tk.Tk()
root['bg'] = 'white'


class GraphFrame (tk.Canvas):
    '''Make a Frame to display the different graphs'''
    
    def __init__(self, master, kwargs={}):
        '''GraphFrame(args, kwargs):
            master: Budget calculator
            kwargs: dictionary: tkinter.Canvas parameters -- NOT 'bg'
        '''
        
        tk.Canvas.__init__(self, master, bg='white', **kwargs)

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

    def create_line_axis(self, independant, dependant, xName='', yName='', title='', xAreDates=False, treatAsText =False, treatAsRange=False, timespan='1.W'):
        '''
        GraphFrame.create_line_axis(independant, dependant, ..., timespan = '1.W'): void
        
        independant: seq: x-axis values
        dependant: numeric seq: y-axis values
        xName: str: x-axis label
        yName: str: y-axis label
        title: str: title of graph
        xAreDates: boolean: whether or not you want to look at the x axis data as a date
        treatAsText: boolean: treat x data as text, not as dates or numeric
        treatAsRange: boolean: treat x data as numeric
        timespan: str: format: "<num units>.<units>"
                units: 'W' -> week, 'M' -> month (30 days), 'Y' -> year (12 months)
        '''

        def treat_as_range(x):
            """
            treat_as_range(x, y)
            x: numeric seq: data for independant variable
            labels the x axis
            treats x axis data as a range, and splits the range of the x axis into equal segments
            used to make the scatterplot look cleaner
            """
            #make sure the data is in proper order

            #everything i did to y i also do to x now
            #set x range
            xValues = x

            #if there is a decimal range between the xvalues, convert the min and max values to integers
            #convert min to integer using int() function
            #convert max to intefer using math.ceil() function to ceiling the maximum
            #an easier way to approach this would be to celieng the difference of the maximum and minimum
            #may do the above

            xValues = list(float(value) for value in xValues)

            if (max(xValues) - min(xValues)) % 1 != 0:
                xHigh = math.ceil(max(xValues))
                xLow = math.floor(min(xValues))
            else:
                xHigh = max(xValues)
                xLow = min(xValues)

            #save the xHigh and the xLow to the class
            self.xHigh, self.xLow = xHigh, xLow
            
            #try to find the cleanest split of the x values... goal is to have 10 increments
            #first, find how many values go in between the highest and lowest values
            xSplit = math2.factors(xHigh - xLow)

            #now, just get all the values in order
            xSplit = list(
                factor[0] for factor in xSplit
            )
            # add distance each number is from 10 to the list
            xSplit.extend(
                list(
                    abs(10-value) for value in xSplit
                )
            )

            #xSplit is in two parts: the factors of the range of the x values and the distance of the factors from 10
            #we look at the second half with the distance from ten -- index that value in the list
            #the target xSplit will be halfway across the list, so the value indexed halfway across the list is our xSplit
            xSplit = xSplit[
                xSplit.index(
                    min(
                        xSplit[(len(xSplit)//2):]
                    )
                ) - (len(xSplit) // 2)
            ]

            #draw the lines
            #should start at x = 100 and split evenly until it hits the length of the x axis (though shuold not be on the y axis)

            divisionWidth = (length - 120)/xSplit


            for x in range(xSplit + 1):
                xPoint = 120 + divisionWidth * x

                self.create_line(
                    xPoint,
                    height - 1,
                    xPoint, 
                    100,
                    fill='light grey',
                    width=1
                )

                self.create_text(
                    xPoint,
                    height + 10,
                    fill='black',
                    font=('Georgia', 10),
                    text= int(xLow + x * ((xHigh - xLow)/xSplit)) # writing from left to right so its min + interval
                )

            

            return yHigh, yLow, xHigh, xLow

        def treat_as_text(x):
            '''
            treat_as_variables(x)
            x: seq: values of the independant variables
            creates an x axis and labels each value on the x axis
            '''

        def treat_as_dates(x, timespan):
            '''
            treat_as_dates(x, timespan)
            x: seq or Strings: dates: format: mm/dd/yyyy
            timespan: str: format: "<num units>.<units>"
                units: 'W' -> week, 'M' -> month (30 days), 'Y' -> year (12 months)
            '''
    
    def make_scatterplot(
            self, independant, dependant, xName='', yName='', title='', xAreDates=False,
            treatAsText =False, treatAsRange=False, timespan='1.W', pointSize=10, pointColor='black'
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
       
    def make_bar_graph(self):
        pass
    def make_line_chart(self):
        pass
    def make_pie_chart(self):
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
        #store the dates in a new format

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

test = GraphFrame(
    root,
    kwargs = {
        'width': 850,
        'height': 800
    }
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
