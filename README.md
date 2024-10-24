
------------------------------------------------------------------

Description

CloudySoe Port Scanner is a multi-threaded port scanning tool written in Python. It allows users to scan specific ports or a range of ports on multiple machines concurrently, providing quick feedback on which ports are open.

------------------------------------------------------------------

Features

Multi-threaded scanning for speed.
Option to scan specific ports or all ports (1-65535).
Error logging to track issues.
User-friendly prompts for input.
Installation
To get started, you need to have Python 3.x installed on your machine. Once you have Python set up, you can install the required dependencies using pip.

Install Required Packages
Run the following command to install the necessary external package:
------------------------------------------------------------------

pip install colorama

------------------------------------------------------------------

------------------------------------------------------------------
Standard Library Modules

The following modules are included in Python's standard library and do not require installation:

socket
threading
sys
os
time
These modules are essential for the functionality of the CloudySoe Port Scanner.

------------------------------------------------------------------

Usage

Run the script using Python:

python port-scanner.py
Follow the prompts to input the number of threads, IP addresses, and ports to scan.

The results will be displayed in the terminal, and you can find any errors logged in log.txt in your home directory.

------------------------------------------------------------------

Example Input

For a single machine scan:

Enter the server IP: 192.168.1.1
Enter the port to scan (or 'all' to scan all ports): all
For multiple machines:

Enter server in the format 'name:ip
' (or type 'done' to finish): Server1:192.168.1.1:80
Enter server in the format 'name:ip
' (or type 'done' to finish): done
Output
After the scan, you will see the following:

List of open ports.
A message indicating if no open ports were found.
Logs of any errors that occurred during the scan.
Error Handling
If there are any issues during the scanning process, errors will be logged in log.txt located in your home directory.
