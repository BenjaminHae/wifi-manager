#!/usr/bin/python3
import configparser
import database

# parse wifi from networkManager
# data = opened textfile
def parseWifi(data):
    parser = configparser.ConfigParser()
    parser.read_file(data)
    _misc = 'connection'
    _info = '802-11-wireless'
    _security = '802-11-wireless-security'
    wifiData = [parser.get(_misc,'id'), parser.get(_info,'ssid'), parser.get(_security,'key-mgmt'), parser.get(_security, 'psk'), '', '', '']
    return database.wifiRecord._make(wifiData)

if __name__ == '__main__':
    pass
