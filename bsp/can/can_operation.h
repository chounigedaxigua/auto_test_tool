
extern "C"
{
#include "controlcan.h"
}

#include <iostream>
#include <thread>
#define CAN1    0
#define CAN2    1

typedef enum 
{
    CAN_STATUS_OK = 0,
    CAN_STATUS_FILE
}CAN_STATUS;

class can_device
{
private:
    int number;
public:
    PVCI_INIT_CONFIG config;
    PVCI_CAN_OBJ data;
    can_device();
    can_device(PVCI_INIT_CONFIG c) : config(c)
    {
        std::cout<< "config init......"<<std::endl;
    }
    int init(int chanl,PVCI_INIT_CONFIG pInitConfig);
    int start(int chanl,PVCI_INIT_CONFIG pInitConfig);
    int send(int chanl,PVCI_CAN_OBJ data);
    int device_open(DWORD DeviceType,DWORD DeviceInd,DWORD Reserved);
    void* receive_func(void* param);  //接收线程。
};

void find_can_device();
CAN_STATUS can_send_message_to_tsu();
void tsu_program_mode(int tx_flag);