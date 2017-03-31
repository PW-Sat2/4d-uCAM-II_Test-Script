import serial
import time

class UCamIICommands(object):
    def SYNC(self):
        return b'\xAA\x0D\x00\x00\x00\x00'

    def RESET(self):
        return b'\xAA\x0E\xFF\x00\x00\x00'

class UCamIICommunication(object): 
    def DEFAULT_BAUDRATE(self):
        return 57600
        
    def FRAME_LENGTH(self):
        return 12

    def connect(self, port):
        self.ser = serial.Serial(port, self.DEFAULT_BAUDRATE())

    def disconnect(self):
        self.ser.close()
    
    def send_command(self, command):
        self.ser.write(command)

    def received_bytes(self):
        return self.ser.in_waiting
        
    def a_frame_received(self):
        if self.received_bytes()==self.FRAME_LENGTH():
            return True
        return False
        
    def clear_buffers(self):
        self.ser.reset_input_buffer()
        self.ser.reset_output_buffer()

class UCamII(object):
    def __init__(self, port):
        self.commands = UCamIICommands()
        self.communication = UCamIICommunication()
        
        self.communication.connect(port)

    def MAX_SYNCS(self):
        return 60
    
    def DELAY_RESET(self):
        return 0.005
        
    def DELAY_BASE(self):
        return 0.02
    
    def DELAY_MULTIPLIER(self):
        return 0.001
        
    def ERROR_NOT_SYNCED(self):
        return -1
    
    def disconnect(self):
        self.communication.disconnect()
    
    def get_sync_delay(self, sync_index):
        return self.DELAY_BASE() + self.DELAY_MULTIPLIER() * sync_index
    
    def sync_once(self):
        self.communication.send_command(self.commands.SYNC())
    
    def sync(self):
        self.communication.clear_buffers();
    
        for sync_index in range(1, self.MAX_SYNCS()):
            self.sync_once()
            
            time.sleep(self.get_sync_delay(sync_index))
            
            if(self.communication.received_bytes()>0):
                self.communication.send_command(self.commands.RESET())
                time.sleep(self.DELAY_RESET())
                
                if self.communication.a_frame_received():
                    return sync_index 
            
        return self.ERROR_NOT_SYNCED()