import time as t
from smbus2 import SMBus
import sys
# import smbus
import time
import threading
# AVG_CURENT = 100   #滑动窗口输出值

DEVICE_BUS  = 1
DEVICE_ADDR = 0x10
class pwr_status:
    pwr_high = 0xFF           # 打开继电器的值
    pwr_low = 0x00          # 关闭继电器的值

class pwr_out:
    on = pwr_status.pwr_low
    off = pwr_status.pwr_high

RELAY1 = 0x01       # 继电器1寄存器地址
RELAY2 = 0x02       # 继电器2寄存器地址
RELAY3 = 0x03       # 继电器3寄存器地址
RELAY4 = 0x04       # 继电器4寄存器地址

BAT_REG = RELAY1
IG_REG  = RELAY2
ACC_REG = RELAY3
USB_REG = RELAY4

# Config Register (R/W)
_REG_CONFIG                 = 0x00
# SHUNT VOLTAGE REGISTER (R)
_REG_SHUNTVOLTAGE           = 0x01

# BUS VOLTAGE REGISTER (R)
_REG_BUSVOLTAGE             = 0x02

# POWER REGISTER (R)
_REG_POWER                  = 0x03

# CURRENT REGISTER (R)
_REG_CURRENT                = 0x04

# CALIBRATION REGISTER (R/W)
_REG_CALIBRATION            = 0x05




class BusVoltageRange:
    """Constants for ``bus_voltage_range``"""
    RANGE_16V               = 0x00      # set bus voltage range to 16V
    RANGE_32V               = 0x01      # set bus voltage range to 32V (default)

class Gain:
    """Constants for ``gain``"""
    DIV_1_40MV              = 0x00      # shunt prog. gain set to  1, 40 mV range
    DIV_2_80MV              = 0x01      # shunt prog. gain set to /2, 80 mV range
    DIV_4_160MV             = 0x02      # shunt prog. gain set to /4, 160 mV range
    DIV_8_320MV             = 0x03      # shunt prog. gain set to /8, 320 mV range

class ADCResolution:
    """Constants for ``bus_adc_resolution`` or ``shunt_adc_resolution``"""
    ADCRES_9BIT_1S          = 0x00      #  9bit,   1 sample,     84us
    ADCRES_10BIT_1S         = 0x01      # 10bit,   1 sample,    148us
    ADCRES_11BIT_1S         = 0x02      # 11 bit,  1 sample,    276us
    ADCRES_12BIT_1S         = 0x03      # 12 bit,  1 sample,    532us
    ADCRES_12BIT_2S         = 0x09      # 12 bit,  2 samples,  1.06ms
    ADCRES_12BIT_4S         = 0x0A      # 12 bit,  4 samples,  2.13ms
    ADCRES_12BIT_8S         = 0x0B      # 12bit,   8 samples,  4.26ms
    ADCRES_12BIT_16S        = 0x0C      # 12bit,  16 samples,  8.51ms
    ADCRES_12BIT_32S        = 0x0D      # 12bit,  32 samples, 17.02ms
    ADCRES_12BIT_64S        = 0x0E      # 12bit,  64 samples, 34.05ms
    ADCRES_12BIT_128S       = 0x0F      # 12bit, 128 samples, 68.10ms

class Mode:
    """Constants for ``mode``"""
    POWERDOW                = 0x00      # power down
    SVOLT_TRIGGERED         = 0x01      # shunt voltage triggered
    BVOLT_TRIGGERED         = 0x02      # bus voltage triggered
    SANDBVOLT_TRIGGERED     = 0x03      # shunt and bus voltage triggered
    ADCOFF                  = 0x04      # ADC off
    SVOLT_CONTINUOUS        = 0x05      # shunt voltage continuous
    BVOLT_CONTINUOUS        = 0x06      # bus voltage continuous
    SANDBVOLT_CONTINUOUS    = 0x07      # shunt and bus voltage continuous

