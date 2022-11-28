import re

a = '''
Router# show cdp neighbors detail 

-------------------------
Device ID: device2.cisco.com
Entry address(es):
  IP address: 171.68.162.134
Platform: cisco 4500,  Capabilities: Router
Interface: Ethernet0/1,  Port ID (outgoing port): Ethernet0
Holdtime : 156 sec
 
Version :
Cisco Internetwork Operating System Software
IOS (tm) 4500 Software (C4500-J-M), Version 11.1(10.4), MAINTENANCE INTERIM SOFTWARE
Copyright (c) 1986-1997 by Cisco Systems, Inc.
Compiled Mon 07-Apr-97 19:51 by dschwart
'''

def tempregex(a):
    #output = re.findall(r'HOMEWORLD:\s+(\w+)\nAPPROVAL RATING:\s+(\w+)', a, re.MULTILINE)
    output = re.findall(r'Device ID: (\w.+)', a, re.MULTILINE)
    print (output)
    output = re.findall(r'Interface: (\w.+)', a, re.MULTILINE)
    print (output)
    output = re.findall(r'  IP address: (\w.+)', a, re.MULTILINE)
    print (output)
    print ('Multiline Regex')
    output = re.findall(r'Device ID: (\w.+)\n', a, re.MULTILINE)
    print (output)

#tempregex(a)

'''
TEXTO = "Var"
subject = r"Var\boundary"

if re.search(rf"\b(?=\w){TEXTO}\\boundary(?!\w)", subject, re.IGNORECASE):
    print("match")
'''

import re
var = 13546537
serial = "asdfID:13546537(0xCEB429)"

if re.search(fr"ID:{var}", serial):
    print("match found")
else:
    print("match not found")