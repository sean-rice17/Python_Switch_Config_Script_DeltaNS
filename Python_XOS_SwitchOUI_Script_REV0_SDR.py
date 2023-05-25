# version 1
# Credit: Extreme Networks GitHub, located in README

import re
import exsh

def exosCmd(cmd):
        # print cmd
        result = exsh.clicmd(cmd, True)
        # result = cmd
        print(result)
        return result

def configSwitchVlans():
    # build regex patterns to use later
    # OUI pattern
    pattern1 = "((\w+:){3})"

    # sho_fdb = open("show_fdb.log", 'r')
    show_fdb = exosCmd('show fdb') 
    #create file to write result of shoFDB to directly
    fdb_file = open("fdb_file_Initial.txt", 'w')

    # use Regex to find Device Data based on OUI pattern match, then write data to file
    found_match = False
    for line in show_fdb:
        fdb_file.write(line)
    fdb_file.close()
    formatted_fdb = open("fdb_file_Initial.txt", 'r')
    macMatches = open("fdb_MatchesOnly.txt", 'w')
    for line in formatted_fdb:
        match = re.search(pattern1, line)
        if match != None:
            # print line
            macMatches.write(line)
            found_match = True
    
    if found_match == True:
        pass
    else:
        print("~~~~~No regex matches found. Check regex in script")
        exit()
    
    formatted_fdb.close()
    macMatches.close()

    # reopen data file for reading, create 2D array where each index corresponds
    # to one device discovered using show fdb

    deviceDataFile = open('fdb_MatchesOnly.txt', 'r')
    deviceListInitial = deviceDataFile.readlines()
    i = 0
    j = 0
    k = 0
    deviceList2Darr = []
    while i < len(deviceListInitial):
        print("loop entered")
        currentDevice = deviceListInitial[i].split()
        deviceList2Darr.append(currentDevice)
        i += 1
        j += 1
    j = 0
    deviceDataFile.close()

    print ("")

    deviceBufferString = "--------------------"

    # print contents of 2d array
    while j < len(deviceList2Darr):
        print (deviceBufferString)
        print ("")
        while k < len(deviceList2Darr[j]):
            print(deviceList2Darr[j][k])
            k += 1
        j += 1
        k = 0

    print(deviceBufferString)
    print("")

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
        print (item)

    #logic for creating list of undesirable ports
    userInput = ""
    # uplinkPorts = ["1:40", "2:32"]

    uplinkPorts = []
    print("Enter the uplink ports which will be excluded from the configuration process. Enter q to finish entering ports.")
    while userInput != 'q':
        userInput = str(raw_input("\n"))
        uplinkPorts.append(userInput)
    uplinkPorts.pop()
    print ("")


    #logic for removing uplink ports from list

    deviceListArrFinal = []
    found = False
    for i in range(len(deviceList2darr_filtered)):
        currentPort = deviceList2darr_filtered[i][-1]
        for j in range(len(uplinkPorts)):
            if currentPort == uplinkPorts[j]:
                found = True
                
        if found == False:
            deviceListArrFinal.append(deviceList2darr_filtered[i])
        # only add items to the list if they do not match any uplink ports
        else:
            found = False
            

    # print the completely filtered device list
    print("Final list size is", len(deviceListArrFinal))
    for i in range(len(deviceListArrFinal)):
        print(str(deviceListArrFinal[i]))



    #logic for sending configuration commands to switch
    print("\nEnter the name of the vlan you want to assign to these devices.\n")
    #input Vlan Name
    vlanName = raw_input("Vlan Name: ")
    #input tag status
    tagStatus = raw_input("tagged/untagged: ")

    #logic for creating a list of all unique port numbers
    portListNoDoubles = []
    portListFinal = []
    #initial loop to create a 1D list of all port numbers
    for i in range (len(deviceListArrFinal)):
        portListNoDoubles.append(deviceListArrFinal[i][-1])
    
    #second loop to create final list of only unique port numbers
    for i in range (len(portListNoDoubles)):
        if portListNoDoubles[i] not in portListFinal:
            portListFinal.append(portListNoDoubles[i])

    #final loop to send configuration command based on remaining ports
    for i in range(len(portListFinal)):
        portNum = portListFinal[i]
        configStr = "configure " + vlanName + " add ports " + portNum + " " + tagStatus
        exosCmd(configStr)
        print(configStr + "-- Config Successful")


#driver loop (main)
moreConfigs = 'y'
while (moreConfigs != 'n'):
    configSwitchVlans()
    print("Would you like to configure another vlan?")
    moreConfigs = raw_input("(y/n)")

print("Vlan Configuration Completed")