#!/usr/bin/env python
''' Authors      : Huy Nguyen, Nhi
    Program      : GUI for the program that track culture growing
    Start        : 09/02/2018
    End          : 09/06/2018
    Dependecies  : networkx, pydot, matplotlib
'''
try:
    import tkinter as tk
    from tkinter import ttk
    import tkinter.messagebox as messageBox
    from tkinter import filedialog as fileDialog
except:
    import Tkinter as tk
    import ttk
    import tkMessageBox as messageBox
    import tkFileDialog as fileDialog
from cell import Cell
import datetime
import json

from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.figure import Figure
import matplotlib.image as mpimg
import networkx as nx
import pydot
###############################################################################
#global variable
###############################################################################
LARGE_FONT= ("Verdana", 40)
MIDDLE_FONT= ("Verdana", 30)
SMALL_FONT= ("Verdana", 20)
##function to get input for pageOne
rootFields = ['Name', 'Media', 'Optical Density', 'Volume (ml)','Date (yyyy-mm-dd)']
updateFields1 = ['Name']
updateFields2 = ['Optical Density', 'Volume (ml)','Date (yyyy-mm-dd)','Media']
diluteFields1 = ['Name','Number of children']
diluteFields2 = ['Optical Density', 'Volume (ml)']

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
        date = int(n[2])
    except ValueError:
        return False           
    try:
        x = datetime.date(year,month,date)
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
input    : controller,entries,checkName,checkDate
output   : dictionary
"""
def checkInput(controller,entries,checkName,checkDate):
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
            volume = validateInput(text,field, lambda myType: True if isFloat(myType) else False, 
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
                date = int(text[2])
                date = datetime.date(year,month,date)
                # validate the value 
                date = validateInput(date,field, lambda myType: True, 
                       lambda myVal: True if checkDate(myVal) else False )
                if date:
                    dictionary['date']= date
                else:
                    return False
            else:
                return False
        elif field =='Name':
            name = validateInput(text,field, lambda myType: True if checkName(text) else False, 
                       lambda myVal: True )
            if name:
                dictionary['name']= name
            else:
                return False
        elif field =='Media':
            media = text
            dictionary['media']= media
        elif field =='Number of children':
            numChildren = validateInput(text,field, lambda myType: True if myType.isdigit() else False, 
                       lambda myVal: True if int(myVal)>0 and int(myVal)<10 else False)
            if numChildren:
                dictionary['numChildren']= int(numChildren)
            else:
                return False
    return dictionary
"""
function : function takes in user input, check it with errorChecking function, and 
           keep promting if input is not good. If theinput is good and user accepts it, it goes to
           the nextPage of diluting or somethingelse
input    : controller,entries
output   : N/A
"""
def validateRoot(controller,entries):
    dictionary = checkInput(controller,entries,lambda x: True,lambda x: True)
    if dictionary:
        name,od,volume,media,date = dictionary['name'],dictionary['od'],dictionary['volume'],dictionary['media'],dictionary['date']
        
        # success, then make a root, set the root to the controller, and move to next phase
        if messageBox.askyesno("Congratz!!!","Are you sure to create a root that has name as  {}, od as {}, volume as {}mL,media as {},and date as {}? "
                             .format(name,od,volume,media,date)):       
            root = Cell(name=name,od=od,volume=volume,media=media,date=date)
            # show the page of PageThree
            controller.setRoot(root)

            # add the new pages to the dictionary

            controller.showFrame(PageThree)
 
"""
function : function validates the entries for updating purpose. It has 2 phases
            Phase 1 takes in the name
