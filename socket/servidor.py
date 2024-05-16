import socket
import threading

def handle_client(conn, addr):
    print('Conectado em:', addr)
    while True:
        data = conn.recv(1024)
        if not data:
            print('Fechando a conexão com:', addr)
            conn.close()
            break
        print(data.decode())

def send_messages(conn):
    while True:
        message = input('')
        conn.sendall(message.encode())

def main():
    host = 'localhost'
    port = 50000

    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.bind((host, port))
        s.listen()

        print('Aguardando conexão')
        conn, addr = s.accept()

        receive_thread = threading.Thread(target=handle_client, args=(conn, addr))
        send_thread = threading.Thread(target=send_messages, args=(conn,))

        receive_thread.start()
        send_thread.start()

        receive_thread.join()
        send_thread.join()

if __name__ == '__main__':
    main()
