import sys

# Constants
DMM_INT = '100ms'
SLM_INT = '100ms'
PRIORITY = '0'

# Variable Declarations
version = None
location = None
port = None
vlan = None
mepType = None
switch = None
carrier = None
localMep = None
remoteMep = None
serviceType = None
circuit = None
servicename = None
testName = None


# Handle the password input, and ConnectHandler to be able to connect to the device
from netmiko import ConnectHandler, NetMikoTimeoutException, NetMikoAuthenticationException
import getpass

# Ask for device details to allow input for different devices
device_ip = input("Enter the device IP address: ").strip()
device_username = input("Enter the SSH username: ").strip()
device_password = getpass.getpass("Enter the SSH password: ")

device = {
    'device_type': 'ciena_saos',
    'host': device_ip,
    'username': device_username,
    'password': device_password,
    'port': 22
}

# Establish a connection
try:
    print("Attempting to connect to the device...")
    net_connect = ConnectHandler(**device)

    # Confirm successful connection
    print(f"Successfully connected to {device['host']}")
except NetMikoTimeoutException:
    print(f"Connection timed out when attempting to reach {device['host']}")
    sys.exit(1)
except NetMikoAuthenticationException:
    print(f"Authentication failed for device {device['host']}")
    sys.exit(1)
except Exception as e:
    print(f"Failed to connect to {device['host']}: {e}")
    sys.exit(1)
#Initialize commands as a list
commands = []

#Get the information for the test
version = int(input('Please enter the version (6 or 10): '))#Get the version of the test
while version not in {6,10}:
    version = int(input('Invalid version, please enter 6 or 10 according to the version of the device: '))

if version == 6: #Logic for Version 6 Ciena devices

    location = input('Please enter the location of the device (A, Z-vs, Z-vlan): ').strip().lower() # Get the location of the device
    while location not in {'a','z-vs','z-vlan'}:
        location = input('Invalid Entry please enter a valid location (A, Z-vs, Z-vlan): ').strip().lower()

    port = int(input('Please enter the port number: '))#Get the port number
    while port < 0 or port > 65535:
        port = int(input('Please enter a valid port number: '))

    vlan = int(input('Please enter the Vlan ')) #Get the Vlan
    while vlan < 0 or vlan > 4095:
        vlan = int(input('Invalid entry, please entry a valid Vlan: '))

    mepType = input('Please enter the MEP Type (Up or Down): ').strip().lower() #Get the MEP Type
    while mepType not in ['up','down']:
        mepType = input ('Invalid Entry please enter a valid MEP Type (Up or Down): ').strip().lower()

    switch = int(input('Please enter the Switch (1 or 2): ')) #Get the Switch
    while switch not in {1, 2}:
        switch = int(input('Invalid entry please enter the Switch (1 or 2): '))

    carrier = input('Please enter the Carrier initials (TMO, VZW, ATT,): ').strip().lower() #Get the carrier
    while carrier not in ['tmo','vzw','att']:
        carrier = input('Invalid Entry, Please enter the Carrier initials (TMO, VZW, ATT): ').strip().lower()

    if carrier == 'vzw': #Modify the carrier to name convention
        carrier = 'Verizon'
    else:
        carrier = carrier.upper()

    if location == 'a': #get the localMEP
        localMep = vlan
    elif location == 'z-vs' or location =='z-vlan':
        localMep = switch

    if location == 'a': #Get the remote MEP
        remoteMep = switch
    elif location == 'z-vs' or location == 'z-vlan':
        remoteMep = vlan

    if location == 'a' or location == 'z-vs': #Get the service type
        serviceType = "vs"
    else:
        serviceType = 'vlan'

    circuit = int(input('Please enter the circuit number: ')) #Get the circuit number
    while circuit < 1 or circuit > 1000000000:
        circuit = int(input('Invalid entry please enter a valid circuit number: '))

    if circuit < 100000: # format the circuit number to 5 digits
        circuit = f'{circuit:05}'

    servicename = "TEST" + str(circuit) + ':' + str(vlan)  # Get and format the service name
    add_nid = input('It is anything else that you would like to add to the service name? (yes/no) ').strip().lower()
    if add_nid == 'yes':
        add_nid = input('Please enter here what you want to add to the service name ')
        servicename += add_nid
    testName = servicename

    #Add commands to the list
    commands.append('cfm enable') #Main config
    commands.append(f'cfm md create md 3 md-name-string Y1731-{carrier}-Level3')
    if location == 'a' or location == 'z-vs':
        commands.append(f'cfm service create vs {servicename} name {testName} md 3')
    else:
        commands.append(f'cfm service create vlan {vlan} name {testName} md 3')
    commands.append(f'cfm service set service {testName} alarm-priority 2')
    commands.append(f'cfm service set service {testName} alarm-time 0')
    commands.append(f'cfm service set service {testName} remote-mep-aging-time 300000')
    commands.append(f'cfm service enable service {testName}')
    if location == 'a':
        commands.append(f'cfm mep create service {testName} port {port} vlan {vlan} type {mepType} mepid {localMep}')
    commands.append(f"cfm mep set service {testName} local-mep {localMep} ccm-priority {PRIORITY}")
    commands.append(f'cfm service set service {testName} ccm-interval 100ms')
    commands.append(f'cfm delay send service {testName} local-mepid {localMep} mepid {remoteMep} iterate 0 priority {PRIORITY} dmm-interval {DMM_INT}')
    commands.append(f'cfm synthetic-loss send service {testName} local-mepid {localMep} mepid {remoteMep} test-id 1 iterate 0 priority {PRIORITY} slm-interval {SLM_INT}')
    commands.append('con sa')


