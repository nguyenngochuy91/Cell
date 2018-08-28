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
                print (typeErrorMess)
        else:
            print (ValueErrorMess)
            
"""
function : function asking user for a Cell object info to create one
input    : NtypeErrorMess (string),ValueErrorMessA (string)
output   : Cell object
"""    
def createRoot(typeErrorMess,ValueErrorMess):
    name   = takeInput("Please type in the name of this experiment:", 
                       lambda myType: True, lambda myVal: True,
                       typeErrorMess,ValueErrorMess)
    
    volume = float(takeInput("Please type in the volume:", 
                       lambda myType: True if myType.isdigit() else False, 
                       lambda myVal: True if float(myType)>0 and float(myType)<1000 else False,
                       typeErrorMess,ValueErrorMess))

    od     = float(takeInput("Please type in the OD:", 
                       lambda myType: True if myType.isdigit() else False, 
                       lambda myVal: True if float(myType)>0 and float(myType)<1 else False,
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
            

"""
function : main function, takes in the user choice of whether start new experiment, or read in from file
input    : choice
output   : 
"""    
def start(choice,typeErrorMess,ValueErrorMess):
    # if choice is Y or y, then create a Cell (or experiment object)
    if choice in "Yy":
        root = createRoot(typeErrorMess,ValueErrorMess)
    # else, ask the user for which file to read in
    else:
        infile = takeInput("Please type in the textfile to read:",
                           lambda myType: True,
                           lambda myVal: True if os.path.isfile(myVal) else False,
                           typeErrorMess,
                           "The file can not be found in the current directory!")
        root = readIn(infile)

if __name__ == "__main__":
    print ("*"*160)
    typeErrorMess  = "Please provide the correct input format!!!"
    ValueErrorMess = "Please provide the correct input value (within range)!!!"
    # check whether user want to start from scratch
    choice = takeInput("Do you want to start a scratch experiment (Y,N)):",
                       lambda myType: True if myType in "YyNn" else False,
                       lambda myVal: True,
                       typeErrorMess,ValueErrorMess)
    start(choice,typeErrorMess,ValueErrorMess)