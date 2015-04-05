#!/usr/bin/python3
import csv
from collections import namedtuple

fields = ('name','ssid','encryption','passphrase','location','latlong','comment')
wifiRecord = namedtuple('WifiRecord',fields)

def wifiRecordContains(wifi, expression):
    expression = str.lower(expression)
    if expression in str.lower(wifi.name):
        return True
    if expression in str.lower(wifi.ssid):
        return True
    if expression in str.lower(wifi.location):
        return True
    if expression in str.lower(wifi.comment):
        return True
    return False

class DB():
    def __init__(self, path):
        self.path = path
    
    def getData(self):
        with open(self.path, 'rU') as data:
            data.readline()
            reader = csv.reader(data)
            for row in map(wifiRecord._make, reader):
                yield row
    
    def filteredData(self,expression):
        for wifi in self.getData():
            if wifiRecordContains(wifi, expression):
                yield wifi

    def addItem(self, data):
        with open(self.path, 'a') as csvfile:
            writer = csv.writer(csvfile)
            for wifi in data:
                if wifi != None:
                    writer.writerow((wifi.name, wifi.ssid, wifi.encryption, wifi.passphrase, wifi.location, wifi.latlong, wifi.comment))
    
    def removeItem(self, wifi):
        pass

if __name__=='__main__':
    db = DB('list.csv')
    for wifi in db.getData():
        print (wifi)
