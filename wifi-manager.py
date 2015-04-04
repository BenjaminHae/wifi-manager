#!/usr/bin/python3
from curses import wrapper
import database
import network
import argparse
#import urwid
#from table import Table

def parseArgs():
    parser = argparse.ArgumentParser(description='Manage list of wifi networks')
    parser.add_argument('--filter', action='store', help='search for WIFI network')
    parser.add_argument('--path', action='store', help='use file as database')
    parser.add_argument('--connect', action='store', help='connect to first network in list')
    parser.add_argument('--add', action='store_true', help='add network')
    parser.add_argument('--remove', action='store', help='remove all found entries')
    parser.add_argument('--replace', action='store', help='replace network')
    parser.add_argument('--parse-add', action='store', help='add multiple networks by parsing standard input')
    args = parser.parse_args()
    return args

def main():
    args = parseArgs()
    path = 'list.csv'
    if args.path != None:
        path = args.path
    db = database.DB(path)
    if args.add == True:
        addWifi(db) 
    if args.filter != None:
        data = db.filteredData(args.filter)
    else:
        data = db.getData()

    #palette = [('entry', 'default,bold', 'default')]
    #urwid.MainLoop(Table((formatWifiGen((data)))), palette).run()
    # start display
    minWidth = [15 for i in range(0,5)]
    minWidth[0] = 2
    id = 0
    for wifi in data:
        id += 1
        print(formatWifi(id, wifi, minWidth))
        
def fillWidth(strings, minWidth):
    if minWidth == None:
        return strings
    newStrings = ['' for i in range(0, len(strings)-1)]
    for i in range(0,min(len(minWidth),len(strings))-1):
        newStrings[i] = strings[i]+' ' * (minWidth[i]-len(strings[i]))
    return newStrings

def formatWifi(id, wifi, minWidth = None):
    return ' | '.join(fillWidth([str(id), wifi.name, wifi.ssid, wifi.location, wifi.comment],minWidth))

def addWifi(db):
    pass

if __name__ =='__main__':
    main()
