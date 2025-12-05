#include "xlxs_opt.h"
#include "gpio.h"
#define CONFIG_XLXS_PATH "/home/cx/version_base_test/conf/config.xlsx"

struct pwr_command {
    static inline const std::string BAT = "bat";
    static inline const std::string IG = "ig";
    static inline const std::string ACC = "acc";
    static inline const std::string V_BUS = "v_bus";
    
    static inline const std::string LPM = "lpm";
};

struct pwr_target {
    static inline const std::string ON = "ON";
    static inline const std::string OFF = "OFF";
};

std::string get_str_from_xlxs (int row, config_col col)
{
    std::string cell_str;
    try {
        OpenXLSX::XLDocument doc;
        doc.open(CONFIG_XLXS_PATH);
        
        auto wks = doc.workbook().worksheet("Sheet1");
        
        auto cell = wks.cell((int)row, (int)col);

        cell_str = cell.value().get<std::string>();
        // switch (cell.value().type()) {
        //     case XLValueType::Empty:
        //         break;
        //     case XLValueType::Boolean:
        //         break;
        //     case XLValueType::Integer:
        //         cell_int_value = cell.value();
        //         cell_str = to_string(cell_int_value);
        //         break;
        //     case XLValueType::Float:
        //         cell_float_value = cell.value();
        //         cell_str = to_string(cell_int_value);
        //         break;
        //     case XLValueType::String:
        //         break;
        //     default:
        //         break;
        // }
        doc.close();
    }
    catch (const std::exception& e) {
        std::cerr << "Error: " << e.what() << std::endl;
    }
    return cell_str;
}

int get_int_from_xlxs (int row, config_col col) {
    int cell_int = 0;
    try {
        OpenXLSX::XLDocument doc;
        doc.open(CONFIG_XLXS_PATH);
        
        auto wks = doc.workbook().worksheet("Sheet1");
        
        auto cell = wks.cell((int)row, (int)col);
        if (!cell.empty()) 
        {
            cell_int = cell.value();
        } else {
            cell_int = 0;
        }
        
        doc.close();
    }
    catch (const std::exception& e) {
        std::cerr << "Error: " << e.what() << std::endl;
    }
    return cell_int;
}
gl_status_t lpm_judgment(int row)
{
    int time_out = get_int_from_xlxs(3, config_col::TIMEOUT_COL);
    // while () {
        
    // } 
    std::cout << time_out << std::endl;


    return STATE_OK;
}
gl_status_t pwr_gpio_ctr(std::string gpio, std::string sta, int row)
{
    gl_status_t status = STATE_FAIL;
    int gpio_sta = sta.find("ON") != std::string::npos ? GPIO_OFF : GPIO_ON;//如果OFF，继电器置位，断开电源
    if (gpio.find(pwr_command::BAT) != std::string::npos) {
        gpio_write(GPIO_B, gpio_sta);
    }
    if (gpio.find(pwr_command::IG) != std::string::npos) {
        gpio_write(GPIO_IG, gpio_sta);
    }
    if (gpio.find(pwr_command::ACC) != std::string::npos) {
        gpio_write(GPIO_ACC, gpio_sta);
    }
    if (gpio.find(pwr_command::V_BUS) != std::string::npos) {
        gpio_write(GPIO_USB_POWER, gpio_sta);
    }
    if (gpio.find(pwr_command::LPM) != std::string::npos) {
        /*低功耗判断，在超时时间之内进入低功耗模式*/
        lpm_judgment(row);
    }
    return status;
}

gl_status_t power_callback(std::string& ct, int row)
{
    std::string gpio_name = get_str_from_xlxs(row, config_col::COMMAND_COL);
    std::string target = get_str_from_xlxs(row, config_col::TARGET_COL);
    std::cout << "gpio_name: " << gpio_name << " target: " << target <<std::endl;
    // if(gpio_name.find(pwr_command::BAT) != std::string::npos)
    // {
        
        pwr_gpio_ctr(gpio_name, target, row);
    // }
    return STATE_OK;
}

gl_status_t command_callback(std::string& ct, int row)
{
    std::string cmd = get_str_from_xlxs(row, config_col::COMMAND_COL);
    std::string expected = get_str_from_xlxs(row, config_col::TARGET_COL);
    std::string get_str;
    try {
        std::unique_ptr<FILE, decltype(&pclose)> pipe(
            popen(cmd.c_str(), "r"),
            &pclose
        );

        if (!pipe) {
            throw std::runtime_error("popen failed");
        }

        char out_str[256] = {0};
        if (fgets(out_str, sizeof(out_str), pipe.get()) != nullptr) {
            out_str[strcspn(out_str, "\n")] = '\0';
            get_str = out_str;
        } else {
            throw std::runtime_error("shell returns empty result");
        }
        if (!expected.empty()) {
            if (get_str.find(expected) != std::string::npos) {
                std::cout << "return string: " << get_str<<std::endl;
                std::cout << "exptcted: " << expected << std::endl;
                return STATE_OK;
            }
            else {
                return STATE_FAIL;
            }
        }
            
        } catch (const std::exception& e) {
            std::cout << (std::string("Instruction execution failed: ") + e.what()) << std::endl;
            return STATE_FAIL;
    }
    return STATE_OK;
}

gl_status_t flow_execute() {
    int row = 2;
                           int error_cnt = 0;
    std::string command_type;
    for (; row<10000; ++row)
    {
        command_type = get_str_from_xlxs(row, config_col::COMMAND_TYPE_COL);
        if (command_type.empty()) {
            ++error_cnt;
            if (error_cnt >= 10) {  //连续十行为空，退出测试
                break;
            }
            continue;
        }
        if(command_type.find("power") != std::string::npos)
        {
            power_callback(command_type, row);
        }
        if(command_type.find("command") != std::string::npos)
        {
            command_callback(command_type, row);
        }
        // std::cout << command_type << std::endl;
        sleep(1);
    }
    return STATE_OK;
}

void ReadWithOpenXLSX() {
    flow_execute();
}