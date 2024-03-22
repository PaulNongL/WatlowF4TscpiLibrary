# WatlowF4TscpiLibrary

A Python 3 built-in library using the Standard Commands Programming Instrumentation (SCPI) was implemented to communicate, control and operate Watlow F4T for this application.

Communication protocol can support TCP/IP. The sample program included in this implementation makes use of TCP/IP configuration. 

## Requirements

This library makes use of the built-in Python Library. It requires importing atexit and register/unregister. 

Thus, only following are needed: 
 
 - Python 3.7.3+
 - Python3-pip

The SCPI protocol for Watlow F4T is application with new firmware (tested on 04:07:0012). It also only applies in TCP/IP protocol application, using port 5025. IT does not support serial itnerface.  

## Installation

This implementation was originally written for GNU/Linux, but it can support Mac OS and MS Windows platform, provided the necessary requirements and packages are met.

The following provides guidance for preparing Debian 11 GNU/Linux and CentOS 7 platforms to use this implementation.

### Debian 11 GNU/Linux

Debian 11 basic install readily contains the Python 3 distribution. However, the pyserial package needs to be installed if an RS-233/485 method is to be used for the application.

Commands should be issued as sudo (or under root shell):

- apt update
- apt install python3-pip
- python3 -m pip install --upgrade pip

### CentOS 7 GNU/Linux

CentOS 7 basic install has Python 2.7. Thus, Python 3 must be install manually.
To accomplish this, CentOS 7 must be modified to link to the CentOS repository and RMPFusion. 

- yum update
- yum install python3 python3-pip
- python3 -m pip install --upgrade pip

## Testing

This implementation has been tested on various Watlow F4T with different configurations according to their installed modules for: 

- Temp with cascade
- Temp and Humi single staged refrig
- Temp with single state refrig
- Temp and Humi with cascade refrig

Tested on Debian 9 with custom install of Python 3.7.3; CentOS 7 on Python 3.6.8 Debian 10/11 (on default Python 3 install) platform via the TCP/IP protocol.
Tested with Python:

- Python 3.6.8
- Python 3.7.3
- Python 3.9.1

Thus, this implementation will work on all Python 3.6+  

## Implementation 

For required application not implemented in the sample run program 'f4t_run.py', various methods can be implemented to call the interface modules in action.  
