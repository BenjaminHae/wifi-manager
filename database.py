#!/usr/bin/python3
import csv
from collections import namedtuple
import tempfile
import shutil

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
        whash = hash(wifi) # calc hash of wifi
        with tempfile.SpooledTemporaryFile(mode='w+') as mem:
            writer = csv.writer(mem)
            with open(self.path, 'r') as csvfile:
                reader = csv.reader(csvfile)
                for data in map(wifiRecord._make, reader):
                    if hash(data) != whash:
                        writer.writerow((data.name, data.ssid, data.encryption, data.passphrase, data.location, data.latlong, data.comment))
            mem.seek(0)
            with open(self.path, 'w') as destfile:
                shutil.copyfileobj(mem, destfile)

if __name__=='__main__':
    db = DB('list.csv')
    for wifi in db.getData():
        print (wifi)
