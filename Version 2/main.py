import sys
from Modules.connection import establish_connection, disconnect
from Modules.saos_version6 import version6, ver6del
from Modules.saos_version10 import version10, ver10del

def main():
    """
    Main entry point for the program.
    Prompts for version, establishes a connection,
    collects commands from the appropriate version module,
    and (optionally) sends them to the device.
    """
    # Establish a Netmiko connection


    while True:

        net_connect = establish_connection()

        # Prompt for SAOS version
        while True:
            try:
                version = int(input('Please enter the version (6 or 10): ')) #This have to be changed to support more version in the future
                if version in (6, 10):
                    break
                else:
                    print('Invalid version, please enter 6 or 10: ')
            except ValueError:
                print('Invalid version, please enter 6 or 10: ')


        # Build the commands for the chosen version
        if version == 6:
            commands, sern6, localMep = version6()
        else:
            commands, sern10 = version10()

        # Show user the commands
        print("\nCommands to be executed:")
        for cmd in commands:
            print(cmd)

        # Confirm whether to send commands
        confirm = input("\nDo you want to send these commands to the device? (yes/no): ").strip().lower()
        if confirm == 'yes':
            try:
                output = net_connect.send_config_set(commands)
                print("\nCommands executed successfully.")
                print(output)
            except Exception as e:
                print(f"Failed to execute commands: {e}")
        else:
            print("No commands were sent to the device.")

        # Prompts the user for test conservation
        conserve = input("Do you want to conserve this test? (yes/no): ")
        if conserve == 'yes':
            disconnect(net_connect)
        else:
            if version == 6:
                borr6 = ver6del(sern6, localMep)
                borrado = net_connect.send_config_set(borr6)
                print(f'{borrado}')
                disconnect(net_connect)
            if version == 10:
                borr10 = ver10del(sern10)
                borrado = net_connect.send_config_set(borr10)
                print(f'{borrado}')
                disconnect(net_connect)

        # Asks the user about test conservation
        another_device = input("\nDo you want to connect another device? (yes/no): ").strip().lower()
        if another_device not in ['yes', 'no']:
            another_device = input("Please enter yes or no ").strip().lower()
        if another_device != 'yes':
            print("Exiting program")
            break

if __name__ == "__main__":
    main()
