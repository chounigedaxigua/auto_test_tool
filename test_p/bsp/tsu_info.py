from bsp.log import my_log
import os
class tsu_info_type:
    SOC_VER = 0
    MCU_VER = 1
    TSU_CAR_NAME = 2
    TSU_ICCID = 3
    TSU_IMEI = 4
    TSU_IMSI = 5

    TSU_INFO_TYPE_MAX = 6

class tsu_info_entry:
    def __init__(self,cn,cd):
        self.cmd_name = cn
        self.cmd = cd
        
class tsu_info_t:
    def __init__(self):
        self.info_list = []
        self.soc_ver = tsu_info_entry("SOC_VER","adb shell \"cat /etc/cx_version\" |grep version|awk -F'=' '{print $2}' ")
        self.mcu_ver = tsu_info_entry("MCU_VER","adb shell \"cat /data/run_info/mcu_ver.txt\"| awk -F' : ' '{print $2}'")
        self.tsu_car_name = tsu_info_entry("CAR_NAME","adb shell \" cat /data/run_info/car_name.txt \" ")
        self.tsu_iccid = tsu_info_entry("ICCID","adb shell \" cat /data/run_info/iccid.txt \" ")
        self.tsu_imei = tsu_info_entry("IMEI","adb shell \" cat /data/run_info/imei.txt \" ")
        self.tsu_imsi = tsu_info_entry("IMSI","adb shell \" cat /data/run_info/imsi.txt \" ")
        self.tsu_part_num = tsu_info_entry("TSU_PART_NUM","adb shell \" cat /usrdata/conf/tsu_part_num.txt \" ")
        self.ecall_version = tsu_info_entry('ECALL_VERSION','adb shell "cat /etc/ecall_version"')
    def get_soc_ver(self):
        _soc_ver =  os.popen(self.soc_ver.cmd).read()
        return str(self.soc_ver.cmd_name) + " = " + str(_soc_ver)
    def get_mcu_ver(self):
        _mcu_ver = os.popen(self.mcu_ver.cmd).read()
        return str(self.mcu_ver.cmd_name) + " = " + str(_mcu_ver)
    def get_car_name(self):
        _tsu_car_name = os.popen(self.tsu_car_name.cmd).read()
        return str(self.tsu_car_name.cmd_name) + " = " + str(_tsu_car_name)

    def get_tsu_info(self):
        
        _soc_ver = os.popen(self.soc_ver.cmd).read()
        # my_log.info((str(self.soc_ver.cmd_name) + " = " + str(_soc_ver)).strip('\n'))
        self.info_list.append((str(self.soc_ver.cmd_name) + " = " + str(_soc_ver)).strip('\n'))

        _mcu_ver = os.popen(self.mcu_ver.cmd).read()
        # my_log.info((str(self.mcu_ver.cmd_name) + " = " + str(_mcu_ver)).strip('\n'))
        self.info_list.append((str(self.mcu_ver.cmd_name) + " = " + str(_mcu_ver)).strip('\n'))

        _tsu_car_name = os.popen(self.tsu_car_name.cmd).read()
        # my_log.info(str(self.tsu_car_name.cmd_name) + " = " + str(_tsu_car_name))
        self.info_list.append(str(self.tsu_car_name.cmd_name) + " = " + str(_tsu_car_name))

        _tsu_iccid = os.popen(self.tsu_iccid.cmd).read()
        # my_log.info(str(self.tsu_iccid.cmd_name) + " = " + str(_tsu_iccid))
        self.info_list.append(str(self.tsu_iccid.cmd_name) + " = " + str(_tsu_iccid))

        _tsu_imei = os.popen(self.tsu_imei.cmd).read()
        # my_log.info(str(self.tsu_imei.cmd_name) + " = " + str(_tsu_imei))
        self.info_list.append(str(self.tsu_imei.cmd_name) + " = " + str(_tsu_imei))

        _tsu_part_num = os.popen(self.tsu_part_num.cmd).read()
        # my_log.info((str(self.tsu_part_num.cmd_name) + " = " + str(_tsu_part_num)).strip('\n'))
        self.info_list.append((str(self.tsu_part_num.cmd_name) + " = " + str(_tsu_part_num)).strip('\n'))

        _ecall_version = os.popen(self.ecall_version.cmd).read()
        # my_log.info(str(self.ecall_version.cmd_name) + " = " + str(_ecall_version))
        self.info_list.append(str(self.ecall_version.cmd_name) + " = " + str(_ecall_version))


tsu_info = tsu_info_t()
