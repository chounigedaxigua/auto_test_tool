import subprocess
import os
import time
from bsp.low_pow_test import low_power
from bsp.log import my_log
from bsp.tsu_info import tsu_info
from bsp.mode_test import mode_test
from bsp.power_manage import power_ctrl
from bsp.power_manage import ina219_ch1
from services.cx_sock import cx_sock
if __name__=='__main__':
    
    # power_ctrl.cleanup()
    # tsu_info.get_tsu_info()
    # low_power.test_task()
    # mode_test.reboot_test_task_start()
    # mode_test.all_test() 
    # cx_sock.task_start()
    cx_sock.start_tcp_server()
    try:
        while True:
            time.sleep(1)
            
            
            pass
    except KeyboardInterrupt:
        print("中断 (Ctrl+C)")
        # cx_sock.sock_end()
    finally:
        cx_sock.exit_event.set() 
        ina219_ch1.exit_event.set()
        mode_test.exit_event.set()
        power_ctrl.cleanup()
        print("清理完成，程序退出")