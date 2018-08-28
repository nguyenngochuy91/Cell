#!/usr/bin/env python
''' Author       : Huy Nguyen
    Program      : Cell Tracking
                    class of cell
    Start        : 08/04/2018
    End          : /2018
    Dependencies : sudo pip install networkx
                   sudo pip install plotly
'''
# a class of cell, each cell object will be defined with a name, od, and volume
# and a dictionary that stores info so we can dump it later into json file to
# keep update and write.
# The way we add link to children is a bit unconventional, since we want to calculate
# the volume of the children, the getVolumeChildren will calculate how much media
# will be added
class Cell(object):
    def __init__(self,name,od,volume=None):
        self.name       = name
        self.od         = od
        self.volume     = volume
        self.dictionary = {"name":name,"od":od,"volume":volume}
    # giving the od of the children node, find the wanted volume for each
        # also include a day Observe
    def getVolumeChildren(self,ods, dayObserve):
        seld.dictionary['day'] = dayObserve
        numberChildren         = len(ods)
        bacteriaVolume         = self.od*self.volume
        
        
        