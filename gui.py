#!/usr/bin/env python
''' Authors      : Huy Nguyen, Nhi
    Program      : GUI for the program
    Start        : 08/04/2018
    End          : /2018
'''
try:
    import tkinter as tk
    import messagebox as messageBox
except:
    import Tkinter as tk
    import tkMessageBox as messageBox
from cell import Cell
import cellTracking
import datetime

###############################################################################
#global variable
###############################################################################
LARGE_FONT= ("Verdana", 40)
##function to get input for pageOne
fields = ['Name of the experiment', 'Name of the Media', 'Optical Density', 'Volume (ml)','Date (yyyy-mm-dd)']
###############################################################################
## helper functions
###############################################################################
## check if a number is float:
def isFloat(n):
    try:
        x = float(n)
    except ValueError:
        return False
    else:
        return True
    
## check if a number is date:
def isDate(n):
    n = n.split("-")
    if len(n)!=3:
        return False
    try:
        year = int(n[0])
    except ValueError:
        return False
    try:
        month = int(n[1])
    except ValueError:
        return False 
    try:
        day = int(n[2])
    except ValueError:
        return False           
    try:
        x = datetime.date(year,month,day)
    except ValueError:
        return False
    else:
        return True
 

"""
function : function takes in user input, check it with errorChecking function, and 
           keep promting if input is not good
input    : message,typeChecking,valueChecking
output   : value of message
"""
def validateInput(message,field,typeChecking,valueChecking):
    
    if typeChecking(message):
        if valueChecking(message):
            return message
        else:
            messageBox.showerror ("Value Error","Sorry, your value {} in field {} is not within range!!!".format(message,field))
    else:
        messageBox.showerror("Type Error","Sorry, your type {} in field {} is not corrected!!!".format(message,field))
    return None



"""
function : function takes in user input, check it with errorChecking function, and 
           keep promting if input is not good
input    : entries
output   : N/A
"""
# fetching info from the entries, error checking as well
def validate(entries):
    dictionary = {}
    for entry in entries:
        field = entry[0]
        text  = entry[1].get()
        if field == "Optical Density":
            od  = validateInput(text,field, lambda myType: True if isFloat(myType) else False, 
                       lambda myVal: True if float(myVal)>0 and float(myVal)<1 else False)
            if od:
                dictionary['od']= float(od)
            else:
                return False
        elif field == "Volume (ml)":
            volume = validateInput(text,field, lambda myType: True if cellTracking.isFloat(myType) else False, 
                       lambda myVal: True if float(myVal)>0 and float(myVal)<1000 else False)
            if volume:
                dictionary['volume']= float(volume)
            else:
                return False
        elif field =='Date (yyyy-mm-dd)':
            date = validateInput(text,field, lambda myType: True if isDate(myType) else False, 
                       lambda myVal: True)
            if date:
                text = text.split("-")
                year = int(text[0])
                month = int(text[1])
                day = int(text[2])
                date = datetime.date(year,month,day)
                dictionary['date']= date
            else:
                return False
        elif field =='Name of the experiment':
            name = text
            dictionary['name']= name
        else:
            media = text
            dictionary['media']= media
    # success
    if messageBox.askyesno("Congratz!!!","Are you sure to create a root that has name as  {}, od as {}, volume as {},media as {},and date as {}? "
                         .format(name,od,volume,media,date)):       
        root = Cell(name=dictionary['name'],od =dictionary['od'],volume=dictionary['volume'],
                media = dictionary['media'], day =dictionary['date'])
        return root
            
"""
function : After validating the user input, output Cell
input    : master,entries
output   : Cell object
"""          

def makeform(master, fields):
   entries = []
   for field in fields:
      row = tk.Frame(master)
      lab = tk.Label(row, width=30, text=field, anchor='w')
      ent = tk.Entry(row)
      row.pack(side=tk.TOP, fill=tk.X, padx=5, pady=5)
      lab.pack(side=tk.LEFT)
      ent.pack(side=tk.RIGHT, expand=tk.YES, fill=tk.X)
      entries.append((field, ent))
   return entries

# classes for handling frames
class Main(tk.Tk):

    def __init__(self, *args, **kwargs):
        
        tk.Tk.__init__(self, *args, **kwargs)
        container = tk.Frame(self)

        container.pack(side="top", fill="both", expand = True)

        container.grid_rowconfigure(0, weight=1)
        container.grid_columnconfigure(0, weight=1)
        print (container)
        self.frames = {}

        for F in (StartPage, PageOne, PageTwo):

            frame = F(container, self)

            self.frames[F] = frame

            frame.grid(row=0, column=0, sticky="nsew")

        self.showFrame(StartPage)

    def showFrame(self, cont):

        frame = self.frames[cont]
        frame.tkraise()

        
class StartPage(tk.Frame):

    def __init__(self, parent, controller):
        tk.Frame.__init__(self,parent)
        label = tk.Label(self, text="Welcome to the Culture Tracking Program", font=LARGE_FONT)
        label.pack(pady=10,padx=10)
        button = tk.Button(self, text="Start new experiment",
                            command=lambda: controller.showFrame(PageOne))
        button.pack()
        button2 = tk.Button(self, text="Continue old experiment",
                            command=lambda: controller.showFrame(PageTwo))
        button2.pack()


class PageOne(tk.Frame):

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        label = tk.Label(self, text="Start new experiment", font=LARGE_FONT)
        label.pack(pady=10,padx=10)
        # generate entry to store info
        ents = makeform(self, fields)
        # enter means storing info, validate the values, only validate after user
        # press OK button
        b1 = tk.Button(self, text='OK',
                        command=(lambda e=ents: validate(e)))
        b1.pack(side=tk.LEFT, padx=5, pady=5)
        
        
        # buttons to navigate through frames
        button1 = tk.Button(self, text="Back to Home",
                            command=lambda: controller.showFrame(StartPage))
        button1.pack()

        button2 = tk.Button(self, text="Continue old experiment",
                            command=lambda: controller.showFrame(PageTwo))
        button2.pack()


class PageTwo(tk.Frame):

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        label = tk.Label(self, text="Continue old experiment", font=LARGE_FONT)
        label.pack(pady=10,padx=10)
        
        # buttons to navigate through frames
        button1 = tk.Button(self, text="Back to Home",
                            command=lambda: controller.showFrame(StartPage))
        button1.pack()

        button2 = tk.Button(self, text="Start new experiment",
                            command=lambda: controller.showFrame(PageOne))
        button2.pack()
        

def main():
    app = Main()
    app.mainloop()
main()