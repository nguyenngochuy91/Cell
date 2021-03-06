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
import os
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
input    : controller,entries,checkName,checkDate,checkOd
output   : dictionary
"""
def checkInput(controller,entries,checkName,checkDate,checkOd):
    dictionary = {}
    for entry in entries:
        field = entry[0]
        text  = entry[1].get()
        if field == "Optical Density":
            od  = validateInput(text,field, lambda myType: True if isFloat(myType) else False, 
                       lambda myVal: True if float(myVal)>0 and float(myVal)<1 else False)
            if od:
                od = validateInput(text,field, lambda myType: True , 
                       lambda myVal: True if checkOd(od) else False)
                if od:
                    dictionary['od']= float(od)
                else:
                    return False
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
                       lambda myVal: True if int(myVal)>0 and int(myVal)<=10 else False)
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
    dictionary = checkInput(controller,entries,lambda x: True,lambda x: True,lambda x: True)
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
    dictionary = checkInput(controller,entries,lambda x: True if x in leafNames else False,lambda x: True,lambda x: True)
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
    dictionary = checkInput(controller,entries,lambda x: True,lambda x: True if x>= currentDate else False,lambda x: True)
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
    dictionary = checkInput(controller,entries,lambda x: True if x in leafNames else False,lambda x: True,lambda x: True)
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
input    : controller,entries,current od
output   : N/A
"""
def validateNodeDilutePhase2(controller,entries,od):
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
    dictionary  = checkInput(controller,dateEntry,lambda x: True,lambda x: True if x>= currentDate else False,lambda x: True)

    if dictionary:
        date = dictionary['date']
    else:
        check = False
        return
    for i in range(numChildren):
        childName  = name+"_"+str(i)
        names.append(childName)
        dictionary = checkInput(controller,entries[i*size+1:i*size+size+1],lambda x: True ,lambda x: True,
                                lambda x: True if float(x)<=od else False )
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
        name = "name: {}\ndate: {}\nod: {}\nvolume: {}ml\nmedia: {}".format(attribute['label'],attribute['date'],attribute['od'],attribute['volume'],media)
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
            media   = node.media
            DG.add_node("{}({})".format(name,dates[0]),label = name,volume = volume,add = add,od = ods[0],date =dates[0],media = media)
            for i in range(1,len(dates)):
                add = 0
                # add the updating node
                currentName = "{}({})".format(name,dates[i])
                parentName = "{}({})".format(name,dates[i-1])
                DG.add_node(currentName,label = name,volume = volume,add = add,od = ods[i],date =dates[i],media = media)
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
        try:
            root   = readIn(infile)
        except:
            return 
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
    root    = controller.getRoot()
    graph = visualization(root)
    # check if user want to save this
    graph.write_png("temp")
    # mac and linux
    try:
        os.system("open temp")
    except:
        os.system("start temp")
    if messageBox.askyesno("Does this look good to you :)???"): 
        outfile = fileDialog.asksaveasfile(parent=master,mode='w',title='Save File')
        dictionary = root.toDictionary()
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
    # check if user want to save this
    graph.write_png("temp")
    # mac and linux
    try:
        os.system("open temp")
    except:
        os.system("start temp")
    if messageBox.askyesno("Does this look good to you :)???"):    
        outfile = fileDialog.asksaveasfile(parent=master,mode='w',title='Save File')
        if outfile and graph:
            graph.write_png(outfile.name)
    controller.showFrame(DonePage)
    
"""
function : given the controller,  giving the name, then set the currentNode 
            to the name, also go to the modify2
input    : controller, name
output   : N/A
"""   
def goToModify2(controller,name):
    targetNode = controller.root.getNodeFromRoot(name)
    controller.setCurrentNode(targetNode)
    controller.showFrame(ModifyPage2)
 
"""
function : given the controller,  giving index i, set up the index in the controller, show modify3 frame
input    : controller, i
output   : N/A
"""   
def goToModify3(controller,i):
    controller.setIndex(i)
    controller.showFrame(ModifyPage3) 
    
"""
function : function validates the entries for updating purpose. If the input is
           good and user accepts it, it modifies the info
input    : controller,entries
output   : N/A
"""
def modify(controller,entries):
    currentNode = controller.getCurrentNode()
    name        = currentNode.name
    index       = controller.getIndex()
    dictionary = checkInput(controller,entries,lambda x: True,lambda x: True ,lambda x: True)
    if dictionary:
        od,volume,media,date = dictionary['od'],dictionary['volume'],dictionary['media'],dictionary['date']
        # success, then make a root, set the root to the controller, and move to next phase
        if messageBox.askyesno("Modifying!!!","Are you sure to modify the node that has name as  {}, od as {}, volume as {}mL, media as {}, and date as {}? "
                             .format(name,od,volume,media,date)):     
            # update the node
            # if nothing in od,volum,media, then delete this index
            if not od or not volume or not media or not date:
                currentNode.date.pop(index)
                currentNode.od.pop(index)
            else:
                currentNode.date[index] = date
                currentNode.od[index]   = od
                currentNode.volume      = volume
                currentNode.media       = media
            # go back to PageThree
            controller.showFrame(DonePage)