# bus = SMBus(DEVICE_BUS) 
class MovingAverage:
    def __init__(self, move_average_length):
        self.move_average_length = move_average_length  # 滑动窗口长度
        self.index = -1                                 # 当前写入位置
        self.buffer = [0.0] * move_average_length       # 缓冲区
        self.sum = 0.0                                  # 当前缓冲区的总和

    def moving_average(self, xn):
        if self.index == -1:
            # 初始化阶段：将缓冲区全部填充为 xn，并计算初始总和
            for i in range(self.move_average_length):
                self.buffer[i] = xn
            self.sum = xn * self.move_average_length
            self.index = 0
        else:
            # 正常运行阶段：更新缓冲区和总和
            self.sum -= self.buffer[self.index]  # 减去即将被替换的值
            self.buffer[self.index] = xn         # 写入新值
            self.sum += xn                       # 加上新值
            self.index += 1                      # 更新写入位置
            if self.index >= self.move_average_length:
                self.index = 0                   # 环形缓冲区：回到起点

        # 计算平均值
        yn = self.sum / self.move_average_length
        return yn

# 示例用法
if __name__ == "__main__":
    MOVE_AVERAGE_LENGTH = 5
    ma = MovingAverage(MOVE_AVERAGE_LENGTH)

class JDQ:
    def __init__(self, i2c_bus=1, addr=0x10):
        # self.bus = SMBus(i2c_bus)
        self.addr = addr
        self.bus = SMBus(DEVICE_BUS) 
    def __del__(self):
        print("JDQ.__del__")
        self.bus.write_byte_data(0x10, BAT_REG, 0x00)
        self.bus.write_byte_data(0x10, IG_REG, 0x00)
        self.bus.write_byte_data(0x10, ACC_REG, 0x00)
        self.bus.write_byte_data(0x10, USB_REG, 0x00)

    def power_set(self,address,data):
        sta = self.bus.write_byte_data(self.addr, address, data)
        print(f"sta = {sta}")
        if sta == None:
            return 0
        else:
            return -1
        
    def bat_set(self, sta):
        return self.power_set(BAT_REG,sta)

    def ig_set(self, sta):
        return self.power_set(IG_REG,sta)

    def acc_set(self, sta):
        return self.power_set(ACC_REG,sta)

    def usb_set(self, sta):
        return self.power_set(USB_REG,sta)

    def cleanup(self):
        print("JDQ.cleanup")
        self.bus.write_byte_data(0x10, BAT_REG, 0x00)
        self.bus.write_byte_data(0x10, IG_REG, 0x00)
        self.bus.write_byte_data(0x10, ACC_REG, 0x00)
        self.bus.write_byte_data(0x10, USB_REG, 0x00)

    def test(self, sta):
        self.bus.write_byte_data(0x10, BAT_REG, sta)
        self.bus.write_byte_data(0x10, IG_REG, sta)
        self.bus.write_byte_data(0x10, ACC_REG, sta)
        self.bus.write_byte_data(0x10, USB_REG, sta)

