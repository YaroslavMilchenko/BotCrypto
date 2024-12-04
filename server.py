import socket
import json
from database import add_subscription, remove_subscription, get_subscriptions, get_all_subscriptions

HOST = '127.0.0.1'
PORT = 65433

def handle_client(client_socket):
    try:
        data = client_socket.recv(1024).decode("utf-8")
        request = json.loads(data)
        action = request.get('action')
        user_id = request.get('user_id')
        service = request.get('service')

        if action == 'subscribe' and user_id and service:
            add_subscription(user_id, service)
            response = {"message": f"Ви успішно підписалися на {service}."}
        elif action == 'unsubscribe' and user_id and service:
            remove_subscription(user_id, service)
            response = {"message": f"Ви успішно відписалися від {service}."}
        elif action == 'get_subscribers':
            try:
                subscribers = get_all_subscriptions()
                response = {"subscribers": subscribers} if subscribers else {"subscribers": []}
            except Exception as e:
                print(f"Помилка у обробці get_subscribers: {e}")
                response = {"subscribers": []}
        else:
            response = {"message": "Невірний запит."}

        client_socket.sendall(json.dumps(response).encode("utf-8"))
    except Exception as e:
        print(f"Помилка обробки клієнта: {e}")
        client_socket.sendall(json.dumps({"message": "Сталася помилка."}).encode("utf-8"))
    finally:
        client_socket.close()

def main():
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as server_socket:
        server_socket.bind((HOST, PORT))
        server_socket.listen(5)
        print(f"Сервер працює на {HOST}:{PORT}")

        while True:
            client_socket, addr = server_socket.accept()
            handle_client(client_socket)

if __name__ == "__main__":
    main()
