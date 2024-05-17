import socket
import threading
import inquirer

def handle_client(conn, addr, expected_password):
    print('Conectado em:', addr)
    attempts = 0
    while attempts < 3:
        password = conn.recv(1024).decode().strip()
        if password == expected_password:
            conn.sendall("Servidor: Senha correta".encode('utf-8'))
            while True:
                data = conn.recv(1024)
                if not data:
                    print('Fechando a conexão com:', addr)
                    conn.close()
                    break
                print('\nCliente:', data.decode())
        else:
            conn.sendall("Servidor: Senha incorreta".encode('utf-8'))
            attempts += 1
    print('Fechando a conexão com:', addr)
    conn.close()

def send_messages(conn):
    while True:
        questions = [
            inquirer.Text('message', message="Você")
        ]
        answer = inquirer.prompt(questions)
        message = answer['message']
        conn.sendall(message.encode())

def get_input(prompt, default, validator):
    while True:
        user_input = input(f"{prompt} (padrão: {default}): ").strip()
        if not user_input:
            return default
        if validator(user_input):
            return user_input
        else:
            print(f"Entrada inválida. Por favor, insira um valor válido para {prompt.lower()}.")

def passwd_input(prompt, default):
    while True:
        user_input = input(f"{prompt} (padrão: {default}): ").strip()
        if not user_input:
            return default
        else:
            return user_input

def is_valid_ip(ip):
    try:
        socket.inet_aton(ip)
        return True
    except socket.error:
        return False
    
def is_valid_port(port):
    try:
        port = int(port)
        return 0 <= port <= 65535
    except ValueError:
        return False

def main():
    host = 'localhost'
    port = 50000
    password = 'root'

    host = get_input("Escolha um IP", host, is_valid_ip)
    port = int(get_input("Escolha uma porta", port, is_valid_port))
    password = passwd_input("Escolha a senha", password)

    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        while True:
            try:
                s.bind((host, port))
                break
            except OSError as e:
                if e.errno == 98:  # Address already in use
                    print(f"Porta {port} já está em uso. Escolha uma porta diferente.")
                    port = int(get_input("Escolha uma porta", port, is_valid_port))
                else:
                    raise

        s.listen()
        print('Aguardando conexão')
        while True:
            conn, addr = s.accept()
            threading.Thread(target=handle_client, args=(conn, addr, password)).start()

if __name__ == '__main__':
    main()
