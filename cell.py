#!/usr/bin/env python
''' Author       : Huy Nguyen
    Program      : Cell Tracking
                    class of cell
    Start        : 08/04/2018
    End          : /2018
    Dependencies : sudo pip install networkx
                   sudo pip install plotly
                   sudo pip install json
'''
# a class of cell, each cell object will be defined with a name, od, and volume
# and a dictionary that stores info so we can dump it later into json file to
# keep update and write.
# The way we add link to children is a bit unconventional, since we want to calculate
# the volume of the children, the getVolumeChildren will calculate how much media
# will be added

class Cell(object):
    def __init__(self,name,od,volume=None,day = 0,parent= None,children= []):
        self.name       = name
        self.od         = od
        self.volume     = volume
        self.day        = day
        self.children   = children
        self.parent     = parent
    """
    function : Giving arrays of volume and ods for the children, calculate how much media volumn to be added
              and how much volumn after in each dilution
    input    : ods(array of float), volumes(array of float, these volumes have to add up to the self.volume)
    output   : N/A
    """
    def setChildren(self,ods, volumes,dayObserve):
        if sum(volumes)!= self.volume:
            print ("Attention folks, sum of the volumes is not equal to our old volume!!!")
        else:
            numberChildren = len(ods)
            childDay       = self.day+dayObserve
            for i in range(numberChildren):
                v     = volumes[i]
                od    = float(ods[i])
                newV  = self.od*v/od
                # create new Cell object
                child = Cell(name=self.name+"_"+str(i),od=od,volume=newV,day=childDay,parent=self)
                self.children.append(child)
    """
    function : giving the cell object, saving all the info in a dictionary and dump into a json file
    input    : Cell object
    output   : dictionary
    """    
    def toDictionary(self):
        dictionary = {}
        def dfs(node,d):
            if node:
                d["name"]     = node.name
                d["od"]       = node.od
                d["day"]      = node.day
                d["volume"]   = node.volume
                d["children"] = []
                if node.parent:
                    d["parent"]   = node.parent.name
                else:
                    d["parent"]   = None
                for child in node.children:
                    childD = {}
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
            
                        
            
            
            
            
            
            
            
            
            
            
            