if version == 10: #Logic for version 10 ciena devices
    location = input('Please enter the location of the device (A or Z): ').strip().lower()  # Get the location of the device
    while location not in {'a', 'z'}:
        location = input('Invalid Entry please enter a valid location (A or Z): ').strip().lower()

    vlan = int(input('Please enter the Vlan: '))  # Get the Vlan
    while vlan < 0 or vlan > 4095:
        vlan = int(input('Invalid entry, please entry a valid Vlan: '))

    switch = int(input('Please enter the Switch (1 or 2): '))  # Get the Switch
    while switch not in {1, 2}:
        switch = int(input('Invalid entry please enter the Switch (1 or 2): '))

    carrier = input('Please enter the Carrier initials (TMO, VZW, ATT): ').strip().lower()  # Get the carrier
    while carrier not in ['tmo', 'vzw', 'att']:
        carrier = input('Invalid Entry, Please enter the Carrier initials (TMO, VZW, ATT,): ').strip().lower()

    if carrier == 'vzw': #Modify the carrier to name convention
        carrier = 'Verizon'
    else:
        carrier = carrier.upper()

    if location == 'a': #get the localMEP
        localMep = vlan
    else:
        localMep = switch

    if location == 'a': #Get the remote MEP
        remoteMep = switch
    else:
        remoteMep = vlan

    circuit = int(input('Please enter the only the circuit number: '))  # Get the circuit number
    while circuit < 1 or circuit > 1000000000:
        circuit = int(input('Invalid entry please enter a valid circuit number: '))

    if circuit < 100000:  # format the circuit number to 5 digits
        circuit = f'{circuit:05}'

    servicename = "TEST" + str(circuit) + ':' + str(vlan)  # Get and format the service name
    add_nid = input('It is anything else that you would like to add to the service name? (yes/no) ').strip().lower()
    if add_nid == 'yes':
        add_nid = input('Please enter here what you want to add to the service name: ')
        servicename += add_nid
    testName = servicename

    flow1 = int(input('Insert the first numbers of the flow point: '))
    while flow1 < 0 or flow1 > 48:
        flow1 = int(input('Invalid entry please re enter the first flow point: '))

    flow2 = int(input('Insert the second number of the flow point: '))
    while flow2 < 0 or flow2 > 9:
        flow2 = int(input('Invalid entry please re enter the first flow point: '))

    flowPointName = str(flow1) + '_' + servicename + '_' + str(flow2)

    #Add commands to the list
    commands.append('config') #Initial Config
    commands.append('cfm-global-config admin-state enable')
    commands.append(f'maintenance-domain Y1731-{carrier}-Level3 md-level 3 mhf-creation none id-permission chassis name-type character-string name Y1731-{carrier}-Level3')
    commands.append(f'maintenance-domain Y1731-{carrier}-Level3 maintenance-association {testName} name-type character-string name {testName} ccm-interval 100ms component-list 1 fd-name {testName} mhf-creation none id-permission chassis')
    commands.append(f'maintenance-domain Y1731-{carrier}-Level3 maintenance-association {testName} maintenance-association-end-point {localMep} direction up interface {flowPointName} administrative-state true ccm-ltm-priority 0 continuity-check cci-enabled true')
    commands.append(f'maintenance-domain Y1731-{carrier}-Level3 maintenance-association {testName} maintenance-association-end-point {localMep} continuity-check fng-alarm-time 0')
    commands.append(f'maintenance-domain Y1731-{carrier}-Level3 maintenance-association {testName} maintenance-association-end-point {localMep} l2-transform vlanid {vlan} pcp pcp-0 tpid tpid-8100')
    commands.append('exit')


    commands.append('config') #DMM
    commands.append(f'maintenance-domain Y1731-{carrier}-Level3')
    commands.append(f'maintenance-association {testName}')
    commands.append(f'maintenance-association-end-point {localMep}')
    commands.append(f'delay-measurements delay-measurement-config 1')
    commands.append(f'message-period 100')
    commands.append(f'measurement-interval 1')
    commands.append(f'operation-type create')
    commands.append(f'remote-mep-id {remoteMep}')
    commands.append('start-time-type immediate')
    commands.append('stop-time-type none')
    commands.append('bins-per-fd-interval 3')
    commands.append('bins-per-fdr-interval 2')
    commands.append('bins-per-ifdv-interval 2')
    commands.append('priority 0')
    commands.append('repetition-period 0')
    commands.append('Frame-size 2000')
    commands.append('exit')
    commands.append('return')


    commands.append('config') #SLM
    commands.append(f'maintenance-domain Y1731-{carrier}-Level3')
    commands.append(f'maintenance-association {testName}')
    commands.append(f'maintenance-association-end-point {localMep}')
    commands.append(f'loss-measurements loss-measurement-config 1')
    commands.append('measurement-type slm')
    commands.append('message-period 100')
    commands.append('measurement-interval 1')
    commands.append('operation-type create')
    commands.append(f'remote-mep-id {remoteMep}')
    commands.append('start-time-type immediate')
    commands.append('stop-time-type none')
    commands.append('priority 0')
    commands.append('repetition-period 0')
    commands.append('Frame-Size 2000')
    commands.append('availability-measurement-interval 1')
    commands.append('availability-number-consecutive-flr-measurements 100')
    commands.append('exit')
    commands.append('return')

# Print all commands
print("Commands to be executed:")
for command in commands:
    print(command)

# Finally, send the commands to the device
try:
    output = net_connect.send_config_set(commands)
    print("\nCommands executed successfully.")
    print(output)
except Exception as e:
    print(f"Failed to execute commands: {e}")

# Disconnect from the device
net_connect.disconnect()
print(f"Disconnected from {device['host']}")

sys.exit()
