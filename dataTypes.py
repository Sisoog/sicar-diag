from CommandType import *

class CmdPropItem:
    def __init__(self):
        self.code = 0
        self.ename = ""
        self.f116id = 0
        self.pname = ""
        self.value = 0




class Request:
    def __init__(self):
        self.MultiLine = False
        self.cmd_Desc = ""
        self.cmd_decmin = 0
        self.cmd_group_id = 0
        self.cmd_max = 0
        self.cmd_min = 0
        self.cmd_proplist = []
        self.cmd_resp = ""
        self.cmd_seq = 0
        self.cmd_text = ""
        self.cmd_time_delay = 0
        self.cmd_unit = ""
        self.cmd_unit_sim = ""
        self.deviceTimeDelay = 0
        self.iType = 0
        self.isporp = 0
        self.unitid = 0
        self.cmd_id = 0
        self.cmd_type = Commandtype.cmd_InitCommunication
        self.cmd_SMain = SubCmdType.cmd_Main
        self.cmd_try_num = 1
        self.cmd_try_num_main = 1
        self.cmd_header = ""
        self.cmd_formula = ""
        self.Attribute = ""
        self.replaceStrRsp = ""

    def fillDiffData(self):
        self.cmd_resp = "OK"
        self.cmd_time_delay = 50
        self.cmd_header = ""
        self.cmd_try_num = 2



class Response:
    def __init__(self):
        self.cmd_SubMainType = SubCmdType.cmd_Main
        self.cmd_group_id = 0
        self.cmd_id = 0
        self.cmd_type = Commandtype.cmd_noCmd
        self.max = 0
        self.min = 0
        self.value = ""
        self.netValue = ""
        self.mainValue = ""
        self.success = False
        self.notSupport = False
        self.formula = ""
        self.unit_sim = ""
        self.cmdText = ""
        self.cmdDesc = ""
        self.cmdHeader = ""
        self.Error7FCode = 0

    def __str__(self):
        return self.cmdText