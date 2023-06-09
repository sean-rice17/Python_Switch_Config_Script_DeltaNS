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

# REMOVE PRINTING OF INDIVIDUAL FDB ENTRIES
    # print contents of 2d array
    """
    while j < len(deviceList2Darr):
        print (deviceBufferString)
        print ("")
        while k < len(deviceList2Darr[j]):
            print(deviceList2Darr[j][k])
            k += 1
        j += 1
        k = 0
    """ 
    #Removed Printing
    
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
    # display the new array
    for item in deviceList2darr_filtered:
        print (item)
        
#ADD printing of "sho vlan" command -- display vlan names only

    show_Vlans = exosCmd('sho vlan')
    
    #logic for creating list of undesirable ports
    userInput = ""
    # uplinkPorts = ["1:40", "2:32"]
    
    
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
    print("\nEnter the name of the vlan you want to assign to these devices.\n")
    #input Vlan Name
    vlanName = raw_input("Vlan Name: ")
    if vlanName not in show_Vlans:
        while vlanName not in show_Vlans:
            print("Error: vlanName is not one of the available vLans on this Network.\nPlease try Again.")
            vlanName = raw_input("Vlan Name: ")
        
    #input tag status
    tagStatus = ""
    while "tagged" not in tagStatus:
        tagStatus = raw_input("tagged/untagged: ")
        if "tagged" not in tagStatus:
            print("Error. Please enter tagged or untagged only.")

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