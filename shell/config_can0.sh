#!/usr/bin/expect

set timeout -1
spawn sudo ip link set can0 up type can bitrate 125000
expect "xhh:" {send "1\n"}
sleep 1
spawn sudo ifconfig can0 txqueuelen 65536
expect "xhh:" {send "1\n"}

expect eof
