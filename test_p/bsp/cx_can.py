import os
import can
import time

class can_dev:
    def __init__(self):
        print("正在设置 CAN 接口...")
        # os.system('sudo ip link set can0 down')
        # os.system('sudo ip link set can1 down')
        # os.system('sudo ip link set can0 up type can bitrate 125000')
        # os.system('sudo ip link set can1 up type can bitrate 125000')

        print("正在初始化 CAN 接口...")
        try:
            self.can0 = can.interface.Bus(channel='can0', interface='socketcan')
            self.can1 = can.interface.Bus(channel='can1', interface='socketcan')
        except Exception as e:
            print(f"CAN 接口初始化失败: {e}")
            raise  # 抛出异常，停止程序运行

        self.msg = can.Message(is_extended_id=True, arbitration_id=0x123, data=[0, 0, 0, 0, 0, 0, 0, 0])
        print("CAN 接口和消息已成功初始化。")

    def bcan_send(self):
        print("正在向 can0 发送消息...")
        try:
            self.can0.send(self.msg)
            print("消息已发送到 can0")
        except Exception as e:
            print(f"向 can0 发送消息失败: {e}")
        time.sleep(0.05)

    def fcan_send(self):
        print("正在向 can1 发送消息...")
        try:
            self.can1.send(self.msg)
            print("消息已发送到 can1")
        except Exception as e:
            print(f"向 can1 发送消息失败: {e}")

        time.sleep(0.05)

    def shutdown(self):
        print("正在关闭 CAN 总线接口...")
        try:
            self.can0.shutdown()
            self.can1.shutdown()
            print("CAN 总线接口已成功关闭。")
        except Exception as e:
            print(f"关闭 CAN 总线接口时出错: {e}")

cx_can = can_dev()

try:
    can_send.msg = can.Message(arbitration_id=0x123, data=[0, 1, 2, 0, 0, 0, 0, 0])
    can_send.bcan_send()

    a = can_send.can0.recv(10.0)
    print(a)
finally:
    can_send.shutdown()