input    : controller,entries,leafNames
output   : N/A
"""
def validateUpdatePhase1(controller,entries,leafNames):
    dictionary = checkInput(controller,entries,lambda x: True if x in leafNames else False,lambda x: True)
    if dictionary:
        name= dictionary['name']
        # success, then make a root, set the root to the controller, and move to next phase
        if messageBox.askyesno("Updatinggg!!!","Are you sure to update the culture that has name as  {}? "
                             .format(name)):     
            # get the node, and set the node as current
            targetNode = controller.root.getNodeFromRoot(name)
    
            controller.setCurrentNode(targetNode)

            # add new page to the dictionary 

            
            controller.showFrame(UpdatePage2)

"""
function : function validates the entries for updating purpose. If the input is
           good and user accepts it, it goes to the ThirdPage
input    : controller,entries
output   : N/A
"""
def validateUpdatePhase2(controller,entries):
    currentNode = controller.getCurrentNode()
    name        = currentNode.name
    currentDate = currentNode.date[-1]
    dictionary = checkInput(controller,entries,lambda x: True,lambda x: True if x>= currentDate else False)
    if dictionary:
        od,volume,media,date = dictionary['od'],dictionary['volume'],dictionary['media'],dictionary['date']
        # success, then make a root, set the root to the controller, and move to next phase
        if messageBox.askyesno("Updatinggg!!!","Are you sure to update the node that has name as  {}, od as {}, volume as {}mL, media as {}, and date as {}? "
                             .format(name,od,volume,media,date)):     
            # update the node
            currentNode.update(od,date,volume)
            # go back to PageThree
            controller.showFrame(PageThree)
            
"""
function : function validates the entries for diluting purpose. It has 2 phases
            Phase 1 prompting for name of the culture, and the number of dilution will happens.
input    : controller,entries,leafNames
output   : N/A
"""
def validateNodeDilutePhase1(controller,entries,leafNames):
    dictionary = checkInput(controller,entries,lambda x: True if x in leafNames else False,lambda x: True )
    if dictionary:
        name,numChildren = dictionary['name'],dictionary['numChildren']
        # success, then make get the current node to dilute, number of children, the date, then move on to phase 2
        if messageBox.askyesno("Congratz!!!","Are you sure to dilute the node that has name as  {} into {} children cultures? "
                             .format(name,numChildren)):     
            # update the current Node 
            currentNode = controller.root.getNodeFromRoot(dictionary['name'])
            controller.setCurrentNode(currentNode)
            # set the number of children 
            controller.setNumberChildren(numChildren)


            # go to phase 2 of dilution
            controller.showFrame(DilutePage2)   

"""
function : function validates the entries for diluting purpose. It has 2 phase, 
            Phase 2 asks for the od and volume of those cultures
