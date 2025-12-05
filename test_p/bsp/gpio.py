import time as t
from smbus2 import SMBus
import sys

DEVICE_BUS  = 1
DEVICE_ADDR = 0x10
class pwr_status:
    pwr_on = 0xFF           # 打开继电器的值
    pwr_off = 0x00          # 关闭继电器的值


RELAY1 = 0x01       # 继电器1寄存器地址
RELAY2 = 0x02       # 继电器2寄存器地址
RELAY3 = 0x03       # 继电器3寄存器地址
RELAY4 = 0x04       # 继电器4寄存器地址

bus = SMBus(DEVICE_BUS) 

def gpio_set(add = DEVICE_ADDR,reg,status = pwr_status.gpio_off):
    bus.write_byte_data(add, reg, pwr_status.gpio_off)


# while True:
#     try:
#         for i in [RELAY1,RELAY2,RELAY3,RELAY4]:
#             gpio_set(i, pwr_status.pwr_on)
#             t.sleep(1)
#             gpio_set( i, pwr_status.pwr_off)
#             t.sleep(1) 
#     except KeyboardInterrupt as e:
#         print("Quit the Loop")
#         for i in [RELAY1,RELAY2,RELAY3,RELAY4]:
#             bus.write_byte_data(DEVICE_ADDR, i, pwr_status.gpio_off)
#         sys.exit()

 