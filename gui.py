#!/usr/bin/env python
''' Authors      : Huy Nguyen, Nhi
    Program      : GUI for the program
    Start        : 08/04/2018
    End          : /2018
'''
try:
    import tkinter as tk
    from tkinter import ttk
except:
    import Tkinter as tk
    from Tkinter import ttk
try:
    import tkinter.messagebox as messageBox
except:
    import tkMessageBox as messageBox
from cell import Cell
import cellTracking
import datetime

###############################################################################
#global variable
###############################################################################
LARGE_FONT= ("Verdana", 40)
MIDDLE_FONT= ("Verdana", 30)
##function to get input for pageOne
rootFields = ['Name', 'Media', 'Optical Density', 'Volume (ml)','Date (yyyy-mm-dd)']
nodeFields = ['Name', 'Optical Density', 'Volume (ml)','Date (yyyy-mm-dd)']
dictionary = {}
###############################################################################
## helper functions, validating
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
           keep promting if input is not good. 
input    : controller,entries,checkName
output   : dictionary
"""
def checkInput(controller,entries,checkName):
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
        elif field =='Name':
            name = validateInput(text,field, lambda myType: True if checkName(text) else False, 
                       lambda myVal: True )
            dictionary['name']= name
        else:
            media = text
            dictionary['media']= media
    return dictionary
"""
function : function takes in user input, check it with errorChecking function, and 
           keep promting if input is not good. If theinput is good and user accepts it, it goes to
           the nextPage of diluting or somethingelse
input    : controller,entries
output   : N/A
"""
def validateRoot(controller,entries):
    dictionary = checkInput(controller,entries,lambda x: True)
    name,od,volume,media,date = dictionary['name'],dictionary['od'],dictionary['volume'],dictionary['media'],dictionary['date']
    
    # success, then make a root, set the root to the controller, and move to next phase
    if messageBox.askyesno("Congratz!!!","Are you sure to create a root that has name as  {}, od as {}, volume as {}mL,media as {},and date as {}? "
                         .format(name,od,volume,media,date)):       
        root = Cell(name=dictionary['name'],od =dictionary['od'],volume=dictionary['volume'],
                media = dictionary['media'], day =dictionary['date'])
        # show the page of PageThree
        controller.setRoot(root)
#        print (controller.getRoot().name)
        # add the new pages to the dictionary
        for F in controller.phase2:

            frame = F(controller.container, controller)

            controller.frames[F] = frame

            frame.grid(row=0, column=0, sticky="nsew")
        controller.showFrame(PageThird)
 
"""
function : function takes in user input, check it with errorChecking function, and 
           keep promting if input is not good. If theinput is good and user accepts it, it goes to
           the nextPage of diluting or somethingelse
