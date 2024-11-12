from ConnectionManager import *
from LiveData import *

import argparse
from signal import signal, SIGINT
from sys import exit
from queue import Queue
import json


q = Queue(2)

############################ Argument Difinition ############################
parser = argparse.ArgumentParser(formatter_class=argparse.RawTextHelpFormatter)   
parser.add_argument("-c", "--config", help="config file is", default="jsons/PEG_206_IRA_SIE.json")       # get input database file
parser.add_argument("-p", "--port", help="port is", default="/dev/ttyUSB0")       # get input database file
############################ Argument Difinition ############################

############################ Argument Getting ############################
args = parser.parse_args()
configFile = args.config
serial_port = args.port
############################ Argument Getting ############################

############################ Class Difinition ############################
class Adapter:
    def __init__(self, to_dict):
        self.specs = to_dict["CONNECTION"]["SPECS"]
        self.initCmds = to_dict["CONNECTION"]["INITCMDLIST"]
        self.wakeupCmds = to_dict["CONNECTION"]["WAKEUPCMDLIST"]
        self.reinitCmds = to_dict["CONNECTION"]["REINITCMDLIST"]
        self.parameter = to_dict["PARAMETER"]
        self.dtc = to_dict["DTC"]

        self.Cm = ConnectionManager(self.specs, self.initCmds, self.wakeupCmds, self.reinitCmds)
        self.liveParm = LiveParameter(self.parameter)

        try:
            ser = serial.Serial(port=serial_port, baudrate=38400, bytesize=8, parity='N', stopbits=1)
            elm327_port.ser = ser
        except Exception as ex:
            print(ex)
            exit(0)

    def connect(self):
        if self.Cm.execute_TryConnect(False, False):
            return True
        return False
    
    def disconnect(self):
        ConnectionManager.runCloseSessionCmd()

    def monitorParameter(self):
        self.liveParm.LiveParamTask()
############################ Class Difinition ############################


############################ Main Program ############################
adapter = None
def main(qSignal):
    # ordering json file
    f = open(configFile, "r")
    config = json.loads(f.read())
    f.close()
    
    adapter = Adapter(config)
    adapter.connect()
    while True:
        adapter.monitorParameter()
    
def handler(signal_received, frame):
    # Handle any cleanup here
    print('SIGINT or CTRL-C detected. Exiting gracefully')
    q.put(False)
    adapter.disconnect()
    exit(0)

if __name__ == "__main__":
    signal(SIGINT, handler)
    print('Running. Press CTRL-C to exit.')
    main(q)  
