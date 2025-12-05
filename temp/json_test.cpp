#include <iostream>
#include <fstream>
#include "../tools/json.hpp"
// for convenience
using json = nlohmann::json;

// #define WRITE_FILE 
#define READ_FILE

#define CONFIG_FILE_PASTH "config.json"

/*选择在树莓派执行还是在tsu执行*/
#define RUN_IN_TSU   "tsu"
#define RUN_IN_RASPBERRY "raspberry"
#ifdef WRITE_FILE
int main() {
    json config;
    json mcu;
    json soc;
    mcu["country"] = "JP";
    mcu["project"] = "3BWT";
    soc["chip"] = "EEU";
    soc["country"] = "EU";
    config["mcu_update"] = mcu;
    config["soc_update"] = soc;

    std::ofstream o("config.json");
    if (o.is_open()) {
        o << config.dump(4);  // dump(4) 表示格式化输出，缩进4个空格
        o.close();
        std::cout << "配置文件已写入: config.json" << std::endl;
    } else {
        std::cerr << "无法打开文件进行写入！" << std::endl;
    }

    return 0;
}
#endif

#ifdef READ_FILE
using json = nlohmann::json;
enum class test_case_type { GET, SET, CHECK, UPDATE , LPM, UNKNOW};
enum class test_result_t { PASS, FAIL, ERROR };

struct _GetCase
{

};

struct _SetCase
{

};
struct _GetCase
{

};

struct _CheckCase
{

};

struct UpdateCase
{
    std::string case_type;
    std::string case_name;
    bool is_update;
    std::string project_name;
    std::string chip;
    std::string country;
};
struct LPMCase
{

};


struct TestCase
{
    std::string case_type;
    std::string case_name;
    std::string where_to_run;
    std::string command;
    std::string expected;
    int timeout_s;
};

test_result_t copy_test_data_get(TestCase &test_case,std::string& test_title) {
    std::ifstream i(CONFIG_FILE_PASTH);
    if (!i.is_open()) {
        std::cerr << "无法打开配置文件 config.json" << std::endl;
        return test_result_t::FAIL;
    }

    try {
        json config;
        i >> config;  // file >> json_var是 nlohmann/json库重载的特殊用法，不是C++的原生用法

        test_case.case_type = config[test_title]["case_type"];
        test_case.case_name = config[test_title]["case_name"];
        test_case.where_to_run = config[test_title]["where_to_run"];
        test_case.command = config[test_title]["command"];
        // test_case.expected = config[test_title]["expected"];
        test_case.timeout_s = config[test_title]["timeout"];
    } catch (const std::exception& e) {
        std::cerr << "JSON 解析错误: " << e.what() << std::endl;
    }
    return test_result_t::PASS;
} 
test_result_t copy_test_data_check(TestCase &test_case,std::string& test_title) {
    std::ifstream i(CONFIG_FILE_PASTH);
    if (!i.is_open()) {
        std::cerr << "无法打开配置文件 config.json" << std::endl;
        return test_result_t::FAIL;
    }

    try {
        json config;
        i >> config;  // file >> json_var是 nlohmann/json库重载的特殊用法，不是C++的原生用法

        test_case.case_type = config[test_title]["case_type"];
        test_case.case_name = config[test_title]["case_name"];
        test_case.where_to_run = config[test_title]["where_to_run"];
        test_case.command = config[test_title]["command"];
        test_case.expected = config[test_title]["expected"];
        test_case.timeout_s = config[test_title]["timeout"];
    } catch (const std::exception& e) {
        std::cerr << "JSON 解析错误: " << e.what() << std::endl;
    }
    return test_result_t::PASS;
} 

void print_test_case(const TestCase& tc) {
    std::cout << "Type: " << tc.case_type 
              << ", Name: " << tc.case_name 
              << ", Command: " << tc.command 
              << ", Expected: " << tc.expected 
              << ", Timeout: " << tc.timeout_s << "ms" << std::endl;
}

test_case_type get_case_type(TestCase& tc) {
    if (tc.case_type == "get") {
        return test_case_type::GET;
    }
    else if (tc.case_type == "set") {
        return test_case_type::SET;
    }
    else if (tc.case_type == "check") {
        return test_case_type::CHECK;
    }
    else if (tc.case_type == "update") {
        return test_case_type::UPDATE;
    }
    else if (tc.case_type == "lpm") {
        return test_case_type::LPM;
    }
    else {}

    return test_case_type::UNKNOW;
}
std::string extract_test_case_type(const std::string& name) {
    std::string type;
    try {
        std::ifstream file(CONFIG_FILE_PASTH);
        if (!file.is_open()) {
            std::cerr << "Error: Cannot open JSON file: " << CONFIG_FILE_PASTH << std::endl;
            return type;
        }

        json root;
        file >> root;

        type = root[name]["case_type"];

    } catch (const json::exception& e) {
        std::cerr << "JSON 解析错误: " << e.what() << std::endl;
    } catch (const std::exception& e) {
        std::cerr << "其他错误: " << e.what() << std::endl;
    }

    return type;
}
/*读取json 文件*/
std::vector<std::string> extract_test_case_names(const std::string& json_path) {
    std::vector<std::string> names;
    try {
        std::ifstream file(json_path);
        if (!file.is_open()) {
            std::cerr << "Error: Cannot open JSON file: " << json_path << std::endl;
            return names;
        }

        json root;
        file >> root;

        for (auto& [key, value] : root.items()) {
            if (key.rfind("test_case_", 0) == 0) {
                names.push_back(key);
            }
        }

    } catch (const json::exception& e) {
        std::cerr << "JSON 解析错误: " << e.what() << std::endl;
    } catch (const std::exception& e) {
        std::cerr << "其他错误: " << e.what() << std::endl;
    }

    return names;
}