"""
function : given the controller, and the currentFrame, analyze the data, learn to remind
input    : controller, master
output   : N/A
"""   
def analyzeData(controller,master):
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
        self.pages = [StartPage, PageOne, PageTwo, PageThree, UpdatePage1,UpdatePage2, DilutePage1, DilutePage2,DonePage,
                      ModifyPage1,ModifyPage2,ModifyPage3]
        self.index = None
        for F in self.pages:

            frame = F(self.container, self)

            self.frames[F] = frame

            frame.grid(row=0, column=0, sticky="nsew")

        self.showFrame(StartPage)
        self.createCanvas()
        self.openImage()
    # generating the image
    def openImage(self):
        try:
            img = mpimg.imread("NH.jpg")
        except:
            img = mpimg.imread("NH.png")
        self.ax1.imshow(img)
        self.canvas1.draw()
    def createCanvas(self):
        """ Add a canvas to plot images """        
        self.fig1 = Figure(frameon=False, figsize=(3, 3))
        self.canvas1 = FigureCanvasTkAgg(self.fig1, master=self.frames[StartPage])
        self.canvas1.get_tk_widget().pack(fill=tk.X, expand=1)
        self.ax1 = self.fig1.add_axes([0, 0, 1, 1])
        self.ax1.axis('off')    
    def getPage(self, pageClass):
        return self.frames[pageClass]
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
    # get the index and set the index
    def setIndex(self,index):
        self.index = index
    def getIndex(self):
        return self.index
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
        self.bind("<<ShowFrame>>", self.onShowFrame)
    # showing event
    def onShowFrame(self, event):
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
        self.bind("<<ShowFrame>>", self.onShowFrame)
    # showing event
    def onShowFrame(self, event):
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
        self.bind("<<ShowFrame>>", self.onShowFrame)
    # showing event
    def onShowFrame(self, event):
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
        self.bind("<<ShowFrame>>", self.onShowFrame)
    def onShowFrame(self, event):
        # destroy all widget
        for widget in self.winfo_children():
            widget.destroy()
        scrollable_body = Scrollable(self, width=10)
        # get the number and name
        # the the number of children so we know how many loop we are going through
        numChildren = self.controller.getNumberChildren()
        # get the current to add
        currentNode = self.controller.getCurrentNode()    
        name        = currentNode.name
        od          = currentNode.od[-1]
        volume      = currentNode.volume
        date        = currentNode.date[-1] 

        label = tk.Label(scrollable_body, text="Please type in the following information for the children cultures",
                         font=MIDDLE_FONT)
        label.pack(pady=10,padx=10)   
        
        label = tk.Label(scrollable_body, text="We are diluting culture {}, current od {}, current volume {}ml, and last updated on {} ".format(name,od,volume,date),
                         font=SMALL_FONT)
        label.pack(pady=10,padx=10) 
        # get the date
        dateEntry  = makeForm(scrollable_body,["Date (yyyy-mm-dd)"])[0]
        # create entries for this update
        entries = [dateEntry]
        for i in range(numChildren):
            childName = name+"_"+str(i)
            label = tk.Label(scrollable_body, text=childName,
                         font=SMALL_FONT)
            label.pack(pady=10,padx=10)   
            ents = makeForm(scrollable_body, diluteFields2)
            entries.extend(ents)
        # enter means storing info, validate the values, only validate after user
        # press OK button
        button1 = ttk.Button(scrollable_body, text='OK',
                        command=(lambda e=ents: validateNodeDilutePhase2(self.controller,entries,od)))
        button1.pack(side=tk.LEFT, padx=5, pady=5)
        # go back to dilutepage1 Page
        button2 = ttk.Button(scrollable_body, text='Back',
                        command=lambda: self.controller.showFrame(DilutePage1))
        button2.pack(side=tk.LEFT, padx=5, pady=5)
        scrollable_body.update()

# page that is done to do more thing like quit, main menu, save, visualize, analyze or modify
class DonePage(tk.Frame):

    def __init__(self, parent, controller):
        self.controller= controller
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
        
        button5 = ttk.Button(self, text="Modify",
                            command=lambda: controller.showFrame(ModifyPage1))
        button5.pack()
        
        button6 = ttk.Button(self, text="Analyze",
                            command=lambda: analyzeData(controller,self))
        button6.pack()      
        
