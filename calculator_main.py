# -*- coding: utf-8 -*-
"""
Created on Tue Jul 18 18:34:30 2023

Makes the main calculator where all the parts come together and makes one calculator
"""

import tkinter as tk
import time
import sys

sys.path.insert(1, '/Users/anayaahanotu/Documents/Coding/GitHub')





root = tk.Tk()
root.geometry('1200x800') #set size of window
root['bg'] = '#7BB4EE' #makes for a soft, neutral blue background
root.title('Budget Calculator')



class Budget_Calculator(tk.Frame):
    '''Budget_Calculator
    makes the GUI budget calculator'''
    
    def __init__(self, master):
        """Budget_Calculator(self, master, kwargs)
        master: tkinter.Tk
        Initiates the budget_calculator
        """
        #set up frame
        tk.Frame.__init__(self, master, bg=master['bg'],) 
        self.place(relx=0, rely=0, relwidth=1, relheight=1)

        #title of project
        title = tk.Label( 
        root,
        bg=root['bg'],
        fg='white',
        text='Budget Calculator',
        font=('Georgia', 26, 'bold'),
        )

        #set relative position of all the widgets, instead of a fixed position

        title.place(relx=0.5, rely=0, relwidth=0.5, relheight=0.05, anchor='n') 

        #give selected and unselected tabs two distinct colors
        #selected tabs are a few shaeds darker than unselected tabs

        self.unselectedColor = [list(tk2.hex_to_rgb(self['bg'])), self['bg']] 
        self.selectedColor = [
             tuple(value - 50 for value in self.unselectedColor[0]),           
        ]


        self.selectedColor.append(tk2._from_rgb(self.selectedColor[0]))

        self.modes = ['income and savings',
                    'expenses',
                    'analysis'
                    ] #keep track of all possible modes
        
        self.mode = self.modes[0] #know what mode you are in


        #keep the tabs in a narrow frame about right next to each other

        tabFrame = tk.Frame(
            self,
            bg=self['bg']
        )


        tabFrame.place(relx=0, rely=0.052, relwidth=1) 

        #create a button have user select the income section -- tkinter.Button not working on MacOS

        self.incomeTab = tk.Label(tabFrame, 
                        text=self.modes[0],
                        font=('Georgia', 24,),
                        fg='white',
                        bg=self.unselectedColor[1],
                        relief='groove'
                        )
        
        self.incomeTab.bind('<Button>', lambda: self.set_mode(0)) #make it a working button
        
        self.incomeTab.grid(row=0, column=0, padx=2) #place it on the screen

        #create a button have user select the income analysis section

        self.expensesTab = tk.Label(tabFrame,
                        text=self.modes[1],
                        font=('Georgia', 24,),
                        fg='white',
                        bg=self.unselectedColor[1],
                        relief='groove'
                        )
        
        self.expensesTab.bind('Button', lambda: self.set_mode(1)) #make it a working button
        
        #use grid() to place the analysis tabs right next to each other with consistent space between the tabs easily
        
        self.expensesTab.grid(row=0, column=1, padx=2)

        #create a button have user select the budget for desires button section

        self.budgetTab = tk.Label(tabFrame, 
                        text=self.modes[2],
                        font=('Georgia', 24,),
                        fg='white',
                        bg=self.selectedColor[1],
                        relief='groove'
                        )
        
         #make it a working button
        self.budgetTab.bind('<Button>', lambda: self.set_mode(2))
        
        self.budgetTab.grid(row=0, column=2, padx=2) #place it on the screen


        #allow people to save their data

        self.saveButton = tk.Label( 
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

        #allow the program gather up to date info on placement of tabs

        self.master.update_idletasks() 

         #figure out where the main window should begin

        starty = float(tabFrame.place_info()['rely']) + float(tabFrame.winfo_height()/self.winfo_height())

        #above code allows for less messy placement of the window
        self.window.place(relx=0, rely=starty, relwidth=1, relheight=1-starty) 

        #set up the frames that display the data
        
        self.incomeFrame = None 
        self.incomeAnalysisFrame = None
        self.spendingsFrame = None
        self.investmentsFrame = None

        self.mode(0) #set default mode
        self.revive_data() # get data previously saved

        #we put this last to make sure users do not accidentally save unused data

        self.saveButton.bind('<Button>', self.save_data) 

        #keep the frame up to date on the placement of all the widgets

        self.master.update()

    def set_mode(self, value):
        pass 
    def save_data(self):
        pass
    def revive_data(self):
        pass

 


a = Budget_Calculator(root)

root.mainloop() #show the window

