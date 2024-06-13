import tkinter as tk
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import sys
import math
sys.path.append( '/Users/anayaahanotu/Coding/GitHub/')

from other_python_docs import quick_math_operations as math2

root = tk.Tk()
root['bg'] = 'white'


class GraphFrame (tk.Canvas):
    '''Make a Frame to display the different graphs'''
    
    def __init__(self, master, kwargs={}):
        '''GraphFrame(args, kwargs):
            master: Budget calculator
            kwargs: dictionary: tkinter.Canvas parameters
        '''
        
        tk.Canvas.__init__(self, master, bg='white', **kwargs)
    
    def switch_graph(self, graphType):
        '''GraphFrame.switch_graph(graphType)
        graphType: any literal in [timeline chart, bar chart, or pie chart]
        switches the graph to be displayed
        '''
        
        pass
    
    def create_graph(self, graphType, independant, dependant):
        '''GraphFrame.create_graph(graphType)
        graphType: any literal in [timeline chart, bar chart, or pie chart]
        creates the graph for the frame to display
        '''
        
        pass

    def create_line_axis(self, independant, dependant, xName='', yName='', title='', dateIncrements=None):
        '''
        GraphFrame.make_scaterplot(independant, dependant)
        independant: seq: x-axis values
        dependant: numeric seq: y-axis values
        dateIncrements: str: "d", "w", "m", or "y" for day, week, month, year, respectively
        creates a graph axis
        returns none
        '''

        def treat_as_range(x):
            """
            treat_as_range(x, y)
            x: numeric seq: data for independant variable
            makes a scatterplot, assuming the range of the independant data is greater than 10
            used to make the scatterplot look cleaner
            """
            #make sure the data is in proper order

            #everything i did to y i also do to x now
            #set x range
            xValues = list(value[0] for value in data)

            #if there is a decimal range between the xvalues, convert the min and max values to integers
            #convert min to integer using int() function
            #convert max to intefer using math.ceil() function to ceiling the maximum
            #an easier way to approach this would be to celieng the difference of the maximum and minimum
            #may do the above

            if (max(xValues) - min(xValues)) % 1 != 0:
                xHigh = math.ceil(max(xValues))
                xLow = int(min(xValues))
            else:
                xHigh = max(xValues)
                xLow = min(xValues)
            
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

            for x in range(1, xSplit + 2):
                xPoint = 100 + ((((length-100)/(xSplit + 1))) * x)
                if x != 0: self.create_line(
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
                    text= int(xLow + ((x-1) * ((xHigh-xLow)/xSplit))) # writing from left to right so its min + interval
                )

            

            return yHigh, yLow, xHigh, xLow


        def treat_as_values(matrix):
            pass
        def treat_as_dates(matrix):
            pass

        
        #clear canvas before creating scatterplot
        self.delete("all")

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

        data = np.array(
                list(
                    (x[index], y[index]) for index in range (len(x))
                ),
                dtype = [('x', float), ('y', float)]
            )

        data = np.sort(data, order='x')

        #separate the y values to make the y axis
        yValues = list(
            value[1] for value in data
            )
                        
        #if there is a decimal range between the values, convert the min and max values to integers
        #convert min to integer using int() function
        #convert max to intefer using math.ceil() function to ceiling the maximum

        if (max(yValues) - min(yValues)) % 1 != 0:
            yHigh = math.ceil(max(yValues))
            yLow = int(min(yValues))
        else:
            yHigh = max(yValues)
            yLow = min(yValues)
            
            
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
        #the target ySplit will be halfway across the list, so the value indexed halfway across the list is out ySplit
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

        treat_as_range(list(value[0] for value in data))







        self.update()
    
    def make_scatterplot(self):
        pass
    def make_bar_graph(self):
        pass
    def make_pie_chart(self):
        pass


a = GraphFrame(
    root,
    kwargs = {
        'width': 1200,
        'height': 800
    }
)
a.pack(fill='both', expand=1)
root.update()

x = np.array([ -8923, 4532, 7654, -3245, 998, -6423, 3121, -9584, 1102, 5678])
y = np.array([-7532, 8493, -1254, 6789, -4321, 9876, -2109, 5634, -8765, 4320])

a.create_line_axis(x, y, 'years worked', 'earnings', 'Earnings Versus Years Worked')




root.mainloop()
