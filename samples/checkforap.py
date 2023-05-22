print('\n *****Starting Check for AP Script***** \n')
#
def exosCmd(cmd):
        #print cmd
        result = exsh.clicmd(cmd, True)
        #print result
        return result
#
apPorts=[]
lldp_ports=[]
port_list=[]
line_split=[]
last_num=[]
vlanPortList=''
# Get LLDP neighbors from EXOS
lldp_neighbors = exosCmd('show lldp neighbor')
# Split LLDP neighbors output into lines
lldp_neighbors_lines=lldp_neighbors.splitlines()
#Isolate just the LLDP neighbor output to just the port lines
lldp_ports += lldp_neighbors_lines[4:-3]
#
#print(lldp_neighbors)
#
#De-dup LLDP port list
for line in lldp_ports:
        line_split=list(line.split(" "))
        if last_num != line_split[:1]:
                port_list+=line_split[:1]
                last_num = line_split[:1]
        else:
                next
#
#print(port_list)
#
#Use LLDP port list to look for ports with AP, searching for entries with "WLAN AP"
print('\n Detected APs on the following ports \n')
for port in port_list:
        portLldpInfo = exosCmd('show lldp port '+port+' neighbor detail').splitlines()
        for line in portLldpInfo:
                if "WLAN AP" in line:
                        apPorts.append(port)
                        print('\n'+port + line)
                        break
#
#print(apPorts)
#
for port in apPorts:
    vlanPortList = exosCmd('show port '+port+' vlan')
    if 'Default' in vlanPortList and 'LabNet' in vlanPortList and 'Staff' in vlanPortList and 'Student' in vlanPortList:
#        print(vlanPortList)
        print('\n AP detected!!! Port '+port+' already has correct VLANs')
    else:
        print('\n AP detected!!! Adding correct VLANs to port '+port)
        print(vlanPortList)
#        exosCmd('configure vlan 1 add port '+port)
#        exosCmd('configure vlan 10,36,40 add ' +port+' tagged')
print('\n *****Check for AP Script complete*****')