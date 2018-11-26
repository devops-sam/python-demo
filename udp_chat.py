import socket


# 创建套接字
udp_sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)


def main():
    # 本地地址
    src_ip = ""
    src_port = 7788

    # 绑定本地ip、port
    udp_sock.bind((src_ip, src_port))

    # while循环处理消息
    while True:
        # 发送
        send_msg()
        
        # 接受并显示
        rec_msg()

def send_msg():
    # 目的地址
    dest_ip = "192.168.56.1"
    dest_port = 8080

    # 定义发送信息
    send_data = input("请输入你要发送的消息: ")

    # 发送数据
    udp_sock.sendto(send_data.encode("utf-8"), (dest_ip, dest_port))

def rec_msg():
    # 接受信息
    rec_data = udp_sock.recvfrom(1024)
    rec_data_msg = rec_data[0].decode("gbk")
    rec_srcinfo = "%s:%s" % (rec_data[1][0], rec_data[1][1])

    print("接受的消息: %s来自于客户端: %s"  %  (rec_data_msg, rec_srcinfo))


if __name__ == "__main__":
    main()
