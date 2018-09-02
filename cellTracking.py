#!/usr/bin/env python
''' Authors      : Huy Nguyen, Nhi
    Program      : Cell Tracking
                    This will take input from the user, the user can either 
                    create a Cell object (or experiment) from scrath, or read it in from a textfile (json format)
                    This program will provide a visualization, math check of the process,
                    and period of time the experiment has run, as well as the amount of media used  
                    as w
    Start        : 08/04/2018
    End          : /2018
    Dependencies :  networkx
                    pydot
'''
import datetime
import networkx as nx
import pydot
from cell import Cell
import json
import os.path
### some modify the screen stdout
reset     = '\033[0m'
underline = '\033[04m'
bold      = '\033[01m'

###############################################################################
## helper functions to take input, check error, create Cell object, 
## some specific functions to take in od, volume, name, and choice since reused 
## a lot
###############################################################################
## check if a number is float:
def isFloat(n):
    try:
        x = float(n)
    except ValueError:
        return False
    else:
        return True

"""
function : function takes in user input, check it with errorChecking function, and 
           keep promting if input is not good
input    : message (string), errorChecking(function)
output   : input (any type really)
"""
def takeInput(message,typeChecking,valueChecking,typeErrorMess,ValueErrorMess):
    while True:
        try:
            choice = raw_input(message)    
        except:
            choice = input(message)    
        if typeChecking(choice):
            if valueChecking(choice):
                return choice
            else:
                print (ValueErrorMess)
        else:
            print (typeErrorMess)
       
"""
function : function takes in user od, check it with errorChecking function, and 
           keep promting if input is not good
input    : typeErrorMess (string), errorChecking(function)
output   : od
"""
def getOd(typeErrorMess,ValueErrorMess):
    od     = float(takeInput("Please type in the OD:\n", 
                       lambda myType: True if isFloat(myType) else False, 
                       lambda myVal: True if float(myVal)>0 and float(myVal)<1 else False,
                       typeErrorMess,ValueErrorMess))
    return od
 
"""
function : function takes in user volume, check it with errorChecking function, and 
           keep promting if input is not good
input    : typeErrorMess (string), errorChecking(function)
output   : volume
"""
def getVolume(typeErrorMess,ValueErrorMess):
    volume = float(takeInput("Please type in the volume:\n", 
                       lambda myType: True if isFloat(myType) else False, 
                       lambda myVal: True if float(myVal)>0 and float(myVal)<1000 else False,
                       typeErrorMess,ValueErrorMess))
    return volume

"""
function : function takes in culture name, check it with errorChecking function, and 
           keep promting if input is not good
input    : message (string),typeErrorMess(string), errorChecking(function),names,leaves
output   : name
"""
def getName(message,typeErrorMess,ValueErrorMess,names,leaves):
    name = takeInput("Please type in the name of the culture to {}:\n".format(message),
                     lambda myVal: True if myVal in names else False, 
                     lambda myVal: True if myVal in leaves else False,
                     "We don't have your culture name in the database, please choose one of the following: {}".format(",".join(names)),
                     "Your culture is already {}, please provide a culture from this list: {}\n".format(message+"d",",".join(leaves)))
    return name

"""
function : function takes in user choice, check it with errorChecking function, and 
           keep promting if input is not good
input    : message (string), errorChecking(function)
output   : choice
"""
def getChoice(message,typeErrorMess,ValueErrorMess):
    choice = takeInput(message,
                       lambda myType: True if myType in "YyNn" else False,
                       lambda myVal: True,
                       typeErrorMess,ValueErrorMess)
    return choice

"""
function : get the date for updating, either as today from the machine, or the date user type in
input    : N/A
output   : date
"""   
def getDate(typeErrorMess,ValueErrorMess):
    today = datetime.date.today()
    while True:
        choice = getChoice("Do you want to use today date {}{}{} (yyyy-mm-dd) ?\n".format(bold,today,reset),typeErrorMess,ValueErrorMess)
        if choice in "Yy":
            break
        day   = int(takeInput("Please enter a day:\n",
                        lambda myType: True if myType.isdigit() else False,
                        lambda myVal: True if int(myVal)>=1 and int(myVal)<=31 else False,
                        typeErrorMess
                        ,ValueErrorMess))
        month = int(takeInput("Please enter a month:\n",
                        lambda myType: True if myType.isdigit() else False,
                        lambda myVal: True if int(myVal)>=1 and int(myVal)<=12 else False,
                        typeErrorMess
                        ,ValueErrorMess))
        year = int(takeInput("Please enter a year:\n",
                        lambda myType: True if myType.isdigit() else False,
                        lambda myVal: True if int(myVal)>=2018 and int(myVal)<=2118 else False,
                        typeErrorMess
                        ,ValueErrorMess))
        try:
            today = datetime.date(year,month,day)
        except:
            print ("We are sorry but the day is out of range for month, pleaes provide the date again\n")
        
        
    return today
