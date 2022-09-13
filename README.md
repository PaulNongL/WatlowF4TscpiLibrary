# WatlowF4TscpiLibrary

A Python 3 built-in library using the Standard Commands Programming Instrumentation (SCPI) was implemented to communicate, control and operate Watlow F4T for this application.

Communication protocol can support TCP/IP, serial RS-232/485 and USB-to-serial communication. The Serial RS-232/485 interface requires the communication module installed in slot 6 of F4T.

The sample program included in this implementation makes use of TCP/IP configuration. For serial connect, a section is required in the f4t_class file and f4t_run.py file. 

## Requirements

This library makes use of the built-in Python Library. It requires importing atexit and register/unregister. 

Thus, only following are needed: 
 
 - Python 3
 - Python3-pip
 - Pyserial

The pyserial is needed for ModbusRTU communication. 

## Installation

This implementation was originally written for GNU/Linux, but it can support Mac OS and MS Windows platform, provided the necessary requirements and packages are met.

The following provides guidance for preparing Debian 11 GNU/Linux and CentOS 7 platforms to use this implementation.

### Debian 11 GNU/Linux

Debian 11 basic install readily contains the Python 3 distribution. However, the pyserial package needs to be installed if an RS-233/485 method is to be used for the application.

Commands should be issued as sudo (or under root shell):

- apt update
- apt install python3-pip
- pip3 install --upgrade pip
- pip3 install pyserial

### CentOS 7 GNU/Linux

CentOS 7 basic install has Python 2.7. Thus, Python 3 must be install manually.
To accomplish this, CentOS 7 must be modified to link to the CentOS repository and RMPFusion. 

- yum update
- yum install python3 python3-pip
- pip3 install --upgrade pip
- pip3 install pyserial 

## Testing

This implementation has been tested on various Watlow F4T with different configurations according to their instaleld modules for: 

- Temp with cascade
- Temp and Humi single staged refrig
- Temp with single state refrig
- Temp and Humi with cascade refrig

Tested on Debian 11 platform via the TCP/IP protocol.
Tested with Python:

- Python 3.5.7
- Python 3.6.8
- Python 3.9.1

Thus, this implementation will work on all Python 3+  

## Implementation 

For required application not implemented in the sample run program 'f4t_run.py', various methods can be implemented to call the interface modules in action.  
