from app_Info import *
from typing import List
import time
from datetime import *
from elm327 import *
from Calculator import *
from dataTypes import *



class Run_request:
    def GetEndBTagIndex(i, Str:str):
        strArr = ["1", "2", "3", "4", "5", "6", "7", "8", "9", "0", "[", "]", "B", "O", "C"]
        i2 = i
        while i2 < len(Str):
            i3 = i2 + 1
            if Str[i2:i3] not in strArr:
                return i2
            i2 = i3
        return i2
    
    def customGetEndBTagIndex(i, Str:str):
        strArr = ["1", "2", "3", "4", "5", "6", "7", "8", "9", "0", "[", "]", "(", ")", "B", "<", "-", "&"]
        i2 = i
        while i2 < len(Str):
            i3 = i2 + 1
            if Str[i2:i3] not in strArr:
                return i2
            i2 = i3
        return i2

    def getValueExp(str1:str, str2:str, commandtype:Commandtype):
        HexToBinary:str = ""
        split = str1.split("B")

        str3 = ""
        if str2 == "":
            return ""
        length = len(split)
        GetIndexFormFormula2 = App.GetIndexFormFormula(str1, "O")
        if GetIndexFormFormula2 > 7:
            GetIndexFormFormula2 = 0
        
        i2 = 1
        if GetIndexFormFormula2 > -1:
            i = App.GetIndexFormFormula(str1, "C")
            GetIndexFormFormula = 1
        else:
            GetIndexFormFormula = App.GetIndexFormFormula(str1, "C")
            i = 1
        
        if i < 1:
            i = 1
        if GetIndexFormFormula <= 0:
            GetIndexFormFormula = 1
        
        str4 = ""
        i3 = 0
        while i3 < length:
            GetIndexFormFormula3 = App.GetIndexFormFormula("B" + split[i3], "B")
            if app.getByteLen(str2) >= GetIndexFormFormula3 and GetIndexFormFormula3 >= 0:
                str4 = str4 + App.getByteWithLen_1(str2, GetIndexFormFormula3 - 1, (GetIndexFormFormula3 + GetIndexFormFormula) - i2, False)
            i3 += 1
            i2 = 1
        
        i4 = Commandtype(commandtype).value
        if i4 != 2:
            if i4 == 5:
                str4 = str(App.HexToChar(str4))
            elif i4 == 6:
                str4 = str(App.HexToAlphabetWithIndex(str4))
            return str4

        if GetIndexFormFormula2 > -1:
            if len(App.HexToBinary(str4)) > 7:
                str3 = str(App.BinaryToDecimal(App.HexToBinaryPosition(str4, GetIndexFormFormula2, i)))
            str4 = str3
        else:
            str4 = str(App.HexToDecimal(str4))
        return str4

    def customGetValueExp(str1:str, str2:str, commandtype:Commandtype):
        
        split = str1.split("B")
        length = len(split)
        str4 = ""
        i3 = 0
        while i3 < length:
            partByte = split[i3]            
            startByte, endByte = "", ""

            indexOf = partByte.find("B[") + 2
            startByte = partByte[indexOf:]
            indexOf = startByte.find("~")
            if indexOf == -1: 
                indexOf = startByte.find("]")
                startByte = startByte[0:indexOf]
                endByte = startByte
            else:
                endByte = startByte[indexOf:]
                startByte = startByte[0:indexOf]
                indexOf = endByte.find("]")
                endByte = endByte[0:indexOf]
            
            if startByte == "":
                startByte = "-1"
            if app.getByteLen(str2) >= int(startByte) and int(startByte) >= 0:
                str4 = str4 + App.getByteWithLen_1(str2, int(startByte) - 1, int(endByte), False)
            i3 += 1

        i4 = Commandtype(commandtype).value
        if i4 != 2:
            if i4 == 5:
                str4 = str(App.HexToChar(str4))
            elif i4 == 6:
                str4 = str(App.HexToAlphabetWithIndex(str4))
            return str4
        if "&" in str1:
            indexOf = str1.find("&(") + 2
            bitValue = str1[indexOf:]
            indexOf = bitValue.find("<<")
            numShift = str1[str1.find("<<") + 2:]
            bitValue = bitValue[0:indexOf]
            indexOf = numShift.find(")")
            numShift = numShift[0:indexOf]
            
            if len(App.HexToBinary(str4)) > 7:
                str3 = str(App.BinaryToDecimal(App.HexToBinaryPosition(str4, int(numShift), bitValue.count('1'))))
            str4 = str3
        else:
            str4 = str(App.HexToDecimal(str4))
        return str4
        
    def getValueFromReqList(i, response_list:List[Response]):
        for response in response_list:
            if response.cmd_id == i:
                return str(response.value)
        return "0"

    def make_expression_WithCID(array_list, Str:str):
        length = len(Str.split("CID"))
        for i in range(length):
            GetIndexFormFormula = App.GetIndexFormFormula(Str, "CID")
            Str = Str.replace("CID[" + str(GetIndexFormFormula) + "]", Run_request.getValueFromReqList(GetIndexFormFormula, array_list))
        return Str

    def make_expression(Str:str, Str2:str, commandtype, arrayList):
        return Run_request.customMake_expression(Str, Str2, commandtype, arrayList)

    
    def customMake_expression(Str:str, Str2:str, commandtype, arrayList):
        length = len(Str.split("B"))
        for i in range(length):
            Str = Str.replace(" ", "")
            indexOf = Str.find("B[")
            if indexOf < 0:
                break
            substring = Str[indexOf:Run_request.customGetEndBTagIndex(indexOf, Str)]
            Str = Str.replace(substring, Run_request.customGetValueExp(substring, Str2, commandtype))
        if App.GetIndexFormFormula(Str, "CID") > 0:
            Str = Run_request.make_expression_WithCID(arrayList, Str)
        return Str


    def getValueExp_2(substring:str, inputValue:str):
        inputValue_Arr = inputValue.split(" ")
        strArr = substring.split("B")
        strArr = strArr[1:]
        for i in range(len(strArr)):
            strArr[i] = 'B' + strArr[i]

        if inputValue == "":
            return ""
        
        # replacement
        frame = ""
        for i in range(len(strArr)):
            indexbit = App.GetIndexFormFormula(strArr[i], "O")
            count = App.GetIndexFormFormula(strArr[i], "C")
            count = count if count > -1 else 1
            indexbyte = App.GetIndexFormFormula(strArr[i], "B") -1
            
            for i in range(count):
                bytes_str = inputValue_Arr[indexbyte+i]
                if indexbit > -1:
                    byte_bin = App.HexToBinary(App.replSpc(bytes_str))
                    bit_result = str(byte_bin[indexbit])
                    frame += "0b1" if bit_result == "1" else '0b0'
                else:
                    frame += '0x' + str(bytes_str)
        
        bin_split = frame.split("0b")
        if bin_split[0] == "":
            bin_split = bin_split[1:]
        for i in range(len(bin_split)):
            if bin_split[i].startswith('0x'):
                bin_split[i] = bin_split[i].replace('0x', '')
                bin_split[i] = '0x' + bin_split[i]
            else:
                bin_split[i] = "1" if bin_split[i] == "1" else "0"
        result = "".join(bin_split)
        return result

    def getValueFromCondition(condition:str, inputValue:str):
        condition = condition.lower()
        if "case" in condition:
            coundition_list = condition[4:].split("when")[1:]
            for cond in coundition_list:
                cond = cond.replace('¶', '').replace(' ', '')
                indexThen = cond.find("then")
                indexElse = cond.find("else")
                indexEnd = cond.find("end")
                cound = cond[0:indexThen]
                
                for i in range(len(cound)):
                    c = ord(cound[i])
                    if c == 60 or c == 61 or c == 62:
                        break
                cound_SL = cound[0:i]
                cound = cound[i:]

                i = 0
                for i in range(len(cound)):
                    c = ord(cound[i])
                    if c == 60 or c == 61 or c == 62:
                        i += 1
                        break
                cound_OP = cound[0:i]
                cound = cound[i:]
                cound_SR = cound

                if cound_OP == "=":
                    cound_OP = "=="

                instruction_else = '\"\"'
                if indexElse > -1:
                    instruction_then = cond[(indexThen+4): indexElse]
                    instruction_else = cond[(indexElse+4): indexEnd]
                elif indexEnd > -1:
                    instruction_then = cond[(indexThen+4): indexEnd]

                else:
                    instruction_then = cond[(indexThen+4):]

                result = str(eval(instruction_then + "if " + cound_SL+cound_OP+cound_SR + "else " + instruction_else))
                if result == str(eval(instruction_then)) or result == str(eval(instruction_else)) and result != '':
                    return result       
        return condition

    def getParamFromFormula(FormulaValue:str, respValue:str, arralist:List[Response]):
        length = len(FormulaValue.split("B"))

        for i in range(length):
            FormulaValue = FormulaValue.replace(" ", "")
            indexOf = FormulaValue.find("B[")
            if indexOf < 0:
                break
            substring = FormulaValue[indexOf:Run_request.GetEndBTagIndex(indexOf, FormulaValue)]
            FormulaValue = FormulaValue.replace(substring, Run_request.getValueExp_2(substring, respValue))
        
        if App.GetIndexFormFormula(FormulaValue, "CID") > -1:
            FormulaValue = Run_request.make_expression_WithCID(arralist, FormulaValue)
        
        FormulaValue = Run_request.getValueFromCondition(FormulaValue, respValue)
        return FormulaValue


    def ReadValueFromHex(request:Request, str1:str):
        make_exp = Run_request.make_expression(request.cmd_formula, str1, Commandtype.cmd_ReadHex_12, [])
        return make_exp if request.unitid <= 0 or request.cmd_proplist == [] else Run_request.getCmdPropName(request.cmd_proplist, App.to_int(make_exp))

    def getCmdPropName(arrayList:List[CmdPropItem], i:int):
        if len(arrayList) > 0 and arrayList[0].value >= 299:
            i = Run_request.GetTrueBit(i) + 300
        propName = Run_request.getPropName(arrayList, i)
        return propName if i < 299 or not propName == "" else Run_request.getPropName(arrayList, 400)

    def getPropName(arrayList:List[CmdPropItem], i:int):
        it = arrayList
        for next in it:
            if next.value == i:
                str1 = next.pname
        return str1
    
    def GetTrueBit(i:int):
        i2 = 0
        for str1 in App.HexToBinary(App.to_Hex(i).split("")):
            if App.to_int(str1) == 1:
                return i2 - 1
            i2 += 1
        return -1    

    def calc_formula(self, str1:str, i:int):
        return self.customCalc_formula(str1, i)

    def calcFromCondition(str1:str):
        newCondition = ""
        newStr = str1
        while True:
            indexOf = newStr.find("?")
            if indexOf == -1:
                break
            _if = newStr[0:indexOf]

            newStr = newStr[indexOf+1:]
            indexOf = newStr.find(":")
            _then = newStr[0:indexOf]
            
            newCondition += f"{_then} if {_if} else "
            if newStr[indexOf+1:].find("?") == -1:
                _else = newStr[indexOf+1:]
                newCondition += f"{_else}"
                break
            else:
                newStr = newStr[indexOf+1:]
        return eval(newCondition)
    
    def customCalc_formula(self, str1:str, i:int):
        try:
            cl = Calculator()
            if "?" in str1.upper():
                return Run_request.calcFromCondition(str1)
            return App.roundDouble(float(Calculator.From(str1)), i)
        
        except Exception as ex:
            print(ex)
            return "0"


    def setCmdText(request : Request):
        return request
    
    def checkResp(request:Request, Str:str):
        return App.replSpc(Str).startswith(App.replSpc(request.cmd_resp).strip())
    
    def ReplaceArrayHead(Str:str, Str2:str, Str3:str):
        i:int = 0
        replace = Str2.replace("\r\n", "\r").replace("\n", "\r").replace("\\r", "\r")
        if not app.f148un.IsCanProtocol() or f148un.IsForDevice(Str):
            i = 0
        else:
            Str4 = "\n" if replace.find("\n") > -1 else "\r"
            i = App.GetIndexFormFormula(Str3, "E") if Str3.find("E[") > -1 else 1
            split = replace.split(Str4)
            if len(split) > 1:
                Str5 = ""
                for Str6 in split:
                    if len(split) <= 1:
                        Str5 = Str5 + Str6
                    elif not Str6[3, len(Str6)].startswith("7F"):
                        Str5 = Str5 + Str6[i * 3, len(Str6)]
                replace = Str5

            Str3 = Str3.replace("E[" + str(i) + "]", "")

        indexOf = App.indexOf(replace, app.GetStrFormBracket(Str3, "RBB"))
        if Str3.find("RBB[") > -1 and indexOf > 0:
            bytePosition = App.getBytePosition(replace, indexOf - 2) + i
            if i > 0 and app.getByteLen(replace) > bytePosition:
                replace = App.getByteWithLen(replace, i - 1, bytePosition)
            if i > 0:
                indexOf -= (i - 1) * 3
            if len(replace) >= indexOf:
                replace = replace.replace(replace[:indexOf], "").strip()
        for Str7 in Str3.split(","):
            replace = App.replaceStartWith(replace, Str7).strip()
        return replace

    def Remove7F_IfHaveMultiResp(Str:str, Str2:str, z:bool):
        replace = Str2.replace("\r\n", "\r").replace("\n", "\r")
        split = replace.split("\r")
        if len(split) == 1 or f148un.IsForDevice(Str) or z:
            return replace

        Str3:str = ""
        for Str4 in split:
            if not app.isHexadecimal(Str4):
                return Str4
            
            temp:str = "7F" + App.getByteWithLen(Str, 0, 1)
            if not (temp in App.replSpc(Str4)):
                # str3 = str3 + Remove_ASA_Address(str, str4);
                Str3 = Str3 + Str4

        if len(split) <= 1 or Str3 != "":
            return Str3
        else:
            return split[ (len(split) -1) ]

    def replaceHeaderXX(Str:str, Str2:str):
        if "XX" in Str2:
            length = len(Str2.split("XX"))
            for i in range(length):
                Str2 = Str2.replace("XX", App.getBytePositionHex(Str, i), 1)
            
            return App.replSpc(Str).replace(App.replSpc(Str2), "", 1)
        
        return Str

    def replaceRespXX(Str:str, Str2:str):
        if "XX" in Str:
            length = len(Str.split("XX")) - 1
            for i in range(length):
                Str = Str.replace("XX", App.getBytePositionHex(Str2, i), 1)
            
            return Str
        
        return Str

    def getNegativeResponseCode(Str:str):
        return App.HexToInt(App.getByteWithLen(Str, 2, 3))

    def checkResp(request:Request, Str:str):
        return App.replSpc(Str).startswith(App.replSpc(request.cmd_resp).strip())

    def Exec_Cmd_try_1(request:Request, z:bool, z2:bool, z3:bool):
        responce = Response()

        while True:
            
            try:
                responce.mainValue = str(elm327_port.send_ATcmd(request.cmd_time_delay+2000, request.cmd_text))[2:-1]
                if responce.mainValue.find(">") > -1:
                    responce.mainValue = responce.mainValue.replace(request.cmd_text, "").replace("\\r", "").replace("\\n", "").replace(">", "")
                if responce.mainValue.startswith("BUS INIT:"):
                    responce.mainValue = responce.mainValue[10:]

                Str:str = request.cmd_header if request.cmd_header != "" else ""

                responce.mainValue = Run_request.ReplaceArrayHead(request.cmd_text, responce.mainValue, Str)
                responce.mainValue = Run_request.Remove7F_IfHaveMultiResp(request.cmd_text, responce.mainValue, z3)
                responce.mainValue = responce.mainValue.replace(request.replaceStrRsp, "")
                responce.mainValue = Run_request.replaceHeaderXX(responce.mainValue, Str)
                request.cmd_resp = Run_request.replaceRespXX(request.cmd_resp, responce.mainValue)
                responce.cmd_type = request.cmd_type
                responce.formula = request.cmd_formula
                if request.cmd_try_num == 0:
                    request.cmd_try_num = request.cmd_try_num_main
                responce.success = Run_request.checkResp(request, responce.mainValue)
                if request.cmd_type != Commandtype.cmd_Opr_IgnoreResp_36 and not responce.success:
                    if not responce.success and app.f148un.is9141() and f148un.IsInitCmd(request.cmd_text):
                        time.sleep(5)
                    request.cmd_try_num -= 1
                    if len(request.cmd_text) > 1:
                        responce.notSupport = "7F" + request.cmd_text.strip()[0:2] in App.replSpc(responce.mainValue)
                    if responce.notSupport:
                        responce.Error7FCode = Run_request.getNegativeResponseCode(responce.mainValue)
                        i:int = responce.Error7FCode
                        if i == 35:
                            request.cmd_try_num += 1
                        elif i == 53:
                            request.cmd_try_num = 0
                        elif i != 120:
                            if i in [16, 17, 18]:
                                request.cmd_try_num = 0
                        else:
                            if not request.MultiLine:
                                if True:
                                    Run_request.Exec_Cmd(app.f148un.getNewCmd_3(app.f148un.cmd_MuteLine(request.deviceTimeDelay), ""))
                                request.MultiLine = True
                            request.cmd_try_num = request.cmd_try_num_main
                            if request.cmd_try_num < 40:
                                request.cmd_try_num += 1
                    elif request.cmd_type != Commandtype.cmd_Opr_RespIsImportant_39 and request.cmd_type != Commandtype.cmd_InitCommunication:
                        time.sleep(1)
                else:
                    responce.value = responce.mainValue
                    app.f148un.countNoRespDevice[0] = 0
                    app.f148un.countNoRespDevice[1] = 0
                    app.f148un.countNoRespDevice[2] = 0
                    responce.value = responce.value.replace("\r", "")
                    request.cmd_try_num = 0
                if not f148un.IsForDevice(request.cmd_text):
                    uInfo = app.f148un
                    uInfo.LastRSP = responce
                    uInfo2 = app.f148un
                    uInfo.LastCmd = request
                if request.cmd_try_num >= 1:
                    pass
                
                if responce.success == True or request.cmd_try_num == 0:
                    return responce
            except Exception as ex:
                print(ex)

            if app.f148un.forceJobCancel:
                break
        return responce

    def Exec_Cmd_try(request:Request):
        return Run_request.Exec_Cmd_try_1(request, False, False, False)        



    def Exec_Cmd(request : Request):
        responce = Response()

        GetStrFromBracket : str = app.GetStrFormBracket(request.Attribute, "T2")
        if GetStrFromBracket == "":
            GetStrFromBracket = app.f148un.getSou()

        if app.f148un.IsCanProtocol() and app.f148un.lastTarget != GetStrFromBracket:
            uInfo7 : f148un = app.f148un
            app.f148un.lastTarget = GetStrFromBracket
        
        cmdText = Request()
        cmdText = Run_request.setCmdText(request)

        if app.f148un.IsLargeCmdForCan(cmdText.cmd_text):
            split : str = app.f148un.add_enter(cmdText.cmd_text.split("\n"))
            i2 : int = 0
            while i2 < len(split):
                Str:str = ""
                if i2 == 0:
                    Str = "30"
                else:
                    Str = ""
                if i2 == (len(split) -1):
                    Str = cmdText.cmd_resp
                
                i2 += 1

            return responce
        
        responce_show = Run_request.Exec_Cmd_try(cmdText)
        print(f"CMD[{cmdText.cmd_text}]\tRESPONCE[{responce_show.value}]\tTIMEOUT[{cmdText.cmd_time_delay}ms]\tSTATE[{responce_show.success}]")
        return responce_show

    def removeNotValidChr(Str : str):
        return Str.replace("\r", "").replace("\n", "")

    def getMainRespInArray(arrayList : List[Response]):
        responce = Response()
        for next in arrayList:
            if next.cmd_SubMainType == SubCmdType.cmd_Main:
                responce = next
        return responce

    def exe_cmd(self, arrayList : List[Request], Bool):
        arrayList2:List[Response] = []

        for request in arrayList:
            responce = Response()

            if app.f148un.forceJobCancel:
                print(f"force job cancel Run_Request {app.f148un.forceJobCancel} ")
            else:
                request.cmd_text = Run_request.removeNotValidChr(request.cmd_text)
                request.cmd_formula = Run_request.removeNotValidChr(request.cmd_formula)
                Address = app.f148un.getAddress(request.cmd_text)
                if request.cmd_text.upper().find("ATZ") > 0 or request.cmd_text.upper().find("ATD") > 0 or request.cmd_text.upper().find("ATWS") > 0:
                    uInfo : f148un = app.f148un
                    f148un.LastEcuAddress = ""
                if not f148un.IsForDevice(request.cmd_text):
                    if not app.f148un.IsCanProtocol() and not Address == "" and app.f148un.eid != 1 and not app.f148un.is9141():
                        uInfo2 = app.f148un
                        if f148un.LastEcuAddress != app.f148un.getHeaderAddress(request.cmd_text):
                            uInfo3 = app.f148un
                            f148un.LastEcuAddress = app.f148un.getHeaderAddress(request.cmd_text)
                            uInfo4 = app.f148un
                            Run_request.Exec_Cmd(f148un.getCmdReq(request, ("AT SH" + " " + app.f148un.getHeaderAddress(request.cmd_text)), "OK", 50, "" ))

                            if app.f148un.reInitTiming > 0 and request.cmd_type != Commandtype.cmd_InitCommunication and (App.getDateTime().timestamp() - App.lastExecuteCmdTime.timestamp()) >= app.f148un.reInitTiming:
                                uInfo5 = app.f148un
                                for request in f148un.reIntCmdList:
                                    Run_request.Exec_Cmd(request)

                i : int = SwitchMap_SubCmdType[request.cmd_SMain]
                if i == 1:
                    responce = Run_request.Exec_Cmd(request)
                elif i == 2:
                    if Bool == True:
                        responce = Run_request.Exec_Cmd(request)
                    else:
                        mainRespInArray = Run_request.getMainRespInArray(arrayList2)
                        responce.success = mainRespInArray.success
                        responce.mainValue = mainRespInArray.mainValue

                responce.formula = request.cmd_formula
                responce.cmd_type = request.cmd_type
                responce.cmdText = request.cmd_text
                responce.cmdDesc = request.cmd_Desc
                responce.cmdHeader = request.cmd_header
                responce.cmd_SubMainType = request.cmd_SMain
                
                if responce.success:
                    try:
                        typeCmd = SwitchMap_Commandtype[request.cmd_type]

                        if typeCmd == 1:
                            responce.value = request.cmd_formula
                        elif typeCmd == 2:
                            responce.value = Run_request.make_expression(request.cmd_formula, responce.mainValue, request.cmd_type, arrayList2)
                        elif typeCmd == 3:
                            responce.value = Run_request.ReadValueFromHex(request, responce.mainValue)
                        elif typeCmd == 4:
                            responce.value = responce.mainValue.replace(request.cmd_formula, "")
                        elif typeCmd in [5, 6, 7]:
                            responce.value = Run_request.make_expression(request.cmd_formula, responce.mainValue, request.cmd_type, arrayList2)
                        elif typeCmd in [8, 9, 10, 11]:
                            if not request.cmd_formula == "":
                                responce.value = self.calc_formula(Run_request.make_expression(request.cmd_formula, responce.mainValue, request.cmd_type, arrayList2), request.cmd_decmin)
                                responce.netValue = responce.value
                                if request.isporp == 1:
                                    responce.value = Run_request.getCmdPropName(request.cmd_proplist, App.to_int(responce.value))
                                if request.cmd_type == Commandtype.cmd_AvgParam.value:
                                    responce.value = Run_request.getCmdPropName(request.cmd_proplist, App.to_int(responce.value))
                                    pass
                        App.lastExecuteCmdTime = App.getDateTime()

                    except Exception as ex:
                        pass
                
                responce.cmd_id = request.cmd_id
                responce.unit_sim = request.cmd_unit_sim
                responce.min = request.cmd_min
                responce.max = request.cmd_max
                responce.cmd_group_id = request.cmd_group_id

                arrayList2.append(responce)

        return arrayList2                   

    def __init__(self):
        pass