"""
function : function asking user for a Cell object info to create one
input    : NtypeErrorMess (string),ValueErrorMessA (string)
output   : Cell object
"""    
def createRoot(typeErrorMess,ValueErrorMess):   
    # create a Cell object
    while True:
        today  = getDate(typeErrorMess,ValueErrorMess)
        name   = takeInput("Please type in the name of this experiment:\n", 
                       lambda myType: True, lambda myVal: True,
                       typeErrorMess,ValueErrorMess)
        od     = getOd(typeErrorMess,ValueErrorMess)
        volume = getVolume(typeErrorMess,ValueErrorMess)
        media  = takeInput("Please type in the name of the media:\n", 
                       lambda myType: True, lambda myVal: True,
                       typeErrorMess,ValueErrorMess)
        ## double check if this is what the user want to do
        choice = getChoice("Are you sure to create a root that has \nname as {} {}{},\nod as {} {}{},\nvolume as {} {}{},\nmedia as {} {}{},\nand date as {} {}{}? :\n".format(
                bold,name,reset,bold,od,reset,bold,volume,reset,bold,media,reset,bold,today,reset),
                           typeErrorMess,ValueErrorMess)

        if choice in "yY":
            root  = Cell(name=name,od=od,volume=volume,day=today,media=media)
            break
    
    return root

###############################################################################
## helper functions to read in json, write out json 
###############################################################################
"""
function : function that reads in a json text file, and parse info into a Cell object
input    : N/A
output   : root (Cell object)
"""   
def readIn():
    infile = takeInput("Please type in the textfile to read:\n",
                       lambda myType: True,
                       lambda myVal: True if os.path.isfile(myVal) else False,
                       "",
                       "The file can not be found in the current directory!\n")
    with open(infile) as data_file:
        dictionary = json.load(data_file)
    data_file.close()
    def dfs(d):
        if d:
            name     = d["name"]     
            od       = d["od"]   
            day      = []
            for k in d["day"]:

                k = [int(i) for i in k.split("-")]
                day.append(datetime.date(k[0],k[1],k[2]))

            volume   = d["volume"] 
            add      = d["add"]
            media    = d["media"]
            children = []
            node     = Cell(name=name,od=od,volume=volume,media=media)
            node.day = day
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
function : function that reads given a cell, ask user for a file to write to
input    : root (Cel),typeErrorMess,ValueErrorMess
output   : N/A
"""   
def writeOut(root,typeErrorMess,ValueErrorMess):
    while True:
        outfile = takeInput("Please type in the textfile to write (.txt):\n",
                            lambda myType: True,lambda myVal: True,"","")
        if os.path.isfile(outfile):
            choice = getChoice("File {}{}{} is already exists, do you want to replace it (Y,N)?:\n".format(bold,outfile,reset),
                               typeErrorMess,ValueErrorMess)
            if choice:
                break
        else:
            break
    dictionary = root.toDictionary() 
    # write out
    with open(outfile,"w") as data_file:
        json.dump(dictionary, data_file,indent=4)  

###############################################################################
## helper visualize using networkx
###############################################################################
"""
function : Quick function to add a day and unique culture name to a dictionary. 
input    : dictionary,day,name
output   : N/A
"""   
def addDay(dictionary,day,name):
    if day in dictionary:
        dictionary[day].append(name)
    else:
        dictionary[day] = [name]
    
"""
function : Given a digraph, draw accordingly to options
input    : DG,typeErrorMess,ValueErrorMess
output   : graph (pydot)
"""   
def specificDraw(G,typeErrorMess,ValueErrorMess,media):
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
        name = "name: {}\ndate: {}\nod: {}\nvolume: {}ml".format(attribute['label'],attribute['day'],attribute['od'],attribute['volume'])
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
        
        
    while True:
        outfile = takeInput("Please type in the textfile to save the picture (.png):\n",
                            lambda myType: True,lambda myVal: True,"","")
        if os.path.isfile(outfile):
            choice = getChoice("File {}{}{} is already exists, do you want to replace it (Y,N)?:\n".format(bold,outfile,reset),
                               typeErrorMess,ValueErrorMess)
            if choice:
                break
        else:
            break
    graph.write_png(outfile)
    return graph

"""
function : Given root, draw a plot, x-axis indicate time line, y axis is just to space our graph
           Our main plot is a graph, with the root is the starting point, directed edge from
           1 culture to other to show diluting process, and directed edge from 1 culture to 1 other
           for updating. 
           
