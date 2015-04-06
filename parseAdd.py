#!/usr/bin/python3
import configparser
import database
import sys

# parse wifi from networkManager
# data = opened textfile
def parseWifi(data):
    parser = configparser.ConfigParser()
    parser.read_file(data)
    _misc = 'connection'
    _info = '802-11-wireless'
    _security = '802-11-wireless-security'
    try:
        wifiData = [parser.get(_misc,'id'), parser.get(_info,'ssid'), parser.get(_security,'key-mgmt'), parser.get(_security, 'psk'), '', '', '']
    except Exception as e:
        print("couldn't parse: " + str(e), file = sys.stderr)
        return None
    return database.wifiRecord._make(wifiData)

if __name__ == '__main__':
    pass
