# version 0

import re
#import exsh

# Credit: 
"""
def exosCmd(cmd):
        # print cmd
        result = exsh.clicmd(cmd, True)
        # print(result)
        return result
#

# build regex patterns to use later
# OUI pattern
"""
pattern1 = "((\w+:){3})"

# input stream from 'sho fdb' command
show_fdb = open("show_fdb.log", 'r')
#show_fdb = exosCmd('sho fdb')
#create file to write device data to from showfdb
fdb_file = open("fdb_file.txt", 'w')

# use Regex to find Device Data based on OUI pattern match, then write data to file
for line in show_fdb:
    match = re.search(pattern1, line)
    if match != None:
        print(line)
        fdb_file.write(line)

fdb_file.close()

# reopen data file for reading, create 2D array where each index corresponds
# to one device discovered using show fdb
deviceDataFile = open('fdb_file.txt', 'r')
deviceListInitial = deviceDataFile.readlines()
i = 0
j = 0
k = 0
deviceList2Darr = []
while i < len(deviceListInitial):
    currentDevice = deviceListInitial[i].split()
    deviceList2Darr.append(currentDevice)
    i += 1
    j += 1
j = 0
while j < len(deviceList2Darr):
    while k < len(deviceList2Darr[j]):
        print(deviceList2Darr[j][k])
        k += 1
    j += 1
    k = 0

#prompt user for OUI and delete all items from list that do not contain that OUI

OUI = str(input("Enter an OUI: \n"))
i = 0
j = 0
while i < len(deviceList2Darr):
    if OUI not in deviceList2Darr[i][0]:
        deviceList2Darr.pop(i)
    i += 1

i = 0
while i < len(deviceList2Darr):
    print(deviceList2Darr[i])
    i += 1

#logic for creating list of undesirable ports
userInput = ""
uplinkPorts = []
print("Enter any number of uplink ports. Enter q to finish entering ports. ")
while userInput != 'q':
    userInput = str(input("\n"))
    uplinkPorts.append(userInput)
uplinkPorts.pop()

#logic for removing uplink ports from list
x = 0
while x < len(deviceList2Darr):
    currentPort = deviceList2Darr[x][-1] 
    if currentPort in uplinkPorts:
        poppedItem = deviceList2Darr.pop(x)
    x+=1
i = 0
while i < len(deviceList2Darr):
    print(deviceList2Darr[i])
    i+=1

#logic for sending configuration commands to switch

flag = True
while flag == True:
    print("\nEnter Vlan name to begin configuration process.\n")
    vlanName = input("Vlan Name: ")
    print("\nEnter port you wish to add\n")
    portNum = input("Port: ")
    print("\nEnter status of tag (tagged or untagged)\n")
    tagStatus = input("Status: ")
    configStr = "configure " + vlanName + " add ports " + portNum + " " + tagStatus
    #vlanPortList = exosCmd(configStr)
    print(configStr)
    print("Would you like to configure another port?")
    moreConfigs = input("(y/n)")
    if moreConfigs == 'n':
        flag = False