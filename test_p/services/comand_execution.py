import os
import sys
# 获取当前脚本所在的目录
current_dir = os.path.dirname(os.path.abspath(__file__))

# 获取项目根目录（假设项目根目录是当前脚本的上一级目录）
project_root = os.path.dirname(current_dir)

# 将项目根目录添加到 sys.path
if project_root not in sys.path:
    sys.path.insert(0, project_root)

# 现在可以正常导入 test_p 包
from bsp.power_manage import power_ctrl
from bsp.power_manage import ina219_ch1
from bsp.tsu_info import tsu_info

class CommandHandler:
    def __init__(self):
        # 初始化指令与处理函数的映射字典
        self.command_map = {
            'bat on': self.handle_bat_on,
            'bat off': self.handle_bat_off,
            'ig on': self.handle_ig_on,
            'ig off': self.handle_ig_off,
            'acc on': self.handle_acc_on,
            'acc off': self.handle_acc_off,
            'usb on': self.handle_usb_on,
            'usb off': self.handle_usb_off,
            'curent check': self.handle_curent_check,
            'tsu info': self.handle_tsu_info,
            'status': self.handle_status, 
            'reset': self.handle_reset,
        }
    def handle_bat_on(self, client_socket, client_address):
        # print(f"[{client_address}] 执行指令: bat on")
        sta = power_ctrl.bat_set(0x00) 
        if sta == 0:
            response_message = "bat on Success"
        else:
            response_message = "bat on Failure"
        client_socket.send(response_message.encode('utf-8'))

    def handle_bat_off(self, client_socket, client_address):
        # print(f"[{client_address}] 执行指令: bat off")
        sta = power_ctrl.bat_set(0xff)
        if sta == 0:
            response_message = "bat off Success"
        else:
            response_message = "bat off Failure"
        client_socket.send(response_message.encode('utf-8'))

    def handle_ig_on(self, client_socket, client_address):
        # print(f"[{client_address}] 执行指令: ig on")
        sta = power_ctrl.ig_set(0x00)
        if sta == 0:
            response_message = "ig on Success"
        else:
            response_message = "ig on Failure"
        client_socket.send(response_message.encode('utf-8'))

    def handle_ig_off(self, client_socket, client_address):
        # print(f"[{client_address}] 执行指令: ig off")
        sta = power_ctrl.ig_set(0xff)
        if sta == 0:
            response_message = "ig off Success"
        else:
            response_message = "ig off Failure"
        client_socket.send(response_message.encode('utf-8'))

    def handle_acc_on(self, client_socket, client_address):
        # print(f"[{client_address}] 执行指令: acc on")
        sta = power_ctrl.acc_set(0x00)
        if sta == 0:
            response_message = "acc on Success"
        else:
            response_message = "acc on Failure"
        client_socket.send(response_message.encode('utf-8'))

    def handle_acc_off(self, client_socket, client_address):
        # print(f"[{client_address}] 执行指令: acc off")
        sta = power_ctrl.acc_set(0xff)  
        if sta == 0:
            response_message = "acc off Success"
        else:
            response_message = "acc off Failure"
        client_socket.send(response_message.encode('utf-8'))

    def handle_usb_on(self, client_socket, client_address):
        # print(f"[{client_address}] 执行指令: usb on")
        sta = power_ctrl.usb_set(0x00)
        if sta == 0:
            response_message = "usb on Success"
        else:
            response_message = "usb on Failure"
        client_socket.send(response_message.encode('utf-8'))

    def handle_usb_off(self, client_socket, client_address):
        # print(f"[{client_address}] 执行指令: usb off")
        sta = power_ctrl.usb_set(0xff)  
        if sta == 0:
            response_message = "usb off Success"
        else:
            response_message = "usb off Failure"
        client_socket.send(response_message.encode('utf-8'))
        
    def handle_curent_check(self,client_socket,client_address):
        curent = ina219_ch1.getCurrent_mA()
        ret = "{:6.2f}".format(curent)
        # ret = "{:6.2f} mA".format(curent)
        client_socket.send(ret.encode('utf-8'))

    def handle_tsu_info(self,client_socket,client_address):
        tsu_info.get_tsu_info()
        ret = str(tsu_info.info_list)
        client_socket.send(ret.encode('utf-8'))
        
    def handle_status(self, client_socket, client_address):
        # print(f"[{client_address}] 执行指令: status")
        status = "Device is running"
        response_message = f"Status: {status}"
        client_socket.send(response_message.encode('utf-8'))

    def handle_reset(self, client_socket, client_address):
        # print(f"[{client_address}] 执行指令: reset")
        power_ctrl.acc_set(0x00)  
        power_ctrl.acc_set(0xff)  
        response_message = "Device reset!"
        client_socket.send(response_message.encode('utf-8'))

    def handle_unknown(self, client_socket, client_address):
        print(f"[{client_address}] Unknown command")
        response_message = f"Unknown command"
        client_socket.send(response_message.encode('utf-8'))

    def process_command(self, command, client_socket, client_address):
        handler = self.command_map.get(command, self.handle_unknown)
        handler(client_socket, client_address)

comand_hander = CommandHandler()