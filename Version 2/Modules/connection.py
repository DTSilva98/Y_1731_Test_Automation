# This module contains important connection related functions

from netmiko import ConnectHandler, NetMikoTimeoutException, NetMikoAuthenticationException
import getpass
import sys

def establish_connection():
    # Prompt for device details and return a Netmiko connection object.
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

    try:
        print("Attempting to connect to the device...")
        net_connect = ConnectHandler(**device)
        print(f"Successfully connected to {net_connect.host}")
        return net_connect
    except NetMikoTimeoutException:
        print(f"Connection timed out when attempting to reach {device_ip}")
        sys.exit(1)
    except NetMikoAuthenticationException:
        print(f"Authentication failed for device {device_ip}")
        sys.exit(1)
    except Exception as e:
        print(f"Failed to connect to {device_ip}: {e}")
        sys.exit(1)

def disconnect(net_connect):
    # Close the Netmiko connection.
    print(f"Disconnecting from {net_connect.host}...")
    net_connect.disconnect()
    print("Disconnected successfully.")
