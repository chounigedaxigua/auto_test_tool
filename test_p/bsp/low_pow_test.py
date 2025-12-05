from bsp.power_manage import power_ctrl
# from bsp.power_manage import INA219
from bsp.power_manage import ina219_ch1
import os
import time
from bsp.log import my_log
import threading


class low_power_t:
    def __init__(self):
        # self.ina4 = INA219(addr = 0x43)
        # self.power = JDQ()
        current_task = threading.Thread(target=ina219_ch1.current_check_task)
        current_task.start()
        
    def low_power_test(self):

        timer = 0
        
        # /**1、root 成功
        #  * 
        #  * 2、断开acc|ig|usb
        #  * 3、看6分钟的时候电流是否在2ma左右
        #  * 4、链接acc|ig 唤醒
        #  * 5、再次进入低功耗
        #  */
        
        # info_printf("\n-> low power test\n")
        while timer < 40:
            if os.system("adb root") == 0:
                break
            time.sleep(1)
            timer + 1
            if timer  > 40:
                my_log.error("The tsu timeout is not started")
                return -1
        # print(dir(ina4))
        timer = 0
        # power_gpio_set(1,0,0,0)
        power_ctrl.bat_set(0x00)
        power_ctrl.acc_set(0xff)
        power_ctrl.ig_set(0xff)
        power_ctrl.usb_set(0xff)

        my_log.debug("ACC|IG|USB_OPWER off\n")
        my_log.debug("Waiting to enter low-power mode......\n")
        while timer < 600:
            time.sleep(1)
            timer += 1
            print("Current:{:9.4f}ma".format(ina219_ch1.avg_curent))
            if ina219_ch1.avg_curent < 5 and ina219_ch1.avg_curent > 0:
                my_log.debug("Successfully entered low-power mode\n")
                break
            if timer >= 600:
                my_log.error("Enter the low-power timeout\n")
                return -1

        timer = 0
        time.sleep(120)
        power_ctrl.bat_set(0x00)
        power_ctrl.acc_set(0x00)
        power_ctrl.ig_set(0x00)
        power_ctrl.usb_set(0x00)
        my_log.debug("ACC|IG|USB_OPWER on\n")
        my_log.debug("Waiting to exit low-power mode......\n")
        while timer < 5:
            time.sleep(1)
            timer += 1
            if os.system("adb root") == 0:
                my_log.debug("SOC successfully awakened\n")
                break
            if timer > 5:
                my_log.error("Failed to exit the low-power consumption\n")
                return -1
        my_log.debug("low power mode test success\n")
        return 0
    def test_task(self):
        # current_task = threading.Thread(target=self.ina4.current_check_task)
        # current_task.start()
        self.low_power_test()
        return 0

low_power = low_power_t()