//case_type : get/set/check/update
class CaseGenerator
{
public:
    CaseGenerator(){};
    CaseGenerator(std::string& test_title, std::string& test_type);
    virtual ~CaseGenerator(){};
    test_result_t get_test_data(std::string test_title) { return test_result_t::PASS; }; 
    test_result_t run_test_case();
    test_result_t check_expected(TestCase& test_case) { return test_result_t::PASS; };

    test_result_t get_task_work();
    test_result_t check_task_work();
    test_result_t set_task_work();
    test_result_t update_task_work();
    test_result_t lpm_task_work();
    test_result_t unknow_task_work(){ return test_result_t::FAIL; };
private:
    TestCase test_case;
};

CaseGenerator::CaseGenerator(std::string& test_title, std::string& test_type) {
    if (test_type == "get")
    {
        copy_test_data_get(test_case,test_title);
    }
    else if (test_type == "set")
    {
        copy_test_data_check(test_case,test_title);
    }
    else if (test_type == "check")
    {
        copy_test_data_check(test_case,test_title);
    }
    else if (test_type == "update")
    {
        
    }
    else if (test_type == "lpm")
    {
        
    }
    else {

    }
    
    // print_test_case(test_case);
}

// test_result_t CaseGenerator::get_test_data(std::string test_title) {
//     // return copy_test_data(test_case,test_title);
// }

test_result_t CaseGenerator::run_test_case() {

    test_case_type type = get_case_type(test_case);
    // std::cout << (int)type << std::endl;
    switch (type)
    {
    case test_case_type::GET:
        return get_task_work();
      break;
    case test_case_type::CHECK:
        return check_task_work();
        break;
    case test_case_type::SET:
        return set_task_work();
        break;
    case test_case_type::UPDATE:
        return update_task_work();
        break;
    default:
        return unknow_task_work();
      break;
    }
    return test_result_t::PASS;
}

test_result_t CaseGenerator::get_task_work() {
    std::string get_str;
    std::string cmd ;
    /*先确保adb成功连接*/
    if (test_case.where_to_run.find(RUN_IN_TSU) != std::string::npos)
    {
        
        cmd = "adb shell " + test_case.command;
    }
    else {
        cmd = test_case.command;
    }
    
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

        std::cout << get_str << std::endl;
        } catch (const std::exception& e) {
            std::cout << (std::string("Instruction execution failed: ") + e.what()) << std::endl;
            return test_result_t::ERROR;
    }

    return test_result_t::PASS;
}

test_result_t CaseGenerator::check_task_work() {
    std::string get_str;
    std::string cmd ;
    if (test_case.where_to_run.find(RUN_IN_TSU) != std::string::npos)
    {
        cmd = "adb shell " + test_case.command;
    }
    else {
        cmd = test_case.command;
    }
    
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

        if (get_str.find(test_case.expected) != std::string::npos) {
            std::cout << "return string: " << get_str<<std::endl;
            std::cout << "exptcted: " << test_case.expected << std::endl;
            return test_result_t::PASS;
        }
        } catch (const std::exception& e) {
            std::cout << (std::string("Instruction execution failed: ") + e.what()) << std::endl;
            return test_result_t::ERROR;
    }

    return test_result_t::PASS;
}

test_result_t CaseGenerator::set_task_work() {
    return test_result_t::PASS;
}

test_result_t CaseGenerator::update_task_work() {
    return test_result_t::PASS;
}
test_result_t CaseGenerator::lpm_task_work() {
    
  return test_result_t::PASS;
}
test_result_t command_run_handel() {
    test_result_t status;
    std::string type;
    std::vector<std::string>names =  extract_test_case_names(CONFIG_FILE_PASTH);
    for (auto it = names.begin();it != names.end();++it)
    {
      /**/
      type = extract_test_case_type(*it);
      CaseGenerator *test_entry = new CaseGenerator(*it,type);
      status = test_entry->run_test_case();
      delete test_entry;
    }
    return status;
}

int main() {

    command_run_handel();
    return 0;
}
#endif