input    : root (Cell)
output   : DG, a
"""   
def visualization(root,typeErrorMess,ValueErrorMess):
    ## create a digraph
    DG = nx.DiGraph()
    days_dictionary = {}
    days            = ["{}-{}-{}".format(k.year,k.month,k.day) for k in root.day]
    starting        = "{}({})".format(root.name,days[0])
    def dfs(node):
        if node:
            days    = ["{}-{}-{}".format(k.year,k.month,k.day) for k in node.day]
            ods     = node.od
            # add node as the beginning 
            name    = node.name
            volume  = node.volume
            add     = node.add
            DG.add_node("{}({})".format(name,days[0]),label = name,volume = volume,add = add,od = ods[0],day =days[0])
            for i in range(1,len(days)):
                add = 0
                # add the updating node
                currentName = "{}({})".format(name,days[i])
                parentName = "{}({})".format(name,days[i-1])
                DG.add_node(currentName,label = name,volume = volume,add = add,od = ods[i],day =days[i])
                DG.add_edge(parentName,currentName,volume= volume,add = add,type="update")
                # take care of updating 
                addDay(days_dictionary,node.day[i],currentName)
            
            # add edge from parent            
            if node.parent:
                parentdays = ["{}-{}-{}".format(k.year,k.month,k.day) for k in node.parent.day]
                parentName = "{}({})".format(node.parent.name,parentdays[-1])
                nodeName   = "{}({})".format(node.name,days[0])
                volume     = node.volume
                DG.add_edge(parentName,nodeName,volume= volume,add = node.add,type="dilute")
            # at leaf node, add normally using addDay
            if node == root:
                addDay(days_dictionary,node.day[0],"{}({})".format(name,days[0]))
            # else, will have to add the current node as a dictionary
            if node.children:
                name = "{}({})".format(node.name,days[-1])
                day  = node.day[-1]
                days = []
                for c in node.children:

                    cDays = ["{}-{}-{}".format(k.year,k.month,k.day) for k in c.day]        
                    cName = "{}({})".format(c.name,cDays[0])
                    days.append(cName)
                if day in days_dictionary:
                    days_dictionary[day].append(days)
                else:
                    days_dictionary[day]=[days]
            for child in node.children:
                dfs(child)
                
    dfs(root)  
    ## drawing
    p = specificDraw(DG,typeErrorMess,ValueErrorMess,root.media)
    print ("Thank you for using the software, come again soon ^^!!\n")
    return DG,days_dictionary,p
####################################################################################        
# Main function to update, dilute and starts
#################################################################################### 
"""
function : Ask the user which solution to update, and update the od and date
input    : root (Cell), names (list), leaves (list), typeErrorMess,ValueErrorMess
output   : N/A
"""     
def update(root,names,leaves,typeErrorMess,ValueErrorMess):
    # check if the name in names
    while True:
        print ("The culture that you can update are:{} {}{}".format(bold,",".join(leaves),reset))
        name   = name = getName("update",typeErrorMess,ValueErrorMess,names,leaves)
        today  = getDate(typeErrorMess,ValueErrorMess)
        od     = getOd(typeErrorMess,ValueErrorMess)
        choice = getChoice("Are you sure to update culture {} {}{} with od {} {}{} and date {} {}{}? :\n".format(
                bold,name,reset,bold,od,reset,bold,today,reset),
                           typeErrorMess,ValueErrorMess)
        if choice in "yY":
            break
        else:
            print ("Let's redo this ^^\n")
    # update 
    targetNode = root.getNodeFromRoot(name)
    targetNode.update(od,today)
    
"""
function : Ask the user which solution to dilution, and dilution into how many solutions, with what od
input    : root (Cell), names (list), leaves (list), typeErrorMess,ValueErrorMess
output   : N/A
"""   
def dilute(root,names,leaves,typeErrorMess,ValueErrorMess):
        # check if the name in names
    while True:
        print ("The culture that you can dilute are: {}{}{}".format(bold,",".join(leaves),reset))
        name  = getName("dilute",typeErrorMess,ValueErrorMess,names,leaves)
        today = getDate(typeErrorMess,ValueErrorMess)
        numberDilution = int(takeInput("Please type in the number of culture after diluting (>=1):\n",
                                   lambda myType: True if myType.isdigit() else False,
                                   lambda myVal: True if int(myVal)>0 else False,
                                   typeErrorMess,
                                   ValueErrorMess))
        print ("You have chosen to dilute {} into {} cultures, please type in the following info as instructed \n".format(name,numberDilution))
        print ("***CAUTION*** \n")
        print ("The new ods can take any value between 0 and 1, the new volumes together has to add up to volume of {}\n".format(name))
        newVolumes = []
        newOds     = []
        namesAdd   = []
        targetNode = root.getNodeFromRoot(name)
        volume     = targetNode.volume
        # retrieve info into newVolumes, newOds
    
        for i in range(numberDilution):
            print ("Info for new culture number {}:\n".format(i))
            od     = getOd(typeErrorMess,ValueErrorMess)
            v      = getVolume(typeErrorMess,ValueErrorMess)
            
            child_name = name+"_"+str(i)
            newVolumes.append(v)
            newOds.append(od)
            namesAdd.append(child_name)
#            print ( sum(newVolumes),volume)
        if sum(newVolumes) <=  volume: 
            ## double check if this is what the user want to do
            culture = "name: {}, od: {}, volume: {} \n"
            result  = ""
            for i in range(numberDilution):
                result+=culture.format(namesAdd[i],newOds[i],newVolumes[i])
            if sum(newVolumes)<volume:
                print ("Be careful, it looks like the newVolumes is less than the current volume!!!\n")
            choice = getChoice("Are you sure to dilute culture {} {}{} as follow {} {}{} with date as {} {}{}? :\n".format(
                    bold,name,reset,bold,result,reset,bold,today,reset),
                               typeErrorMess,ValueErrorMess)
            if choice in "Yy":
                leaves.remove(name)
                leaves.extend(namesAdd)
                names.extend(namesAdd)
                break
            else:
                print ("Let's redo this ^^\n")
        else:
            print ("Attention folks, sum of the volumes is not equal to our old volume, you will be need to retype the infos!!!\n")
    
    # set the new Children for the target node
    targetNode.setChildren(ods = newOds,volumes= newVolumes,dayObserve =today)
    
"""
function : main function, takes in the user choice of whether start new experiment, or read in from file
input    : choice,typeErrorMess,ValueErrorMess
output   : 
"""    
def start(choice,typeErrorMess,ValueErrorMess):
    # if choice is Y or y, then create a Cell (or experiment object)
    if choice in "Yy":
        root = createRoot(typeErrorMess,ValueErrorMess)
    # else, ask the user for which file to read in
    else:
        root = readIn()
    # get all the leaf names
    leaves = root.getLeafNames()
    names  = root.getNames()
    print ("Here are all the culture that can be updated: {} {}{}\n".format(bold,", ".join(names),reset))
    # updating until done
    while True:
        while True:
            choice = getChoice("Do you want to update a culture (Y,N):\n",typeErrorMess,ValueErrorMess) 
            if choice in "Yy":
                update(root,names,leaves,typeErrorMess,ValueErrorMess)
            else:
                print ("Let's move on to diluting our cultures!!!\n")
                break        
        # keep on diluting until done
        print ("Here are all the culture that can be diluted: {}\n".format(", ".join(leaves)))
        while True:
            choice = getChoice("Do you want to dilute a culture (Y,N):\n",typeErrorMess,ValueErrorMess)  
            if choice in "Yy":
                dilute(root,names,leaves,typeErrorMess,ValueErrorMess)
            else:
                print ("We are done with diluting!!!\n")
                break
        choice = getChoice("Are you done with everything (Y,N)?:\n",typeErrorMess,ValueErrorMess) 
        if choice in "Yy":
            print ("Let's save our progress")
            break
    # write the item into a file using json
    writeOut(root,typeErrorMess,ValueErrorMess)
    # visualize the process
    DG,d,p = visualization(root,typeErrorMess,ValueErrorMess)
    
###############################################################################
## driver program
###############################################################################
if __name__ == "__main__":
    print ("*"*160)
    typeErrorMess  = "Please provide the correct input format!!!\n"
    ValueErrorMess = "Please provide the correct input value (within range)!!!\n"
    
    # check whether user want to start from scratch
    choice = getChoice("Do you want to start a scratch experiment (Y,N)):\n",
                      typeErrorMess,ValueErrorMess)
    # start the cycle
    start(choice,typeErrorMess,ValueErrorMess)