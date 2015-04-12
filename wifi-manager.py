#!/usr/bin/python3
#from curses import wrapper
import database
import network
import argparse
import sys
import os
import parseAdd
import readline
import barcode
#ToDo: Add Verbosity/Question befor removing

def parseArgs():
    parser = argparse.ArgumentParser(description='Manage list of wifi networks')
    parser.add_argument('--filter', metavar='expression', action='store', help='search for WIFI network')
    parser.add_argument('--show', action='store_true', help='show all information about wifi')
    parser.add_argument('--s', action='store_true', dest='showShort', help='show short information of wifi')
    parser.add_argument('--bar', action='store_true', help='show a barcode to connect')
    parser.add_argument('--path', action='store', help='use file as database')
    parser.add_argument('--connect', action='store_true', help='connect to network')
    parser.add_argument('--add', action='store_true', help='add network')
    parser.add_argument('--remove',  action='store_true', help='remove entry id')
    parser.add_argument('--edit', action='store_true', help='edit entry')
    parser.add_argument('--parse-add', action='store_true', dest='parse', help='add multiple networks by parsing standard input or files')
    parser.add_argument('id', help='ids for actions', metavar='id', nargs='*', type=int, action='store')
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
    
    data = getData(args.filter, db)

    id = args.id # ToDo multiple IDs
    if (id == None or len(id) == 0) and (args.remove == True):
        parser.error("--remove requires id")
    elif id == None or len(id) == 0:
        id = [1]
    wifis = [getWifiById(data,id[0])]# ToDo return multiple wifis
    
    actions = []
    if args.showShort:
        actions.append(lambda wifi: print(shortInfo(wifi)))
    if args.bar:
        actions.append(lambda wifi: print(barcode.getBarcode(wifi)))
    if args.show:
        actions.append(lambda wifi: print(showInfo(wifi)))
    if args.edit:
    	actions.append(lambda wifi: replaceEdit(db, wifi))
        
    if args.connect:
        connect(wifis[0]) # for obvious reasons connect to only one wifi
    if args.remove:
    	actions.append(lambda wifi: db.removeItem(wifi))

    for wifi in wifis:
    	for action in actions:
	    action(wifi)

    data = getData(args.filter, db)
    
    # ToDo reset filters bevor showing results
    minWidth = getColumnWidth()
    id = 0
    for wifi in data:
        id += 1
        print(formatWifi(id, wifi, minWidth))
        
def getData(filter, db):
    if filter != None:
        return db.filteredData(filter)
    else:
        return db.getData()


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
    text = ""
    for field in wifi._fields:
        text += (field + ': ' + getattr(wifi, field))+"\r\n"
    return text

def shortInfo(wifi):
    text = wifi.name
    return text

def editInfo(wifi):
    newinfo = []
    for field in wifi._fields:
        newinfo.append(rlinput(field + ': ', getattr(wifi, field)))
    return database.wifiRecord._make(newinfo)

def replaceEdit(db, wifi):
    oldWifi=wifi
    newWifi=editInfo(oldWifi)
    db.removeItem(oldWifi)
    db.addItem([newWifi])

def getColumnWidth():# ToDo use
    rows, columns = map(int,os.popen('stty size', 'r').read().split())
    colWidth = (columns - 4*2 - 2)// 4 # -7 für spalten und id
    minWidth = [colWidth for i in range(0,5)]
    minWidth[0] = 2
    return minWidth

def fillWidth(strings, minWidth):
    if minWidth == None:
        return strings
    newStrings = ['' for i in range(0, len(strings))]
    oversize = 0
    for i in range(0,len(strings)):
        newStrings[i] = strings[i]+' ' * (minWidth[i] - len(strings[i]) - oversize)
        oversize += len(newStrings[i]) - minWidth[i]
    return newStrings

def formatWifi(id, wifi, minWidth = None):
    return '| '.join(fillWidth([str(id), wifi.name, wifi.ssid, wifi.location, wifi.comment],minWidth))

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
