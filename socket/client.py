import socket
import threading
import inquirer

def receive_messages(s):
    while True:
        data = s.recv(1024)
        if not data:
            print('Fechando a conexão')
            s.close()
            break
        print('\nServidor:', data.decode())

def send_messages(s):
    while True:
        questions = [
            inquirer.Text('message', message="Você")
        ]
        answer = inquirer.prompt(questions)
        message = answer['message']
        s.sendall(message.encode())

def get_input(prompt, default, validator):
    while True:
        user_input = input(f"{prompt}, (padrão: {default}): ").strip()
        if not user_input:
            return default
        if validator(user_input):
            return user_input
        else:
            print(f"Entrada inválida. Por favor, insira um valor válido para {prompt.lower()}.")

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

    host = get_input("Escolha um IP", host, is_valid_ip)
    port = int(get_input("Escolha uma porta", port, is_valid_port))

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
