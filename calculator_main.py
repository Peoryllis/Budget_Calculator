# -*- coding: utf-8 -*-
"""
Created on Tue Jul 18 18:34:30 2023

Makes the main calculator where all the parts come together and makes one calculator, ig
"""

import tkinter as tk
import time
import sys



root = tk.Tk()
root.geometry('1200x800') #set size of window
root['bg'] = '#7BB4EE' #makes for a soft, neutral blue background
root.title('Budget Calculator')

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
    

class Budget_Calculator(tk.Frame):
    '''Budget_Calculator
    makes the GUI budget calculator'''
    
    def __init__(self, master, kwargs):
        """Budget_Calculator(self, master, kwargs)
        master: tkinter.Tk
        kwargs: k arguments for tkinter.Frame
        Initiates the budget_calculator
        """
        
        pass 


root.mainloop() #show the window