input    : controller,entries
output   : N/A
"""
def validateNodeUpdate(controller,entries,leafNames):
    dictionary = checkInput(controller,entries,lambda x: True if x in leafNames else False)
    name,od,volume,date = dictionary['name'],dictionary['od'],dictionary['volume'],dictionary['date']
    # success, then make a root, set the root to the controller, and move to next phase
    if messageBox.askyesno("Congratz!!!","Are you sure to update a node that has name as  {}, od as {}, volume as {}mL, and date as {}? "
                         .format(name,od,volume,date)):     
        # update the node
        targetNode = controller.root.getNodeFromRoot(dictionary['name'])
        targetNode.update(od,date)
        # go back to pageThird
        controller.showFrame(PageThird)
        
                       
"""
function : given the fields for user to fill in, make Entries for the frame
input    : master,entries
output   : list of Entries
"""          

def makeForm(master, fields):
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
        self.container = tk.Frame(self)

        self.container.pack(side="top", fill="both", expand = True)

        self.container.grid_rowconfigure(0, weight=1)
        self.container.grid_columnconfigure(0, weight=1)
        self.frames = {}
        self.root = None
        self.phase1 = [StartPage, PageOne, PageTwo]
        self.phase2 = [PageThird, UpdatePage, DilutePage, DonePage]
        for F in self.phase1:

            frame = F(self.container, self)

            self.frames[F] = frame

            frame.grid(row=0, column=0, sticky="nsew")

        self.showFrame(StartPage)

    def showFrame(self, cont):

        frame = self.frames[cont]
        frame.tkraise()
    def setRoot(self,root):
        self.root = root
    def getRoot(self):
        return self.root
        
class StartPage(tk.Frame):

    def __init__(self, parent, controller):
        tk.Frame.__init__(self,parent)
        label = tk.Label(self, text="Welcome to the Culture Tracking Program", font=LARGE_FONT)
        label.pack(pady=10,padx=10)
        button = ttk.Button(self, text="Start new experiment",
                            command=lambda: controller.showFrame(PageOne))
        button.pack()
        button2 = ttk.Button(self, text="Continue old experiment",
                            command=lambda: controller.showFrame(PageTwo))
        button2.pack()


class PageOne(tk.Frame):

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        label = tk.Label(self, text="Start new experiment", font=LARGE_FONT)
        label.pack(pady=10,padx=10)
        # generate entry to store info
        ents = makeForm(self, rootFields)
        # enter means storing info, validate the values, only validate after user
        # press OK button
        b1 = ttk.Button(self, text='OK',
                        command=(lambda e=ents: validateRoot(controller,e)))
        b1.pack(side=tk.LEFT, padx=5, pady=5)
        
        
        # buttons to navigate through frames
        button1 = ttk.Button(self, text="Back to Home",
                            command=lambda: controller.showFrame(StartPage))
        button1.pack()

        button2 = ttk.Button(self, text="Continue old experiment",
                            command=lambda: controller.showFrame(PageTwo))
        button2.pack()


class PageTwo(tk.Frame):

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        label = tk.Label(self, text="Continue old experiment", font=LARGE_FONT)
        label.pack(pady=10,padx=10)
        
        # buttons to navigate through frames
        button1 = ttk.Button(self, text="Back to Home",
                            command=lambda: controller.showFrame(StartPage))
        button1.pack()

        button2 = ttk.Button(self, text="Start new experiment",
                            command=lambda: controller.showFrame(PageOne))
        button2.pack()
        
class PageThird(tk.Frame):

    def __init__(self, parent, controller):
        tk.Frame.__init__(self,parent)
        self.root = None
        label = tk.Label(self, text="Do you want to update, dilute, or are you done?", font=LARGE_FONT)
        label.pack(pady=10,padx=10)
        button = ttk.Button(self, text="Update",
                            command=lambda: controller.showFrame(UpdatePage))
        button.pack()
        button2 = ttk.Button(self, text="Dilute",
                            command=lambda: controller.showFrame(DilutePage))
        button2.pack()
        button3 = ttk.Button(self, text="Done",
                            command=lambda: controller.showFrame(DonePage))
        button3.pack()     

class UpdatePage(tk.Frame):

    def __init__(self, parent, controller):
        tk.Frame.__init__(self,parent)
        leafNames =",".join(controller.root.getLeafNames()) 
        label = tk.Label(self, text="Please type in the culture you want to update, it can only come from the following list: {}\n".format(leafNames),
                         font=MIDDLE_FONT)
        label.pack(pady=10,padx=10)        
        # create entries for this update
        ents = makeForm(self, nodeFields)
        # enter means storing info, validate the values, only validate after user
        # press OK button
        b1 = ttk.Button(self, text='OK',
                        command=(lambda e=ents: validateNodeUpdate(controller,ents,leafNames)))
        b1.pack(side=tk.LEFT, padx=5, pady=5)
class DilutePage(tk.Frame):

    def __init__(self, parent, controller):
        tk.Frame.__init__(self,parent)
        leafNames =",".join(controller.root.getLeafNames()) 
        label = tk.Label(self, text="Please type in the culture you want to dilute, it can only come from the following list: {}\n".format(leafNames),
                         font=MIDDLE_FONT)
        label.pack(pady=10,padx=10)        
        # create entries for this update
        ents = makeForm(self, nodeFields)
        # enter means storing info, validate the values, only validate after user
        # press OK button
        b1 = ttk.Button(self, text='OK',
                        command=(lambda e=ents: validateNodeUpdate(controller,ents,leafNames)))
        b1.pack(side=tk.LEFT, padx=5, pady=5)
        # Ok button
#        b1 = ttk.Button(self, text='OK',
#                        command=(lambda e=ents: validate(controller,e)))
#        b1.pack(side=tk.LEFT, padx=5, pady=5)    
class DonePage(tk.Frame):

    def __init__(self, parent, controller):
        tk.Frame.__init__(self,parent)
        label = tk.Label(self, text="We are done, let us save our process", font=LARGE_FONT)
        label.pack(pady=10,padx=10)
        button = ttk.Button(self, text="Quit",
                            command=lambda: controller.destroy())
        button.pack()
        button2 = ttk.Button(self, text="Main Menu",
                            command=lambda: controller.showFrame(StartPage))
        button2.pack()
###############################################################################
## running the program
###############################################################################
app = Main()
app.mainloop()