"""
Defines the file format for reading and writing the data for piezo trays
XXX May not be directly compatible with other code, though that should be easily fixable
This is just a mock up of a way to store the data in a way that can easily be transformed, essentially multiple CSV files in a single file. It was done like this so that is most closely matched the old,
bulky format though XML may be better.
Furthermore, there is a config file containing the frequency spread, for example, since it won't change once an experiment has begun (though at this point, a user cannot change the frequency ever...)

Zeddiciaus Pearson <serjeant.work@gmail.com>
"""

import os
import sys
import numpy as np
from datetime import datetime
from collections import OrderedDict

config_prefix = "_config"
config_suffix = ".txt"
tray_suffix = ".txt"

config_format = {
    "ExperimentName":"Trial1",
    "StartFrequency":"200",
    "EndFrequency":"1300",
    "StepFrequency":"10",
    "StartTray":"1",
    "EndTray":"100",
    "CreationDate":"2017-11-30 15:14:34.888049"

}

class Experiment:
    def __init__(self):
        """If path is an experiment load its data, otherwise make a new experiment"""
        self.configuration = {}
        # self.path = path
        # try:
        #     self.loadConfig(path)
        # except FileNotFoundError:
        #     try:
        #         self.createConfig(path, config_format)
        #     except:
        #         raise #XXX

    def loadConfig(self, path):
        """Load the properties of the experiment"""
        try:
            with open(os.path.join(path, config_prefix+config_suffix), 'r') as config_file:
                for line in config_file:
                    key,value = line.split(";")
                    if key in config_format:
                        self.configuration[key] = value #XXX maybe check the value is right type here?
                    else:
                        raise KeyError("File Format Error")
                self.path = path
        except KeyError:
            raise #XXX handle format issues if it becomes a problem

        except FileNotFoundError:
            raise FileNotFoundError("No Experiment Found") # Use this in the GUI most likely. cover this as well, its a bit hard with the code split between two of us

    def createConfig(self, path, configuration):
        """Create a configuration file that defines a project"""
        os.makedirs(path)
        self.path = path
        with open(os.path.join(path,config_prefix+config_suffix), 'w') as config_file:
            for key,value in configuration.items():
                self.configuration[key] = value
                config_file.write(key+";"+value+"\n")

    def appendTrayData(self, tray_address, data):
        """tray_address:<string>, data: numpy array of powers, format above"""
        try:
            with open(os.path.join(self.path, tray_address+tray_suffix), 'a') as tray_file:
                tray_file.write(datetime.today().isoformat(' ')) #Date goes on the first line
                tray_file.write("\n")
                for row in data:
                    for column in row:
                        tray_file.write(str(column)+",")
                    tray_file.write("\n")
        except FileNotFoundError:
            raise #XXX

    def getTrayData(self, tray_address):
        tray = OrderedDict()
        current_key = ""
        try:
            with open(os.path.join(self.path, tray_address+tray_suffix), 'r') as tray_file:
                for line in tray_file:
                    str_row = line.split(",")
                    if len(str_row) == 1:
                        tray[line.strip()] = []
                        current_key = line.strip()
                    else:
                        int_row = []
                        for item in str_row:
                            if item.strip():
                                int_row.append(int(item.strip()))
                        tray[current_key].append(int_row)
            return tray
        except FileNotFoundError:
            raise #XXX
        except ValueError:
            raise ValueError("Corrupt Tray!!!!") #probably add which line, so people can correct or respond to corrupt data

    def getStartFrequency(self):
        return int(self.configuration["StartFrequency"])
    def getEndFrequency(self):
        return int(self.configuration["EndFrequency"])
    def getStepFrequency(self):
        return int(self.configuration["StepFrequency"])
    def getExperimentName(self):
        return self.configuration["ExperimentName"]
    def getCreationDate(self):
        return self.configuration["CreationDate"]
