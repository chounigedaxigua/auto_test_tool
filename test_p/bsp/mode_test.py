from bsp.log import my_log
from bsp.power_manage import power_ctrl
import os
import time
import subprocess
import threading
class mode_test_t:
    def __init__(self):
        self.thread_flag = True
        print(" ")
        self.exit_event = threading.Event()

    def __del__(self):
        print("mode test end ")
        self.thread_flag = False

    def usb_reset(self):
        power_ctrl.usb_set(0xff)
        time.sleep(0.3)
        power_ctrl.usb_set(0x00)
        print("usb reset")

    def process_test(self):

        r = os.popen('adb shell "ls /oemapp/bin"').read()
        print(r)
        file_list = r.strip().split('\n')
        print("文件列表:", file_list)
        for file_name in file_list:
            # 构造 adb shell 命令，检查进程是否存在
            command = f'adb shell "ps -ef | grep {file_name} | grep -v grep"'

            # 执行命令并获取结果
            process_check = os.popen(command).read().strip()

            # 判断进程是否在运行
            if process_check:
                # print(f"进程 '{file_name}' 正在运行:")
                print(process_check)
            else:
                my_log.error(f"'{file_name}' 进程未启动")
    def adb_connect(self):
        cnt = 20
        while (cnt) and not self.exit_event.is_set():
            time.sleep(2)
            cnt -=1
            if os.system("adb root") == 0:
                return 0
            self.usb_reset()
        return -1

    def reflash_test(self):
        my_log.debug("-> reflash test")
        if os.system("adb shell \"ls /proc/recoveryinfo\"") != 0:
            my_log.error("tsu_reflash err")
            return -1
        my_log.debug("Reflash test successful")
        return 0
    def cellular_test(self):

        my_log.debug("-> cellular test")
        if os.system("adb shell \"ps -ef| grep oemapp/bin/cellular | grep -v grep\"") != 0:
            my_log.error("cellular No startup")
            return -1

        # tsu_part_num_file = os.popen("adb shell \"cat /usrdata/conf/tsu_part_num.txt\"").read()
        # if(fgets(buf,sizeof(buf),fp)>(char*)0)
        
        #     my_log.debug("tsu_part_num: %s",buf)
        #     if(strncmp("8B100-3BWT-COMM-M1",buf,sizeof("8B100-3BWT-COMM-M1")-1))
            
        #         my_log.error("cat tsu_part_num.txt err != 8B100-3BWT-COMM-M1")
        #         return -1
        if os.system("adb shell \"ifconfig | grep rmnet_data\"") != 0:
            my_log.error("The dial status is wrong")
            return -1
        cert_cn_file = os.popen("adb shell \"cat /data/run_info/cert_cn.txt\"").read()
        my_log.debug(f"cert_cn : {cert_cn_file}")
        my_log.debug("cellular test successful")
        return 0
    def extract_rt_cnt(self):
        process_rt_dict = {}
        cmd = ['adb', 'shell', 'cat /data/run_info/process_monintor.txt']
        with subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True) as proc:
            lines = proc.stdout.readlines()
            
            for line in lines[1:]:
                line = line.strip()
                if not line:
                    continue
                columns = line.split()
                if len(columns) >= 2:
                    process_name = columns[0]
                    rt_cnt = columns[1] 
                    process_rt_dict[process_name] = rt_cnt  
        
        return process_rt_dict

    def reboot_test(self):
        
        my_log.debug("start reboot start")
        
        tm = 0
        if self.adb_connect() == -1:
            my_log.error("Adb connection failed")
            return -1
        adb_root_counter = 0
        
        while not self.exit_event.is_set():
            if os.system("adb root") != 0:
                self.usb_reset()
                adb_root_counter += 1
            if adb_root_counter >= 4:
                
                my_log.error("TSU has been shut down")
                adb_root_counter = 0
                # return -1
            time.sleep(2)
            tm += 1
            if tm % 149 == 0:
                process_rt_data  = self.extract_rt_cnt()
                for process, rt_cnt in process_rt_data.items():
                    if int(rt_cnt) > 1:
                        my_log.error(f"{process}: {rt_cnt}")



    def reboot_test_task_start(self):
        power_ctrl.cleanup()
        task = threading.Thread(target=self.reboot_test)
        task.start()

    def all_test(self):
        self.process_test()
        self.reflash_test()
        self.cellular_test()
    

mode_test = mode_test_t()