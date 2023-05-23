# version 0

import re

# build regex patterns to use later
# OUI pattern
pattern1 = "((\w+:){3})"

# input stream from 'sho fdb' command
show_fdb = open("show_fdb.log", 'r')
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
deviceList2Darr = [[0]*2]*2
while i < len(deviceListInitial):
    currentDevice = deviceListInitial[i].split()
    deviceList2Darr[j] = currentDevice
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
print (len(deviceList2Darr))
"""
for i in range(len(deviceList2Darr)):
    if OUI not in deviceList2Darr[i][0]:
        deviceList2Darr.pop(i)

for i in range(len(deviceList2Darr)):
    print(deviceList2Darr[i])

"""

