import binascii
import io
import socket
import sys
from struct import unpack_from
from threading import Thread
from time import sleep
import serial #import serial module from pyserial

#replace '/dev/ttyUSB0' and 9600 with proper baud rate
serial_port_name = '/dev/ttyUSB0'
baud_rate = 9600

#The send_tm function is defined, which takes a 'simulator' object as a parameter. 
def send_tm(simulator):

    serial_port = serial.Serial(serial_port_name, baud_rate)

    with io.open('testdata.ccsds', 'rb') as f:
#opens the file in binary mode
        simulator.tm_counter = 1
#initalize simulated telemetry counter to one
        header = bytearray(6)
#defines the header as an array of 6 bytes
        while f.readinto(header) == 6:
            (len,) = unpack_from('>H', header, 4)
#length of packet is unpacked from the header. This assumes the length is stored as an unsigned short (2 bytes) in big-endian format
            packet = bytearray(len + 7)
            f.seek(-6, io.SEEK_CUR)
            f.readinto(packet)
            serial_port.write(packet)
            simulator.tm_counter += 1

            sleep(1)


def receive_tc(simulator):
    serial_port = serial.Serial(serial_port_name, baud_rate) 
    while True:
        data = serial_port.read(serial_port.in_waiting)
        
        simulator.last_tc = data
        simulator.tc_counter += 1

class Simulator():

    def __init__(self):
        self.tm_counter = 0
        self.tc_counter = 0
        self.tm_thread = None
        self.tc_thread = None
        self.last_tc = None

    def start(self):
        self.tm_thread = Thread(target=send_tm, args=(self,))
        self.tm_thread.daemon = True
        self.tm_thread.start()
        self.tc_thread = Thread(target=receive_tc, args=(self,))
        self.tc_thread.daemon = True
        self.tc_thread.start()

    def print_status(self):
        cmdhex = None
        if self.last_tc:
            cmdhex = binascii.hexlify(self.last_tc).decode('ascii')
        return 'Sent: {} packets. Received: {} commands. Last command: {}'.format(
                         self.tm_counter, self.tc_counter, cmdhex)


if __name__ == '__main__':
    simulator = Simulator()
    simulator.start()

    try:
        prev_status = None
        while True:
            status = simulator.print_status()
            if status != prev_status:
                sys.stdout.write('\r')
                sys.stdout.write(status)
                sys.stdout.flush()
                prev_status = status
            sleep(0.5)
    except KeyboardInterrupt:
        sys.stdout.write('\n')
        sys.stdout.flush()