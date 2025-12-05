#ifndef COMMON_H_
#define COMMON_H_

#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <string>
#include <unistd.h>
#include <stdarg.h>
#include <pthread.h>
#include <iostream>
#include <fstream>
#define info_printf(msg,arg ...)  test_info_fprintf((char*)msg,## arg)
enum gl_status_t
{
    STATE_OK,
    STATE_FAIL,
    NO_STARTUP,
    SLEEP_FAIL,
    WEAKUP_FAIL,
    KEEP_ERR,
    CURRENT_LOW,
    TIMEOUT_ERR,
    SINGLE_ERR,
    ADB_CON_ERR,
    PROCESS_QUERY_ERR,
    DIAL_ERR
} ;

typedef struct _test_info_t
{
    int status;
    float cur_val;
    float avg_val;
    // int timer;
    // int power_range_status;
    int time_limit; // 时间限制
    int retry_flag;
    int curent_order;
    int succes_flag;
} test_info_t;
typedef struct _process_info
{
    char process_name[64][64];
    int err_process_num;
} process_info_t;

typedef enum
{
    PROCESS_QUERY = 1,
    CALL_NUMBRE
} adb_operation_t;

extern process_info_t process_info;

extern test_info_t test_info;

void log_clear();
int test_info_fprintf(char *msg,...);
#endif