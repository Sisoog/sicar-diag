import re
import binascii
from typing import List
import copy
import string
from datetime import *

from dataTypes import *


class f148un:
    LastEcuAddress = ""
    wakeupCmdList = Request()
    reIntCmdList = []


    def IsInitCmd(Str : str):
        return (Str.strip().startswith("81"))

    def IsCANExtendedAddress(self):
        return self.IsCanProtocol() and self.f161dw != ""

    def getAddress(self, Str):
        if self.f161dw != "" and f148un.IsInitCmd(Str) == False:
            return self.f161dw
        return self.f160d
    
    def getType(self, Str : str):
        i = 0
        if f148un.IsInitCmd(Str) == False and self.typeW != "":
            i = App.to_int(self.typeW)
        else:
            i = self.type

        if i != 1 or len(Str) <= 50:
            return i
        return 2
    
    def getCmdCount(self, Str:str):
        if app.isHexadecimal(Str):
            return app.getByteLen(Str)
        else:
            return 0
    
    def getWKCmdDefault(self):
        if self.baudType == 6:
            return "3E 01"
        else:
            return "3E"

    def getCmdCountHexType(self, Str:str):
        if self.getType(Str) == 2 or self.getType(Str) == 3:
            return App.to_Hex(self.getCmdCount(Str))
        else:
            return ""

    def getWCmd(self):
        Str = str("")
        GetStrFormBracket = ""
        if self.f163wc == "":
            Str = app.f148un.getHeaderAddress(self.getWKCmdDefault()) + self.getCmdCountHexType(self.getWKCmdDefault()) + " " + self.getWKCmdDefault()
        else:
            Str = self.f163wc
        if self.f163wc.find("NEH") > 0:
            Str = app.f148un.getHeaderAddress(GetStrFormBracket) + self.getCmdCountHexType(GetStrFormBracket) + " " + app.GetStrFormBracket(self.f163wc, "NEH")
        return Str
    
    def getNewCmd(Str : str):
        request = Request()
        request.fillDiffData()
        request.cmd_text = Str
        request.cmd_header = Str
        return request
    
    def getNewCmd_3(self, Str : str, Str2 : str):
        return self.getNewCmd_2(Str, Str2, Commandtype.cmd_InitCommunication, 2)

    def getNewCmd_2(self, Str : str, Str2 : str, cmdType : Commandtype, i : int):
        return self.getNewCmd_1(Str, Str2, cmdType, i, "", 10)

    def getNewCmd_1(self, Str : str, Str2 : str, cmdType : Commandtype, i : int, Str3 : str, l : int):
        newCmd = f148un.getNewCmd(Str)
        newCmd.cmd_resp = Str2
        newCmd.cmd_type = cmdType
        newCmd.cmd_try_num = i
        newCmd.cmd_try_num_main = i
        newCmd.replaceStrRsp = Str3
        newCmd.cmd_time_delay = l
        return newCmd
    
    def getCloseCmd(self):
        arrayList = []
        if ((self.isKWP() or self.baudType == 0) and not self.BypassInit()):
            if True:
                arrayList.append(self.getNewCmd_3("AT BI", ""))
            if True:
                arrayList.append(self.getNewCmd_2("82", "C2", Commandtype.cmd_Opr_IgnoreResp_36, 1))
        if True:
            arrayList.append(self.getNewCmd_3("AT PC", ""))
        if (True and self.baudType == 6):
            arrayList.append(f148un.getNewCmd("AT FE"))
        return arrayList

    def cmd_MuteLine(self, i:int):
        return self.AWF_MultiLine + "05"

    def getWKTime(self):
        return App.to_Hex(int(self.f164wt / 20))

    def getT74(self):
        return self.getT74_calc(self.t74)
    
    def getT74_calc(self, i : int):
        if i > 1020:
            i = 1020
        return App.to_Hex(int(i / 4))

    def getDeviceSetupCmd(self):
        arrayList = []

        arrayList.append(self.getNewCmd_3("ATWS", "ELM"))
        arrayList.append(f148un.getNewCmd("ATE0"))
        arrayList.append(f148un.getNewCmd("ATH0"))
        arrayList.append(f148un.getNewCmd("ATL0"))
        arrayList.append(f148un.getNewCmd("AT SP" + str(app.f148un.baudType)))
        
        i : int = app.f148un.baudType
        if i == 3 or i == 4 or i == 5:
            app.f148un.f163wc = self.getWCmd()
            i2 : int = self.f164wt
            if i2 != 3000 and i2 > 0:
                arrayList.append(f148un.getNewCmd("AT SW" + " " + self.getWKTime()))
            if self.f163wc != "":
                arrayList.append(f148un.getNewCmd("AT WM" + " " + self.f163wc))

        elif i == 6 or i == 8:
            arrayList.append(f148un.getNewCmd("AT CAF0"))
            arrayList.append(f148un.getNewCmd("AT SH" + " " + app.f148un.f160d))
            arrayList.append(f148un.getNewCmd("AT CRA" + " " + str(app.f148un.getSou())))
            arrayList.append(f148un.getNewCmd("AT FC SH" + " " + app.f148un.f160d))
            if app.f148un.f161dw != "":
                arrayList.append(f148un.getNewCmd("AT FC SD" + " " + app.f148un.f161dw + "30 00 00"))
            else:
                arrayList.append(f148un.getNewCmd("AT FC SD" + " " + "30 00 00"))
            arrayList.append(f148un.getNewCmd("AT FC SM 1"))
            if app.f148un.f161dw != "":
                arrayList.append(f148un.getNewCmd("AT CEA" + " " + app.f148un.f161dw))
                arrayList.append(f148un.getNewCmd("AT CER" + " " + app.f148un.f161dw))

        if self.t74 > 0:
            arrayList.append(f148un.getNewCmd("AT ST" + " " + self.getT74()))

        app.f148un.lastTarget = self.getSou()
        return arrayList

    def NoInit(self):
        return self.IsCanProtocol()
    
    def getECUInitCmdList(self, i:int, z:bool, localDataBase):
        arrayList = []
        i2:int = 0
        if app.f148un.initTry > 0:
            i2 = app.f148un.initTry
        else:
            i2 = 1
        Str:str = ""
        arrayList.extend(localDataBase.get_CmdArrayList(i, " and ctype = " + str(Commandtype.cmd_InitCommunication.value) + Str, App, app))
        return arrayList

    def IsForDevice(Str : str):
        if len(Str) < 2:
            return False
        return Str.startswith("AT")
    
    def IsCanProtocol(self):
        i = self.type
        return (i == 4 or i == 5)
    
    def is9141(self):
        return (self.baudType == 3)

    def is14230(self):
        i:int = self.baudType
        return i==4 or i==5

    def isKWP(self):
        return self.is9141() or self.is14230()

    def BypassInit(self):
        return app.GetStrFormBracket(self.attribute, "BI").lower() == "t"

    def getSou(self):
        i = self.Sou
        if i == 0:
            return "F1"
        else:
            return App.DesToHexStrNoFix(i)

    def getHeaderAddress(self, Str : str):
        address = self.getAddress(Str)
        type = self.getType(Str)
        cmdCount = self.getCmdCount(Str)
        if address != "":
            if self.f159c == 0:
                return address
            if type == 1 or type == 6:
                sb2 = []
                i = self.f159c
                if self.is9141():
                    cmdCount = 0
                sb2.append(App.to_Hex(i + cmdCount))
                sb2.append(" ")
                sb2.append(address)
                sb2.append(" ")
                sb2.append(self.getSou())
                sb = "".join(map(str, sb2))
            else:
                sb = ""
            if type == 2:
                sb = App.to_Hex(self.f159c) + " " + address + " " + self.getSou()
            Str2 = sb
            if type != 3:
                return Str2
        return ""
    
    def getCmdReq(request : Request, Str : str, Str2 : str, l : int, Str3 : str):
        request2 : Request = Request()
        request3 : Request = Request()
        try:
            request2 = copy.deepcopy(request)
        except Exception as e:
            ex = e
        try:
            request2.cmd_text = Str
            request2.cmd_resp = Str2
            request2.cmd_time_delay = l
            request2.cmd_header = Str3
            return request2
        except Exception as e2:
            ex = e2
            request3 = request2
            return request3
        
    def cmd_setCanTarget():
        return "AT CRA"

    def IsLargeCmdForCan(self, Str : str):
        return f148un.IsForDevice(Str) == False and app.f148un.IsCanProtocol() == True and app.getByteLen(Str) >= 8

    def set_8_byte_for_each(Str : str):
        split = Str.strip().split("\n")
        length = len(split)
        i = 0
        Str2 = ""
        while i < length:
            length2 = len(app.ToByteArray(split[i]))
            sb = []
            sb.append(Str2)
            sb.append(split[i])
            sb.append("\n" if i != length - 1 else "")
            if length2 < 8:
                sb.append(App.add_char(" 00", 8-length2))
            else:
                sb.append("")
            Str2 = str(sb)
            i += 1
        return Str2

    def add_enter(self, Str : str):
        uInfo : f148un
        Str2 = App.to_Hex(app.f148un.getCmdCount(Str)) + App.addSpc(" ") + ("".join(Str) if isinstance(Str, list) else Str)
        if len(app.ToByteArray(Str2)) <= 8:
            return Str2
        StrArr = ["10", "21", "22", "23", "24", "25", "26", "27", "28", "29", "2A", "2B", "2C", "2D", "2E", "2F", "20", "21", "22", "23", "24", "25", "26", "27", "28", "29", "2A", "2B", "2C", "2D", "2E", "2F", "20", "21", "22", "23", "24", "25", "26", "27", "28", "29"]
        split = Str2.strip().split(" ")
        if App.HexToLong(split[0]) > 7:
            Str3 : str = ""
            i : int = 0
            for i2 in range(len(split)):
                if i2 % 7 == 0:
                    Str3 += "\n" if Str3 else ""
                    Str3 += StrArr[i]
                    i += 1
                Str3 += App.addSpc(Str3) + split[i2]
            uInfo = self
            Str2 = Str3
        else:
            uInfo = self
        return uInfo.set_8_byte_for_each(Str2)


    def __init__(self):
        self.Sou = 0
        self._eid = 0
        self.baudRate = 0
        self.baudType = 0
        self.cahngeBaud = False
        self.deviceVersion = ""
        self.fileName = ""
        self.forceJobCancel = False
        self.historyId = 0
        self.initTry = 0
        self.init_group_id = 0
        self.menu_level = 0

        self.f162p = 0
        self.reInitTiming = 0
        self.t65 = 0
        self.t74 = 0
        self.wakeupTiming = 0

        self.f163wc = ""  
        self.f164wt = 0
        self.attribute = ""
        self.STS = ""

        self.f157K1 = ""
        self.lastTarget = ""

        self.f158K2 = ""
        self.isUpASA3Sharp = False
        self.countNoRespDevice = [0,0,0]
        self.bufferSession = ""
        self.ver_Db = 1
        self.AWF_MultiLine = "AT 87 00 01 "

        self.f160d = ""

        self.f159c = 0
        self.eid = 0

        self.f161dw = ""
        self.type = 1
        self.typeW = "1"

