'''
:author: Paul Nong-Laolam <paul.nong-laolam@espec.com>
:license: MIT, see LICENSE for more detail.
:copyright: (c) 2022. ESPEC North America, INC.
:file: f4t_interface.py

Upper level interface for Watlow F4T controller; control implementation 
for communication via SCPI register, unregister using built-in Python Library.
'''
import time
import logging
from f4t_class import Controller, TempUnits

LOG = logging.getLogger(__name__)

class F4T(Controller):
#    def __init__(self, set_point:float = 22.0, 
#                 units:TempUnits = TempUnits.C, profile:int = 1, *args, **kwargs):
#        super().__init__(*args, **kwargs)
#        self.set_point = set_point
#        self.temp_units = units
#        self.current_profile = profile
#        if self.timeout is None:
#            self.timeout = 1.5
#        self.profiles = {}

    def __init__(self,  profile:int = 1, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.current_profile = profile
        if self.timeout is None:
            self.timeout = 1.5
        self.profiles = {}

    def get_id(self):
        '''reading device id and info
        '''
        self.clear_buffer()
        time.sleep(0.5) 
        self.send_cmd('*IDN?')
        self.f4t_id = self.read_items()
        return self.f4t_id 

    def get_units(self):
        '''probe controller for current set units
        '''
        self.clear_buffer()
        time.sleep(0.5)
        self.send_cmd(':UNIT:TEMPERATURE?')
        rsp = self.read_items()
        self.temp_units = TempUnits(rsp)   
        return self.temp_units

    def set_units(self, units:TempUnits = None):
        '''apply new units to controller
        '''
        if units is None:
            units = self.temp_units
        self.send_cmd(f':UNITS:TEMPERATURE {units.value}')

    def get_profiles(self):
        '''set max limit for profile list
        '''
        for i in range(1, 40):
            self.select_profile(i)
            time.sleep(0.5)
            self.send_cmd(':PROGRAM:NAME?')
            time.sleep(0.5)
            name = self.read_items().strip().replace('"','')
            if name:
                self.profiles[i] = name
            else:
                break

    def select_profile(self, profile: int):
        '''
           set range of limit for profiles on list to be read
           profile number must be: 1 =< or =< 40
        '''
        self.send_cmd(f':PROGRAM:NUMBER {profile}')
    
    def prog_mode(self, mode):
        '''a method with to control profile action
           and its programming mode:

           - state: start
             execute a program based on selected profile.
           - state: stop
             stop currently running program.
           - state: pause
             pause current line of currently running program
           - state: resume
             resume the state of currently paused program.
        '''
        self.send_cmd(f':PROGRAM:SELECTED:STATE {mode}')

    def get_pv(self, loop):
        '''read temperature and humidity process values from controller
           based on loop selection

           TempPV: loop = 1
           HumiPV: loop = 2
        '''
        self.clear_buffer() 
        self.send_cmd(f':SOURCE:CLOOP{loop}:PVALUE?')
        return self.read_items()

    def get_sp(self, loop):
        '''read temperature and humidity set point values from controller
           based on loop selection

           TempSP: loop = 1
           HumiSP: loop = 2
        '''
        self.send_cmd(f':SOURCE:CLOOP{loop}:SPOINT?')
        return self.read_items()

    def get_cascadeSP(self, cascade = 1):
        '''read cascade set point value from controller
        '''
        self.send_cmd(f':SOURCE:CASCADE{cascade}:SPOINT?')
        return self.read_items()

    def get_cascadeLoopPV(self, loop, cascade = 1):
        '''read cascade outer loop process value from controller

           cascade outer loop PV: outerPV 
           cascade inner loop PV: innerPV
        '''
        sloop = "OUTER" if loop else "INNER"  
        self.send_cmd(f':SOURCE:CASCADE{cascade}:{sloop}:PVALUE?')
        return self.read_items()

    def get_cascadeLoopSP(self, loop, cascade = 1):
        '''read cascade outer loop set point value from controller

           cascade outer loop SP: outerSP
           cascade inner loop SP: innerSP
        '''
        sloop = "OUTER" if loop else "INNER"  
        self.send_cmd(f':SOURCE:CASCADE{cascade}:{sloop}:SPOINT?')
        return self.read_items()

    def write_sp(self, val, loop):
        '''write temperature or humidity set point controller
           based on loop selection

           TempSP: loop 1
           HumiSP: loop 2 
        '''
        self.send_cmd(f'SOURCE:CLOOP{loop}:SPOINT {val}')

    def get_ts(self, ts_num):
        '''read the state of time signal output
        '''
        self.send_cmd(f':OUTPUT{ts_num}:STATE?') 
        time.sleep(0.5)
        rsp = self.read_items()
        print (f'Time Signal#{ts_num} : {rsp}')
        pass

    def set_output(self, ts_num):
        '''output of selected time signal will be set
           in opposite state of its current condition
        '''
        self.send_cmd(f':OUTPUT{ts_num}:STATE?') 
        time.sleep(0.5)
        rsp = self.read_items()
        state = "ON" if rsp == 'OFF' else "OFF"
        time.sleep(0.5)
        self.send_cmd(f':OUTPUT{ts_num}:STATE {state}')

    def get_tsName(self, ts_num):
        '''read the name of assigned time signal
        '''
        self.send_cmd(f':OUTPUT{ts_num}:NAME?') 
        time.sleep(0.5)
        rsp = self.read_items()
        print (f'Name of Time Signal {ts_num} : {rsp}')
        pass

    def ramp_mode(self, mode, loop):
        '''set ramp mode: 
           define option for each mode:
              mode: OFF (turn off ramping, start instant change)
              mode: STARTUP (set startup)
              mode: SETPOINT (apply setpoint change)
              mode: BOTH (apply both values silmultaneously)
        '''
        self.send_cmd(f':SOURCE:CLOOP{loop}:RACTION {mode}')

    def get_ramp(self, rampType, loop):
        '''get ramp mode in rate or time
           
           rate: RRATE
           time: RTIME

           loop : [1,4]; loop = 1 : Temp, loop = 2 : Humi, etc 
        '''
        rateMode = 'RRATE' if rampType == 'rate' else 'RTIME'
        self.send_cmd(f':SOURCE:CLOOP{loop}:{rateMode}?')
        time.sleep(0.5)
        rsp = self.read_items()
        print (f'RAMP RATE : {rsp}') if rateMode == 'RRATE' else print (f'RAMP TIME : {rsp}') 

    def set_ramp(self, rampType, value, loop):
        '''apply ramp setting in rate or time

           rate: RRATE
           time: RTIME 
        '''
        rateMode = 'RRATE' if rampType == 'rate' else 'RTIME'
        self.send_cmd(f':SOURCE:CLOOP{loop}:{rateMode} {value}')
        print ('Done.')

    def set_rampScale(self, ramp_scale, loop):
        '''set ramp scaling for loop
        '''
        self.send_cmd(f':SOURCE:CLOOP{loop}:RSCALE {ramp_scale}')
        print ('Done.')