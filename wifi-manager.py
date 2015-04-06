#!/usr/bin/python3
from curses import wrapper
import database
import network
import argparse
import sys
import parseAdd
import readline

def parseArgs():
    parser = argparse.ArgumentParser(description='Manage list of wifi networks')
    parser.add_argument('--filter', metavar='expression', action='store', help='search for WIFI network')
    parser.add_argument('--show', action='store', help='show all information about wifi', metavar='id', type=int)
    parser.add_argument('--bar', action='store', help='show a barcode to connect', metavar='id', type=int)# ToDo
    parser.add_argument('--path', action='store', help='use file as database')
    parser.add_argument('--connect', metavar='id', type=int, action='store', help='connect to first network in list')
    parser.add_argument('--add', action='store_true', help='add network')
    parser.add_argument('--remove', metavar='id', type=int, action='store', help='remove entry id')
    parser.add_argument('--edit', action='store', metavar='id', type=int, help='edit entry')
    parser.add_argument('--parse-add', action='store_true', dest='parse', help='add multiple networks by parsing standard input or files')
    parser.add_argument('inputFiles', help='files for parsing', metavar='file', nargs='*', type=str, action='store')
    args = parser.parse_args()
    return args

def main():
    args = parseArgs()
    path = 'list.csv'
    if args.path != None:
        path = args.path
    db = database.DB(path)
    
    if args.add == True:
        db.addItem([inputWifi()])
    if args.parse == True:
        inputFile = args.inputFiles
        if len(inputFile) == 0:
            parse = [sys.stdin]
        else:
            parse = [open(File) for File in inputFile]
        db.addItem(map(addParse,parse))
    if args.filter != None:
        data = db.filteredData(args.filter)
    else:
        data = db.getData()
    
    if args.edit != None:
        oldWifi=getWifiById(data, args.edit)
        newWifi=editInfo(oldWifi)
        db.removeItem(oldWifi)
        db.addItem([newWifi])
    if args.connect != None:
        connect(getWifiById(data, args.connect))
    if args.show != None:
        showInfo(getWifiById(data, args.show))
    if args.remove != None:
        db.removeItem(getWifiById(data, args.remove))

    minWidth = getColumnWidth()
    id = 0
    for wifi in data:
        id += 1
        print(formatWifi(id, wifi, minWidth))

def getWifiById(data, id):
    if id == None:
        id = 1
    count = 0
    for wifi in data:
        count += 1
        if id == count:
            return wifi
    return None

def connect(wifi):
    print("Connecting to "+ wifi.name)
    network.connectWifi(wifi.ssid, wifi.encryption, wifi.passphrase)

def showInfo(wifi):
    for field in wifi._fields:
        print(field + ': ' + getattr(wifi, field))

def editInfo(wifi):
    newinfo = []
    for field in wifi._fields:
        newinfo.append(rlinput(field + ': ', getattr(wifi, field)))
    return database.wifiRecord._make(newinfo)

def getColumnWidth():# ToDo use
    minWidth = [15 for i in range(0,5)]
    minWidth[0] = 2
    return minWidth

def fillWidth(strings, minWidth):
    if minWidth == None:
        return strings
    newStrings = ['' for i in range(0, len(strings)-1)]
    for i in range(0,min(len(minWidth),len(strings))-1):
        newStrings[i] = strings[i]+' ' * (minWidth[i]-len(strings[i]))
    return newStrings

def formatWifi(id, wifi, minWidth = None):
    return ' | '.join(fillWidth([str(id), wifi.name, wifi.ssid, wifi.location, wifi.comment],minWidth))

def inputWifi():
    wifiInput = []
    wifiInput.append(input("Enter connection name: "))
    wifiInput.append(input("SSID: "))
    wifiInput.append("wpa-psk")
    wifiInput.append(input("Passphrase: "))
    wifiInput.append(input("Location: "))
    wifiInput.append("")
    wifiInput.append(input("Comment: "))
    return database.wifiRecord._make(wifiInput)

def rlinput(prompt, prefill=''):
   readline.set_startup_hook(lambda: readline.insert_text(prefill))
   try:
      return input(prompt)
   finally:
      readline.set_startup_hook()

def addParse(parse):
    return parseAdd.parseWifi(parse)

if __name__ =='__main__':
    main()