class INA219:
    def __init__(self, i2c_bus=1, addr=0x40):
        # self.bus = smbus.SMBus(i2c_bus);
        self.bus = SMBus(i2c_bus) 
        self.addr = addr

        # Set chip to known config values to start
        self._cal_value = 0
        self._current_lsb = 0
        self._power_lsb = 0
        self.cur_curent = 0
        self.avg_curent = 0
        self.set_calibration_32V_2A()
        self.exit_event = threading.Event()
    def read(self,address):
        data = self.bus.read_i2c_block_data(self.addr, address, 2)
        return ((data[0] * 256 ) + data[1])

    def write(self,address,data):
        temp = [0,0]
        temp[1] = data & 0xFF
        temp[0] =(data & 0xFF00) >> 8
        self.bus.write_i2c_block_data(self.addr,address,temp)

    def set_calibration_32V_2A(self):
        """Configures to INA219 to be able to measure up to 32V and 2A of current. Counter
           overflow occurs at 3.2A.
           ..note :: These calculations assume a 0.1 shunt ohm resistor is present
        """
        # By default we use a pretty huge range for the input voltage,
        # which probably isn't the most appropriate choice for system
        # that don't use a lot of power.  But all of the calculations
        # are shown below if you want to change the settings.  You will
        # also need to change any relevant register settings, such as
        # setting the VBUS_MAX to 16V instead of 32V, etc.

        # VBUS_MAX = 32V             (Assumes 32V, can also be set to 16V)
        # VSHUNT_MAX = 0.32          (Assumes Gain 8, 320mV, can also be 0.16, 0.08, 0.04)
        # RSHUNT = 0.1               (Resistor value in ohms)

        # 1. Determine max possible current
        # MaxPossible_I = VSHUNT_MAX / RSHUNT
        # MaxPossible_I = 3.2A

        # 2. Determine max expected current
        # MaxExpected_I = 2.0A

        # 3. Calculate possible range of LSBs (Min = 15-bit, Max = 12-bit)
        # MinimumLSB = MaxExpected_I/32767
        # MinimumLSB = 0.000061              (61uA per bit)
        # MaximumLSB = MaxExpected_I/4096
        # MaximumLSB = 0,000488              (488uA per bit)

        # 4. Choose an LSB between the min and max values
        #    (Preferrably a roundish number close to MinLSB)
        # CurrentLSB = 0.0001 (100uA per bit)
        self._current_lsb = .1  # Current LSB = 100uA per bit

        # 5. Compute the calibration register
        # Cal = trunc (0.04096 / (Current_LSB * RSHUNT))
        # Cal = 4096 (0x1000)

        self._cal_value = 4096

        # 6. Calculate the power LSB
        # PowerLSB = 20 * CurrentLSB
        # PowerLSB = 0.002 (2mW per bit)
        self._power_lsb = .002  # Power LSB = 2mW per bit

        # 7. Compute the maximum current and shunt voltage values before overflow
        #
        # Max_Current = Current_LSB * 32767
        # Max_Current = 3.2767A before overflow
        #
        # If Max_Current > Max_Possible_I then
        #    Max_Current_Before_Overflow = MaxPossible_I
        # Else
        #    Max_Current_Before_Overflow = Max_Current
        # End If
        #
        # Max_ShuntVoltage = Max_Current_Before_Overflow * RSHUNT
        # Max_ShuntVoltage = 0.32V
        #
        # If Max_ShuntVoltage >= VSHUNT_MAX
        #    Max_ShuntVoltage_Before_Overflow = VSHUNT_MAX
        # Else
        #    Max_ShuntVoltage_Before_Overflow = Max_ShuntVoltage
        # End If

        # 8. Compute the Maximum Power
        # MaximumPower = Max_Current_Before_Overflow * VBUS_MAX
        # MaximumPower = 3.2 * 32V
        # MaximumPower = 102.4W

        # Set Calibration register to 'Cal' calculated above
        self.write(_REG_CALIBRATION,self._cal_value)

        # Set Config register to take into account the settings above
        self.bus_voltage_range = BusVoltageRange.RANGE_32V
        self.gain = Gain.DIV_8_320MV
        self.bus_adc_resolution = ADCResolution.ADCRES_12BIT_16S
        self.shunt_adc_resolution = ADCResolution.ADCRES_12BIT_16S
        self.mode = Mode.SANDBVOLT_CONTINUOUS
        self.config = self.bus_voltage_range << 13 | \
                      self.gain << 11 | \
                      self.bus_adc_resolution << 7 | \
                      self.shunt_adc_resolution << 3 | \
                      self.mode
        self.write(_REG_CONFIG,self.config)
        
    def getShuntVoltage_mV(self):
        self.write(_REG_CALIBRATION,self._cal_value)
        value = self.read(_REG_SHUNTVOLTAGE)
        if value > 32767:
            value -= 65535
        return value * 0.01
        
    def getBusVoltage_V(self):  
        self.write(_REG_CALIBRATION,self._cal_value)
        self.read(_REG_BUSVOLTAGE)
        return (self.read(_REG_BUSVOLTAGE) >> 3) * 0.004
        
    def getCurrent_mA(self):
        value = self.read(_REG_CURRENT)
        if value > 32767:
            value -= 65535
        return value * self._current_lsb
        
    def getPower_W(self):
        value = self.read(_REG_POWER)
        if value > 32767:
            value -= 65535
        return value * self._power_lsb    
        
    def current_check_task(self):
        # ina4 = INA219(addr=0x43)
        ma = MovingAverage(10)
        while not self.exit_event.is_set():
            self.cur_curent = self.getCurrent_mA()
            # ret = current4
            self.avg_curent = ma.moving_average(self.cur_curent)
            # print("Current:{:9.4f}ma".format(self.avg_curent))
            time.sleep(1)

