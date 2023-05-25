# version 1
# Credit: Extreme Networks GitHub, located in README

import re
import exsh

def exosCmd(cmd):
        # print cmd
        result = exsh.clicmd(cmd, True)
        # print(result)
        return result

def configSwitchVlans():
    # build regex patterns to use later
    # OUI pattern
    print("initialize pattern1")
    pattern1 = "((\w+:){3})"

    print("initialize input streams") 
    # sho_fdb = open("show_fdb.log", 'r')
    show_fdb = exosCmd('show fdb') 
    #create file to write result of shoFDB to directly
    fdb_file = open("fdb_file_Initial.txt", 'w')

    # use Regex to find Device Data based on OUI pattern match, then write data to file
    print("attempting for line in show_fdb")
    found_match = False
    for line in show_fdb:
        fdb_file.write(line)
    fdb_file.close()
    formatted_fdb = open("fdb_file_Initial.txt", 'r')
    macMatches = open("fdb_MatchesOnly.txt", 'w')
    for line in formatted_fdb:
        match = re.search(pattern1, line)
        if match != None:
            print("if match != none")
            # print line
            macMatches.write(line)
            found_match = True
    
    if found_match == True:
        print("~~~~~Regex matches found!")
    else:
        print("~~~~~No matches found. Check regex in script")
        user_continue = str(input("Press Enter to continue.\n"))
    
    print("closing fdb_file")
    formatted_fdb.close()
    macMatches.close()

    # reopen data file for reading, create 2D array where each index corresponds
    # to one device discovered using show fdb

    print("attempting Create 2d array")
    print("opening device data file")
    deviceDataFile = open('fdb_MatchesOnly.txt', 'r')
    deviceListInitial = deviceDataFile.readlines()
    i = 0
    j = 0
    k = 0
    deviceList2Darr = []
    print("attempting to enter 'while i < len(devicelistInitial)'")
    while i < len(deviceListInitial):
        print("loop entered")
        currentDevice = deviceListInitial[i].split()
        deviceList2Darr.append(currentDevice)
        i += 1
        j += 1
    j = 0
    print("closing device data file")
    deviceDataFile.close()

    print ("")

    deviceBufferString = "--------------------"

    # print contents of 2d array
    print("print contents of 2d array")
    while j < len(deviceList2Darr):
        print("entered loop")
        print (deviceBufferString)
        print ("")
        while k < len(deviceList2Darr[j]):
            print(deviceList2Darr[j][k])
            k += 1
        j += 1
        k = 0

    print(deviceBufferString)
    print("")
    print("prompt user for OUI")

    #prompt user for OUI

    OUI = str(raw_input("Enter an OUI: \n"))
    # OUI = "00:10:49"

    print("add entries with matching OUIs to new array")
    # add entries with matching OUIs to new array
    deviceList2darr_filtered = []
    for i in range(len(deviceList2Darr)):
        print("entered loop")
        if OUI in deviceList2Darr[i][0]:
            print("entered 'if OUI in deviceList2darr'")
            deviceList2darr_filtered.append(deviceList2Darr[i])
        i += 1
    # display the new array
    print("display the new array")
    for item in deviceList2darr_filtered:
        print("entered loop")
        print (item)

    print("logic for creating list of uplink ports")
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
    print("removing uplink ports from the list")

    deviceListArrFinal = []
    found = False
    for i in range(len(deviceList2darr_filtered)):
        print("entered loop")
        currentPort = deviceList2darr_filtered[i][-1]
        for j in range(len(uplinkPorts)):
            print("entered nested loop")
            if currentPort == uplinkPorts[j]:
                found = True
                
        if found == False:
            print("if found == False")
            deviceListArrFinal.append(deviceList2darr_filtered[i])
        # only add items to the list if they do not match any uplink ports
        else:
            print("else")
            found = False
            

    # print the completely filtered device list
    print("Final list size is", len(deviceListArrFinal))
    for i in range(len(deviceListArrFinal)):
        print("entered loop")
        print(str(deviceListArrFinal[i]))



    #logic for sending configuration commands to switch
    print("\nEnter the name of the vlan you want to assign to these devices.\n")
    vlanName = raw_input("Vlan Name: ")
    # TODO: loop for each item in the list
    
    tagStatus = raw_input("tagged/untagged: ")

    print("attempting to config")
    portListNoDoubles = []
    portListFinal = []
    for i in range (len(deviceListArrFinal)):
        print("Entered loop 1")
        portListNoDoubles.append(deviceListArrFinal[i][-1])
    
    for i in range (len(portListNoDoubles)):
        print("Entered loop 2")
        if portListNoDoubles[i] not in portListFinal:
            portListFinal.append(portListNoDoubles[i])

    for i in range(len(portListFinal)):
        print("Entered loop 3")
        portNum = portListFinal[i]
        configStr = "configure " + vlanName + " add ports " + portNum + " " + tagStatus
        # exosCmd(configStr)
        print(configStr)

    print("---------------")
    print("------DONE-----")
    print("---------------")

print("entering driver loop")

#driver loop (main)
moreConfigs = 'y'
while (moreConfigs != 'n'):
    configSwitchVlans()
    print("Would you like to configure another vlan?")
    moreConfigs = raw_input("(y/n)")

print("Goodbye\n")