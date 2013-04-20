#!/usr/bin/python3

import sys
import sqlite3
import re
import urllib.request

def clear():
    conn = sqlite3.connect('macaddresses.db')
    c = conn.cursor()
    c.execute('delete from macaddresses')
    conn.commit()

def init():
    conn = sqlite3.connect('macaddresses.db')
    c = conn.cursor()
    c.execute('create table macaddresses (macaddress text, name text)')
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
        c.execute('select name from macaddresses where macaddress = ?', param)
        result = c.fetchone()
        if(result is None):
            storeAddys(addy, 'UNKNOWN [' + addy + ']')
            param = (addy, 'UNKOWN [' + addy + ']')
        else:
            param = (addy, result)
        
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
        print(i[1][0])

if __name__ == '__main__':
    if(len(sys.argv) == 3):
        storeAddys(sys.argv[1], sys.argv[2])
    elif(len(sys.argv) == 2):
        if(sys.argv[1] == 'init'):
            init()
        elif(sys.argv[1] == 'clear'):
            clear()
    else:
        main()
