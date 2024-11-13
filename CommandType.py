from enum import Enum

class Commandtype(Enum):
    cmd_noCmd = 0
    cmd_InitCommunication = 1
    cmd_Param_2 = 2
    cmd_Operation = 3
    cmd_Trouble = 4
    cmd_ClearTrouble = 5
    cmd_ConnectToDevice_ELM = 6
    cmd_ConnectToDevice_ASAN = 7
    cmd_CountTroubleCode_08 = 8
    cmd_ReadChar_09 = 9
    cmd_EndOperation_10 = 10
    cmd_PramReplaceText_11 = 11
    cmd_ReadHex_12 = 12
    cmd_AllDecimal_13 = 13
    cmd_GetValue_Configuration_14 = 14
    cmd_SetValue_Configuration_15 = 15
    cmd_PendingTrouble_16 = 16
    cmd_GroupLoop_17 = 17
    cmd_ReInit = 18
    cmd_ReadFreezeFrame_19 = 19
    cmd_Stop_Communication_20 = 20
    cmd_SingleLoop_21 = 21
    cmd_TextStr = 22
    cmd_wakeup = 23
    cmd_Trouble_No_OBD2_CAN = 24
    cmd_ReInit_Communication = 25
    cmd_Trouble_NoObd2 = 26
    cmd_LoopUnlimited_27 = 27
    cmd_SingleDecimal_28 = 28
    cmd_MessageBox_29 = 29
    cmd_Trouble_ReverseCode = 30
    cmd_Trouble_NoOby2_NoFaultCode = 31
    cmd_AvgParam = 32
    cmd_ReadAlphabetWithIndex_33 = 33
    cmd_LoopCmdToExit_34 = 34
    cmd_inputBox_35 = 35
    cmd_Opr_IgnoreResp_36 = 36
    cmd_CloseSession_37 = 37
    cmd_findFirstValidResultInGroup = 38
    cmd_Opr_RespIsImportant_39 = 39
    cmd_MapTable = 40
    cmd_SplitValueToCommands = 41
    cmd_Condition_42 = 42
    cmd_SubGroupInOperation = 43
    cmd_BatchCommand = 44
        
class SubCmdType(Enum):
    cmd_Main = 0,
    cmd_SubMain = 1
