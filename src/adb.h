#ifndef ADB_H_
#define ADB_H_
#include "power_manage.h"
// #include <string.h>
// #include <stdio.h>
// #include <stdlib.h>
extern "C"
{
#include "common.h"
}

#define ADB_CMD_LENGTH 512
#define ADB_CMD_OUT_LENGTH 512

class adb_dev
{
public:
    adb_dev();
    ~adb_dev()
    {
        power_gpio_set(1,1,1,1);
    }
    bool is_connect;
    // bool adb_is_connect();
    int connect(int timeout);
    int edl_enter();
    int edl_out();
};
// typedef struct _process_info
// {
//     char process_name[64][64];
//     int err_process_num;
// }process_info_t;
// typedef enum{
//     PROCESS_QUERY = 1,
//     CALL_NUMBRE
// }adb_operation_t;

// extern process_info_t process_info;


gl_status_t adb_shell_cmd(char * adb_cmd,adb_operation_t adb_operation);
int edl_enter();
int edl_out();
#endif