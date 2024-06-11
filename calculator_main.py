# -*- coding: utf-8 -*-
"""
Created on Tue Jul 18 18:34:30 2023

Makes the main calculator where all the parts come together and makes one calculator
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
        self.place(relx=0, rely=0, relwidth=1, relheight=1)

        title = tk.Label( #title of project
        root,
        bg=root['bg'],
        fg='white',
        text='Budget Calculator',
        font=('Georgia', 26, 'bold'),
        )

        title.place(relx=0.5, rely=0, relwidth=0.5, relheight=0.05, anchor='n')

        self.unselectedColor = [list(tk2.hex_to_rgb(self['bg'])), self['bg']] #give selected and unselected tabs two distinct colors
        self.selectedColor = [
             tuple(value - 50 for value in self.unselectedColor[0]),           
        ] #selected tabs are a few shaeds darker than unselected tabs


        self.selectedColor.append(tk2._from_rgb(self.selectedColor[0]))

        self.modes = ['income and expenses',
                    'income and expenses analysis',
                    'spendings and tends',
                    'investments'] #keep track of all possible modes
        
        self.mode = self.modes[0] #know what mode you are in

        tabFrame = tk.Frame(
            self,
            bg=self['bg']
        )


        tabFrame.place(relx=0, rely=0.052, relwidth=1) #keep the tabs in a narrow frame about right next to each other

        self.incomeTab = tk.Label(tabFrame, #create a button have user select the income section -- tkinter.Button not working on MacOS
                        text=self.modes[0],
                        font=('Georgia', 24,),
                        fg='white',
                        bg=self.unselectedColor[1],
                        relief='groove'
                        )
        
        self.incomeTab.bind('<Button>', lambda: self.set_mode(0)) #make it a working button
        
        self.incomeTab.grid(row=0, column=0, padx=2) #place it on the screen

        self.analysisTab = tk.Label(tabFrame, #create a button have user select the income analysis section
                        text=self.modes[1],
                        font=('Georgia', 24,),
                        fg='white',
                        bg=self.unselectedColor[1],
                        relief='groove'
                        )
        
        self.analysisTab.bind('Button', lambda: self.set_mode(1)) #make it a working button
        
        self.analysisTab.grid(row=0, column=1, padx=2) #place it on the screen

        self.spendingsTab = tk.Label(tabFrame, #create a button have user select the savings analysis section
                        text=self.modes[2],
                        font=('Georgia', 24,),
                        fg='white',
                        bg=self.selectedColor[1],
                        relief='groove'
                        )
        
        self.spendingsTab.bind('<Button>', lambda: self.set_mode(2)) #make it a working button
        
        self.spendingsTab.grid(row=0, column=2, padx=2) #place it on the screen

        self.investTab = tk.Label(tabFrame, #create a button have user select the savings analysis section
                        text=self.modes[3],
                        font=('Georgia', 24,),
                        fg='white',
                        bg=self.unselectedColor[1],
                        relief='groove'
                        )
        
        self.investTab.bind('<Button>', lambda: self.set_mode(3)) #make it a working button
        
        self.investTab.grid(row=0, column=3, padx=2) #place it on the screen

        self.saveButton = tk.Label( #allow people to save their data
            self,
            text='Save',
            font=('Georgia', 18, 'bold'),
            bg = '#2BAF6A',
            fg = 'white',
            relief='raised'
        )

        self.saveButton.place(
            relx=1,
            rely=0,
            relwidth=0.06,
            relheight=0.05,
            anchor='ne'
        )

        self.window = tk.Frame(
            self,
            bg=self.selectedColor[1]
        )

        self.master.update_idletasks() #allow the program gather up to date info on placement of tabs


        starty = float(tabFrame.place_info()['rely']) + float(tabFrame.winfo_height()/self.winfo_height()) #figure out where the main window should begin

        self.window.place(relx=0, rely=starty, relwidth=1, relheight=1-starty) #above code allows for less messy placement of the window

        self.incomeFrame = None #set up the frames that display the data
        self.incomeAnalysisFrame = None
        self.spendingsFrame = None
        self.investmentsFrame = None

        self.set_mode(0) #set default mode
        self.revive_data() # get data previously saved
        self.saveButton.bind('<Button>', self.save_data) #we put this last to make sure users do not accidentally save unused data


        self.master.update()

    def set_mode(self, value):
        pass 
    def save_data(self):
        pass
    def revive_data(self):
        pass

 


a = Budget_Calculator(root)

root.mainloop() #show the window

