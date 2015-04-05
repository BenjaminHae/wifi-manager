#!/usr/bin/python3
import configparser
import database

# parse wifi from networkManager
# data = opened textfile
def parseWifi(data):
    parser = configparser.configparser()
    parser.read_file(data)
    _misc = 'connection'
    _info = '802-11-wireless'
    _security = '802-11-wireless-security'
    wifiData = [parse.get(_misc,'id'), parse.get(_info,'ssid'), parse.get(_security,'key-mgmt'), parse.get(_security, 'psk'), '', '', '']
    return database.wifiRecord._make(wifiData)

if __name__ == '__main__':
    pass
