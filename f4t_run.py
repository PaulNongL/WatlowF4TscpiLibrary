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
            #ip_addr = input('Enter F4T IP address (e.g., 192.168.0.101): ')
            ip_addr = '10.30.100.75'
            chk_ip = re.match(r"^\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}$", ip_addr)
            if chk_ip:
                print ('\n')
                break
        except Exception:
            print ('Invalid IP address.')
    return ip_addr

def setTemp():
    '''set new temp value
    '''
    print ('\n<Applying new Set Point>')
    while True:
        try:
            tempVal = float(input('Enter new value for Set Point (SP): '))
            if isinstance(tempVal, int) or isinstance(tempVal,float):
                tst.write_tempSP(tempVal)
                break
        except ValueError:
            print ('Invalid value.\n')

    print ('Please wait...\n')
    time.sleep(2)
    tst.send_cmd(':SOURCE:CLOOP1:SPOINT?')
    time.sleep(2)
    currentSP = tst.read_items().strip()
    print(f'Temperature Status: \n   PV: {float(tst.get_tempPV())}'
              f'\n   SP: {float(currentSP)}')

def listTempPV():
    '''list temp process value in 1-second interval

       TempPV
    '''
    try:
        print ('\nList of Temp process values in 1-second interval.'
               '\nPress Ctrl+C to terminate Temp list.\n')
        while True:
            print(tst.get_tempPV())
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

def setRamp():
    '''set ramping mode

       defined variables:
        start, stop, step, ramp_time_min, soak_time_min

        temps = range(start Temp, stop + step, step Temp)

        initial starting point: determined by operator:
        e.g.:
            start, stop, step = 25, 38, 5
            ramp_time_min = 2
            soak_time_min = 3
    '''
    start = input('Enter RAMP start point: ')
    stop = input ('Enter RAMP end point: ')
    step = input ('Enter ramp step: ')
    ramp_time_min = input ('Enter ramp time in minute value: ')
    soak_time_min = input ('Enter sock time in minute value: ')
    temps = range(start,stop+step,step)
    tst.set_ramp('time',ramp_time_min)
    tst.set_ramScale(RampScale.MINUTES)

    for temp in temps:

        print (f'\nSet new Temp at: {start}')
        tst.write_tempSP(temp)
        time.sleep(1)

        print (f'ramp_time_min = {ramp_time_min}')
        time.sleep(ramp_time_min*5)

        while abs(float(tst.get_tempPV()) - temp) > 0.2:
            time.sleep(1)
            # begin soak
            print(f'beginning soak at temp {tst.get_tempPV()}')
            time.sleep(soak_time_min*60)

def readTS():
    '''read time signal state
    '''
    try:
        ts_num = int(input('Enter TS number: '))
        if isinstance(ts_num, int):
            tst.ts_state(ts_num)
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

def selection():  # test 
    '''set up selection menu for operation
    '''
    try:
        ans=True
        while ans:
            print ('\nControl options:') 
            print ('''
             1. Set new Temp SP
             2. List Temp PV
             3. Execute Profile
             4. Stop Profile
             5. Pause Profile
             6. Resume Profile
             7. Read TS output
             8. Set TS output
             9. Exit
            ''')
            try: 
                ans = input('Select option (1-9): ')
                if ans == '1':
                    setTemp()
                elif ans == '2':
                    listTempPV()
                elif ans == '3':
                    runProg()
                elif ans == '4':
                    progMode(mode='STOP')
                elif ans == '5':
                    progMode(mode='PAUSE')
                elif ans == '6':
                    progMode(mode='RESUME')
                elif ans == '7':
                    readTS()
                elif ans == '8':
                    setTS()
                elif ans == '9':
                    print ('Program termiated.')
                    ans = None
                else:
                    print('\nInvalid input. Try again...')
            except ValueError:
                pass  
    except KeyboardInterrupt:
        pass 

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
    currentPV = tst.get_tempPV()
    currentSP = tst.get_tempSP() 
    print (f'\nTemperature Status: \n  PV: {float(currentPV)} \n  SP: {float(currentSP)}')

    # initiate menu
    selection()

    # sys.exit('Terminated')