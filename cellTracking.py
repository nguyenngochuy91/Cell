#!/usr/bin/env python
''' Author       : Huy Nguyen
    Program      : Cell Tracking
                    This will take input from the user, the user can either 
                    create a Cell object (or experiment) from scrath, or read it in from a textfile (json format)
                    This program will provide a visualization, math check of the process,
                    and period of time the experiment has run, as well as the amount of media used  
                    as w
    Start        : 08/04/2018
    End          : /2018
    Dependencies :  sudo pip install numpy
                    sudo pip install networkx
                    sudo pip install matplotlib
'''
from datetime import date
from datetime import time

import networkx as nx
import matplotlib.pyplot as plt 
import numpy as np
from cell import Cell
import json
import os.path

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
function : function asking user for a Cell object info to create one
input    : NtypeErrorMess (string),ValueErrorMessA (string)
output   : Cell object
"""    
def createRoot(typeErrorMess,ValueErrorMess):
    name   = takeInput("Please type in the name of this experiment:\n", 
                       lambda myType: True, lambda myVal: True,
                       typeErrorMess,ValueErrorMess)
    
    volume = float(takeInput("Please type in the volume:\n", 
                       lambda myType: True if myType.isdigit() else False, 
                       lambda myVal: True if float(myVal)>0 and float(myVal)<1000 else False,
                       typeErrorMess,ValueErrorMess))

    od     = float(takeInput("Please type in the OD:\n", 
                       lambda myType: True if myType.isdigit() else False, 
                       lambda myVal: True if float(myVal)>0 and float(myVal)<1 else False,
                       typeErrorMess,ValueErrorMess))
    
    # create a Cell object
    root  = Cell(name=name,od=od,volume=volume)
    
    return root

"""
function : function that reads in a json text file, and parse info into a Cell object
input    : text file
output   : root (Cell object)
"""   
def readIn(infile):
    with open(infile) as data_file:
        dictionary = json.load(data_file)
    def dfs(d):
        if d:
            name     = d["name"]     
            od       = d["od"]     
            day      = d["day"]      
            volume   = d["volume"]   
            children = []
            node     = Cell(name=name,od=od,volume=volume,day=day,children=children)
            for child in d["children"]:
                # create the childNode
                childNode        = dfs(child)
                childNode.parent = node
                children.append(childNode)
            return node
    return dfs(dictionary)

####################################################################################        
# Main function and helpers functions
#################################################################################### 
"""
function : Ask the user which solution to dilution, and dilution into how many solutions, with what od
input    : root (Cell), names (list), leaves (list), typeErrorMess,ValueErrorMess
output   : N/A
"""   
def dilute(root,names,leaves,typeErrorMess,ValueErrorMess):
    # check if the name in names
    name = takeInput("Please type in the name of the culture to dilute:\n",
                     lambda myVal: True if myVal in names else False, 
                     lambda myVal: True if myVal in leaves else False,
                     "We don't have your culture name in the database, please choose one of the following {}".format(",".join(names)),
                     "Your culture is already diluted, please provide a culture from this list {}\n".format(",".join(leaves)))
    
    numberDilution = int(takeInput("Please type in the number of culture after diluting (>=1):\n",
                               lambda myType: True if myType.isdigit() else False,
                               lambda myVal: True if myVal>0 else False,
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
    while True:
        for i in range(numberDilution):
            print ("Info for new culture number {}\n:".format(i))
            volume = float(takeInput("Please type in the volume:\n", 
                       lambda myType: True if myType.isdigit() else False, 
                       lambda myVal: True if float(myVal)>0 and float(myVal)<1000 else False,
                       typeErrorMess,ValueErrorMess))

            od     = float(takeInput("Please type in the OD:\n", 
                       lambda myType: True if myType.isdigit() else False, 
                       lambda myVal: True if float(myVal)>0 and float(myVal)<1 else False,
                       typeErrorMess,ValueErrorMess))
            
            child_name = name+"_"+str(i)
            newVolumes.append(volume)
            newOds.append(od)
            namesAdd.append(child_name)
        if sum(newVolumes) ==  volume: 
            # 
            leaves.remove(name)
            leaves.extend(namesAdd)
            names.extend(namesAdd)
            break
        else:
            print ("Attention folks, sum of the volumes is not equal to our old volume, you will be need to retype the infos!!!\n")
    
    # set the new Children for the target node
    targetNode.setChildren(ods, volumes)
    
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
        infile = takeInput("Please type in the textfile to read:\n",
                           lambda myType: True,
                           lambda myVal: True if os.path.isfile(myVal) else False,
                           typeErrorMess,
                           "The file can not be found in the current directory!\n")
        root = readIn(infile)
    # get all the leaf names
    leaves = root.getLeafNames()
    names  = root.getNames()
    print ("Here are all the culture that can be diluted: {}\n".format(", ".join(leaves)))
    # keep on diluting until done
    
        
if __name__ == "__main__":
    print ("*"*160)
    typeErrorMess  = "Please provide the correct input format!!!\n"
    ValueErrorMess = "Please provide the correct input value (within range)!!!\n"
    # check whether user want to start from scratch
    today   = date.today()
    choice = takeInput("Do you want to start a scratch experiment (Y,N)):",
                       lambda myType: True if myType in "YyNn" else False,
                       lambda myVal: True,
                       typeErrorMess,ValueErrorMess)
    start(choice,typeErrorMess,ValueErrorMess)