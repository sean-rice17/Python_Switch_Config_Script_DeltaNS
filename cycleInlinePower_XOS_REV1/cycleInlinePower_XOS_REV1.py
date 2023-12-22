# version 1
# Credit: Extreme Networks GitHub, located in README

import re
import exsh
import time

def exosCmd(cmd):
        # print cmd
        result = exsh.clicmd(cmd, True)
        # result = cmd
        print(result)
        return result

def cycleInlinePower():
    # build regex patterns to use later
    # OUI pattern
    pattern1 = "((\w+:){3})"

    # sho_fdb = open("show_fdb.log", 'r')
    show_fdb = exosCmd('show fdb') 
    #create file to write result of shoFDB to directly
    fdb_file = open("fdb_file_Initial.txt", 'w')

    # use Regex to find Device Data based on OUI pattern match, then write data to file
    found_match = False
    #write initial show FDB result directly to file
    for line in show_fdb:
        fdb_file.write(line)
    fdb_file.close()
    #Reopen file containing show FDB data and work with this
    formatted_fdb = open("fdb_file_Initial.txt", 'r')
    #create file that contains only information from matching mac Addresses
    macMatches = open("fdb_MatchesOnly.txt", 'w')
    for line in formatted_fdb:
        match = re.search(pattern1, line)
        if match != None:
            macMatches.write(line)
            found_match = True
    
    if found_match == True:
        pass
    else:
        print("~~~~~No regex matches found. Check regex in script")
        exit()
    
    formatted_fdb.close()
    macMatches.close()
    

    # reopen data file (macMatches) for reading
    # create 2D array where each index corresponds
    # to one device discovered using show fdb

    deviceDataFile = open('fdb_MatchesOnly.txt', 'r')
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
    deviceDataFile.close()

    print ("")

    deviceBufferString = "--------------------"

    
    print(deviceBufferString)
    print("")

    #prompt user for OUI

    OUI = str(raw_input("Enter an OUI <##:##:##>: \n"))
    # OUI = "00:10:49"

    # add entries with matching OUIs to new array
    deviceList2darr_filtered = []
    for i in range(len(deviceList2Darr)):
        if OUI in deviceList2Darr[i][0]:
            deviceList2darr_filtered.append(deviceList2Darr[i])
        i += 1
    
    #ADD printing of "sho vlan" command -- display vlan names only

    show_Vlans = exosCmd('sho vlan')
    
    # display the new array
    for item in deviceList2darr_filtered:
        print (item)
        

    
    #logic for creating list of undesirable ports
    userInput = ""
    # uplinkPorts = ["1:40", "2:32"]
    
    
    show_Edp = exosCmd('sho edp ports all')
#ADD error checking for user input
    uplinkPattern = "\d+:\d+\d*"
    uplinkPorts = []
    print("Enter the uplink ports which will be excluded from the configuration process. Enter q to finish entering ports.")
    while userInput != 'q':
        userInput = str(raw_input("\n"))
        match2 = re.search(uplinkPattern, userInput)
        if match2 != None:
            uplinkPorts.append(userInput)
    
        elif userInput == 'q' or 'Q':
            print("Finished Entering Uplink Ports.")
        else: 
            print("Error: Please Enter uplink ports in the format #:##")
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
    for i in range(len(deviceListArrFinal)):
        print(str(deviceListArrFinal[i]))



    #logic for sending configuration commands to switch
        

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

    #Loop to disable inline power to all ports 
    for i in range(len(portListFinal)):
        portNum = portListFinal[i]
        configStr = "disable inline-power port " + portNum 
        exosCmd(configStr)
        print(configStr + "-- Command Successful")

    #Wait 10 seconds before beginning second loop
    print("\nPower on will begin in 10 seconds...\n")
    time.sleep(10)


    #Loop to enable inline power to all ports
    for i in range(len(portListFinal)):
        portNum = portListFinal[i]
        configStr = "enable inline-power port " + portNum 
        exosCmd(configStr)
        print(configStr + "-- Command Successful")


#driver loop (main)
moreConfigs = 'y'
while (moreConfigs != 'n'):
    cycleInlinePower()
    print("Would you like to cycle power for another OUI?")
    moreConfigs = raw_input("(y/n)")

print("Power Cycle Complete")