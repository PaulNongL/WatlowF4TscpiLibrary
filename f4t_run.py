#!/bin/python3
'''
:author: Paul Nong-Laolam <paul.nong-laolam@espec.com>
:license: MIT, see LICENSE for more detail.
:copyright: (c) 2022. ESPEC North America, INC.
:file: f4t_run.py 

Application interface for controlling Watlow F4T operations. 
This program may be and can be reimplemented with additional
call methods to utilize the Watlow F4T control interface
from its class and method definitions. 

TCP/IP protocol is applied. 
'''
import os, sys, re
sys.path.insert(0,'./f4t')
import time
import logging

from f4t.f4t_class import Controller, TempUnits, RampScale
from f4t.f4t_interface import F4T

LOG = logging.getLogger(__name__)

def ip_addr():
    '''select and check for proper IP address format
    '''
    while True:
        try:
            ip_addr = input('Enter F4T IP address (e.g., 192.168.0.101): ')
            chk_ip = re.match(r"^\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}$", ip_addr)
            if chk_ip:
                print ('\n')
                break
        except Exception:
            print ('Invalid IP address.')
    return ip_addr

def setTemp(str, loop):
    '''set new temp value
    '''
    print ('\n<Applying new Set Point>')
    while True:
        try:
            val = float(input('Enter new value for Set Point (SP): '))
            if isinstance(val, int) or isinstance(val,float):
                tst.write_sp(val, loop)
                break
        except ValueError:
            print ('Invalid value.\n')

    print ('Please wait...\n')
    time.sleep(2)
    tst.send_cmd(f':SOURCE:CLOOP{loop}:SPOINT?')
    time.sleep(2)
    currentSP = tst.read_items().strip()
    print(f'{str} status: \n   PV: {tst.get_pv(loop)}'
              f'\n   SP: {currentSP}')

def listTempPV(loop):
    '''list temp process value in 1-second interval

       TempPV
    '''
    try:
        print ('\nList of Temp process values in 1-second interval.'
               '\nPress Ctrl+C to terminate Temp list.\n')
        while True:
            print(tst.get_pv(loop))
            time.sleep(1)
    except KeyboardInterrupt:
        pass

def runProg():   # test def 
    '''select and set profile for execution.
    '''
    print ('\n<Select a profile to execute>')
    try: 
        while True:
            prog_num = int(input('Enter profile number (Ctrl+C to exit profile execution): '))
            if isinstance(prog_num, int) and 1 <= prog_num <= 40:
                print (f'\nExecuting profile {prog_num}:')
                tst.select_profile(prog_num)
                time.sleep(0.5)
                tst.send_cmd(':PROGRAM:NAME?')
                time.sleep(0.5)
                tst.prog_mode('START')
                break
            else:
                print ('Invalid Profile No. Must be between 1 and 40.')
    except KeyboardInterrupt:
            pass

def progMode(mode):
    '''set program mode of currently running profile

       available modes: 
          stop: terminate program
          pause: suspend current running program
          resume: resume execution of program

          mode: STOP, PAUSE, RESUME 
    '''
    print (f'{mode} currently running profile...')
    tst.select_profile(0)
    time.sleep(0.5)
    tst.send_cmd(':PROGRAM:NAME?')
    time.sleep(0.5)
    tst.prog_mode(mode)

def readTS():
    '''read time signal state
    '''
    try:
        ts_num = int(input('Enter TS number: '))
        if isinstance(ts_num, int):
            tst.get_ts(ts_num)
    except ValueError:
        print ('Invalid TS number.')

def setTS():
    '''Set TS value on the selected TS number
    '''
    try:
        print ('Selected TS will be set to "OFF" if it is "ON" and vice versa.')
        ts_num = int(input('Enter TS number: '))
        if isinstance(ts_num, int):
            tst.set_output(ts_num)
    except ValueError:
        print ('Invalid TS number.')

def instantChange(mode, loop):
    '''Start the instant temperature change to set point
    '''
    print ('Starting Instant Change on temperature...')
    time.sleep(0.5)
    tst.ramp_mode(mode,loop)

def selection():  # test 
    '''set up selection menu for operation
    '''
    while(True):
        print_menu()
        option = ''
        try:
            option = input('Select option (a-z): ')
        except:
            print('Invalid input; expected a letter [a-z].')
        #Check what choice was entered and act accordingly
        if option == 'a':
            setTemp('Temp',1)
        elif option == 'b':
            setTemp('Humi',2)
        elif option == 'c':
            runProg()
        elif option == 'd':
            progMode('PAUSE')
        elif option == 'e':
            progMode('RESUME')
        elif option == 'f':
            progMode('STOP')
        elif option == 'g':
            listTempPV(1)
        elif option == 'h':
            readTS()
        elif option == 'i':
            setTS()
        elif option == 'j':
            instantChange('OFF',1)
        elif option == 'z':
            print('Program terminated.')
            exit()
        else:
            print('Invalid option; expected a letter [a-z].')

def menu():
    '''menu'''
    menu_options = {
        'a': 'Set new Temp SP ',
        'b': 'Set new Humi SP ',
        'c': 'Execute Program ',
        'd': 'Pause Program   ',
        'e': 'Resume Program  ',
        'f': 'Stop Program    ',
        'g': 'List Temp PV    ',
        'h': 'Read TS output  ',
        'i': 'Set TS output   ',
        'j': 'Start Temp to SP', 
        'z': 'Exit            ',
    }
    return menu_options

def print_menu():
    '''set up selection menu
    '''
    print ('\nControl options:'
           '\n--------------------------') 
    for key in menu().keys():
        print (f'  [{key}]:', menu()[key] )
    print ('--------------------------') 

if __name__ == "__main__":

    # clear terminal pay attention to GNU/Linux and MS Windows
    os.system('clear||cls')

    # connecto to watlow F4T via proper IP address using TCP/IP protocol
    tst = F4T(host = ip_addr(), timeout = 1)

    # Get profiles from controller and units
    print ('\nReading profiles from F4T. Profile gap in the list is ignored.')
    print ("Profile list may be inaccurate if list is acquired while a profile is being executed.")
    print ("Please wait...")
    tst.get_profiles()
    tst.get_units()
    print (f"\nF4T profiles found in sequence (slot number: 'name'): \n{tst.profiles}")
    print (f"\nTemperature Units currently used: \n   [Units]: {tst.temp_units}")

    # Get current temp P and SP values
    loop = 1
    currentPV = tst.get_pv(loop)
    currentSP = tst.get_sp(loop) 
    print (f'\nTemperature Status: \n  PV: {currentPV} \n  SP: {currentSP}')

    # initiate menu
    selection()

    # sys.exit('Terminated')
