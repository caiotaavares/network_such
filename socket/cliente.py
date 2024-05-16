import socket
import threading

def receive_messages(s):
    while True:
        data = s.recv(1024)
        if not data:
            print('Fechando a conexão')
            s.close()
            break
        print(data.decode())

def send_messages(s):
    while True:
        message = input('')
        s.sendall(message.encode())

def main():
    host = 'localhost'
    port = 50000

    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.connect((host, port))

        receive_thread = threading.Thread(target=receive_messages, args=(s,))
        send_thread = threading.Thread(target=send_messages, args=(s,))

        receive_thread.start()
        send_thread.start()

        receive_thread.join()
        send_thread.join()

if __name__ == '__main__':
    main()
