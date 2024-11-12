
from ConnectionManager import *
from MainCmd import *
from tabulate import tabulate
from bidi.algorithm import get_display
import arabic_reshaper
class LiveParameter:

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
            if request.isporp > 0:
                pass
                # request.cmd_proplist = self.get_CmdPropList(request.unitid, "", App)
            arraylist.append(request)

        return arraylist

    def fillMainCmdList(self):
        self.mnotes = []
        for group in self.params:
            structNote_MainCmd = StructNote_MainCmd()
            structNote_MainCmd.cmd_list = self.getCmdArrayList(self.params[group])
            self.mnotes.append(structNote_MainCmd)

    def GetLiveDataTask(self):
        valid_responce:List[Response] = []
        mnotes_temp:List[StructNote_MainCmd] = []
        for it in self.mnotes:
            next:StructNote_MainCmd = it
            run_Request = Run_request()
            exe_cmd:List[Response] = run_Request.exe_cmd(next.cmd_list, False)
            self.Rsp = exe_cmd
            z = False
            for it2 in exe_cmd:
                next2:Response = it2
                if bool(next2.success) or not bool(next2.notSupport):
                    valid_responce.append(next2)
                z = next2.success
            if z:
                mnotes_temp.append(it)
        
        self.mnotes = mnotes_temp
        return valid_responce

    def LiveParamTask(self):

        self.fillMainCmdList()

        # Update Parameter
        ecu_results = self.GetLiveDataTask() #getLivedataTask.result

        titles = []
        results = []
        for res in ecu_results:
            cmd_text = get_display(arabic_reshaper.reshape(res.cmdDesc))
            titles.append(cmd_text)
            results.append(res.value)
            
        # Combine titles and results into a list of rows
        data = list(zip(titles, results))

        print("\r\n")
        print(tabulate(data,headers=["Title", "Result"], tablefmt="grid",showindex="always"))


    def __init__(self, params):
        self.params = params
        self.mnotes:List[StructNote_MainCmd] = []
        self.Rsp:List[Response] = []