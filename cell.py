#!/usr/bin/env python
''' Authors      : Huy Nguyen, Nhi
    Program      : Cell Tracking
                    class of cell
    Start        : 08/04/2018
    End          : /2018 
'''
# a class of cell, each cell object will be defined with a name, od, and volume
# and a dictionary that stores info so we can dump it later into json file to
# keep update and write.
# The way we add link to children is a bit unconventional, since we want to calculate
# the volume of the children, the getVolumeChildren will calculate how much media
# will be added\
import collections

class Cell(object):
    def __init__(self,name,od,volume=None,date = 0,parent= None,media = ""):
        self.name       = name # name of the culture
        self.od         = [od] # list of ods value, this will getting updated until dilution
        self.volume     = volume
        self.date        = [date]
        self.children   = []
        self.parent     = parent
        self.add        = 0
        self.media      = media
 
    """
    function : giving the cell / culture, and the new od, and the date since last update, we update our Cell object
    input    : od, date
    output   : N/A
    """
    def update(self,od,date,volume)   :
        self.od.append(od)
        self.date.append(date)
        self.volume = volume
    """
    function : Giving arrays of volume and ods for the children, calculate how much media volumn to be added
              and how much volumn after in each dilution
    input    : ods(array of float), volumes(array of float, these volumes have to add up to the self.volume)
    output   : names
    """
    def setChildren(self,ods, volumes,dateObserve):     
        numberChildren = len(ods)
        names          = []
        for i in range(numberChildren):
            name  = self.name+"_"+str(i)
            v     = volumes[i]
            od    = float(ods[i])
            newV  = round(self.od[-1]*v/od,2)
            # create new Cell object
            child     = Cell(name=name,od=od,volume=newV,date=dateObserve,parent=self)
            child.add = newV-v
            self.children.append(child)
            names.append(name)
        return names
    """
    function : giving the cell object, saving all the info in a dictionary and dump into a json file
    input    : Cell object
    output   : dictionary
    """    
    def toDictionary(self):
        dictionary = collections.OrderedDict()
        def dfs(node,d):
            if node:
                d["name"]     = node.name
                d["od"]       = node.od
                d["date"]      = ["{}-{}-{}".format(k.year,k.month,k.day) for k in node.date]
                d["volume"]   = node.volume
                d["add"]      = node.add
                d["media"]    = node.media
                if node.parent:
                    d["parent"]   = node.parent.name
                else:
                    d["parent"]   = None
                d["children"] = []
                for child in node.children:
                    childD = collections.OrderedDict()
                    dfs(child,childD)
                    d["children"].append(childD)
        dfs(self,dictionary)
        return dictionary
    
    """
    function : giving the cell object, get back to the root
    input    : Cell object
    output   : root (Cell)
    """    
    def getRoot(self):
        parent = self.parent
        while parent:
            self   = parent
            parent = self.parent
        return self
    
    """
    function : giving the cell object, and a node name, return the node with the name
    input    : Cell object
    output   : node
    """
    def getNode(self,nodeName):
        current_name = self.name.split("_")
        target_name  = nodeName.split("_")
        for i in range(min(len(current_name),len(target_name))):
            if current_name[i]!=target_name[i]:
                i = i-1
                break
        for j in range(len(current_name)-i-1):
            self=self.parent
        if self.name == nodeName:
            return self
        else:
            for child in self.children:
                if child.name == nodeName:
                    return child
    """
    function : giving the root, and a node name, return the node with the name
    input    : Cell object
    output   : node
    """
    def getNodeFromRoot(self,nodeName):
        target_name  = nodeName.split("_")
        current_node = self
        for i in target_name[1:]:
            current_node = current_node.children[int(i)]
        return current_node
    
    """
    function : giving the root, return all the leaf names
    input    : Cell object
    output   : names(list)
    """
    def getLeafNames(self):
        names = []
        def dfs(node):
            if node:
                if not node.children:
                    names.append(node.name)
                for child in node.children:
                    dfs(child)
        dfs(self)
        return names
    
    """
    function : giving the cell object, get all the names
    input    : Cell object
    output   : names (list)
    """                        
    def getNames(self):
        names = []
        def dfs(node):
            if node:
                names.append(node.name)
                for child in node.children:
                    dfs(child)
        dfs(self)
        return names
            
            

            
            