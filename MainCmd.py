from typing import List
from dataTypes import *

class StructNote_MainCmd:

    def __init__(self):
        self.cmd_list:List[Request] = []
        self.cmdgroupid:int = 0