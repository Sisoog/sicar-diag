import serial
import time

class elm327:

    LastCommiunication_Time:int = 0

    def get_millis():
        return int(round(time.time() * 1000))

    def reset_timer(self, time_out:int):
        self.port.timeout = float(time_out/1000)
        elm327.LastCommiunication_Time = elm327.get_millis() + time_out

    def send_string(self, text:bytes, timeout:int):
        self.reset_timer(timeout)
        self.port.flush()
        self.port.write(text)
        
    def read_string_expect(self):
        responce_text:bytes = b''
        while elm327.LastCommiunication_Time > elm327.get_millis():
            if self.port.in_waiting > 0:
                responce_text = responce_text + self.port.read(self.port.in_waiting)
                if b'>' in responce_text:
                    return responce_text
            else:
                time.sleep(0.001)

        return responce_text

    def send_ATcmd(self, timeout:int, cmd:str):
        cmdbytes = (cmd + '\r\n').encode('ascii')

        self.send_string(cmdbytes, timeout)
        return self.read_string_expect()

    def __init__(self, port):
        self.port:serial.Serial = port

elm327_port = elm327(None)