power_ctrl = JDQ()
ina219_ch1 = INA219(addr = 0x43)
if __name__=='__main__':

    # ina1 = INA219(addr=0x40)
    # ina2 = INA219(addr=0x41)
    # ina3 = INA219(addr=0x42)
    ina4 = INA219(addr=0x43)
    # print("ina219 test")

    while True:
        # bus_voltage1 = ina1.getBusVoltage_V()             # voltage on V- (load side)
        # shunt_voltage1 = ina1.getShuntVoltage_mV() / 1000 # voltage between V+ and V- across the shunt
        # current1 = ina1.getCurrent_mA()                   # current in mA
        # power1 = ina1.getPower_W()                        # power in watts

        # bus_voltage2 = ina2.getBusVoltage_V()             # voltage on V- (load side)
        # shunt_voltage2 = ina2.getShuntVoltage_mV() / 1000 # voltage between V+ and V- across the shunt
        # current2 = ina2.getCurrent_mA()                   # current in mA
        # power2 = ina2.getPower_W()                        # power in watts

        # bus_voltage3 = ina3.getBusVoltage_V()             # voltage on V- (load side)
        # shunt_voltage3 = ina3.getShuntVoltage_mV() / 1000 # voltage between V+ and V- across the shunt
        # current3 = ina3.getCurrent_mA()                   # current in mA
        # power3 = ina3.getPower_W()                        # power in watts

        # bus_voltage4 = ina4.getBusVoltage_V()              # voltage on V- (load side)
        # shunt_voltage4 = ina4.getShuntVoltage_mV() / 1000 # voltage between V+ and V- across the shunt
        current4 = ina4.getCurrent_mA()                   # current in mA
        # power4 = ina4.getPower_W()                        # power in watts
        
        # INA219 measure bus voltage on the load side. So PSU voltage = bus_voltage + shunt_voltage
        # print("PSU Voltage:{:6.3f}V    Shunt Voltage:{:9.6f}V    Load Voltage:{:6.3f}V    Power:{:9.6f}W    Current:{:9.6f}A".format((bus_voltage1 + shunt_voltage1),(shunt_voltage1),(bus_voltage1),(power1),(current1/1000)))
        # print("PSU Voltage:{:6.3f}V    Shunt Voltage:{:9.6f}V    Load Voltage:{:6.3f}V    Power:{:9.6f}W    Current:{:9.6f}A".format((bus_voltage2 + shunt_voltage2),(shunt_voltage2),(bus_voltage2),(power2),(current2/1000)))
        # print("PSU Voltage:{:6.3f}V    Shunt Voltage:{:9.6f}V    Load Voltage:{:6.3f}V    Power:{:9.6f}W    Current:{:9.6f}A".format((bus_voltage3 + shunt_voltage3),(shunt_voltage3),(bus_voltage3),(power3),(current3/1000)))
        # print("PSU Voltage:{:6.3f}V    Shunt Voltage:{:9.6f}V    Load Voltage:{:6.3f}V    Power:{:9.6f}W    Current:{:4f}ma".format((bus_voltage4 + shunt_voltage4),(shunt_voltage4),(bus_voltage4),(power4),(current4)))
        print("Current:{:9.4f}ma".format(current4))
        print("") 
        
        time.sleep(1)

