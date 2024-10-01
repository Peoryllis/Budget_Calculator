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
        self.types = ['Bar Chart', 'Line plot', 'Scatter plot', 'Pie Chart']
        self.type = self.types[0]

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
            xSplit = len(x) #figure out how many columns to make
            xValues = x

            
            
            #save the first and last index of the xValues to the class' xHigh and xLow variables
            self.xHigh, self.xLow = None, None

            #I used xSplit - 1 to have it go through all of the x axis
            divisionWidth = (length-120)/(xSplit - 1)

            #draw the lines
            #should start at x = 120 and split evenly until it hits the length of the x axis (though shuold not be on the y axis)

            for x in range(xSplit):
                xPoint = 120 + x * divisionWidth

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
                    text= xValues[x]
                 ) # writing from left to right so its min + interval

        def treat_as_dates(x, timespan):
            '''
            treat_as_dates(x, timespan)
            x: seq or Strings: dates: format: mm/dd/yyyy
            timespan: str: format: "<num units>.<units>"
                units: 'W' -> week, 'M' -> month (30 days), 'Y' -> year (12 months)
            '''
            #convert to datetime format
            xValues = self.convert_to_datetime(x)

            #Split up number of units and the units as a list so it can be easily referred
            timespan = timespan.split('.')
            timespan[0] = int(timespan[0])

            mostRecentDay = max(xValues)

            #if timespan has 'W' or 'M', make a range from the latest data to data up to 
            # x weeks or x months older. Up to 10 increments.

            #make the axis for number of weeks
            #calculate the number of days to be recorded
            if timespan[1] == 'W':
                numDays = 7 * (int(timespan[0]))
                        
            elif timespan[1] == 'M':
                numDays = 30 * (int(timespan[0]))

            elif timespan[1] == 'Y':
                numDays = 365 * (int(timespan[0]))


            #keep track of all the days to be written. Start with the latest da
            allDays = [mostRecentDay] 

            #for numDays number of intervals,
            #add a date that is one day behind the last day in the list
            for day in range(numDays):
                    #make sure the day is within the data
                    newDay =  allDays[-1] + datetime.timedelta(days=-1)
                    
                    if newDay >= min(xValues):
                        allDays.append(newDay)
            
            #this range of days will be our new X values
            xValues = allDays

            if (timespan[1] == 'W' and timespan[0] < 24) or (timespan[1] == 'M' and timespan[0] < 6):
                #figure out the length of xValues
                xInterval = list(nums [0] for nums in math2.factors(len(xValues)))

                #figure out the distance from each value is from 10

                distanceFromTen = list(
                    abs(10 - num) for num in xInterval
                )

                #put the x values in proper order

                #the value closest to ten at xSplit is indexed at the same location
                #as the lowest value in distanceFromTen

                xInterval = xInterval[distanceFromTen.index(min(distanceFromTen))]

                #our interval will be the quotient of (the length of xValues) and (the xInterval closest to ten)

                xInterval = int(len(xValues)/xInterval)

                #split the xValues into ten evenly spaced increments
                xValues = xValues[::xInterval]
                xValues.append(allDays[-1]) 

                #put the xvalues in chronilogical order
                xValues = xValues [::-1]

                #save the highest and lowest x values to this class maximum and minimum values
                self.xHigh, self.xLow = xValues[-1], xValues[0]

                #convert the text to mm/dd/YYYY format

                oldXValues = xValues
                xValues = []

                for value in oldXValues:
                    intervalText = str(value).split('-')
                    intervalText = [intervalText[1], intervalText[-1], intervalText[0]]
                    intervalText = '{}/{}/{}'.format(*intervalText)

                    xValues.append(intervalText)



            else:
                #get a sense of all the months

                MONTHS_OF_THE_YEAR = [
                    'Jan',
                    'Feb',
                    'Mar',
                    'Apr',
                    'May',
                    'Jun',
                    'Jul',
                    'Aug',
                    'Sep',
                    'Oct',
                    'Nov',
                    'Dec'
                ]

                xValues = list(
                    value for value in xValues if value.day == 1
                )

                if xValues[-1].month > allDays[-1].month:

                    xValues.append(datetime.date(allDays[-1].year, allDays[-1]. month, 1))

                originalValues = xValues
                
                #figure out all the factors of xValues

                xInterval = list(nums [0] for nums in math2.factors(len(xValues)))
                #figure out the distance from each value is from 10

                distanceFromTen = list(
                    abs(10 - num) for num in xInterval
                )
                #the value closest to ten at xSplit is indexed at the same location
                #as the lowest value in distanceFromTen

                xInterval = xInterval[distanceFromTen.index(min(distanceFromTen))]

                #our interval will be the quotient of (the length of xValues) and (the xInterval closest to ten)

                xInterval = int(len(xValues)/xInterval)
                
                if xInterval != len(xValues):
                    xValues = xValues[::xInterval]
                else:
                    xValues = [xValues[0], xValues[-1]]

                

                dateDifference = (xValues[1] - xValues[0]).days

                #Include the earliest months to the chart

                while xValues[-1] > min(originalValues):
                    xValues.append(xValues[-1] + datetime.timedelta(days=dateDifference))

                



                xValues = xValues[::-1]

                # give room for the latest month to be plotted

                xValues.append(xValues[-1] - datetime.timedelta(days=dateDifference))

                #save the highest and lowest x values to this class maximum and minimum values
                self.xHigh, self.xLow = xValues[-1], xValues[0]

                #convert to month then year
                xValues = list(
                    f'{MONTHS_OF_THE_YEAR[value.month - 1]} {value.year}' for value in xValues
                )


            #if we do not subtract 1 from xvalues, the division would have cut off too early
            divisionWidth = (length-120) / (len(xValues) - 1)

            for interval in range(len(xValues)):
                xPoint = 120 + ( (interval * divisionWidth))

                self.create_line(
                    xPoint,
                    height - 1,
                    xPoint,
                    100,
                    fill='gray'
                )

                self.create_text(
                    xPoint,
                    height + 10,
                    fill='black',
                    font = ("Georgia", 10),
                    text=xValues[interval]
                )




            #if timespan is 'Y', then have the x axis divided into month + year. Up to 12 increments.

        #make sure canvas has up to date info on its size
        self.master.update()
        
        #set variables for determining the length of the axes
        length = self.winfo_width() - 100
        height = self.winfo_height() - 100

        #make the title
        self.create_text(
            (100 + length)/2,
            50,
            fill='black',
            font=('georgia', 36, 'bold'),
            text=title
        )

        #make the x axis
        self.create_line(100, height, length, height, fill='black', width=3)
        self.create_text(
            (100 + length) / 2, #place in the middle of the x axis
            height + 50,  #place just below x axis line
            fill='black',
            text= xName,
            font=('Georgia', 16)
        )

        #make the y axis
        self.create_line(100, height, 100, 100, fill='black', width=3)
        self.create_text(
            30, #place just left of y axis
            (100 + height)/2,  #place in middle of y axis
            fill='black',
            text= yName,
            font=('Georgia', 16),
            angle=90
        )

        x = independant
        y = dependant

        #if independant variables is numeric, then store x as floating point values
        #else, store them as strings


        #1. Split timespan
        #find x days by ovncerting weeks, months, or years to days
        #filter out any days less than that
        if xAreDates:
            duration = timespan.split('.')
            if duration[1] == 'Y':
                numDays = 365 * int(duration[0])
            elif duration[1] == 'M':
                numDays = 30 * int(duration[0])
            elif duration[1] =='W':
                numDays = 7 * int(duration[0])

            x = self.convert_to_datetime(x)
            data = pd.DataFrame({'x': x, 'y': y})
            data = data[data.x >= max(data.x) - datetime.timedelta(days=numDays)]

        else:
            data = pd.DataFrame({'x': x ,'y': y})


        #separate the y values to make the y axis
        yValues = list(
            value for value in data['y']
            )
                        
        #if there is a decimal range between the values, convert the min and max values to integers
        #convert min to integer using int() function
        #convert max to intefer using math.ceil() function to ceiling the maximum

        if (max(yValues) - min(yValues)) % 1 != 0:
            yHigh = math.ceil(max(yValues))
            yLow = math.floor(min(yValues))
        else:
            yHigh = max(yValues)
            yLow = min(yValues)


        #save the highest and lowest x values to this class maximum and minimum values
        self.yHigh, self.yLow = yHigh, yLow
            
            
         #try to find the cleanest split of the y values... goal is to have 10 increments
        #first, find how many values go in between the highest and lowest values
        ySplit = math2.factors(yHigh - yLow)

        #now, just get all the values in order
        ySplit = list(
            factor[0] for factor in ySplit
        )

        ySplit.extend(
            list(
                abs(10-value) for value in ySplit
            )
        )

        #ySplit is in two parts: the factors of the range of the y values and the distance of the factors from 10
        #we look at the second half with the distance from ten -- index that value in the list
        #the target ySplit will be halfway across the list, so the value indexed halfway across the list (from the left)
        # is out ySplit
        ySplit = ySplit[
            ySplit.index(
                min(
                    ySplit[(len(ySplit)//2):]
                    )
            ) - (len(ySplit) // 2)
        ]
            #draw the lines
            #should start at y = 100 and split evenly until it hits the length of the y axis (though shuold not be on the x axis)

            #height is the ending y coordinate of the y axis
            #length is the ending x coordinate of the x axis

        for y in range(ySplit + 1):
            yPoint = 100 + ((((height - 100)/ySplit)) * y)
            if y != ySplit: self.create_line(
                101,
                yPoint,
                length,
                yPoint,
                fill='light grey',
                 width=1
            )

            #figure out how far the text should be from y axis

            textDistanceFromAxis = 10 + len(str(int(yHigh - (y * ((yHigh-yLow)/ySplit)))))

            self.create_text(
                100 - textDistanceFromAxis,
                yPoint,
                fill='black',
                font=('Georgia', 10),
                text= int(yHigh - (y * ((yHigh-yLow)/ySplit))) # writing from top to bottom so its max - interval
            )

        if treatAsText:
            treat_as_text(independant)
        elif xAreDates:
            treat_as_dates(independant, timespan)
        elif treatAsRange:
            treat_as_range(independant)
        elif len(independant) > 10 and all(list(tk2.is_a_number(value) for value in independant)):
            treat_as_range(independant)
        else:
            treat_as_text(independant)

        self.update()
    
    def make_scatterplot(
            self, independant, dependant, xName='', yName='', title='', xAreDates=False,
            treatAsText =False, timespan='1.W', pointSize=10, pointColor='black'
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
        #check if the user wants specifically the text to be treated as dates or as text

        #if the list is numeric 
        #check if all the values in the list is numeric
        if all( list(str(value).replace('-', '').isdecimal() for value in independant) ):

            #convert them all to numbers
            independant = np.array( list(float(value) for value in independant), dtype=float )

            #align x and y into the datafram
            data = pd.DataFrame({'x': independant, 'y': dependant})

            #sort dataframe along x axis 
            data = data.sort_values('x')

            #store the new order in independant and dependnt
            independant = np.array(data.x)
            dependant = np.array(data.y)
        else:
            #make sure independant and dependant are numpy arrays anyway
            independant = np.array(independant)
            dependant = np.array(dependant)

        
        #keep track of the parameters
        parameters = (independant, dependant, xName, yName, title)
        if xAreDates:
            self.create_line_axis(*parameters, xAreDates=True, timespan=timespan)
        elif treatAsText:
            self.create_line_axis(*parameters, treatAsText=True)
        else:
            self.create_line_axis(*parameters)

        width, height = self.winfo_width() - 100, self.winfo_height() - 100

        #keep track of all the points so they can all have a function

        #check if it is treated as text
        #if it is not treated as text, find the x and y posisition by relative size


        #if X are dates, then convert each x item to datetime format
        if xAreDates:
            independant = np.array(self.convert_to_datetime(independant))

            data = pd.DataFrame({'x': independant, 'y': dependant})

            #exclude days that occur earlier than given timespan
            data = data[data.x >= self.xLow]

            independant = np.array(data.x)
            dependant = np.array(data.y)


        if not xAreDates:
            xUnitWidth = 1/(self.xHigh - self.xLow)
        else:
            xUnitWidth = 1 / (self.xHigh - self.xLow).days #make sure the day range is just a number

        yUnitWidth = 1/(self.yHigh - self.yLow)

        #check if it is treated as text
        #if it is, there will be no maximum or minimum x value
        #if not treated as text, the point will be placed on the graph based on its x and y values
        #relative to the max and min values.
        if self.xHigh != None and self.xLow != None:
            for index in range(independant.size):
                currentX, currentY = independant[index], dependant[index]

                if not xAreDates: 
                    xPosition = 120 + (width - 120) * xUnitWidth * (currentX - self.xLow)
                else:
                    xPosition = 120 + (width - 120) * xUnitWidth * (currentX - self.xLow).days

                yPosition = height - (height - 100) * yUnitWidth * (currentY - self.yLow)

                infoMessage = f'x ({xName}): {currentX}, y ({yName}): {currentY}'

                self.create_oval(
                    xPosition - pointSize/2, 
                    yPosition - pointSize/2, 
                    xPosition + pointSize/2,
                    yPosition + pointSize/2, 
                    fill = pointColor,
                    outline=pointColor,
                    tags=f'point{index}'
                )

                self.tag_bind(
                    f'point{index}',
                    '<Enter>',
                    lambda e, message = infoMessage: self.show_info(message),
                    '+'
                    )
                self.tag_bind(f'point{index}', '<Leave>', lambda e: self.hide_info(), '+')


        self.update()
       
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

test.make_scatterplot(
    x3, y3,
    'X',
    'Y',
    'X Versus Y', 
    pointSize=3,
    pointColor='black'
)



root.mainloop()
