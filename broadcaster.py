from socket import socket, AF_INET, SOCK_DGRAM

from log_message import log_message


# Configurações do servidor
HOST = '127.0.0.7'  # Endereço IP do servidor
PORT = 10311        # Porta do servidor

target_addresses = ["127.0.0.1",
                    "127.0.0.2",
                    "127.0.0.3",
                    "127.0.0.4",
                    "127.0.0.5",
                    "127.0.0.6",
                    ]

with socket(AF_INET, SOCK_DGRAM) as sock:
    server_id = (HOST, PORT)

    sock.bind(server_id)
    log_message(f"[Broadcaster] Server {server_id} listening")

    while True:
        try:
            message, address = sock.recvfrom(1024)
            decoded_message = message.decode()
            sender, message = decoded_message.split("-", 1)

            log_message(f"[Broadcaster] Message received from server {sender}: {message}")

            resender_message = "broadcaster-" + message

            for target_address in target_addresses:
                log_message(f"[Broadcaster] Sending message to {target_address}")
                sock.sendto(resender_message.encode(), (target_address, 10311))

        except Exception as e:
            log_message(f"[Broadcaster] Error: {e}")
            continue
