import socket
import subprocess
import click
from threading import Thread


def run_cmd(cmd):
    output = subprocess.run(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True)
    return output.stdout


def handle_input(client_socket):
    # 新增：缓存还没凑成完整命令的字节（TCP 是字节流，一次 recv 可能只给半条，也可能给两条）
    buffer = b''
    while True:
        chunk = client_socket.recv(2048)
        if not chunk:
            # 新增：recv 返回 b'' 表示对端已断开，直接退出，否则下面的循环会空转死等
            break
        buffer += chunk

        # 修改：以 \n 作为一条命令的结束符逐条切分；切不出来的半条留在 buffer 等下一轮
        while b'\n' in buffer:
            line, buffer = buffer.split(b'\n', 1)
            # 修改：兼容 \r\n；原来的 decode()[:-1] 只删一个字符，会残留 \r 导致命令执行失败
            cmd = line.decode(errors='replace').rstrip('\r')

            if cmd.strip().lower() == 'exit':
                client_socket.close()
                return
            if not cmd.strip():
                continue  # 新增：空行跳过

            output = run_cmd(cmd)
            client_socket.sendall(output)

    client_socket.close()


@click.command()
@click.option('--port', '-p', default=4444)
def main(port):
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.bind(('0.0.0.0', port))  # 0.0.0.0 = 监听本机所有网卡（回环 + NAT 网卡），宿主机才连得上
    s.listen(4)

    while True:
        # accept() 阻塞等新连接；每个连接开一个线程处理，主线程继续接下一个（课件里的“多线程版本”）
        client_socket, _ = s.accept()
        t = Thread(target=handle_input, args=(client_socket,))
        t.daemon = True  # 新增：Ctrl+C 退出时子线程不会拖着进程不结束
        t.start()


if __name__ == '__main__':
    main()
