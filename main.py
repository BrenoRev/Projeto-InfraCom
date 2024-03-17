import json
import threading
import time
from socket import socket, AF_INET, SOCK_DGRAM

from dijkstra import dijkstra, get_graph_path
from log_message import log_message

broadcast_server = "127.0.0.7"
certify_server = "127.0.0.8"

class ServerPC:
    def __init__(self, server_id, all_server_addresses):
        self.server_id = server_id


        # Configurações do servidor
        HOST = f"127.0.0.{self.server_id}"  # Endereço IP do servidor
        PORT = 10311        # Porta do servidor

        self.SERVER_ADDRESS = (HOST, PORT)

        self.relationships = {
            1: [2, 6],
            2: [3, 1],
            3: [4, 2],
            4: [5, 3],
            5: [6, 4],
            6: [1, 5]
        }

        self.private_key = None
        
        pcs_list = [1, 2, 3, 4, 5, 6]
        pcs_list.remove(self.server_id)
        self.pcsExceptMe = pcs_list

        self.graph = {
            "pc6": {"pc1": 1, "pc5": 2},
            "pc5": {"pc6": 2, "pc4": 3},
            "pc4": {"pc5": 3, "pc3": 1},
            "pc3": {"pc4": 1, "pc2": 2},
            "pc2": {"pc3": 2, "pc1": 1},
            "pc1": {"pc2": 1, "pc6": 2}
        }

        self.all_server_addresses = all_server_addresses

    def get_graph_path(self, from_node):
        path = dijkstra(self.server_id, from_node, self.relationships.items())

        if self.server_id in path:
            path.remove(self.server_id)

        log_message(f"Path from {self.server_id} to {from_node}: {path}", self.server_id)

        return path

    def send_message(self, target_server_id, message):
        """Send a message to the specified server."""

        if target_server_id and isinstance(target_server_id, list):
            target_server_id = target_server_id[0]

        target_address = self.all_server_addresses[target_server_id]
        target_server = target_address.split('.')[-1]

        with socket(AF_INET, SOCK_DGRAM) as sock:
            sock.sendto(message.encode(), (target_address, 10311))

            log_message(f"Sent from Server {self.server_id} to server {target_server}: {message}", self.server_id)
            sock.close()

    def define_message(self, message, target_server_id=None):
        message = f"{self.server_id}-{message}"
        if target_server_id:
            return f"{target_server_id}/{message}"
        else:
            return message

    def treat_message_from_broadcaster(self, decoded_message):
        path_sender, message = decoded_message.split("-", 1)
        log_message(f"{self.server_id}: Received broadcast message: {message}", self.server_id)

    def validate_message_private_key(self, message):
        if "PRIVATE_KEY-" in message:
            return True
        return False
    
    def validate_message_from_certificate_authority(self, message):
        if "certificate_authority-" in message:
            return True
        return False
    
    def validate_message_from_broadcaster(self, message):
        if "broadcaster-" in message:
            return True
        return False

    def validate_normal_message(self, message):
        if "-" in message:
            return True
        return False

    def validate_message_through_path(self, path_sender):
        if "/" in path_sender:
            return True
        return False

    def validate_message_is_allowed(self, sender_id):
        if int(sender_id) in self.relationships[self.server_id]:
            return True
        return False

    def listen_for_messages(self):
        print(f"Server {self.server_id} listening on {self.SERVER_ADDRESS[0]}:{self.SERVER_ADDRESS[1]}")
        with socket(AF_INET, SOCK_DGRAM) as sock:
            sock.bind(self.SERVER_ADDRESS)
            log_message(f"Server {self.server_id} listening on {self.SERVER_ADDRESS[0]}:{self.SERVER_ADDRESS[1]}",
                        self.server_id)

            while True:
                try:
                    message, address = sock.recvfrom(1024)
                    decoded_message = message.decode()

                    if self.validate_message_private_key(decoded_message):
                        private_key = decoded_message.split("-")[1]
                        self.private_key = private_key
                        log_message(f"Private key received", self.server_id)
                        continue
                           
                    if self.validate_message_from_broadcaster(decoded_message):
                        self.treat_message_from_broadcaster(decoded_message)
                        continue

                    if self.validate_normal_message(decoded_message):
                        path_sender, message = decoded_message.split("-", 1)

                        if self.validate_message_through_path(path_sender):
                            path_str, sender_id = path_sender.split("/", 1)

                            try:
                                path = json.loads(path_str)
                            except json.JSONDecodeError:
                                log_message("Invalid path format. Dropping message.", self.server_id)
                                continue

                            path.pop(0)
                            self.send_message_through_path(path, message)
                        else:
                            sender_id = path_sender

                        log_message(f"Message received from server {sender_id}: {message}",
                                    self.server_id)

                        if self.validate_message_is_allowed(sender_id):
                            log_message(f"Received valid message from {sender_id}: {message}", self.server_id)
                        else:
                            log_message(f"Received message from unallowed sender id {sender_id}", self.server_id)
                    else:
                        log_message("Message format error.", self.server_id)

                except Exception as e:
                    log_message(f"Error: {e}", self.server_id)
                    continue

    ### Tests to use ###

    def start_communication(self):
        for target_server_id in self.relationships[self.server_id]:
            message = self.define_message(f"Hello World")
            self.send_message(target_server_id, message)

    def start_wrong_communication(self):
        message = self.define_message(f"Hello World")
        self.send_message(1, message)

    def send_message_through_path(self, path, message):
        if path:
            print("Next servers " + str(path))
            message = self.define_message(message, path)
            self.send_message(path, message)
        else:
            log_message(f"Message reached destination: {message}", self.server_id)

    def send_message_through(self, destiny, message):
        self.send_message_through_path(get_graph_path(self.server_id, destiny, self.relationships.items()), message)

    def send_broadcast_message(self, message):
        message = self.define_message(message)

        with socket(AF_INET, SOCK_DGRAM) as sock:
            sock.sendto(message.encode(), (broadcast_server, 10311))
            log_message(f"Sent to broadcaster: {message}", self.server_id)
            sock.close()

    def start_pc_communication(self):
        for pc in self.pcsExceptMe:
            message = self.define_message(f"Hello World")
            self.send_message_through(pc, message)
        self.send_broadcast_message(f"Mensagem broadcaster from server {self.server_id}")

    # Descomente para testar as funções que validam os envios e recebimento das mensagens
    # Veja o arquivo de log para validar as mensagens  
    def run(self):
        # Inicia os servidores por meio de threads
        threading.Thread(target=self.listen_for_messages).start()

        # Aguardar um tempo para que todos os servidores estejam prontos
        time.sleep(1)

        while self.private_key == None:
            time.sleep(5)
            print(f"Aguardando a criação da chave privada {self.SERVER_ADDRESS}...")
            
        log_message("Chave privada setada para o servidor", self.server_id)

        # Tempo de espera entre todas as chaves privadas dos servidores estarem setadas
        time.sleep(2)

        # Envia mensagens para os seus vizinhos
        # self.start_communication()

        # Enviar mensagem de broadcaster do seu PC para os outros PCs
        # self.send_broadcast_message(f"Mensagem broadcaster from server {self.server_id}")

        # Enviar mensagem do servidor "current_server" para o servidor "target_server"
        # current_server = 1
        # target_server = 5
        # if self.server_id == current_server:
        #      self.send_message_through(target_server, f"Mensagem hello world do {current_server} pro {target_server}")

        # Caso de teste para tentar enviar mensagens para servidores que não são vizinhos sem passar pelo roteamento
        # self.start_wrong_communication()

        # Os nós devem conversar entre si, trocando pelo menos 5 mensagens simultaneamente;
        # ( O PC 1 envia mensagem para os demais pcs ... 2, 3, 4, 5, 6)
        # Após o envio das mensagens ele envia 1 mensagem de broadcaster e todos devem responder
        self.start_pc_communication()


class Main:
    def __init__(self, num_instances):
        # Inicialize os 6 servidores PC

        self.all_server_addresses = {i: f'127.0.0.{i}' for i in range(1, num_instances + 1)}
        self.servers = [ServerPC(i, self.all_server_addresses) for i in range(1, num_instances + 1)]

    def start_servers(self):
        for server in self.servers:
            threading.Thread(target=server.run).start()


if __name__ == "__main__":
    main_instance = Main(6)
    main_instance.start_servers()
