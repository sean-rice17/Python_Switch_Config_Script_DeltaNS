# version 1

import re
# import exsh

# Credit: Extreme Networks GitHub, located in README
#
def exosCmd(cmd):
        # print cmd
        # result = exsh.clicmd(cmd, True)
        result = cmd
        print result
        return result
#

# build regex patterns to use later
# OUI pattern
pattern1 = "((\w+:){3})"

# input stream from 'sho fdb' command
show_fdb = open("show_fdb.log", 'r')
# show_fdb = exosCmd('sho fdb')
#create file to write device data to from showfdb
fdb_file = open("fdb_file.txt", 'w')

# use Regex to find Device Data based on OUI pattern match, then write data to file
for line in show_fdb:
    match = re.search(pattern1, line)
    if match != None:
        # print line
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

print ""

# print contents of 2d array
while j < len(deviceList2Darr):
    deviceBufferString = "--------------------"
    print deviceBufferString
    print ""
    while k < len(deviceList2Darr[j]):
        print deviceList2Darr[j][k]
        k += 1
    j += 1
    k = 0

print deviceBufferString
print ""

#prompt user for OUI

OUI = str(raw_input("Enter an OUI: \n"))
# OUI = "00:10:49"

# add entries with matching OUIs to new array
deviceList2darr_filtered = []
for i in range(len(deviceList2Darr)):
    if OUI in deviceList2Darr[i][0]:
        deviceList2darr_filtered.append(deviceList2Darr[i])
    i += 1
# display the new array
for item in deviceList2darr_filtered:
    print item

#logic for creating list of undesirable ports
userInput = ""
uplinkPorts = []
print("Enter the uplink ports which will be excluded from the configuration process. Enter q to finish entering ports.")
while userInput != 'q':
    userInput = str(raw_input("\n"))
    uplinkPorts.append(userInput)
uplinkPorts.pop()
print ""


#logic for removing uplink ports from list

# FIX: filtering devices that have uplink ports does not work if the list "uplinkPorts" has more than 1 element

deviceList2darr_final = []
found = False
for i in range(len(deviceList2darr_filtered)):
    currentPort = deviceList2darr_filtered[i][-1]
    for j in range(len(uplinkPorts)):
        if currentPort == uplinkPorts[j]:
            found = True
            # break
    
    if found == True:
        found == False
        continue
    # only add items to the list if they do not match any uplink ports
    deviceList2darr_final.append(deviceList2darr_filtered[i])

# print the completely filtered device list
for i in range(len(deviceList2darr_final)):
    print deviceList2darr_final[i]

print "Check TODO comment in script."
exit()

#logic for sending configuration commands to switch

flag = True
while flag == True:
    print("\nEnter the name of the vlan you want to assign to these devices.\n")
    vlanName = raw_input("Vlan Name: ")
    # TODO: loop for each item in the list
    
    #

    # TODO: do all untagged or tagged items, depending on user input
    
    #

    configStr = "configure " + vlanName + " add ports " + portNum + " " + tagStatus
    # vlanPortList = exosCmd(configStr)
    print configStr
    print("Would you like to configure again?")
    moreConfigs = raw_input("(y/n)")
    if moreConfigs == 'n':
        flag = False