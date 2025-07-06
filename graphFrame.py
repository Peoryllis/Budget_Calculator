"""
Anaya Ahaontu
18 June 2025
Creates the graphs to display on the budget calculator
"""

#import needed modules
import tkinter as tk
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import sys
import math
import datetime
from datetime import datetime as dt 

sys.path.append('/Users/anayaahanotu/Documents/Coding/GitHub/')

from Special_tkinter_objects import tkinterPlus2 as tk2
from other_python_docs import quick_math_operations as math2


class Graphing (tk.Frame):
    '''Make a Frame to display the different graphs'''
    
    def __init__(self, master:tk.Frame|tk.Tk, **kwargs):
        '''GraphFrame(args, kwargs):\n
            master: Tkinter.Frame() or Tkinter.Tk()\n
            **kwargs: tkinter.Canvas parameters -- NOT 'bg'
        '''

        if "bg" in kwargs: del kwargs["bg"] #make sure bg is not added twice

        tk.Canvas.__init__(self, master, bg='white', **kwargs) #initialize self

        #give the list of modes and set the mode
        self.charts = ['Bar Chart', 'Line plot', 'Scatter plot', 'Pie Chart']
        self.type = self.charts[0]

        self.xData = []
        self.yData = []
        self.graphAtts={}

        self.bind("<Configure>", 
                       lambda e: self.create_graph(self.xData, self.yData, e=e),
                       "+")
        
    
    def switch_graph(self, graphType, **kwargs):
        '''GraphFrame.switch_graph(graphType)
        graphType: any literal in [timeline chart, bar chart, or pie chart]
        switches the graph to be displayed
        '''
        
        pass
    
    def create_graph(self, independant=[], dependant=[], e = None, **kwargs):
        '''GraphFrame.create_graph(graphType)
        independant: seq: x-axis values
        dependant: seq: numeric: y-axis values
        '''
        #make sure we don't end up with multiple charts in one frame
        for widget in self.winfo_children(): 
            widget.destroy()
        
        #test run
        self.make_scatterplot(independant=independant,
                              dependant=dependant, e=e,
                              **kwargs)
        
    def align_params(self, funcParams: dict):
        """
        GraphFrame.align_params(self, selfParams, funcParams)\n
        funcParams: dict: parameters and corresponding values for the function\n
        updates self.params based on function params\n
        """

        #only update atts if chart is not being made due to
        #self configuration
        if funcParams["e"] == None:
            self.graphAtts = funcParams
            
    def make_scatterplot(self, independant, dependant,*, xName='', yName='',
                          title='', xAreDates=False, treatAsText =False, timespan='1.W', pointSize=10,
                          pointColor='black', e=None):
        '''
        GraphFrame.make_scaterplot(independant, dependant, *, ...): void\n
        independant: seq: x-axis values\n
        dependant: numeric seq: y-axis values\n
        xName: str: x-axis label\n
        yName: str: y-axis label\n
        title: str: title of graph\n
        xAreDates: bool: look at the x axis data as a date: False\n
        treatAsText: boolean: treat all data as text, not as dates: False\n
        timespan: str: format: "<num units>.<units>": 1.w\n
            units: 'W' -> week, 'M' -> month (30 days), 'Y' -> year (12 months)\n
        pointSize: int or float: size of the point wanted (default: 10)\n
        pointColor: str: color of point wanted (default: 'black')\n
        e: event handler: DO NOT CHANGE THIS VALUE
        '''


        #remove rows with no values
        cleanedData = self.clean_data(independant, dependant)


        # separate the independant and dependant variables
        self.xData = cleanedData.loc[:, "x"]
        self.yData = cleanedData.loc[:, "y"]

        #store every important label
        self.align_params(locals())

        self.update_idletasks()
        self.master.update_idletasks()

        #store the length, width, and average of the two on the plot
        plotWidth = self.winfo_width()
        plotHeight = self.winfo_height()
        dpiRef = min(plotHeight, plotWidth)


        #make sure reference dict is not empty
        if self.graphAtts != {}:
            #reset the plot if a chart has already been initialized
            if not hasattr(self, "fig") or self.fig is None:
                #initialize the figure
                self.fig = plt.figure(figsize=(plotWidth//120, plotHeight//110), 
                                         dpi=dpiRef/8)
                #ABOVE ARE THE DIMENSIONS NEEDED TO ENSURE CHART IS TO SCALE.
            if hasattr(self, "ax"):
                del self.ax

            # clear the figure and create a new axis
            self.fig.clear()

            #create the axis where the chart will be made
            self.ax = self.fig.add_subplot(111)

            #resize fig
            self.fig.set_size_inches(plotWidth//120, plotHeight//110)
            self.fig.set_dpi(dpiRef/8)
            #ABOVE ARE THE DIMENSIONS NEEDED TO ENSURE CHART IS TO SCALE.

            #if the data is text: convert to string
            if self.graphAtts["treatAsText"]:
                self.xData = self.xData.astype(str)
            #else if the data are dates, convert to datetime
            elif self.graphAtts["xAreDates"]:
                self.xData = self.convert_to_datetime(self.xData)

            #graph the scatter plot
            self.ax.scatter(self.xData,
                            self.yData,
                            s=self.graphAtts["pointSize"],
                            c=self.graphAtts["pointColor"])
            
            #set axis
            self.ax.title.set_text(self.graphAtts["title"])
            self.ax.set_xlabel(self.graphAtts["xName"])
            self.ax.set_ylabel(self.graphAtts["yName"])

            #save the scatterplot on the frame
            self.graph = FigureCanvasTkAgg(self.fig, self)
            chart = self.graph.get_tk_widget()
            chart.configure(width=plotWidth, height=plotHeight)
            chart.pack()
            
            #draw the chart
            self.graph.draw()

            #update the window
            self.update_idletasks()
            self.master.update_idletasks()

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
         
    def convert_to_datetime(self, dates) -> list[datetime.date]:
        '''
        GraphFrame.convert_to_datetime(dates)\n
        dates: seq: str: valid dates separated by '/'\n
            dates must be in month/day/YYYY format\n
            Warning: if not in YYYY format, your dates may be off\n
        converts all the dates in the sequence to datetime format\n
        returns list: datetime.dates\n
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

    def close(self):
        """
        self.close(self)\n
        closes the window
        """
        #close the plot
        plt.close("all")

        #destory the frame
        self.destroy()

    def clean_data(self, independant, dependant) -> pd.DataFrame:
        '''
        GraphFrame.clean_data(independant, dependant)\n
        independant: seq: x-axis values\n
        dependant: seq: y-axis values\n
        cleans the data by filtering out None types and null\n
        returns DataFrame: {'x': independant, 'y': dependant}\n
        '''
        data = pd.DataFrame({'x': independant, 'y': dependant})

        return data.dropna()

#### test  ####
def main():
    root = tk.Tk()
    root['bg'] = 'white'

    test = Graphing(
        root,
        width = 400,
        height = 400
    )

    test.pack(fill='both', expand=1)
    root.update()

    x = np.arange(-10, 10, step=0.01)
    y = []
    
    for a in x:
        try:
            newValue = math.asin(math.tanh(a))

        except:
            newValue = None
        finally:
            y.append(newValue)

    y = np.array(y)

    indexToDelete = []
    for i in range(len(y)):
        if y[i] != None:
            if (y[i] > 50) or (y[i] < -50):
                indexToDelete.append(i)

    y = np.delete(y, indexToDelete)
    x = np.delete(x, indexToDelete)


    y2 = [datetime.date(year=2024, month=3, day=4)]
    add = datetime.timedelta(days=1)

    for value in range(len(x)):
        pass


    test.create_graph(
        x, y,
        xName='X',
        yName='Y',
        title='X Versus Y', 
        pointSize=3,
        pointColor='black',
    )


    root.mainloop()

if __name__ == "__main__":
    main()