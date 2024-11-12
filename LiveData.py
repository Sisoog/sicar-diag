
from ConnectionManager import *
from MainCmd import *
import curses
from threading import Thread

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
        # Load parameter and start Parameter Updater Task
        self.fillMainCmdList()
        getLivedataTask = AsyncGetLiveParameter(self, 0.05)
        getLivedataTask.start()

        # Initial show Parameter Pages
        stdscr = curses.initscr()
        stdscr.timeout(100)
        item_start, item_end = 0, 10

        while True:
            
            # Update Parameter
            result = getLivedataTask.result

            # calculate Page
            length = len(result)
            start = start if item_start < 0 or item_start > length else item_start
            end = length if length < item_end else item_end
            item_start = start
            item_end = end if length > 0 and item_end > length else item_end
            
            # Show Parameter
            stdscr.clear()
            stdscr.addstr(0,0, f"Pages({int(end/10 + bool(end%10))}/{int(length/10 + bool(length%10))})")
            for i in range(start, end):
                stdscr.addstr((i-start)+1,0, result[i].cmdDesc)
                stdscr.addstr((i-start)+1,60, str(result[i].value))
            stdscr.refresh()

            # Check Push Any Key
            try:
                c = stdscr.getkey()
                curses.endwin()
                if c == '1':
                    item_start += 10
                    item_end += 10

                elif c == '2':
                    item_start -= 10
                    item_end -= 0 if item_start < 0 else (end - start)
                else:
                    getLivedataTask.exitFlag = True
                    break
            except curses.error:
                pass

        # Kill Task Updater Parameter
        getLivedataTask.join()

    def __init__(self, params):
        self.params = params
        self.mnotes:List[StructNote_MainCmd] = []
        self.Rsp:List[Response] = []


# custom thread
class AsyncGetLiveParameter(Thread):
    # constructor
    def __init__(self, LiveParam:LiveParameter, periodTime:float):
        # execute the base constructor
        Thread.__init__(self)
        # set a default value
        self.liveparameter = LiveParam
        self.result:List[Response] = []
        self.exitFlag = False
        self.timeout = periodTime
 
    # function executed in a new thread
    def run(self):
        while not self.exitFlag:
            self.result = self.liveparameter.GetLiveDataTask()

            # block for a moment
            time.sleep(self.timeout)
