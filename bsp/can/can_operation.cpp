//样例只是提供一个简单的调用so库的方法供参考，程序接收，与发送函数设置在两个线程中，并且线程没有同步。
//现实中客户编程中，发送与接收函数不能同时调用（不支持多线程），如果在多线程中，一定需要互锁。需要客户自行完善代码。

#include <stdio.h>
#include <sys/types.h>
#include <sys/stat.h>
#include <fcntl.h>
#include <pthread.h>

#include <ctime>
#include <cstdlib>
#include "unistd.h"
#include "can_operation.h"

VCI_BOARD_INFO pInfo;//用来获取设备信息。
int count=0;//数据列表中，用来存储列表序号。
VCI_BOARD_INFO pInfo1 [50];
int num=0;
can_device::can_device()
{

}
int can_device::send(int chanl,PVCI_CAN_OBJ data)
{
	
	if(VCI_Transmit(VCI_USBCAN2, 0, chanl, data, 1) == 1)
	{
		// printf("Index:%04d  ",count);++count;
		// printf("CAN%d TX ID:0x%08X",chanl+1,data->ID);
		// if(data->ExternFlag==0) printf(" Standard ");
		// if(data->ExternFlag==1) printf(" Extend   ");
		// if(data->RemoteFlag==0) printf(" Data   ");
		// if(data->RemoteFlag==1) printf(" Remote ");
		// printf("DLC:0x%02X",data->DataLen);
		// printf(" data:0x");
 
		// for(int i=0;i<data->DataLen;i++)
		// {
		// 	printf(" %02X",data->Data[i]);
		// }

		// printf("\n");
		// data->ID+=1;
		return 0;
	}
	return -1;
}
void* _receive_func(void* param)  //接收线程。
{
	int reclen=0;
	VCI_CAN_OBJ rec[3000];//接收缓存，设为3000为佳。
	int i,j;
	
	int *run=(int*)param;//线程启动，退出控制。
    int ind=0;
	
	while((*run)&0x0f)
	{
		if((reclen=VCI_Receive(VCI_USBCAN2,0,ind,rec,3000,100))>0)//调用接收函数，如果有数据，进行数据处理显示。
		{
			for(j=0;j<reclen;j++)
			{
				printf("Index:%04d  ",count);count++;//序号递增
				printf("CAN%d RX ID:0x%08X", ind+1, rec[j].ID);//ID
				if(rec[j].ExternFlag==0) printf(" Standard ");//帧格式：标准帧
				if(rec[j].ExternFlag==1) printf(" Extend   ");//帧格式：扩展帧
				if(rec[j].RemoteFlag==0) printf(" Data   ");//帧类型：数据帧
				if(rec[j].RemoteFlag==1) printf(" Remote ");//帧类型：远程帧
				printf("DLC:0x%02X",rec[j].DataLen);//帧长度
				printf(" data:0x");	//数据
				for(i = 0; i < rec[j].DataLen; i++)
				{
					printf(" %02X", rec[j].Data[i]);
				}
				printf(" TimeStamp:0x%08X",rec[j].TimeStamp);//时间标识。
				printf("\n");
			}
		}
		ind=!ind;//变换通道号，以便下次读取另一通道，交替读取。		
	}
	printf("run thread exit\n");//退出接收线程	
	pthread_exit(0);
}
void* can_device::receive_func(void* param)  //接收线程。
{
	int reclen=0;
	VCI_CAN_OBJ rec[3000];//接收缓存，设为3000为佳。
	int i,j;
	
	int *run=(int*)param;//线程启动，退出控制。
    int ind=0;
	
	while((*run)&0x0f)
	{
		if((reclen=VCI_Receive(VCI_USBCAN2,0,ind,rec,3000,100))>0)//调用接收函数，如果有数据，进行数据处理显示。
		{
			for(j=0;j<reclen;j++)
			{
				printf("Index:%04d  ",count);count++;//序号递增
				printf("CAN%d RX ID:0x%08X", ind+1, rec[j].ID);//ID
				if(rec[j].ExternFlag==0) printf(" Standard ");//帧格式：标准帧
				if(rec[j].ExternFlag==1) printf(" Extend   ");//帧格式：扩展帧
				if(rec[j].RemoteFlag==0) printf(" Data   ");//帧类型：数据帧
				if(rec[j].RemoteFlag==1) printf(" Remote ");//帧类型：远程帧
				printf("DLC:0x%02X",rec[j].DataLen);//帧长度
				printf(" data:0x");	//数据
				for(i = 0; i < rec[j].DataLen; i++)
				{
					printf(" %02X", rec[j].Data[i]);
				}
				printf(" TimeStamp:0x%08X",rec[j].TimeStamp);//时间标识。
				printf("\n");
			}
		}
		ind=!ind;//变换通道号，以便下次读取另一通道，交替读取。		
	}
	printf("run thread exit\n");//退出接收线程	
	pthread_exit(0);
}
int can_device::device_open(DWORD DeviceType,DWORD DeviceInd,DWORD Reserved)
{
	int result = VCI_OpenDevice(DeviceType,DeviceInd,Reserved);
	if(result == 1)//打开设备
	{
		printf(">>open deivce success!\n");//打开设备成功
	}else
	{
		printf(">>open deivce error %d!\n",result);
		// exit(1);
	}
	return result;
}
int can_device::init(int chanl,PVCI_INIT_CONFIG pInitConfig)
{
	if(VCI_InitCAN(VCI_USBCAN2,0,chanl,pInitConfig)!=1)
	{
		printf(">>Init CAN1 error\n");
		VCI_CloseDevice(VCI_USBCAN2,0);
		return -1;
	}
	std::cout<<"CAN"<<chanl<<" init OK."<<std::endl;
	return 0;
}
int can_device::start(int chanl,PVCI_INIT_CONFIG pInitConfig)
{
	if(VCI_StartCAN(VCI_USBCAN2,0,chanl)!=1)
	{
		printf(">>Init can%d error\n",chanl);
		VCI_CloseDevice(VCI_USBCAN2,0);
		return -1;
	}
	std::cout<<"CAN"<<chanl<<" start OK."<<std::endl;
	return 0;
}
void find_can_device()
{
	num=VCI_FindUsbDevice2(pInfo1);

	printf(">>USBCAN DEVICE NUM:");printf("%d", num);printf(" PCS");printf("\n");

	for(int i=0;i<num;i++)
	{
		printf("Device:");printf("%d", i);printf("\n");
		printf(">>Get VCI_ReadBoardInfo success!\n");
		
		printf(">>Serial_Num:%c", pInfo1[i].str_Serial_Num[0]);
		printf("%c", pInfo1[i].str_Serial_Num[1]);
		printf("%c", pInfo1[i].str_Serial_Num[2]);
		printf("%c", pInfo1[i].str_Serial_Num[3]);
		printf("%c", pInfo1[i].str_Serial_Num[4]);
		printf("%c", pInfo1[i].str_Serial_Num[5]);
		printf("%c", pInfo1[i].str_Serial_Num[6]);
		printf("%c", pInfo1[i].str_Serial_Num[7]);
		printf("%c", pInfo1[i].str_Serial_Num[8]);
		printf("%c", pInfo1[i].str_Serial_Num[9]);
		printf("%c", pInfo1[i].str_Serial_Num[10]);
		printf("%c", pInfo1[i].str_Serial_Num[11]);
		printf("%c", pInfo1[i].str_Serial_Num[12]);
		printf("%c", pInfo1[i].str_Serial_Num[13]);
		printf("%c", pInfo1[i].str_Serial_Num[14]);
		printf("%c", pInfo1[i].str_Serial_Num[15]);
		printf("%c", pInfo1[i].str_Serial_Num[16]);
		printf("%c", pInfo1[i].str_Serial_Num[17]);
		printf("%c", pInfo1[i].str_Serial_Num[18]);
		printf("%c", pInfo1[i].str_Serial_Num[19]);printf("\n");

		printf(">>hw_Type:%c", pInfo1[i].str_hw_Type[0]);
		printf("%c", pInfo1[i].str_hw_Type[1]);
		printf("%c", pInfo1[i].str_hw_Type[2]);
		printf("%c", pInfo1[i].str_hw_Type[3]);
		printf("%c", pInfo1[i].str_hw_Type[4]);
		printf("%c", pInfo1[i].str_hw_Type[5]);
		printf("%c", pInfo1[i].str_hw_Type[6]);
		printf("%c", pInfo1[i].str_hw_Type[7]);
		printf("%c", pInfo1[i].str_hw_Type[8]);
		printf("%c", pInfo1[i].str_hw_Type[9]);printf("\n");	

		printf(">>Firmware Version:V");
		printf("%x", (pInfo1[i].fw_Version&0xF00)>>8);
		printf(".");
		printf("%x", (pInfo1[i].fw_Version&0xF0)>>4);
		printf("%x", pInfo1[i].fw_Version&0xF);
		printf("\n");
	}
}
CAN_STATUS can_send_message_to_tsu()
{
    VCI_INIT_CONFIG can_device_config;
    can_device_config.AccCode=0;
	can_device_config.AccMask=0xFFFFFFFF;
	can_device_config.Filter=1;//接收所有帧
	can_device_config.Timing0=0x03;/*波特率125 Kbps  0x03  0x1C*/
	can_device_config.Timing1=0x1C;
	can_device_config.Mode=0;//正常模式

	
    can_device *can = new can_device(&can_device_config);
    find_can_device();
    VCI_CAN_OBJ can_data;
    can_data.ID = 0x1610ff91;
    can_data.SendType=0;
	can_data.RemoteFlag=0;
	can_data.ExternFlag=1;
	can_data.DataLen=8;

    for(int i = 0; i < can_data.DataLen; i++)
    {
        can_data.Data[i] = 0x00;
    }
	can_data.Data[7] = 0x80;
    can->device_open(VCI_USBCAN2,0,0);
	int m_run0=1;
	// pthread_t threadid;
	// int ret;
	// ret=pthread_create(&threadid,NULL,_receive_func,&m_run0);
    can->init(CAN1,&can_device_config); /*can1*/
    can->start(CAN1,&can_device_config);

    // can->init(CAN2,&can_device_config);/*can2*/
    // can->start(CAN2,&can_device_config);
    // can->send(CAN1,&can_data);
    
    for(int i = 0; i < can_data.DataLen; i++)
    {
        can_data.Data[i] = 0x00;
    }
	can_data.Data[7] = 0x80;
	for(int j=0;j<360;j++)
	{
		can->send(CAN1,&can_data);
		sleep(1);
	}
    
    delete(can);
	return CAN_STATUS_OK;
}

void tsu_program_mode(int tx_flag)
{
	int i = 360;
	int status = 0;
	// can_send_message_to_tsu();

	while(tx_flag)
	{
		status = system("cansend can0 1610FF91#80");
		if(status)
		{
			printf("ERROR : cansend can0 1610FF91#80,status = %d",status);
		}
		sleep(1);		
	}
}	