input    : controller,entries
output   : N/A
"""
def validateNodeDilutePhase2(controller,entries):
    # the the number of children so we know how many loop we are going through
    numChildren = controller.getNumberChildren()
    # get the current to add
    currentNode = controller.getCurrentNode()
    name        = currentNode.name
    volume      = currentNode.volume
    size        = len(diluteFields2)
    check       = True
    currentDate = currentNode.date[-1]
    # store info for diluting our Cell objects
    ods         = []
    volumes     = []
    names       = []
    dateEntry   = [entries[0]]
    dictionary  = checkInput(controller,dateEntry,lambda x: True,lambda x: True if x>= currentDate else False)

    if dictionary:
        date = dictionary['date']
    else:
        check = False
        return
    for i in range(numChildren):
        childName  = name+"_"+str(i)
        names.append(childName)
        dictionary = checkInput(controller,entries[i*size+1:i*size+size+1],lambda x: True ,lambda x: True )
        if not dictionary:
            check   = False
            ods     = []
            volumes = []
            names   = []
            return
        else:
            ods.append(dictionary['od'])
            volumes.append(dictionary['volume'])
    # CHECK FOR THE SUM
    if sum(volumes) <=  volume:
        if sum(volumes) <  volume:
            messageBox.showwarning("Warning!!!","Be careful, it looks like the newVolumes is less than the current culture volume!!!")
    else:
        check = False
        messageBox.showerror("Value Error","Attention folks, sum of the volumes is greater to our old volume, you will be need to retype the infos!!!")
        return
    if check:       
        culture = "name: {}, od: {}, volume: {} \n"
        result  = ""
        for i in range(numChildren):
            result+=culture.format(names[i],ods[i],volumes[i])
        message = "Are you sure to dilute culture {} as follow \n{} with date as {} ? ".format(name,result,date)
        # success, then dilute, and go back to PageThree
        if messageBox.askyesno("Dilutinggg!!!",message):     
            # dilute the node
            currentNode.setChildren(ods = ods,volumes= volumes,dateObserve =date)

            # go back to PageThree
            controller.showFrame(PageThree) 
        else:
            return
                    
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

###############################################################################
## helper visualize using networkx
###############################################################################
"""
function : Quick function to add a date and unique culture name to a dictionary. 
input    : dictionary,date,name
output   : N/A
"""   
def adddate(dictionary,date,name):
    if date in dictionary:
        dictionary[date].append(name)
    else:
        dictionary[date] = [name]
    
"""
function : Given a digraph, draw accordingly to options
input    : DG,typeErrorMess,ValueErrorMess
output   : graph (pydot)
"""   
def specificDraw(G,media):
    # generate a digraph for Dot
    graph = pydot.Dot(graph_type='digraph')
    d = {}
    try:
        nodes = G.node()
    except:
        nodes = G.node
    newNode = pydot.Node("media: {}".format(media),style="filled", fillcolor="green")
    graph.add_node(newNode)
    newNode.obj_dict['name'] = media
    for n in nodes:
        attribute = G.node[n]
        name = "name: {}\ndate: {}\nod: {}\nvolume: {}ml".format(attribute['label'],attribute['date'],attribute['od'],attribute['volume'])
        d[n] = name
        newNode = pydot.Node(name)
        newNode.obj_dict['name'] = name
        graph.add_node(newNode)
    for e in G.edges():
        parent    = e[0]
        children  = e[1]
        attribute = G[parent][children]
        v         = float(attribute['volume'])
        add       = float(attribute['add'])
        if attribute["type"] =="update":
            newE      = pydot.Edge(d[parent],d[children],color="blue")
        else:
            newE      = pydot.Edge(d[parent],d[children], label ="{}ml+{}ml".format(v-add,add),fontsize="10.0", color="black")
        graph.add_edge(newE)
        
    return graph

"""
function : Given root, draw a plot, x-axis indicate time line, y axis is just to space our graph
           Our main plot is a graph, with the root is the starting point, directed edge from
           1 culture to other to show diluting process, and directed edge from 1 culture to 1 other
           for updating. 
           
input    : root (Cell)
output   : DG, a
"""   
def visualization(root):
    ## create a digraph
    DG = nx.DiGraph()
    def dfs(node):
        if node:
            dates    = ["{}-{}-{}".format(k.year,k.month,k.day) for k in node.date]
            ods     = node.od
            # add node as the beginning 
            name    = node.name
            volume  = node.volume
            add     = node.add
            DG.add_node("{}({})".format(name,dates[0]),label = name,volume = volume,add = add,od = ods[0],date =dates[0])
            for i in range(1,len(dates)):
                add = 0
                # add the updating node
                currentName = "{}({})".format(name,dates[i])
                parentName = "{}({})".format(name,dates[i-1])
                DG.add_node(currentName,label = name,volume = volume,add = add,od = ods[i],date =dates[i])
                DG.add_edge(parentName,currentName,volume= volume,add = add,type="update")

            
            # add edge from parent            
            if node.parent:
                parentdates = ["{}-{}-{}".format(k.year,k.month,k.day) for k in node.parent.date]
                parentName = "{}({})".format(node.parent.name,parentdates[-1])
                nodeName   = "{}({})".format(node.name,dates[0])
                volume     = node.volume
                DG.add_edge(parentName,nodeName,volume= volume,add = node.add,type="dilute")
            # at leaf node, add normally using adddate
            # else, will have to add the current node as a dictionary
            if node.children:
                name = "{}({})".format(node.name,dates[-1])
                dates = []
                for c in node.children:

                    cdates = ["{}-{}-{}".format(k.year,k.month,k.day) for k in c.date]        
                    cName = "{}({})".format(c.name,cdates[0])
                    dates.append(cName)
            for child in node.children:
                dfs(child)
                
    dfs(root)  
    ## drawing
    graph = specificDraw(DG,root.media)
    return graph
###############################################################################
## functions create a window to read, save using tinker
## and readIn that read a js in, store in root
## and writeOut that takes root in, store as a json file
###############################################################################
"""
function : given the controller, and the currentFrame, read file in and store 
            as a root in the controller
