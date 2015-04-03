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
    
    def getData(self, path=''):
        if path == '':
            path = self.path
        with open(path, 'rU') as data:
            data.readline()
            reader = csv.reader(data)
            for row in map(wifiRecord._make, reader):
                yield row
    
    def filteredData(self,expression, path=''):
        for wifi in self.getData(path):
            if wifiRecordContains(wifi, expression):
                yield wifi

if __name__=='__main__':
    db = DB('list.csv')
    for wifi in db.getData():
        print (wifi)
