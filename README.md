# Y 1731 Test Automation

## Overview
This project is a Python-based automation tool designed to configure network devices for Y.1731 test automation, a critical component for network performance monitoring and fault management. While the script was originally created following specific structured input instructions provided by a company, it is designed to be easily modified to meet varying requirements.

## Key Features
- Automated Y.1731 Test Creation: Simplifies the configuration process by generating the necessary commands for network performance testing.
- Support for Multiple Device Versions: Includes logic for both version 6 and version 10 of Ciena SAOS devices, with the potential for future expansion.
- Interactive Input Prompts: Guides the user through standardized inputs such as VLAN, Port, and switch configuration.
- Customizable Code: Built with flexibility in mind, allowing users to adjust the script for specific needs.
- Error Handling: Manages SSH connection issues and invalid user inputs to minimize disruptions.
- Efficient Execution: Reduces manual errors and saves time in configuring tests for new circuits.

## What is Y.1731?
### Y.1731 is an ITU-T standard for Ethernet Operations, Administration, and Maintenance (OAM). It enables:
- Performance Monitoring: Measures frame delay, loss, and variation to ensure compliance with Service Level Agreements (SLAs).
- Fault Management: Provides tools like Continuity Check Messages (CCM) and Loopback Messages (LBM) to identify and troubleshoot network issues.
- Service Verification: Ensures network paths and configurations meet expected quality levels.

## Usage
### Prerequisites:
- Python 3.x

- Install required dependencies using:
  pip install netmiko

# How it works
The script will prompt for:
- Device IP
- SSH Credentials
- Configuration parameters such as VLAN, MEP type, switch, and carrier
Once the inputs are provided, the script generates the necessary configuration commands and sends them to the device.

## Why This Project Matters
- Efficiency: Automates repetitive tasks, saving time and reducing human error.
- Scalability: Supports multiple device versions and is structured for future enhancements.
- Customizability: Designed to be modified to fit specific requirements or use cases.
- Technical Skill Demonstration: Highlights proficiency in Python scripting, network automation, and working with industry standards like Y.1731.

## Purpose
This project is intended to showcase expertise in network automation, Python programming, and Y.1731 implementation. It demonstrates practical problem-solving skills while adhering to industry standards for network performance monitoring.
