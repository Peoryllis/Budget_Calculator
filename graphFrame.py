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
import typing as t

sys.path.append('/Users/anayaahanotu/Documents/Coding/GitHub/')

class Graphing(tk.Frame):
    '''Make a Frame to display different graphs'''
    
    def __init__(self, master:tk.Frame|tk.Tk, **kwargs):
        '''GraphFrame(args, kwargs):\n
            master: Tkinter.Frame() or Tkinter.Tk()\n
            **kwargs: tkinter.Canvas parameters -- NOT 'bg'
        '''

        if "bg" in kwargs: del kwargs["bg"] #make sure bg is not added twice

        #initialize self
        tk.Canvas.__init__(self, master, bg='white', **kwargs) 

        #give the list of charts and set the mode
        #these are meant to be private atts 
        #but would have to change a whole bunch of code to update
        self.__CHARTS:tuple[str] = (
            'Bar Chart', 'Line plot', 'Scatter plot', 'Pie Chart'
            )
        self.type:str = self.__CHARTS[0]

        # initialize where independant, dependant
        # and graph attributes will be stored
        self.xData:list = []
        self.yData:list[int|float] = []
        self.graphAtts:dict = {}

        #allow graphs to change size with window size
        self.bind(
            "<Configure>", 
            lambda e: self.__create_graph(newDates=False), 
            "+"
            )
        
    def get_graph_atts(self) -> dict:
        return self.graphAtts

    def switch_graph(self, graphType:int) -> None:
        '''GraphFrame.switch_graph(graphType)\n
        graphType: int: numeric representation of graph to be shown\n
            0: Bar Chart\n
            1: Line plot\n
            2: Scatter Plot\n
            3: Pie Chart\n
        switches the graph to be displayed
        '''

        #update graph mode
        self.type = self.__CHARTS[graphType]

        #draw the graph
        self.__create_graph()

    def update_data(
            self,
            independant:t.Iterable[t.Any]=None,
            dependant:t.Iterable[int|float]=None,
            **kwargs
            ):
        """
        GraphFrame.set_attributes(): None

        independant: iterable: list of all x values\n
            dates must be in MM/DD/YYYY format! \n
        dependent: iterable: list of all y values\n
        xName: str: x-axis label\n
        yName: str: y-axis label\n
        title: str: title of the graph\n
        xAreDates: bool: treat x values as dates\n
        treatAsText: bool: treat x values as plain text\n
        timespan: str: num_iterations.unit_of_time | all\n
            'W' -> Week\n
            'M' -> Month\n
            'Y' -> year\n
            'all' -> all time\n
        pointSize: int: size of the point\n
        pointColor: str: pointColor\n
        makeHistogram: bool: make the bar chart as a histogram\n
        numBins: int: number of bins\n
        fillColor: str|iterable[str]: color(s) to fill bar chart\n
        lineWidth: int: size of line for line chart\n
        lineColor: str: color of chart line\n

        Used with all charts: xName, yName, title\n

        Unique to scatterplot: xAreDates, treatAsText, timespan, pointSize,
        pointColor\n

        Unique to line graph: xAreDates, treatAsText, timespan, pointSize,
        pointColor, lineWidth, lineColor\n

        unique to bar chart: makeHistorgram, fillColor, numBins\n

        sets up the attributes for the chart and draws the graph
        """

        #update the data
        self.graphAtts.update(kwargs)

        self.__create_graph(newDates=False)
    
    def set_attributes(
            self, independant:t.Iterable[t.Any] = (), 
            dependant:t.Iterable[int|float] = (),
            *, xName:str = '', yName:str = '', title:str = '',
            xAreDates:bool = False, treatAsText:bool = False, timespan:str = 'all',
            pointSize:int = 10, pointColor:str = 'black', makeHistogram:bool = False,
            numBins:int = 10, fillColor:str|t.Iterable[str] = "black",
            lineWidth:int = 5, lineColor:str = "black",
            ) -> None:
        
        """
        GraphFrame.set_attributes(): None

        independant: iterable: list of all x values\n
            dates must be in MM/DD/YYYY format! \n
        dependent: iterable: list of all y values\n
        xName: str: x-axis label\n
        yName: str: y-axis label\n
        title: str: title of the graph\n
        xAreDates: bool: treat x values as dates\n
        treatAsText: bool: treat x values as plain text\n
        timespan: str: num_iterations.unit_of_time | all\n
            'W' -> Week\n
            'M' -> Month\n
            'Y' -> year\n
            'all' -> all time\n
        pointSize: int: size of the point\n
        pointColor: str: pointColor\n
        makeHistogram: bool: make the bar chart as a histogram\n
        numBins: int: number of bins\n
        fillColor: str|iterable[str]: color(s) to fill bar chart\n
        lineWidth: int: size of line for line chart\n
        lineColor: str: color of chart line\n

        Used with all charts: xName, yName, title\n

        Unique to scatterplot: xAreDates, treatAsText, timespan, pointSize,
        pointColor\n

        Unique to line graph: xAreDates, treatAsText, timespan, pointSize,
        pointColor, lineWidth, lineColor\n

        unique to bar chart: makeHistorgram, fillColor, numBins\n

        sets up the attributes for the chart and draws the graph
        """
        # set self.xValues passed independant values
        # and self.yValues to  and dependant values
        self.xData, self.yData = np.array(independant), np.array(dependant)

        #update self.graphAtts to be all attributes except the first two items
        self.graphAtts = dict(locals())
        del self.graphAtts["independant"]
        del self.graphAtts["dependant"]

        #draw the graph
        self.__create_graph()



    def __create_graph(self, newDates = True) -> None:
        '''GraphFrame.create_graph(graphType)\n
        independant: seq: x-axis values\n
        dependant: seq: numeric: y-axis values\n
        newDates: bool: new dates entered (default True)
        '''

        #make sure we don't end up with multiple charts in one frame
        for widget in self.winfo_children(): 
            widget.destroy()
        
        #test run
        self.__make_bar_graph()     
    
    def __reset_plot(self) -> None:
        """
        Graph.__reset_plot(self, plotWidth, plotHeight, dpiRef) -> None
        Resets the fig and axis
        """
        #update window to get most accurate window size
        self.update_idletasks()
        self.master.update_idletasks()

        #store the length, width, and average of length and width.
        #the plot will reference these measurements to determine plot size
        plotWidth = self.winfo_width()
        plotHeight = self.winfo_height()
        dpiRef = min(plotHeight, plotWidth)

        #create a figure if it does not already exist
        if not hasattr(self, "fig") or self.fig is None:
            #initialize the figure
            self.fig = plt.figure()
    
        # remove current axis from memory.
        if hasattr(self, "ax"):
            del self.ax

        # clear the figure and create a new axis
        self.fig.clear()

        #create the axis where the chart will be made
        self.ax = self.fig.add_subplot(111)

        #resize fig
        self.fig.set_size_inches(plotWidth//120, plotHeight//110)
        self.fig.set_dpi(dpiRef/8)
        #ABOVE ARE THE DIMENSIONS NEEDED TO ENSURE CHART FITS IN THE WINDOW.

        #put the scatterplot on the frame
        self.graph = FigureCanvasTkAgg(self.fig, self)
        chart = self.graph.get_tk_widget()
        chart.configure(width=plotWidth, height=plotHeight)
        chart.pack()
            
    def __make_scatterplot(self, formatDates:bool) -> None:
        '''
        GraphFrame.make_scaterplot(self, formatDates): void\n
        formatDates: bool: does we have new dates to update\n

        displays a scatterplot
        '''

        self.update_idletasks()
        self.master.update_idletasks()

        #make sure reference dict is not empty
        #if it is, then it means the window just opened without any data
        # and nothing should be plotted
        if self.graphAtts != {}:
            #remove rows with no values
            self.__clean_data()

            #if the data is text: convert to string
            #allows matplotlib to interpret data as as text, not numeric
            if self.graphAtts["treatAsText"]:
                self.xData = self.xData.astype(str)

            #else if the data are dates, convert to datetime
            elif self.graphAtts["xAreDates"]:

                #if the dates need to be formatted, then we got new dates
                #update dates
                if formatDates:
                    #convert all days to datetime to work with them easier
                    # filter them to be within specified timeframe
                    # the user wants
                    self.__filter_dates()

            #reset the matplotlib plot -- remove current one from memory.
            #create new blank slate
            self.__reset_plot()

            #reduce clutter of x axis
            self.fig.autofmt_xdate()

            #graph the scatter plot
            self.ax.scatter(
                self.xData,
                self.yData,
                s=self.graphAtts["pointSize"],
                color=self.graphAtts["pointColor"]
                )
            
            #set axis labels
            self.ax.title.set_text(self.graphAtts["title"])
            self.ax.set_xlabel(self.graphAtts["xName"])
            self.ax.set_ylabel(self.graphAtts["yName"])
            
            #draw the chart
            self.graph.draw()

            #update the window
            self.update_idletasks()
            self.master.update_idletasks()

    def __make_bar_graph(self) -> None:
        """
        GraphFrame.__make_bar_graph(self): void\n

        displays a bar graph
        """

        #update window
        self.update_idletasks()

        #if graphAtts is not empty, there is data to be plotted
        #create the bar chart
        if self.graphAtts != {}:

            #clean data
            self.__clean_data()

            #reset plot -- clear the current plot from memory
            self.__reset_plot()

            #clean up x axis
            self.fig.autofmt_xdate()
            
            #if the user wants a histogram: make the histogram
            if self.graphAtts["makeHistogram"]:

                # create the histogram
                n, bins, patches = self.ax.hist(
                        self.xData,
                        linewidth=self.graphAtts["lineWidth"],
                        edgecolor=self.graphAtts["lineColor"],
                        bins = self.graphAtts["numBins"]
                        )

                #make the colors

                #if the user included a list of colors,
                #iterate through each color and assign to bar graph

                #create own flag variables 
                # or else if statement will get long and confusing
                isSeq = isinstance(self.graphAtts["fillColor"], t.Iterable)
                isNotStr = not isinstance(self.graphAtts["fillColor"], str)
                isListOfStrs = all(map(
                    lambda value: isinstance(value, str) == True,
                    self.graphAtts["fillColor"]
                    ))

                #now check the conditions
                if (isSeq and isNotStr and isListOfStrs):
                    # if user inputted less colors than there are
                    # bins, iterate through user inputted colors
                    # and add it to a new list of colors until they are the 
                    #same length
                    if len(self.graphAtts["fillColor"]) < len(patches):
                        
                        #index of graphAtts to reference
                        index = 0

                        # add the user inputted colors to colors
                        colors = list(self.graphAtts["fillColor"])

                        #add new color if there are less colors than bars
                        while len(colors) < len(patches):
                            #add a new color
                            colors.append(self.graphAtts["fillColor"][index])

                            #if index is at the last index of the list of
                            #user inputted colors, reset index to 0
                            if index == len(self.graphAtts["fillColor"]) - 1:
                                index = 0
                            #else, add 1 to index
                            else:
                                index += 1

                    #else if there are more colors than bars, cut off the 
                    #excess colors and assign to a new list
                    elif len(self.graphAtts["fillColor"]) < len(patches):
                        colors = self.graphAtts[:len(patches)]
                    
                    #else assign the fill color to a new list
                    else:
                        colors = list(self.graphAtts["fillColor"])
                    
                    #loop through the each bar and each color in colors

                    for color, bar in zip(colors, patches):
                        bar.set_facecolor(color)

                #else, set the facecolor to one color
                else:
                    for bar in patches:
                        bar.set_facecolor(self.graphAtts["fillColor"])


            #else; they want a normal bar graph
            else:
                # draw the bar graph
                self.ax.bar(
                    self.xData,
                    self.yData,
                    color=self.graphAtts["fillColor"],
                    linewidth=self.graphAtts["lineWidth"],
                    edgecolor=self.graphAtts["lineColor"]
                    )

            #set the title, xLabel, yLabel, bar color, and outline thickness
            self.ax.title.set_text(self.graphAtts["title"])
            self.ax.title.set_text(self.graphAtts["title"])
            self.ax.set_xlabel(self.graphAtts["xName"])
            self.ax.set_ylabel(self.graphAtts["yName"])


            #update the window
            self.update_idletasks()


    def __make_line_chart(self, e = None):
        pass

    def __make_pie_chart(self, e = None):
        pass

    def __filter_dates(self):
        """
        GraphFrame.__filter_dates(self)
        filters the dates to be in desired time frame
        """

        # convert the current xData to datetime
        self.__convert_to_datetime()

        #check to see if user wants all time; if not, filter by timespan
        if self.graphAtts['timespan'].lower() != "all":
            #get the desired timeframe
            timeFrame = self.graphAtts["timespan"].split(".")

            #cast the M/W/Y noatation to uppercase
            #reduces case sensitivity
            timeFrame[1] = timeFrame[1].upper()

            #make sure the xData and yData are within the range specified.

            #put self.xValues and self.yValyes in temporary dataFrame to 
            #make sure the xvalues and yvalues are sorted along side each
            #other and data does not get mixed up
            tempData = pd.DataFrame(
                {"date": self.xData, "value": self.yData},
            )

            #sort the dataFrame by date in descending order
            tempData = tempData.sort_values(
                "date",
                ascending=False,
                ignore_index=True
                )
            

            #cast timeFrame[0] to int; this is the number of iterations of
            # the unit of time
            timeFrame[0] = int(timeFrame[0])

            #if timeFrame[1] == "W", filter by num weeks
            if timeFrame[1] == "W":
                # have the earliest date be timeSpan[0] * 7 days before
                #most recent date
                timeSubtract = datetime.timedelta(timeFrame[0] * 7)
                beginningDate = tempData.date[0] - timeSubtract

            #else if timeSpan[1] == "M", filter by num months
            elif timeFrame[1] == "M":
                # have beginning date be 
                #(int value timeSpan[0] * 30.44 days) before most recent date
                timeSubtract = datetime.timedelta(int(timeFrame[0] * 30.44))
                beginningDate = tempData.date[0] - timeSubtract

            #else if timeSpan[1] == "Y", filter by num years
            elif timeFrame[1] == "Y":
                # have the beginning date be
                #(int value of timeSpan[0] * 365.25 days) before most recent date
                timeSubtract = datetime.timedelta(int(timeFrame[0] * 365.25))
                beginningDate = tempData.date[0] - timeSubtract

            # filter the dataframe and remove all rows that are less than
            #specified beginning date
            tempData = tempData[tempData.date >= beginningDate]

            #reassign self.xValues and self.yValues based on dataframe
            self.xData = tempData.date
            self.yData = tempData.value

            #delete temporary dataframe from memory
            del tempData
         
    def __convert_to_datetime(self) -> None:
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
        for element in self.xData:
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

            #make the newdate in datetime format
            newDate = dt.strptime(tempDate, format)

            #add it to the list of dates
            tempIndependant.append(newDate.date())
        
        #update stored independant values to be in datetime format
        self.xData = tempIndependant

    def close(self) -> None:
        """
        self.close(self)\n
        closes the window
        """
        #close the plot
        plt.close("all")

        #destory the frame
        self.destroy()

    def __clean_data(self) -> None:
        '''
        GraphFrame.clean_data(independant, dependant)\n
        independant: seq: x-axis values\n
        dependant: seq: y-axis values\n
        cleans the data by filtering out None types and null\n
        reassigns self.xData and self.yData to be the cleaned data
        '''

        #if the plot is not supposed to be a histogram
        #filter the x and y axis  
        if not self.graphAtts["makeHistogram"]:

            #make sure xData and yData are the same length
            #set tsequenceshe max length of both sequences to be the smallest length
            # between both
            maxLength = min(len(self.xData), len(self.yData))

            #slice both sequences to go up to the length of the smaller list
            self.xData = self.xData[:maxLength]
            self.yData = self.yData[:maxLength]

            #save data to dataframe
            data = pd.DataFrame({'x': self.xData, 'y': self.yData})

            #drop all rows with no values
            data = data.dropna()

            #declare the cleaned data to xData and yData
            self.xData = data.x
            self.yData = data.y
        
        #if it is supposed to be a histogram, look at only x values
        else:
            data = pd.DataFrame({'x': self.xData})

            #drop all rows with no values
            data = data.dropna()

            #declare the cleaned data to xData and yData
            self.xData = data.x

        del data
        


#### test  ####
def main():
    import random

    root = tk.Tk()
    root['bg'] = 'white'

    test:Graphing = Graphing(
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
            newValue = math.sin(a) + math.log1p(abs(a))  
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

    barX = ["California", "New Mexico", "New York", "Virginia", "Delaware"]
    barY = [38_900_000, 2117522, 19867248, 8631393, 989948]
    
    histX = list(random.randrange(1, 100) for a in range(59))

    test.set_attributes(histX, xName='X', yName='Y', title='X Versus Y', 
                        pointSize=3, pointColor='black',xAreDates=False,
                        timespan="3.Y", lineWidth=1,
                        makeHistogram=True, numBins=5)
        
    color = "#" + "".join(random.choice("ABCDEF1234567890") for i in range(6))
    color2 = "#" + "".join(random.choice("ABCDEF1234567890") for i in range(6))

    test.update_data(
        fillColor=color,
        title="WHYYYYY"
        )


    root.update_idletasks()

    root.mainloop()

if __name__ == "__main__":
    main()

    