import binascii
import io
import sys
from struct import unpack_from
from threading import Thread
from time import sleep
import serial

# Replace 'COM1' and 9600 with the appropriate virtual port name and baud rate
serial_port_name = '/dev/pts/3'
baud_rate = 9600

# The send_tm function is defined, which takes a 'simulator' object as a parameter.
def send_tm(simulator):
    with io.open('testdata.ccsds', 'rb') as f:
        simulator.tm_counter = 1
        header = bytearray(6)
        while f.readinto(header) == 6:
            (length,) = unpack_from('>H', header, 4)
            packet = bytearray(length + 7)
            f.seek(-6, io.SEEK_CUR)
            f.readinto(packet)
            simulator.serial_port.write(packet)
            simulator.tm_counter += 1
            sleep(1)

def receive_tc(simulator):
    while True:
        data = simulator.serial_port.read(simulator.serial_port.in_waiting)
        simulator.last_tc = data
        simulator.tc_counter += 1

class Simulator():
    def __init__(self):
        self.tm_counter = 0
        self.tc_counter = 0
        self.tm_thread = None
        self.tc_thread = None
        self.last_tc = None
        self.serial_port = None

    def start(self):
        self.serial_port = serial.Serial(serial_port_name, baud_rate)
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