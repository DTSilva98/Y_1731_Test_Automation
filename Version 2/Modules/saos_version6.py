# This module contains the logic for Ciena devices specifically for saos_version6 devices

DMM_INT = '100ms'
SLM_INT = '100ms'
PRIORITY = '0'

def version6():

    commands = []

    location = input(
        'Please enter the location of the device (A, Z-vs, Z-vlan): ').strip().lower()  # Get the location of the device
    while location not in ['a', 'z-vs', 'z-vlan']:
        location = input('Invalid Entry please enter a valid location (A, Z-vs, Z-vlan): ').strip().lower()

    while True:
        try:
            port = int(input('Please enter the port number (1-48): '))  # Get the port number
            if port <= 0 or port > 48:
                print('Please enter a valid port number (1-48): ')
            else:
                break
        except ValueError:
            print('Please enter a valid port number(1-48): ')

    while True:
        try:
            vlan = int(input('Please enter the Vlan (1-4095): '))  # Get the Vlan
            if vlan <= 0 or vlan > 4095:
                print('Invalid input. VLAN must be a number between 1 and 4095. Please try again: ')
            else:
                break
        except ValueError:
            print("Invalid input. VLAN must be a number between 1 and 4095. Please try again. ")

    mepType = input('Please enter the MEP Type (Up or Down): ').strip().lower()  # Get the MEP Type
    while mepType not in ['up', 'down']:
        mepType = input('Invalid Entry please enter a valid MEP Type (Up or Down): ').strip().lower()

    while True:
        try:
            switch = int(input('Please enter the Switch (1 or 2): '))  # Get the Switch
            if switch not in [1, 2]:
                print('Invalid entry please enter the Switch (1 or 2): ')
            else:
                break
        except ValueError:
            print("Invalid entry please enter the Switch (1 or 2): ")

    carrier = input('Please enter the Carrier initials (TMO, VZW, ATT): ').strip().lower()  # Get the carrier
    while carrier not in ['tmo', 'vzw', 'att']:
        carrier = input('Invalid Entry, Please enter the Carrier initials (TMO, VZW, ATT): ').strip().lower()

    if carrier == 'vzw':  # Modify the carrier to name convention
        carrier = 'Verizon'
    else:
        carrier = carrier.upper()

    if location == 'a':  # Get the localMEP
        localMep = vlan
    elif location == 'z-vs' or location == 'z-vlan':
        localMep = switch

    if location == 'a':  # Get the remote MEP
        remoteMep = switch
    elif location == 'z-vs' or location == 'z-vlan':
        remoteMep = vlan

    while True:
        try:
            circuit = int(input('Please enter the circuit number: '))  # Get the circuit number
            if circuit < 1 or circuit > 1000000000:
                print('Invalid entry please enter a valid circuit number: ')
            else:
                break
        except ValueError:
            print("Invalid entry please enter a valid circuit number: ")

    if circuit < 100000:  # Format the circuit number to 5 digits
        circuit = f'{circuit:05}'

    servicename = "CIR" + str(circuit) + ':' + str(vlan)  # Get and format the service name
    add_nid = input('It is anything else that you would like to add to the service name? (yes/no) ').strip().lower()
    if add_nid == 'yes':
        add_nid = input('Please enter here what you want to add to the service name ')
        servicename += add_nid
    testName = servicename

    # Add commands to the list
    commands.append('cfm enable')  # Main config
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
    commands.append(
        f'cfm delay send service {testName} local-mepid {localMep} mepid {remoteMep} iterate 0 priority {PRIORITY} dmm-interval {DMM_INT}')
    commands.append(
        f'cfm synthetic-loss send service {testName} local-mepid {localMep} mepid {remoteMep} test-id 1 iterate 0 priority {PRIORITY} slm-interval {SLM_INT}')
    commands.append('con sa')

    return commands, servicename, localMep

def ver6del(servicename, localMep):
    delCom = []
    delCom.append(f'cfm mep delete service {servicename} mepid {localMep}')
    delCom.append(f'cfm service delete service {servicename}')
    delCom.append(f'con sa')
    return delCom

