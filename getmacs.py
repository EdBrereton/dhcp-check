#!/usr/bin/python3

import sys
import sqlite3
import re
import urllib.request

def storeAddys(macaddys):
    conn = sqlite3.connect('macaddresses.db')
    c = conn.cursor()
    for x in macaddys:
        t = (x, 'UNKNOWN')
        c.execute('insert into macaddresses values (?, ?)', t)
        conn.commit()

def storeAddys(macaddys, name):
    conn = sqlite3.connect('macaddresses.db')
    c = conn.cursor()
    params = (macaddys,)
    c.execute('select * from macaddresses where macaddress = ?', params)
    params = (macaddys, name)
    if(c.rowcount == 0):
        c.execute('update macaddresses set name = ? where macaddress = ', params)
    else:
        c.execute('insert into macaddresses values (?, ?)', params)
    conn.commit()

def lookupAddys(macaddys):
    conn = sqlite3.connect('macaddresses.db')
    c = conn.cursor()
    array = []
    for addy in macaddys:
        param = (addy, )
        c.execute('select * from macaddresses where macaddress = ?', param)
        if(c.rowcount == 0):
            storeAddys(addy, 'UNKNOWN')
            param = (addy, 'UNKOWN')
        else:
            for name in c:
                param = (addy, name[1])
        
        array.append(param)
    
    return array

def getAddys(url, user, password):
    passman = urllib.request.HTTPPasswordMgrWithDefaultRealm()
    passman.add_password(None, url, user, password)
    authhandler = urllib.request.HTTPBasicAuthHandler(passman)
    opener = urllib.request.build_opener(authhandler)
    urllib.request.install_opener(opener)
    
    pagehandle = urllib.request.urlopen(url)
    pagedata = pagehandle.read()
    pagetext = pagedata.decode('utf8')

    regex = '[0-9A-Fa-f][0-9A-Fa-f]:[0-9A-Fa-f][0-9A-Fa-f]:[0-9A-Fa-f][0-9A-Fa-f]:[0-9A-Fa-f][0-9A-Fa-f]:[0-9A-Fa-f][0-9A-Fa-f]:[0-9A-Fa-f][0-9A-Fa-f]'
    comregex = re.compile(regex)
    
    macaddys = comregex.findall(pagetext)
    return macaddys

def main():
    url = 'http://192.168.0.1/setup.cgi?todo=nbtscan&next_file=DEV_devices.htm'
    user = 'admin'
    password = 'password'
    macaddys = getAddys(url, user, password)
    namearray = lookupAddys(macaddys)

    for i in namearray:
        print(i[1])

if __name__ == '__main__':
    if(len(sys.argv) == 3):
        storeAddys(sys.argv[1], sys.argv[2])
    else:
        main()