# modification frame 1
class ModifyPage1(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self,parent)
        self.controller = controller
        self.bind("<<ShowFrame>>", self.onShowFrame)
    def onShowFrame(self, event):   
        # destroy all widget
        for widget in self.winfo_children():
            widget.destroy()
        scrollable_body = Scrollable(self, width=10)
        label = tk.Label(scrollable_body, text="Modifying graph step 1", font=LARGE_FONT)
        label.pack(pady=10,padx=10)
        # gettign the root
        root = self.controller.getRoot()
        nodeNames = root.getNames()
        buttons =[]
        for name in nodeNames:
            # create a button
            button1 = ttk.Button(scrollable_body, text=name,command = lambda name = name :goToModify2(self.controller,name))
            button1.pack()
            buttons.append(button1)

        button3 = ttk.Button(scrollable_body, text="Main Menu",
                            command=lambda: self.controller.showFrame(StartPage))
        button3.pack(side = tk.BOTTOM)
        button4 = ttk.Button(scrollable_body, text="Back",
                            command=lambda: self.controller.showFrame(DonePage))
        button4.pack(side = tk.LEFT)     
# modification frame 2
class ModifyPage2(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self,parent)
        self.controller = controller
        self.bind("<<ShowFrame>>", self.onShowFrame)
    def onShowFrame(self, event):
        for widget in self.winfo_children():
            widget.destroy()
        scrollable_body = Scrollable(self, width=10)
        label = tk.Label(scrollable_body, text="Modifying graph step 2", font=LARGE_FONT)
        label.pack(pady=10,padx=10)
        # getting the currentNode
        currentNode = self.controller.getCurrentNode()
        name = currentNode.name
        dates       = currentNode.date
        for i in range(len(dates)):
            date = dates[i]
            button1 = ttk.Button(scrollable_body, text=name+" "+str(date),command = lambda i = i :goToModify3(self.controller,i))
            button1.pack()            
        button3 = ttk.Button(scrollable_body, text="Main Menu",
                            command=lambda: self.controller.showFrame(StartPage))
        button3.pack(side = tk.BOTTOM)
        button4 = ttk.Button(scrollable_body, text="Back",
                            command=lambda: self.controller.showFrame(ModifyPage1))
        button4.pack(side = tk.LEFT)

# modification frame3   
class ModifyPage3(tk.Frame):

    def __init__(self, parent, controller):
        tk.Frame.__init__(self,parent)
        self.controller = controller
        self.bind("<<ShowFrame>>", self.onShowFrame)
    # showing event
    def onShowFrame(self, event):
        # destroy all widget
        for widget in self.winfo_children():
            widget.destroy()
        # labeling our frame
        # get the current to add
        currentNode = self.controller.getCurrentNode()  
        index       = self.controller.getIndex()
        name        = currentNode.name
        od          = currentNode.od[index]
        volume      = currentNode.volume
        date        = currentNode.date[index] 
        label = tk.Label(self, text="Please type in the following information for the following culture {}".format(name),
                         font=MIDDLE_FONT)
        label.pack(pady=10,padx=10)   
        
        label = tk.Label(self, text="We are modifying culture {}, current od {}, current volume {}ml, and  updated on {} ".format(name,od,volume,date),
                         font=SMALL_FONT)
        label.pack(pady=10,padx=10) 
        # create entries for this update
        ents = makeForm(self, updateFields2)
        # enter means storing info, validate the values, only validate after user
        # press OK button
        button1 = ttk.Button(self, text='OK',
                        command=(lambda e=ents: modify(self.controller,ents)))
        button1.pack(side=tk.RIGHT, padx=5, pady=5,anchor=tk.E)
        # go back to Third Page
        button2 = ttk.Button(self, text='Back',
                        command=lambda: self.controller.showFrame(ModifyPage2))
        button2.pack(side=tk.LEFT, padx=5, pady=5)             
# scroller class to imbed into my frame
class Scrollable(tk.Frame):
    """
       Make a frame scrollable with scrollbar on the right.
       After adding or removing widgets to the scrollable frame, 
       call the update() method to refresh the scrollable area.
    """

    def __init__(self, frame, width=16):

        scrollbar = tk.Scrollbar(frame, width=width)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y, expand=False)

        self.canvas = tk.Canvas(frame, yscrollcommand=scrollbar.set)
        self.canvas.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

        scrollbar.config(command=self.canvas.yview)

        self.canvas.bind('<Configure>', self.__fill_canvas)

        # base class initialization
        tk.Frame.__init__(self, frame)         

        # assign this obj (the inner frame) to the windows item of the canvas
        self.windows_item = self.canvas.create_window(0,0, window=self, anchor=tk.NW)


    def __fill_canvas(self, event):
        "Enlarge the windows item to the canvas width"

        canvas_width = event.width
        self.canvas.itemconfig(self.windows_item, width = canvas_width)        

    def update(self):
        "Update the canvas and the scrollregion"

        self.update_idletasks()
        self.canvas.config(scrollregion=self.canvas.bbox(self.windows_item))

###############################################################################
## running the program
###############################################################################
app = Main()
app.geometry("1280x720")
app.mainloop()
