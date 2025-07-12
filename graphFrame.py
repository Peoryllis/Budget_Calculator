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
        #these are meant to be private atts 
        #but would have to change a whole bunch of code to update
        self.charts = ['Bar Chart', 'Line plot', 'Scatter plot', 'Pie Chart']
        self.type = self.charts[0]

        # initialize where xData, yData, and graph attributes
        self.xData = []
        self.yData = []
        self.graphAtts={}

        #allow graphs to change size with window size
        self.bind("<Configure>", 
                    lambda e: self.create_graph(e=e), 
                    "+")
        
        #put in key valyes to self.graphAtts
        #so program can start up properly
        self.set_attributes()
            
    def switch_graph(self, graphType, **kwargs):
        '''GraphFrame.switch_graph(graphType)
        graphType: any literal in [timeline chart, bar chart, or pie chart]
        switches the graph to be displayed
        '''
        
        pass
    
    def set_attributes(self, independant= [], dependant=[], *, xName: str='', yName: str='', title: str='',
                       xAreDates: bool=False, treatAsText:bool=False,
                       timespan:str='1.W', pointSize:int=10,
                       pointColor:str='black', makeHistogram:bool=False,
                       fillColor:str="black", lineWidth:int=5,
                       lineColor:str="black", colorcode=[]):
        
        """
        GraphFrame.set_attributes(): sets up the attributes for the chart
        independant: iterable: list of all x values
        dependent: iterable: list of all y values

        Used with all charts: xName, yName, title

        Unique to scatterplot: xAreDates, treatAsText, timespan, pointSize,
        pointColor

        Unique to line graph: xAreDates, treatAsText, timespan, pointSize,
        pointColor, lineWidth, lineColor

        unique to bar chart: makeHistorgram, fillColor

        unique to pie chart: 
            - colorcode: iterable: list: list of colors to be used
        """
        # set self.xValues and self.yValues to passed independant and dependant values
        self.xData, self.yData = independant, dependant

        #update self.graphAtts except the first two items
        self.graphAtts = locals()
        del self.graphAtts["independant"]
        del self.graphAtts["dependant"]

    def create_graph(self, e = None):
        '''GraphFrame.create_graph(graphType)\n
        independant: seq: x-axis values\n
        dependant: seq: numeric: y-axis values\n
        '''

        #make sure we don't end up with multiple charts in one frame
        for widget in self.winfo_children(): 
            widget.destroy()
        
        #test run
        self.__make_scatterplot(e=e)
        
    
    def __reset_plot(self, plotWidth: float|int, plotHeight: float|int,
                     dpiRef:float|int) -> None:
        """
        Graph.__reset_plot(self, plotWidth, plotHeight, dpiRef) -> None
        plotWidth: float|int: width of the window
        plotHeight: float|int: height of the window
        dpiRef: float|int: minimum of plotWidth and plotHeight
        Resets the fig and axis
        """

        #reset the plot if a chart has already been initialized
        if not hasattr(self, "fig") or self.fig is None:
            #initialize the figure
            self.fig = plt.figure()
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

        #save the scatterplot on the frame
        self.graph = FigureCanvasTkAgg(self.fig, self)
        chart = self.graph.get_tk_widget()
        chart.configure(width=plotWidth, height=plotHeight)
        chart.pack()

            
    def __make_scatterplot(self, e=None):
        '''
        GraphFrame.make_scaterplot(self, e): void\n
        e: event handler: DO NOT CHANGE THIS VALUE

        displays a scatterplot
        '''

        #remove rows with no values
        cleanedData = self.clean_data(self.xData, self.yData)


        # separate the independant and dependant variables
        self.xData = cleanedData.loc[:, "x"]
        self.yData = cleanedData.loc[:, "y"]

        self.update_idletasks()
        self.master.update_idletasks()

        #store the length, width, and average of the two on the plot
        plotWidth = self.winfo_width()
        plotHeight = self.winfo_height()
        dpiRef = min(plotHeight, plotWidth)

        #make sure reference dict is not empty
        #if it is, then it means the window just opened without any data
        if self.graphAtts != {}:

            #if the data is text: convert to string
            if self.graphAtts["treatAsText"]:
                self.xData = self.xData.astype(str)
            #else if the data are dates, convert to datetime
            elif self.graphAtts["xAreDates"]:
                #if this function is executed by event handler, x are already dates
                #else, convert them to dates
                if not e:
                    #convert all days to datetime to work with them easier
                    # filter them tp be within specified timeframe
                    self.__filter_dates()

            #reset the matplotlib plot -- remove current one from memory
            #create new blank slate
            self.__reset_plot(plotWidth, plotHeight, dpiRef)

            #reduce clutter of x axis
            self.fig.autofmt_xdate()

            #graph the scatter plot
            self.ax.scatter(self.xData,
                            self.yData,
                            s=self.graphAtts["pointSize"],
                            c=self.graphAtts["pointColor"])
        
            
            #set axis labels
            self.ax.title.set_text(self.graphAtts["title"])
            self.ax.set_xlabel(self.graphAtts["xName"])
            self.ax.set_ylabel(self.graphAtts["yName"])
            
            #draw the chart
            self.graph.draw()

            #update the window
            self.update_idletasks()
            self.master.update_idletasks()

    def __make_bar_graph(self, independant, dependant, *, xName="", yName="",
                       title="", makeHistogram=False, fillColor="black"):
        pass
    def __make_line_chart(self, independant, dependant, *,xName='', yName='',
                          title='', xAreDates=False, treatAsText =False, 
                          treatAsRange=False, timespan='1.W', pointSize=10,
                          lineWidth=5, pointColor='black', lineColor="black"):
        pass
    def __make_pie_chart(self, independant, dependant, *, colorcode=[]):
        pass

    def __filter_dates(self):
        """
        GraphFrame.__filter_dates(self)
        filters the dates to be in desired time frame
        """

        # convert the current xData to datetime
        self.xData = self.convert_to_datetime(self.xData)

        #get the desired timeframe
        timeFrame = self.graphAtts["timespan"].split(".")

        #make sure the xData and yData are within the range specified
            #put self.xValues and self.yValyes in temporary dataFrame
            #the columns are [date, value]
            #sort the dataFrame by date in descending order
            #cast timeFrame[0] to int; this is the number of iterations
            #if timeFrame[1] == "W", filter by num weeks
                # have the earliest date be timeSpan[0] * 7 days before
                #most recent date
            #else if timeSpan[1] == "M", filter by num months
                # have beginning date be int value of
                #(timeSpan[0] * 30.44 days) before most recent date
            #else if timeSpan[1] == "Y", filter by num years
                # have the beginning date be int value of
                #(timeSpan[0] * 365.25 days) before most recent date
            # filter the dataframe and remove all rows that are less than
            #specified beginning date
            #reassign self.xValues and self.yValues based on dataframe

        #delete temporary dataframe from memory
         
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
            newValue = a / (1 + a**2)**2
        except:
            newValue = None
        finally:
            y.append(newValue)

    del a

    y = np.array(y)

    indexToDelete = []
    for i in range(len(y)):
        if y[i] != None:
            if (y[i] > 50) or (y[i] < -50):
                indexToDelete.append(i)

    del i

    y = np.delete(y, indexToDelete)
    x = np.delete(x, indexToDelete)


    x2 = [datetime.date(year=2024, month=3, day=4)]
    add = datetime.timedelta(days=1)

    for i in range(len(y) - 1):
        x2.append(x2[-1] + add)

    

    for i in range(len(x2)):
        year = x2[i].year
        month = x2[i].month
        day = x2[i].day

        x2[i] = "{}/{}/{}".format(month, day, year)

    y = y[:len(x2)]
    


    test.set_attributes(x2, y, xName='X', yName='Y', title='X Versus Y', 
                        pointSize=3, pointColor='black', xAreDates=True)

    test.create_graph()

    root.mainloop()

if __name__ == "__main__":
    main()