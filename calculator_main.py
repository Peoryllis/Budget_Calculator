# -*- coding: utf-8 -*-
"""
Created on Tue Jul 18 18:34:30 2023

Makes the main calculator where all the parts come together and makes one calculator, ig
"""

import tkinter as tk
import time

root = tk.Tk()
root.geometry('1500x900') #set size of window
root['bg'] = '#7BB4EE' #makes for a soft, neutral blue background
root.title('Budget Calculator')

class Budget_Calculator(Frame):
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