input    : controller, master
output   : N/A
"""   
def openFile(controller,master):
    infile = fileDialog.askopenfile(parent=master,mode='rb',title='Open File')
    if infile:
        root   = readIn(infile)
        # set controller root as root
        controller.setRoot(root)
    
        # go to page done
        controller.showFrame(PageThree)
    
"""
function : function that reads in a json text file, and parse info into a Cell object
input    : infile
output   : root (Cell object)
"""   
def readIn(infile):
    try: 
        dictionary = json.load(infile)
    except:
        dictionary = json.load(open(infile.name,'r'))
    def dfs(d):
        if d:
            name     = d["name"]     
            od       = d["od"]   
            date      = []
            for k in d["date"]:

                k = [int(i) for i in k.split("-")]
                date.append(datetime.date(k[0],k[1],k[2]))

            volume   = d["volume"] 
            add      = d["add"]
            media    = d["media"]
            children = []
            node     = Cell(name=name,od=od,volume=volume,media=media)
            node.date = date
            node.od  = od
            node.add = add
            for child in d["children"]:
                # create the childNode
                childNode        = dfs(child)
                childNode.parent = node
                children.append(childNode)
            node.children = children
            return node
    return dfs(dictionary)

"""
function : given the controller, and the currentFrame, write out json file
input    : controller, master
output   : N/A
"""   
def saveTxtFile(controller,master):
    outfile = fileDialog.asksaveasfile(parent=master,mode='w',title='Save File')
    dictionary = controller.getRoot().toDictionary()
    # write out
    if outfile:
        writeOut(outfile,dictionary)

    # go to page Three
    controller.showFrame(DonePage)
    
"""
function : function that reads given a cell, ask user for a file to write to
input    : outfile,dictionary
output   : N/A
"""   
def writeOut(outfile,dictionary):
    # write out
    json.dump(dictionary, outfile,indent=4)
    
"""
function : given the controller, and the currentFrame, write out png file
input    : controller, master
output   : N/A
"""   
def saveVisualizationFile(controller,master):
    root = controller.getRoot()
    graph = visualization(root)
    outfile = fileDialog.asksaveasfile(parent=master,mode='w',title='Save File')
    if outfile and graph:
        graph.write_png(outfile.name)
    controller.showFrame(DonePage)
###############################################################################
## classes for handling frames
###############################################################################
# Main class (controller), this controller stored frames info, and root info
class Main(tk.Tk):

    def __init__(self, *args, **kwargs):
        
        tk.Tk.__init__(self, *args, **kwargs)
        self.container = tk.Frame(self)

        self.container.pack(side="top", fill="both", expand = True)

        self.container.grid_rowconfigure(0, weight=1)
        self.container.grid_columnconfigure(0, weight=1)
        self.frames = {}
        # instance variable for the tracking process
        self.root = None
        self.currentNode = None
        self.leaves = []
        self.numberChildren = 0
        self.date = datetime.date.today()
        self.pages = [StartPage, PageOne, PageTwo, PageThree, UpdatePage1,UpdatePage2, DilutePage1, DilutePage2,DonePage]
        
        for F in self.pages:

            frame = F(self.container, self)

            self.frames[F] = frame

            frame.grid(row=0, column=0, sticky="nsew")

        self.showFrame(StartPage)
        self.createCanvas()
        self.openImage()
    def openImage(self):
        img = mpimg.imread("NH.jpg")
        self.ax1.imshow(img)
        self.canvas1.draw()
    def createCanvas(self):
        """ Add a canvas to plot images """        
        self.fig1 = Figure(frameon=False, figsize=(2, 2))
        self.canvas1 = FigureCanvasTkAgg(self.fig1, master=self.frames[StartPage])
        self.canvas1.get_tk_widget().pack(fill=tk.X, expand=1)
        self.ax1 = self.fig1.add_axes([0, 0, 1, 1])
        self.ax1.axis('off')        
    # bring the current frame up
    def showFrame(self, cont):
        frame = self.frames[cont]
        frame.tkraise()
        # create event 
        frame.event_generate("<<ShowFrame>>")
    # assign root from the user input
    def setRoot(self,root):
        self.root = root
    def getRoot(self):
        return self.root
    # append to the leaves
    def addLeaves(self,names):
        self.leaves.extend(names)
    # set and get the current Node from the user input
    def setCurrentNode(self,currentNode):
        self.currentNode = currentNode
    def getCurrentNode(self):
        return self.currentNode  
    # set and get the numberChildren from the user input
    def setNumberChildren(self,numberChildren):
        self.numberChildren = numberChildren
    def getNumberChildren(self):
        return self.numberChildren
    # set and get the numberChildren from the user input
    def setDate(self,date):
        self.date = date
    def getDate(self):
        return self.date
# Start Page, to create a new experiment from cratch of to continue from old one       
class StartPage(tk.Frame):

    def __init__(self, parent, controller):
        self.controller = controller
        tk.Frame.__init__(self,parent)
        label = tk.Label(self, text="Welcome to the Culture Tracking Program", font=LARGE_FONT)
        label.pack(pady=10,padx=10)
        button1 = ttk.Button(self, text="Start new experiment",
                            command=lambda: controller.showFrame(PageOne))
        button1.pack()
        button2 = ttk.Button(self, text="Continue old experiment",
                            command=lambda: controller.showFrame(PageTwo))
        button2.pack()

# Page One for create new experiment 
class PageOne(tk.Frame):

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.controller = controller
        label = tk.Label(self, text="Start new experiment", font=LARGE_FONT)
        label.pack(pady=10,padx=10)
        # generate entry to store info
        ents = makeForm(self, rootFields)
        # enter means storing info, validate the values, only validate after user
        # press OK button
        button1 = ttk.Button(self, text='OK',
                        command=(lambda e=ents: validateRoot(controller,e)))
        button1.pack(side=tk.LEFT, padx=5, pady=5)
        
        
        # buttons to navigate through frames
        button2 = ttk.Button(self, text="Back to Home",
                            command=lambda: controller.showFrame(StartPage))
        button2.pack()

        button3 = ttk.Button(self, text="Continue old experiment",
                            command=lambda: controller.showFrame(PageTwo))
        button3.pack()

# Page One for reuse old experiment 
class PageTwo(tk.Frame):

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.controller = controller
        label = tk.Label(self, text="Continue old experiment", font=LARGE_FONT)
        label.pack(pady=10,padx=10)
        
        # buttons 
        ## button to open file to real
        button1 = ttk.Button(self, text="Open File",
                            command=lambda: openFile(controller,self))
        button1.pack()
        button2 = ttk.Button(self, text="Back to Home",
                            command=lambda: controller.showFrame(StartPage))
        button2.pack()

        button3 = ttk.Button(self, text="Start new experiment",
                            command=lambda: controller.showFrame(PageOne))
        button3.pack()

# Page Three that let user dilute, update, or done
class PageThree(tk.Frame):

    def __init__(self, parent, controller):
        tk.Frame.__init__(self,parent)
        self.controller = controller
        label = tk.Label(self, text="Do you want to update, dilute, or are you done?", font=LARGE_FONT)
        label.pack(pady=10,padx=10)
        button = ttk.Button(self, text="Update",
                            command=lambda: controller.showFrame(UpdatePage1))
        button.pack()
        button2 = ttk.Button(self, text="Dilute",
                            command=lambda: controller.showFrame(DilutePage1))
        button2.pack()
        button3 = ttk.Button(self, text="Done",
                            command=lambda: controller.showFrame(DonePage))
        button3.pack() 
        
# Update Page 1
class UpdatePage1(tk.Frame):

    def __init__(self, parent, controller):
        tk.Frame.__init__(self,parent)
        self.controller = controller
        self.bind("<<ShowFrame>>", self.on_show_frame)
    # showing event
    def on_show_frame(self, event):
        # destroy all widget
        for widget in self.winfo_children():
            widget.destroy()
        leafNames =self.controller.root.getLeafNames()
        label = tk.Label(self, text="Please type in the culture you want to update from the following list",
                         font=MIDDLE_FONT)        
        label.pack(pady=10,padx=10)
        label = tk.Label(self, text=",".join(leafNames),
                         font=SMALL_FONT)        
        label.pack(pady=10,padx=10)
        # create entries for this update
        ents = makeForm(self, updateFields1)
        # enter means storing info, validate the values, only validate after user
        # press OK button
        button1 = ttk.Button(self, text='OK',
                        command=(lambda e=ents: validateUpdatePhase1(self.controller,ents,leafNames)))
        button1.pack(side=tk.LEFT, padx=5, pady=5)
        # go back to Third Page
        button2 = ttk.Button(self, text='Back',
                        command=lambda: self.controller.showFrame(PageThree))
        button2.pack(side=tk.LEFT, padx=5, pady=5)
        
# Update Page 1
class UpdatePage2(tk.Frame):

    def __init__(self, parent, controller):
        tk.Frame.__init__(self,parent)
        self.controller = controller
        self.bind("<<ShowFrame>>", self.on_show_frame)
    # showing event
    def on_show_frame(self, event):
        # destroy all widget
        for widget in self.winfo_children():
            widget.destroy()
        # labeling our frame
        # get the current to add
        currentNode = self.controller.getCurrentNode()    
        name        = currentNode.name
        od          = currentNode.od[-1]
        volume      = currentNode.volume
        date        = currentNode.date[-1] 
        print (currentNode.date)
        label = tk.Label(self, text="Please type in the following information for the current culture {}".format(name),
                         font=MIDDLE_FONT)
        label.pack(pady=10,padx=10)   
        
        label = tk.Label(self, text="We are updating culture {}, current od {}, current volume {}ml, and last updated on {} ".format(name,od,volume,date),
                         font=SMALL_FONT)
        label.pack(pady=10,padx=10) 
        # create entries for this update
        ents = makeForm(self, updateFields2)
        # enter means storing info, validate the values, only validate after user
        # press OK button
        button1 = ttk.Button(self, text='OK',
                        command=(lambda e=ents: validateUpdatePhase2(self.controller,ents)))
        button1.pack(side=tk.LEFT, padx=5, pady=5)
        # go back to Third Page
        button2 = ttk.Button(self, text='Back',
                        command=lambda: self.controller.showFrame(UpdatePage1))
        button2.pack(side=tk.LEFT, padx=5, pady=5)
        
# Dilute Page, phase 1        
class DilutePage1(tk.Frame):

    def __init__(self, parent, controller):
        tk.Frame.__init__(self,parent)
        self.controller = controller
        self.bind("<<ShowFrame>>", self.on_show_frame)
    # showing event
    def on_show_frame(self, event):
        # destroy all widget
        for widget in self.winfo_children():
            widget.destroy()
        leafNames =self.controller.root.getLeafNames()
        label = tk.Label(self, text="Please type in the culture you want to dilute from the following list",
                         font=MIDDLE_FONT)        
        label.pack(pady=10,padx=10)
        label = tk.Label(self, text=",".join(leafNames),
                         font=SMALL_FONT)        
        label.pack(pady=10,padx=10)      
        # create entries for this update
        ents = makeForm(self, diluteFields1)
        # enter means storing info, validate the values, only validate after user
        # press OK button
        button1 = ttk.Button(self, text='OK',
                        command=(lambda e=ents: validateNodeDilutePhase1(self.controller,ents,leafNames)))
        button1.pack(side=tk.LEFT, padx=5, pady=5)
        # go back to Third Page
        button2 = ttk.Button(self, text='Back',
                        command=lambda: self.controller.showFrame(PageThree))
        button2.pack(side=tk.LEFT, padx=5, pady=5)   
        
 # Dilute Page, phase 2  , only invoke or show after page1 is through
class DilutePage2(tk.Frame):

    def __init__(self, parent, controller):
        tk.Frame.__init__(self,parent)
        self.controller = controller
        self.bind("<<ShowFrame>>", self.on_show_frame)
    def on_show_frame(self, event):
        # destroy all widget
        for widget in self.winfo_children():
            widget.destroy()
        # get the number and name
        # the the number of children so we know how many loop we are going through
        numChildren = self.controller.getNumberChildren()
        # get the current to add
        currentNode = self.controller.getCurrentNode()    
        name        = currentNode.name
        od          = currentNode.od[-1]
        volume      = currentNode.volume
        date        = currentNode.date[-1] 
        # labeling our frame
        label = tk.Label(self, text="Please type in the following information for the children cultures",
                         font=MIDDLE_FONT)
        label.pack(pady=10,padx=10)   
        
        label = tk.Label(self, text="We are diluting culture {}, current od {}, current volume {}ml, and last updated on {} ".format(name,od,volume,date),
                         font=SMALL_FONT)
        label.pack(pady=10,padx=10) 
        # get the date
        dateEntry  = makeForm(self,["Date (yyyy-mm-dd)"])[0]
        # create entries for this update
        entries = [dateEntry]
        for i in range(numChildren):
            childName = name+"_"+str(i)
            label = tk.Label(self, text=childName,
                         font=SMALL_FONT)
            label.pack(pady=10,padx=10)   
            ents = makeForm(self, diluteFields2)
            entries.extend(ents)
        # enter means storing info, validate the values, only validate after user
        # press OK button
        button1 = ttk.Button(self, text='OK',
                        command=(lambda e=ents: validateNodeDilutePhase2(self.controller,entries)))
        button1.pack(side=tk.LEFT, padx=5, pady=5)
        # go back to dilutepage1 Page
        button2 = ttk.Button(self, text='Back',
                        command=lambda: self.controller.showFrame(DilutePage1))
        button2.pack(side=tk.LEFT, padx=5, pady=5)
#         
class DonePage(tk.Frame):

    def __init__(self, parent, controller):
        tk.Frame.__init__(self,parent)
        label = tk.Label(self, text="We are done, what would you like to do?", font=LARGE_FONT)
        label.pack(pady=10,padx=10)
        button1 = ttk.Button(self, text="Quit",
                            command=lambda: controller.destroy())
        button1.pack()
        button2 = ttk.Button(self, text="Main Menu",
                            command=lambda: controller.showFrame(StartPage))
        button2.pack()
        button3 = ttk.Button(self, text="Save",
                            command=lambda: saveTxtFile(controller,self))
        button3.pack()
        button4 = ttk.Button(self, text="Visualize",
                            command=lambda: saveVisualizationFile(controller,self))
        button4.pack()
###############################################################################
## running the program
###############################################################################
app = Main()
app.geometry("1280x720")
app.mainloop()