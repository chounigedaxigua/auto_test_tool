#include <stdio.h>
#include <stdlib.h>
#include <string.h>
int get_bus()
{
    FILE *f = NULL;
    char out[32] = {0};
    int bus = -1;
    f = popen("lsusb|grep Quectel|awk -F' ' '{print $2}'","r");
    if(fgets(out,32,f) > (char*)0)
    system("lsusb|grep Quectel");
    bus = atoi(out);
    pclose(f);
    return bus;
}
int get_port()
{
    FILE *f = NULL;
    char out[32] = {0};
    int port = -1;
    f = popen("lsusb -t|grep usbfs|awk -F' ' '{print $3}'","r");
    if(fgets(out,32,f) > (char*)0)
    system("lsusb|grep Quectel");
    
    for(int i = 0;i<32;++i)
    {
        if(out[i] < '0' || out[i] > '9')
        {
            out[i] = 0;
        }
    }
    printf("%s\n",out);
    port = atoi(out);
    pclose(f);
    return port;
}
// sudo uhubctl -l 1 -p 2 -a 0
int main(int argc, const char* argv[])
{
    char cmd[128] = {0};
    if(argc < 2)
    {
        perror("参数数量太少\n");
        return -1;
    }
    int bus = get_bus();
    int port = get_port();
    if(bus == 0)
    {
        perror("not connect tsu\n");
        return -1;
    }
    if(bus > 0 && port > 0)
    {
        sprintf(cmd,"sudo uhubctl -l %d -p %d -a %d",bus,port,atoi(argv[1]));
        printf("%s\n",cmd);
        system(cmd);
        return 0;
    }
    if(port == 0)
    {
        sprintf(cmd,"sudo uhubctl -l %d -p 1 -a %d",bus,atoi(argv[1]));
        system(cmd);
        memset(cmd,0,sizeof(cmd));
        sprintf(cmd,"sudo uhubctl -l %d -p 2 -a %d",bus,atoi(argv[1]));
        system(cmd);
        return 0;
    }
    // printf("bus = %d, port = %d\n",get_bus(),get_port());

    
    return 0;
}