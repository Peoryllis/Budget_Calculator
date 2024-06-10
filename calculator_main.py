# -*- coding: utf-8 -*-
"""
Created on Tue Jul 18 18:34:30 2023

Makes the main calculator where all the parts come together and makes one calculator, ig
"""

import tkinter as tk
import time
import sys

sys.path.insert(1, '/Users/anayaahanotu/Coding/GitHub/')

from Special_tkinter_objects import tkinterPlus2 as tk2



root = tk.Tk()
root.geometry('1200x800') #set size of window
root['bg'] = '#7BB4EE' #makes for a soft, neutral blue background
root.title('Budget Calculator')

title = tk.Label(
    root,
    bg=root['bg'],
    fg='white',
    text='Budget Calculator',
    font=('Georgia', 18, 'bold'),
    )

title.place(relx=0.5, rely=0, relwidth=0.5, relheight=0.05, anchor='n')

class Budget_Calculator(tk.Frame):
    '''Budget_Calculator
    makes the GUI budget calculator'''
    
    def __init__(self, master, kwargs = {}):
        """Budget_Calculator(self, master, kwargs)
        master: tkinter.Tk
        kwargs (opt): dict: k arguments for tkinter.Frame
        Initiates the budget_calculator
        """
        
        tk.Frame.__init__(self, master, bg=master['bg'], **kwargs) 

        self.unselectedColor = [list(tk2.hex_to_rgb(self['bg'])), self['bg']]
        self.selectedColor = [
             tuple(value - 50 for value in self.unselectedColor[0]),           
        ]


        self.selectedColor.append(tk2._from_rgb(self.selectedColor[0]))

        self.modes = ['income and expenses',
                    'income and expenses analysis',
                    'spendings and tends',
                    'investments']
        
        self.mode = self.modes[0]

        tabFrame = tk.Frame(
            self,
            bg=self['bg']
        )


        tabFrame.place(relx=0, rely=0.052, relwidth=1, relheight=0.07)

        tab1 = tk.Label(tabFrame,
                        text=self.modes[0],
                        font=('Georgia', 24,),
                        fg='white',
                        bg=self.unselectedColor[1],
                        relief='raised'
                        )
        
        tab1.bind('Button', lambda: self.set_mode(0))
        
        tab1.grid(row=0, column=0)

    def set_mode(self, value):
        pass




a = Budget_Calculator(root)
a.place(relx=0, rely=0.05, relwidth=1, relheight=0.95)


root.mainloop() #show the window

