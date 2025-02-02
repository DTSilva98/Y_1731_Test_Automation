# This module contains the logic for Ciena devices specifically for saos_version6 devices



def version10():
    commands = []

    location = input(
        'Please enter the location of the device (A or Z): ').strip().lower()  # Get the location of the device
    while location not in ['a', 'z']:
        location = input('Invalid Entry please enter a valid location (A or Z): ').strip().lower()

    while True:
        try:
            vlan = int(input('Please enter the Vlan (1-4095): '))  # Get the Vlan
            if vlan <= 0 or vlan > 4095:
                print('Invalid input. VLAN must be a number between 1 and 4095. Please try again. ')
            else:
                break
        except ValueError:
            print("Invalid input. VLAN must be a number between 1 and 4095. Please try again. ")

    while True:
        try:
            switch = int(input('Please enter the Switch (1 or 2): '))  # Get the Switch
            if switch not in [1, 2]:
                print('Invalid entry please enter the Switch (1 or 2): ')
            else:
                break
        except ValueError:
            print("Invalid entry please enter the Switch (1 or 2): ")

    carrier = input('Please enter the Carrier initials (TMO, VZW, ATT,): ').strip().lower()  # Get the carrier
    while carrier not in ['tmo', 'vzw', 'att']:
        carrier = input('Invalid Entry, Please enter the Carrier initials (TMO, VZW, ATT): ').strip().lower()

    if carrier == 'vzw':  # Modify the carrier to name convention
        carrier = 'Verizon'
    else:
        carrier = carrier.upper()

    if location == 'a':  # Get the localMEP
        localMep = vlan
    else:
        localMep = switch

    if location == 'a':  # Get the remote MEP
        remoteMep = switch
    else:
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

    # Add commands to the list
    commands.append('config')  # Initial Config
    commands.append('cfm-global-config admin-state enable')
    commands.append(
        f'maintenance-domain Y1731-{carrier}-Level3 md-level 3 mhf-creation none id-permission chassis name-type character-string name Y1731-{carrier}-Level3')
    commands.append(
        f'maintenance-domain Y1731-{carrier}-Level3 maintenance-association {testName} name-type character-string name {testName} ccm-interval 100ms component-list 1 fd-name {testName} mhf-creation none id-permission chassis')
    commands.append(
        f'maintenance-domain Y1731-{carrier}-Level3 maintenance-association {testName} maintenance-association-end-point {localMep} direction up interface {flowPointName} administrative-state true ccm-ltm-priority 0 continuity-check cci-enabled true')
    commands.append(
        f'maintenance-domain Y1731-{carrier}-Level3 maintenance-association {testName} maintenance-association-end-point {localMep} continuity-check fng-alarm-time 0')
    commands.append(
        f'maintenance-domain Y1731-{carrier}-Level3 maintenance-association {testName} maintenance-association-end-point {localMep} l2-transform vlanid {vlan} pcp pcp-0 tpid tpid-8100')
    commands.append('exit')

    commands.append('config')  # DMM
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

    commands.append('config')  # SLM
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

    return commands, servicename

def ver10del(servicename):
    delCom = []
    delCom.append(f'config')
    delCom.append(f'no maintenance-association {servicename} ')
    delCom.append(f'exit')
    return delCom