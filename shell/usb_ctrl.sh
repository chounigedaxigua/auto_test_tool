#!/usr/bin/expect
set timeout -1
spawn ./usb_opeation [lindex $argv 0]
expect "*cx:" {send "1\n"}
expect eof
