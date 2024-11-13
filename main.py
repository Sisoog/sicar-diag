from ConnectionManager import *
from LiveData import *
import argparse
from sys import exit
from queue import Queue
import json
import logging
from tabulate import tabulate
logger = logging.getLogger(__name__)


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

        self.Cm = ConnectionManager(self.specs, self.initCmds, self.wakeupCmds, self.reinitCmds)
        self.liveParm = LiveParameter(self.parameter)

        try:
            port = serial.Serial(port=serial_port, baudrate=38400, bytesize=8, parity='N', stopbits=1)
            elm327_port.port = port
        except Exception as ex:
            logger.error(ex)
            exit(0)

    def connect(self):
        logger.debug("Try Connect to ECU")
        if self.Cm.execute_TryConnect():
            logger.debug("Connect OK.")
            return True
        logger.debug("can not connect to ECU")
        return False
    
    def disconnect(self):
        ConnectionManager.runCloseSessionCmd()

    def monitorParameter(self):
        logger.debug("Read ECU Parameter")
        data = self.liveParm.LiveParamTask()

        print("\r\n")
        print(tabulate(data,headers=["Title", "Result"], tablefmt="grid",showindex="always"))
############################ Class Difinition ############################


############################ Main Program ############################
def main():
    
    # Load ECU Data
    logger.info("Try Load ECU Config From Jsom")
    f = open(configFile, "r")
    config = json.loads(f.read())
    f.close()
    logger.info("ECU data Loaded.")

    adapter = Adapter(config)
    adapter.connect()
    adapter.monitorParameter()
    
if __name__ == "__main__":
    logging.basicConfig(level=logging.DEBUG)
    main()  
