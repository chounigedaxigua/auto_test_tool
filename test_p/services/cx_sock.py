import socket
import sys
import threading
import os

# 获取当前脚本所在的目录
current_dir = os.path.dirname(os.path.abspath(__file__))

# 获取项目根目录（假设项目根目录是当前脚本的上一级目录）
project_root = os.path.dirname(current_dir)

# 将项目根目录添加到 sys.path
if project_root not in sys.path:
    sys.path.insert(0, project_root)

# 现在可以正常导入 test_p 包
from bsp.power_manage import power_ctrl
from services.comand_execution import comand_hander
PORT = 5000
ADDRESS = '0.0.0.0'


class cx_sock_t:
    def __init__(self, host=ADDRESS, port=PORT):
        self.server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.server_socket.bind((host, port))
        self.server_socket.listen(5)
        self.exit_event = threading.Event()
        print(f"TCP 服务端正在监听 {host}:{port} ...")
    def sock_end(self):
        client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        client_socket.connect((ADDRESS, PORT))
        
    def handle_client(self, client_socket, client_address):

        try:
            while True:
                data = client_socket.recv(1024)
                if not data:
                    print(f"客户端 {client_address} 断开连接")
                    break

                received_message = data.decode('utf-8')
                print(f"< {received_message}")
                comand_hander.process_command(received_message, client_socket, client_address)
                # response_message = "Hello from Server!"
                # client_socket.send(response_message.encode('utf-8'))
        except Exception as e:
            print(f"与客户端 {client_address} 通信时出错: {e}")
        finally:
            client_socket.close()

    def start_tcp_server(self):
        try:
            while not self.exit_event.is_set():
                client_socket, client_address = self.server_socket.accept()
                print(f"接收到来自 {client_address} 的连接")

                client_thread = threading.Thread(target=self.handle_client, args=(client_socket, client_address))
                client_thread.daemon = True
                client_thread.start()
        except KeyboardInterrupt:
            print("服务端已停止。")
            self.exit_event.set()
        finally:
            self.server_socket.close()
            print("服务端套接字已关闭。")
    def task_start(self):
        sock_task = threading.Thread(target=self.start_tcp_server)
        sock_task.start()
    # def send(self,data = "Hello from Server"):
    #     self.soc
cx_sock = cx_sock_t()
if __name__ == "__main__":
    s = cx_sock_t()
    s.start_tcp_server()