'''
:author: Paul Nong-Laolam <paul.nong-laolam@espec.com>
:license: MIT, see LICENSE for more detail.
:copyright: (c) 2022. ESPEC North America, INC.
:file: f4t_class.py

Class implementation for Watlow F4T direct communication interface
using built-in Python Library. 

'''
import socket
import struct
import logging
from enum import Enum
from atexit import register, unregister

LOG = logging.getLogger(__name__)
BUFFER_SIZE = 10        # set buffer size for transmission through the socket

class Controller:
    '''Set up a generic socket for device connection
    '''

    @classmethod
    def source_dev(subcls, dev):
        '''generating new instances of objects from factory function 
        for different subclasses
        '''
        assert issubclass(subcls, dev)
        return subcls(dev.host, dev.port, conn = dev._conn, id = dev._id)

    def __init__(self, host, port = 5025, timeout = None, *args, **kwargs):
        self._host = host
        self._port = port
        self.timeout = timeout
        print (f'Connecting to F4T at: {host}:{port}')
        self._conn = kwargs.get('conn', socket.create_connection((self._host, 
                                               self._port), timeout = timeout))
        self.f4t_id = kwargs.get('id', None)
        self.encoding = kwargs.get('encoding', 'ascii')
        self.EOL = struct.pack('>B', 10)
        if self.f4t_id is None:
            self.get_id()
        register(self._conn.close)

    def clear_buffer(self):
        '''clear reading buffer after each attempt
        '''
        self._conn.settimeout(self.timeout)
        try:
            res = self._conn.recv(BUFFER_SIZE)
        except socket.timeout:
            pass

    def read_items(self):
        '''read items from target device
        '''
        msg = 'FAILED'.encode()
        try:
            msg = bytearray(self._conn.recv(BUFFER_SIZE))
            while msg[-1] != ord(self.EOL):
                msg.extend(self._conn.recv(BUFFER_SIZE))
        except socket.timeout:
            pass
        return msg.decode(self.encoding).strip()

    def send_cmd(self, cmd:str):
        '''issue command request to device
        '''
        self._conn.send(cmd.encode(self.encoding) + self.EOL)

    def __del__(self):
        unregister(self._conn.close)
        self._conn.close()

class TempUnits(Enum):
    '''
    specify unit representation for standard temperature reading
    
    define: celcius and farenheit 
            C = c; F = f 
    '''
    C = 'C'
    F = 'F'

class Scale(Enum):
    '''
    Ramp Scale Type
    '''
    H = 'HOURS'
    M = 'MINUTES'