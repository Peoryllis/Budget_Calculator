import tkinter as tk
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import sys
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

    def create_line_axis(self, independant, dependant, xName='', yName='', title=''):
        '''
        GraphFrame.make_scaterplot(independant, dependant)
        independant: seq: x-axis values
        dependant: numeric seq: y-axis values
        creates a scatterplot
        returns none
        '''

        def treat_as_range(x, y):
            """
            treat_as_range(x, y)
            x: numeric seq: data for independant variable
            y: numeric seq: data for dependant variable
            makes a scatterplot, assuming the range of the independant data is greater than 10
            used to make the scatterplot look cleaner
            """
            #make sure the data is in proper order
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
            
            #try to find the cleanest split of the y values... goal is to have 10 increments
            #first, find how many values go in between the highest and lowest values
            ySplit = math2.factors(max(yValues) - min(yValues))

            #now, just get all the values in order
            ySplit = list(
                factor[0] for factor in ySplit
            )

            ySplit.extend(
                list(
                    abs(10-value) for value in ySplit
                )
            )

            ySplit = ySplit[
                ySplit.index(
                    min(
                        ySplit[(len(ySplit)//2):]
                    )
                ) - (len(ySplit)//2)
            ]
#########left off here
            for y in range(ySplit):
                self.create_line(
                    90, 100 + (y * ySplit), length, 100 * (y+1),
                    fill='light grey',
                    width=1
                )


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
            height + 70,  #place just below x axis line
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

        treat_as_range(independant, dependant)







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

x = np.array([39, 23, 65, 12, 7, 43])
y = x * 54

a.create_line_axis(x, y, 'years worked', 'earnings', 'Earnings Versus Years Worked')




root.mainloop()