class Hex:
    def decode(Str : str):
        try:
            return binascii.unhexlify(Str)
        except Exception as e:
            raise Exception("exception decoding Hex string: " + str(e))

    def toHexString(b_arr):
        return Hex.toHexStringWithRange(b_arr, 0, len(b_arr))

    def toHexStringWithRange(b_arr, i, i2):
        return binascii.hexlify(b_arr[i:i+i2]).decode()


class App:

    HEXADECIMAL_PATTERN = re.compile(r'[0-9A-Fa-f]+')
    lastExecuteCmdTime:datetime = None

    def roundDouble(d:float, i:int):
        return format(d, f".{i}f")

    def to_int(Str):
        if Str is not None:
            try:
                if Str != "":
                    # print("to_int", str(Str) + " ")
                    return int(Str)
            except Exception as ex:
                if 'invalid literal for int() with base 10:' in str(ex) and '-' not in Str:
                    return int(float(Str))
                else:
                    print(ex)
        return 0
    
    def fixStringArray(Str:str):
        return Str.replace("[", "(").replace("]", ")")

    def ToByteArray(self, Str : str):
        if self.isHexadecimal(Str):
            return Hex.decode(App.FixHex(App.replSpc(Str)))
        else:
            return ""
    
    def AlphabetToNumber(i:int, Str:str):
        strArr = ["0", "1", "2", "3", "4", "5", "6", "7", "8", "9", "A", "B", "C", "D", "E", "F", "G", "H", "J", "K", "L", "M", "N", "P", "R", "S", "T", "U", "W", "X", "Y", "Z"]
        if Str == "":
            return strArr[i]
        return strArr.index(Str)

    def HexToAlphabetWithIndex(str):
        sb = ""
        i = 0
        while i < len(str):
            i2 = i + 2
            sb += App.AlphabetToNumber(int(str[i:i2], 16), "")
            i = i2
        return sb

    def HexToChar(hex_string):
        output_string = ""
        for i in range(0, len(hex_string), 2):
            hex_value = hex_string[i:i+2]
            char_value = chr(int(hex_value, 16))
            output_string += char_value
        return output_string

    def Set2Digit(str1:str):
        if len(str1) == 1:
            return "0" + str1
        return str1

    def byteToHex(b):
        return ''.join([hex((b >> 4) & 15)[2:], hex(b & 15)[2:]]).upper()

    def insertCher(Str:str, i):
        str2 = ""
        for x in range(i):
            str2 += Str
        return str2

    def HexToBinary(hex_string:str):
        if hex_string == "":
            return ""
        hex_int = int(hex_string, 16)
        binary_string = bin(hex_int)[2:]
        if len(binary_string) % 8 != 0:
            binary_string = App.insertCher('0',8 - len(binary_string) % 8) + binary_string
        return binary_string

    def HexToBinaryPosition(hex_string:str, i, i2):
        binary_string = App.HexToBinary(hex_string)
        # return binary_string[i:i2+i]
        return binary_string[i:i+i2]

    def BinaryToDecimal(binary_string):
        return int(binary_string, 2)

    def HexToDecimal(Str:str):
        return App.HexToLong(Str)

    def indexOf(Str:str, Str2:str):
        return App.replSpc(Str).find(App.replSpc(Str2))

    def to_Hex(i : int):
        return App.FixHex(hex(i).upper())[2:]
    
    def to_Hex2(bArr:bytes, z:bool):
        if z:
            cin = int.from_bytes(bArr, byteorder="big")
            return App.to_Hex(cin).upper()
        return binascii.hexlify(bArr).decode()

    def to_Hex3(bArr):
        temp = ""
        for b in bArr:
            temp = temp + App.addSpc(temp) + App.byteToHex(b)
        return temp

    def HexToInt(Str:str):
        replSpc = App.replSpc(Str)
        if replSpc == "":
            return 0
        return int(replSpc, 16)

    def to_str(Str:str):
        if Str == "" or Str == "null":
            return ""
        else:
            return Str
    
    def ByteToDecimal(b:bytes):
        return b & 255

    def DesToHexStrNoFix(i : int):
        return App.to_str(hex(i).upper()[2:])

    def HexToLong(Str : str):
        try:
            if Str == "":
                return 0
            return int(Str, 16)
        except Exception as e:
            print(e)
            return 0

    def addSpc(Str : str):
        if Str == "":
            return ""
        else:
            return " "
    
    def add_char(Str, i):
        str2 = ""
        for i2 in range(i):
            str2 += Str
        return str2

    def replSpc(Str : str):
        if isinstance(Str, list):
            Str = "".join(Str)
            
        return Str.replace(" ", "")
    
    def replaceStartWith(Str:str, Str2:str):
        indexOf = 0
        indexOf2 = 0
        if "XX" in Str2 and len(Str) > (indexOf2 := (indexOf := Str2.index("XX")) + 2):
            Str2 = Str2.replace("XX", Str[indexOf:indexOf2]).strip().upper()
        if Str.startswith(Str2.upper()):
            Str = Str.replace(Str2, "").strip()
        return Str

    def FixHex(Str : str):
        if len(App.replSpc(Str)) % 2 == 0:
            return Str
        return "0" + Str
    
    def getByteLen(self, Str : str):
        try:
            return len(self.ToByteArray(Str))
        except Exception:
            return 0
    
    def getByteWithLen_1(Str:str, i:int, i2:int, z:bool):
        ToByteArray = app.ToByteArray(Str)
        lenB = len(ToByteArray)
        if lenB <= i or lenB < i2:
            return Str
        else:
            if i - lenB == i2:
                return App.to_Hex2(ToByteArray[i].to_bytes(1, 'big'), z)    
            else:
                return App.to_Hex2(ToByteArray[i].to_bytes(1, 'big'), z)

    def getByteWithLen(Str:str, i:int, i2:int):
        return App.getByteWithLen_1(Str, i, i2, True)

    def getBytePosition(Str:str, i:int):
        ToByteArray:bytes = app.ToByteArray(Str)
        if len(ToByteArray) > i:
            return App.ByteToDecimal(ToByteArray[i])
        return 0
    
    def getBytePositionHex(Str:str, i:int):
        return App.to_Hex(App.getBytePosition(Str, i))

    def isHexadecimal(self, Str: str):
        target = App.replSpc(Str)
        return all(c in string.hexdigits for c in target)
    
    def GetStrFormNotation(Str:str, Str2:str, Str3:str, Str4:str, z:bool):
        upperCase = Str2.upper()
        if z:
            Str = Str.upper()
        if upperCase + Str3 in Str:
            indexOf = Str.index(upperCase + Str3) + len(upperCase) + 1
            return Str[indexOf:Str.index(Str4, indexOf)].strip()
        return ""
    
    def GetStrFormAccolade(Str : str, Str2 : str):
        return App.GetStrFormNotation(Str, Str2, "{", "}", True)

    def GetIntFormBracket(self, Str, Str2):
        return App.to_int(App.GetStrFormNotation(Str, Str2, "[", "]", True))

    def GetStrFormBracket(self, Str, Str2):
        return App.GetStrFormNotation(Str, Str2, "[", "]", True)

    def GetIndexFormFormula(Str:str, Str2:str):
        up:str = Str.upper()
        up2:str = Str2.upper()
        if up.find(up2) > -1:
            indexOf = up.find(up2 + "[") + len(up2) + 1
            indexOf2 = up.find("]", indexOf)
            if indexOf > 1:
                return App.to_int(up[indexOf:indexOf2].strip())
            return -1
        return -1

    def checkSuccessRsp(arrayList:List[Response]):
        z:bool = False
        if arrayList == None or len(arrayList) == 0:
            return False
        
        for responce in arrayList:
            z = z and responce.success
        return z

    def getRespVal(arrayList:List[Response]):
        str1:str = ""
        for responce in arrayList:
            if responce.success:
                str1 = responce.value.upper()
        return str1


    def getDateTime():
        return datetime.now()

    def __init__(self):
        self.f148un = f148un()
        self.lastIntGroupIdForScheduling = 0

app = App()
