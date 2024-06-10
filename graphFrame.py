import tkinter as tk


class GraphFrame (tk.Frame):
    '''Make a Frame to display the different graphs'''
    
    def __init__(self, master, args=(), kwargs={}):
        '''GraphFrame(args, kwargs):
            master: Budget calculator
            args: tuple: tkinter.Frame arguments
            kwargs: dictionary: tkinter.Frame k arguments
        '''
        
        pass
    
    def switch_graph(self, graphType):
        '''GraphFrame.switch_graph(graphType)
        graphType: any literal in [timeline chart, bar chart, or pie chart]
        switches the graph to be displayed
        '''
        
        pass
    
    def create_graph(self, graphType):
        '''GraphFrame.create_graph(graphType)
        graphType: any literal in [timeline chart, bar chart, or pie chart]
        creates the graph for the frame to display
        '''
        
        pass
    
