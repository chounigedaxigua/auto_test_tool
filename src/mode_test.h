#pragma once

#include "common.h"
#include "gpio.h"
#include <iostream>

gl_status_t timing_test();

gl_status_t low_power_test();

gl_status_t reflash_test();

gl_status_t daq_test();

gl_status_t ecall_test();

gl_status_t cellular_test();