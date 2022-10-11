#!/bin/python3
'''
:author: Paul Nong-Laolam <pnong-laolam@espec.com>
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
sys.path.insert(0,'../f4tscpi')
import time
import logging

from f4tscpi.f4t_class import Controller, TempUnits, RampScale
from f4tscpi.f4t_interface import F4T

LOG = logging.getLogger(__name__)

def ip_addr():
    '''select and check for proper IP address format
    '''
    while True:
        try:
            ip_addr = input('Enter F4T IP address (e.g., 192.168.0.101): ')
            #ip_addr = '10.30.100.50'
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

def listProg():
    '''Read programs in F4T storage and list them...
    '''
    # Get profiles from controller and units
    print ('\nReading profiles from F4T. Profile gap in the list is ignored.')
    print ("Profile list may be inaccurate if list is acquired while a profile is being executed.")
    print ("Please wait...")
    time.sleep(0.5)
    tst.get_profiles()
    print (f"\nF4T profiles found in sequence (slot number: 'name'): \n{tst.profiles}")
    pass 

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

def tsName():
    '''get Time Signal name
    '''
    try:
        ts_num = int(input('Enter TS number: '))
        if isinstance(ts_num, int):
            tst.get_tsName(ts_num)
    except ValueError:
        print ('Invalid TS number.')

def instantChange(mode, loop):
    '''Start the instant temperature change to set point
    '''
    print ('Starting Instant Change on temperature...')
    time.sleep(0.5)
    #tst.ramp_mode('STARTUP',1)
    #time.sleep(0.5)
    tst.ramp_mode(mode,loop)

def ramp2SP(mode,loop):
    '''Start ramp to Temp to set point
    '''
    print ('Starting Ramping on temperature to SetPoint value...')
    time.sleep(0.5)
    tst.ramp_mode(mode,loop)

def setScale(loop):
    '''Set ramp scale in unit or hours or unit of minutes

    Unit: HOURS; MINUTES
    '''
    try: 
        scale = input('Enter ramp scale type in M or H: ')
        if scale == 'H':
            time.sleep(0.5) 
            tst.set_rampScale('HOURS',loop)
        elif scale == 'M':
            time.sleep(0.5)
            tst.set_rampScale('MINUTES',loop)
        else:
            print ('Invalid scale type. Expecting letter "M" or "H".')
    except ValueError:
        print ('Invalid input.') 

def setRV(loop):
    '''Set new value for ramp rate
    '''
    try:
        value = float(input('Enter rate value: '))
        if isinstance(value, (int, float)):
            tst.set_ramp('rate',value, loop)
        else:
            print ('Value must be a decimal number.') 
    except ValueError:
        print ('Invalid operation. Option terminated.')  

def setRT(loop):
    '''Set new value for ramp time

    Time: house or minutes 
    '''
    try:
        value = int(input('Enter time value in [MINUTES] unit: '))
        if isinstance(value, int):
            tst.set_ramp('time',value, loop)
        else:
            print ('Value must be integer (whole) number.') 
    except ValueError:
        print ('Invalid operation. Option terminated.')

def deviceID():
    '''read device id information
    '''
    print ('Probing target device...')
    time.sleep(0.5)
    print (f'Manufacturer, Part Number, S/N, Software Version:\n{tst.get_id()}')

def main_menu(): 
    '''
       Set options for program control
    '''
    while(True):
        print_menu('1','Main Menu')
        option = ''
        try:
            option = input('Select option (i, t, p, ...): ')
        except:
            print('Invalid input; expected a letter [a-z].')
        if option == 'i':
            deviceID()
        elif option == 't':
            thCtrl()
        elif option == 'p':
            progMenu()
        elif option == 'e':
            eventCtrl()
        elif option == 'r':
            rampMenu()
        elif option == 'u':
            unit() 
        elif option == 'z':
            print('Program terminated.')
            exit()
        else:
            print('Invalid option; expected a letter [a-z].')

def thCtrl():
    '''
       set options for Temp and Humi controls
    '''
    while(True):
        print_menu('2','Temp/Humi')
        option = ''
        try:
            option = input('Select option (a-z): ')
        except:
            print('Invalid input; expected a letter [a-z].')
        if option == 't':
            setTemp('Temp',1)
        elif option == 'h':
            setTemp('Humi',2)
        elif option == 'l':
            listTempPV(1)
        elif option == 'z':
            print('Returning to Main Menu.')
            time.sleep(.5)
            os.system('clear||cls')
            main_menu()
        else:
            print('Invalid option; expected a letter [a-z].')

def progMenu():  # test 
    '''set up selection menu for operation
       main menu 

       l: list programs
       e: execute program
       p: pause program
       r: resume program
       s: stop program
       z: return to Main Menu 
    '''
    while(True):
        print_menu('3','Program')
        option = ''
        try:
            option = input('Select option (a-z): ')
        except:
            print('Invalid input; expected a letter [a-z].')
        if option == 'l':
            listProg()
        elif option == 'e':
            runProg()
        elif option == 'p':
            progMode('PAUSE')
        elif option == 'r':
            progMode('RESUME')
        elif option == 's':
            progMode('STOP')
        elif option == 'z':
            print('Return to Main.')
            time.sleep(0.5)
            os.system('clear||cls')
            main_menu()
        else:
            print('Invalid option; expected a letter [a-z].')

def eventCtrl():
    '''Test TS events
    '''
    while(True):
        print_menu('4','Event')
        option = ''
        try:
            option = input('Select option (a-z): ')
        except:
            print('Invalid input; expected a letter [a-z].')
        if option == 'r':
            readTS()
        elif option == 's':
            setTS()
        elif option == 'n':
            tsName()
        elif option == 'z':
            print('Return to Main Menu...')
            time.sleep(0.5)
            os.system('clear||cls')
            main_menu() 
        else:
            print('Invalid option; expected a letter [a-z].')

def rampMenu():
    '''define ramp mode and control
        'rr': 'Read ramp rate value 
        'sr': 'Set ramp rate value
        'rt': 'Read ramp time value 
        'st': 'Set ramp time value  
        'rs': 'Ramp to SetPoint     
        'is': 'Instant change to SP
        'sc': 'Set Ramp Scale in [HR or MIN]
        'z' : 'Return to Main Menu 
    '''
    while(True):
        print_menu('5','Ramp Menu')
        option = ''
        chk_range = range(1,4,1)
        try:
            option = input('Select option ("rr", "sr", ...): ')
        except:
            print('Invalid input.')
        if option == 'rr':
            try:
                loop = int(input('Enter loop number (1=Temp, 2=Humi; loop_max=4): '))
                if isinstance(loop, int):
                    if loop in chk_range:
                        tst.get_ramp('rate',loop)
                    else:
                        print ('Loop out of range.') 
            except ValueError:
                print ('Invalid loop number.')  
        elif option == 'sr':
            try:
                loop = int(input('Enter loop number (1=Temp, 2=Humi; loop_max=4): '))
                if isinstance(loop, int):
                    if loop in chk_range:
                        setRV(loop)
                    else:
                        print ('Loop out of range.') 
            except ValueError:
                print ('Invalid loop number.') 
        elif option == 'rt':
            try:
                loop = int(input('Enter loop number (1=Temp, 2=Humi; loop_max=4): '))
                if isinstance(loop, int):
                    if loop in chk_range:
                        tst.get_ramp('time',loop)
                    else:
                        print ('Loop out of range.')  
            except ValueError:
                print ('Invalid loop number.')
        elif option == 'st':
            try:
                loop = int(input('Enter loop number (1=Temp, 2=Humi; loop_max=4): '))
                if isinstance(loop, int):
                    if loop in chk_range:
                        setRT(loop)
                    else:
                        print ('Loop out of range.') 
            except ValueError:
                print ('Invalid loop number.')             
        elif option == 'rs':
            ramp2SP('SETPOINT',1)
        elif option == 'ic':
            instantChange('OFF',1)
        elif option == 'sc':
            try:
                loop = int(input('Enter loop number (1=Temp, 2=Humi; loop_max=4): '))
                if isinstance(loop, int):
                    if loop in chk_range:
                        setScale(loop)
                    else:
                        print ('Loop out of range.') 
            except ValueError:
                print ('Invalid loop number.')
        elif option == 'z':
            print('Return to Main Menu...')
            time.sleep(0.5)
            os.system('clear||cls')
            main_menu() 
        else:
            print('Invalid option.')

def unit():
    '''read device unit
    '''
    while(True):
        print_menu('6','Units')
        option = ''
        try:
            option = input('Select option (r, s, z): ')
        except:
            print('Invalid input; expected a letter [r,s,z].')
        if option == 'r':
            print ('Probing device for Temp unit...')
            time.sleep(0.5)
            print (f'Temperature unit: {tst.get_units()}')
        elif option == 's':
            time.sleep(0.5)
            tst.set_units()
        elif option == 'z':
            print('Returning to Main Menu.')
            time.sleep(.5)
            os.system('clear||cls')
            main_menu()
        else:
            print('Invalid option; expected a letter [r,s,z].')

def menu(choice):
    '''menu list

    option: 
       1: main menu
       2: Temp/Humi menu
       3: Program menu
       4: Output (Time Signal) menu
       5: Ramp menu
       6: Unit menu
    '''
    # main menu 
    main_menu = {
        'i': 'Device information            ',
        't': 'Temp/Humi SP control          ',
        'p': 'Program control               ',
        'r': 'Ramp control                  ',
        'e': 'Event control                 ',
        'u': 'Temperature Unit              ',
        'z': 'Exit                          '
    }

    # temp and humi ctrl menu
    th_menu = {
        't': 'New Temperature Set Point     ',
        'h': 'New Humidity Set Point        ',
        'l': 'List current Temp PV/SP       ',
        'z': 'Return to Main Menu           '
    }

    # program menu 
    prog_menu = {
        'l': 'List program                  ',
        'e': 'Execute program               ',
        'p': 'Pause program                 ',
        'r': 'Resume program                ',
        's': 'Stop program                  ',
        'z': 'Return to Main Menu           '
    }

    # event ctrl menu 
    ts_menu = {
        'r': 'Read event (TS) output        ',
        's': 'Set event (TS) output         ', 
        'n': 'Read event (TS) name          ',
        'z': 'Return to Main Menu           '
    }

    # ramp ctrl menu 
    ramp_menu = {
        'rr': 'Read ramp rate value         ',
        'sr': 'Set ramp rate value          ', 
        'rt': 'Read ramp time value         ',
        'st': 'Set ramp time value          ',
        'rs': 'Ramp to SetPoint             ',
        'ic': 'Instant change to SP         ',
        'sc': 'Set Ramp Scale in H or M     ', 
        'z ': 'Return to Main Menu          '
    }

    # unit menu 
    unit_menu = {
        'r': 'Read Temp unit                ',
        's': 'Set new Temp unit             ', 
        'z': 'Return to Main Menu           '
    }

    if choice == '1':
        return main_menu
    elif choice == '2':
        return th_menu
    elif choice == '3':
        return prog_menu 
    elif choice == '4':
        return ts_menu 
    elif choice == '5':
        return ramp_menu 
    elif choice == '6':
        return unit_menu

def print_menu(choice, menu_name):
    '''set up selection menu
    '''
    print (f'\nF4T control options: {menu_name}'
            '\n--------------------------------') 
    for key in menu(choice).keys():
        print (f'  [{key}]:', menu(choice)[key] )
    print ('--------------------------------') 

if __name__ == "__main__":

    # clear terminal pay attention to GNU/Linux and MS Windows
    os.system('clear||cls')

    # connecto to watlow F4T via proper IP address using TCP/IP protocol
    tst = F4T(host = ip_addr(), timeout = 1)

    # Get current temp P and SP values
    loop = 1
    currentPV = tst.get_pv(loop)
    currentSP = tst.get_sp(loop) 
    print (f'\nTemperature Status: \n  PV: {currentPV} \n  SP: {currentSP}')

    # initiate menu
    main_menu()

    # sys.exit('Terminated')
