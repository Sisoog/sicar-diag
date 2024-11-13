from app_Info import *
from Run_Request import *
import OCMD
import logging
logger = logging.getLogger(__name__)

class ConnectionManager:

    def haveTypeW():
        return App.to_int(app.f148un.typeW) > 0 or app.f148un.f161dw != ""

    def getErrorCode(array_list:List[Response]):
        for response in array_list:
            if f148un.IsInitCmd(response.cmdText):
                HexToInt = App.HexToInt("")
                if HexToInt == 1:
                    return 0
                return HexToInt
        return 0

    def getEcuInfo(self):
        # TODO - Remove Used Fild in Json
        app.f148un.wakeupTiming = App.to_int(self.specs["wakeupTiming"])
        app.f148un.reInitTiming = App.to_int(self.specs["reInitTiming"])
        app.f148un.f160d = str(self.specs["d"])
        #app.f148un.f159c = App.to_int(self.specs["c"])
        app.f148un.type = int(self.specs["type"])
        app.f148un.typeW = str(self.specs["typew"])
        app.f148un.f161dw = str(self.specs["dw"])
        #app.f148un.f162p = int(self.specs["p"])
        #app.f148un.f164wt = int(self.specs["wt"])
        app.f148un.f163wc = str(self.specs["wc"])
        #app.f148un.t74 = int(self.specs["t74"])
        #app.f148un.t65 = int(self.specs["t65"])
        #app.f148un.Sou = int(self.specs["s"])
        app.f148un.baudType = int(self.specs["baudtype"])

        if str(self.specs["attribute"]) != "":
            #app.f148un.baudRate = app.GetIntFormBracket(str(self.specs["attribute"]), "BR")
            app.f148un.initTry = app.GetIntFormBracket(str(self.specs["attribute"]), "IT")
            #app.f148un.attribute = str(self.specs["attribute"])

    def getCmdArrayList(self, array):
        arraylist = []
        result = array
        for row in result:
            request = Request()
            request.cmd_type = Commandtype(App.to_int(row["ctype"]))

            if App.to_int(row["smain"]) == 1:
                request.cmd_SMain = SubCmdType.cmd_SubMain
            else:
                request.cmd_SMain = SubCmdType.cmd_Main

            request.cmd_try_num = App.to_int(row["ctrynum"])
            request.cmd_try_num_main = request.cmd_try_num
            request.cmd_text = OCMD.FixStrCmd(App.to_str(row["cmdtext"]), app, App)
            request.cmd_header = App.to_str(row["cheader"])
            request.cmd_formula = App.to_str(row["cformula"])
            request.cmd_Desc = App.to_str(row["cdesc"])
            request.cmd_resp = App.to_str(row["cresp"])
            request.cmd_min = App.to_int(row["cmin"])
            request.cmd_max = App.to_int(row["cmax"])
            request.cmd_unit = App.to_str(row["cunit"])
            request.cmd_unit_sim = App.to_str(row["unit_sim"])
            request.cmd_seq = App.to_int(row["cseq"])
            request.cmd_time_delay = OCMD.FixTiming(App.to_str(row["ctimewait"]), request.cmd_type)
            request.cmd_decmin = App.to_int(row["decimalp"])
            request.unitid = App.to_int(row["unitid"])
            request.isporp = App.to_int(row["isporp"])
            request.iType = App.to_int(row["itype"])
            request.deviceTimeDelay = app.GetIntFormBracket(App.to_str(row["format"]), "DTD")
            request.MultiLine = "MTLINE" in App.to_str(row["format"])
            request.Attribute = App.to_str(row["format"])

            arraylist.append(request)

        return arraylist

    def Run_Init_Cmd(self):
        z2 : bool = False
        i3 : int = 0

        self.getEcuInfo()
        run_Request = Run_request()
        arrayList : List[Response]

        if True:
            logger.debug("Run Init ECU CMD")

            if ConnectionManager.haveTypeW() or app.f148un.cahngeBaud:
                app.f148un.cahngeBaud = False
                arrayList = run_Request.exe_cmd(app.f148un.getDeviceSetupCmd(), False)
                z2 = True
                for responce in arrayList:
                    z2 = responce.success
            else:
                z2 = True
        
            if z2 == False:
                i3 = 0
            else:
                arrayList = run_Request.exe_cmd(self.getCmdArrayList(self.initCmd),False)
                z2 = True
                for responce in arrayList:
                    z2 = responce.success
                i3 = 0 if z2 else ConnectionManager.getErrorCode(arrayList)

            if app.f148un.wakeupTiming > 0 and z2:
                uInfo : f148un = app.f148un
                f148un.wakeupCmdList = self.getCmdArrayList(self.wakeupCmd)

            if app.f148un.reInitTiming > 0:
                uInfo2 : f148un = app.f148un
                f148un.reIntCmdList = self.getCmdArrayList(self.reinitCmd)

            if len(arrayList) == 0:
                return 0
            if z2:
                return 1
            return i3
        return 0

    def runCloseSessionCmd():
        try:
            # Assuming G.un.getCloseCmd() returns a string command to be executed
            run_request = Run_request()
            command = app.f148un.getCloseCmd()
            responce_ForCommand = run_request.exe_cmd(command, False)
            if App.checkSuccessRsp(responce_ForCommand):
                app.f148un.STS = "00"
        except Exception as e:
            print(f"An error occurred: {str(e)}")

    def execute_TryConnect(self):        
        flag = self.Run_Init_Cmd() == 1
        return flag
    
    def __init__(self, specs, initCmd, wakeupCmd, reinitCmd):
        self.specs = specs
        self.initCmd = initCmd
        self.wakeupCmd = wakeupCmd
        self.reinitCmd = reinitCmd
