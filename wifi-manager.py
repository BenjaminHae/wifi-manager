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
    args = parser.parse_args()
    return args

def main():
    args = parseArgs()
    path = 'list.csv'
    if args.path != None:
        path = args.path
    db = database.DB(path)
    if args.filter != None:
        data = db.filteredData(args.filter)
    else:
        data = db.getData()

    #palette = [('entry', 'default,bold', 'default')]
    #urwid.MainLoop(Table((formatWifiGen((data)))), palette).run()
    # start display
    minWidth = [10 for i in range(0,4)]
    for wifi in data:
        print(formatWifi(wifi, minWidth))
        
def fillWidth(strings, minWidth):
    if minWidth == None:
        return strings
    for i in range(0,min(len(minWidth),len(strings))-1):
        newStrings[i] = strings[i]+' '*(minWidth-len(strings[i]))
    return newStrings

def formatWifi(wifi, minWidth = None):
    return ' | '.join(fillWidth([wifi.name,wifi.ssid,wifi.location,wifi.comment],minWidth))

def formatWifiGen(data):
    for wifi in data():
        yield formatWifi(wifi)

if __name__ =='__main__':
    main()
