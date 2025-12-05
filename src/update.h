#pragma once

#include <string>
#include <iostream>
#include <unistd.h> 
enum device_t{MCU,MODE};

#define BWT_SVN_PATH "https://192.168.52.21/svn/Global5.0/9.baseline/MCU/03.For3BWT/For "
#define DPA_SVN_PATH "https://192.168.52.21/svn/Global5.0/9.baseline/MCU/13.For3DPA/For "
#define A0V_SVN_PATH "https://192.168.52.21/svn/Global27CRV/9.baseline/MCU/03.For3A0V/For "

#define BWT_HEADER "G26V0"
#define DPA_HEADER "G27V0"
#define A0V_HEADER "E27V0"

// #define  "~/DailyTest/3A0V/EEU"
class update_t{
public:
    virtual ~update_t();
    virtual int download_update_package() = 0;
    virtual int update() = 0;
    virtual int get_ver_log_file_name() = 0;
    
    virtual int get_cur_version() = 0;
    int is_update_success;
    std::string pre_version;
    std::string cur_version;
    std::string ver_log_file_name;
    std::string remote_address;
    std::string local_address;
    
};

class mcu_update_t:public update_t{
public:
    std::string mcu_svn_path;
    std::string contry;
    std::string version_header;
    virtual int download_update_package();
    virtual int update();
    virtual int get_ver_log_file_name();
    virtual int get_cur_version();
    ~mcu_update_t(){};
    mcu_update_t();
    int get_update_package_name();
    int clear_mcu_ver_file();
    int download_mcu_new_ver();
    int push_bin_update();
    std::string check_mcu_new_ver();
    int update_sertification();
    std::string update_package_name;
private:
    
    
};

class soc_update_t:public update_t{
public:
    std::string update_package_path;
    std::string car_type;
    std::string soc_hard_type;
    std::string contry;
    virtual int download_update_package();
    virtual int update();
    virtual int get_ver_log_file_name();
    virtual int get_cur_version();
    soc_update_t(){};
    ~soc_update_t(){};
    std::string get_file_name(const std::string& str);
    int get_update_package_path();
    
};
int arg_init(int argc, const char* argv[],soc_update_t *soc,mcu_update_t *mcu);
