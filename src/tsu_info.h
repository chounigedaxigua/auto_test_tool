#pragma once
#include "stdio.h"
#include "common.h"
#include <string>
#include <iostream>
#include <vector>

typedef enum
{
    SOC_VER,
    MCU_VER,
    TSU_VIN,
    TSU_CAR_NAME,
    TSU_ICCID,
    TSU_IMEI,
    TSU_IMSI,
    TSU_PART_NUMBER,
    TSU_INFO_TYPE_MAX
}TSU_INFO_TYPE;

class tsu_info_entry
{
private:
    // std::fstream fp;
    FILE *fp;
    // std::string data;
    std::string  info_get_cmd;
    
public:
    std::string name; 
    std::string data;
    tsu_info_entry() = default;
    tsu_info_entry(std::string i,std::string n) : info_get_cmd(i),name(n){}
    // ~tsu_info_entry() { if (fp.is_open()) fp.close()}
    int info_get();
    void data_printf() {std::cout <<name << " = "<< data << std::endl;}
};
int tsu_info_entry_init();
int get_tsu_info();