from dataTypes import *



def FixStrCmd(Str:str, app, App):
    if app.f148un.IsCanProtocol():
        replace = Str.replace("DDD", str(app.f148un.f160d)).replace("SSS", str(app.f148un.getSou()))
        if app.f148un.IsCANExtendedAddress():
            if App.replSpc(replace).find(App.replSpc("AT FC SD")):
                replace = "AT FC SD" + str(app.f148un.f161dw) + replace.replace("AT FC SD", "")
            return replace.replace("EXXT", str(app.f148un.f161dw))
        return replace
    return Str

def FixTiming(Str:str, commandtype:Commandtype):
    if commandtype == Commandtype.cmd_ReInit_Communication:
        return 50
    else:
        return int(Str)