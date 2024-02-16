import json
import threading
import time
import heapq
from socket import socket, AF_INET, SOCK_DGRAM 

class ServerPC:
    def __init__(self, server_id, all_server_addresses):
        self.server_id = server_id
        
        self.SERVER_ADDRESS = (f'127.0.0.{self.server_id}', 10311)
        
        self.relationships = {
            1: [2, 6],
            2: [3, 1],
            3: [4, 2],
            4: [5, 3],
            5: [6, 4],
            6: [1, 5]
        }
        
        self.graph = {
            "pc6": {"pc1": 1, "pc5": 2},
            "pc5": {"pc6": 2, "pc4": 3},
            "pc4": {"pc5": 3, "pc3": 1},
            "pc3": {"pc4": 1, "pc2": 2},
            "pc2": {"pc3": 2, "pc1": 1},
            "pc1": {"pc2": 1, "pc6": 2}
        }

        self.all_server_addresses = all_server_addresses

    def log_message(self, text: str):
        print(text)
        with open("log.txt", "a") as file:
            file.write(f'\n----------\n{text}')

    def dijkstra(self, destination_id):
        graph = self.convert_relationships_to_graph()
        source = "pc" + str(self.server_id)
        destination = "pc" + str(destination_id)
        
        queue = [(0, source)]
        visited = {source: (0, None)}
        
        while queue:
            (cost, current_node) = heapq.heappop(queue)
            
            if current_node == destination:
                path = [destination]
                while current_node != source:
                    (cost, current_node) = visited[current_node]
                    path.append(current_node)
                path.reverse()
                
                return [int(node[2:]) for node in path] 
            
            for neighbor, weight in graph.get(current_node, {}).items():
                new_cost = cost + weight
                if neighbor not in visited or new_cost < visited[neighbor][0]:
                    heapq.heappush(queue, (new_cost, neighbor))
                    visited[neighbor] = (new_cost, current_node)

        return None

    def convert_relationships_to_graph(self):
        new_graph = {}
        for server_id, neighbors in self.relationships.items():

            server_key = "pc" + str(server_id)
            new_graph[server_key] = {}
            for neighbor in neighbors:
                neighbor_key = "pc" + str(neighbor)

                new_graph[server_key][neighbor_key] = 1  
        return new_graph

    def get_graph_path(self, from_node):
        path = self.dijkstra(from_node)

        if self.server_id in path:
            path.remove(self.server_id)
   
        print(f"Path from {self.server_id} to {from_node}: {path}")
        
        return path
        
    def send_message(self, target_server_id, message):
        """Send a message to the specified server."""

        if target_server_id and isinstance(target_server_id, list):
            target_server_id = target_server_id[0]
            
        target_address = self.all_server_addresses[target_server_id]
        target_server = target_address.split('.')[-1]
        
        with socket(AF_INET, SOCK_DGRAM) as sock:
            sock.sendto(message.encode(), (target_address, 10311))

            self.log_message(f"Sent from Server {self.server_id} to server {target_server}: {message}")
      
    def define_message(self, message, target_server_id = None):
        message = f"{self.server_id}-{message}"
        if target_server_id:
            return f"{target_server_id}/{message}"
        else:
            return message
        
    def listen_for_messages(self):
        with socket(AF_INET, SOCK_DGRAM) as sock:
            sock.bind(self.SERVER_ADDRESS)
            self.log_message(f"Server {self.server_id} listening on {self.server_id}")

            while True:
                try:
                    message, address = sock.recvfrom(1024)
                    decoded_message = message.decode()

                    path = []
                    if "-" in decoded_message:
                        path_sender, message = decoded_message.split("-", 1)
                        
                        if "/" in path_sender:
                            path_str, sender_id = path_sender.split("/", 1)
                            
                            try:
                                path = json.loads(path_str) 
                            except json.JSONDecodeError:
                                self.log_message("Invalid path format. Dropping message.")
                                continue
                        else:
                            sender_id = path_sender
                            path = []

                        self.log_message(f"[{self.server_id}] Message received from server {sender_id}: {message}")
                        
                        if path:
                            path.pop(0)
                            self.send_message_through_path(path, message)
                        elif int(sender_id) in self.relationships[self.server_id]:
                            self.log_message(f"Received valid message from {sender_id}: {message}")
                        else:
                            self.log_message(f"Received message from unallowed sender id {sender_id}")
                    else:
                        self.log_message("Message format error. Expected 'path/sender_id-message'.")

                except Exception as e:
                    self.log_message(f"Error: {e}")
                    continue
        
    def start_communication(self):
        for target_server_id in self.relationships[self.server_id]:
            message = self.define_message(f"Hello World")
            self.send_message(target_server_id, message)
            
    def start_wrong_communication(self):
        message = self.define_message(f"Hello World")
        self.send_message(1, message)
    
    def send_message_through_path(self, path, message):
        if path:
            print("Next servers", path)
            message = self.define_message(message, path)
            self.send_message(path, message)
        else:
            self.log_message(f"[{self.server_id}] Message reached destination: {message}")
      
    def send_message_through_test(self, source, destiny):
        source = 6
        if self.server_id == source:
            self.send_message_through_path(self.get_graph_path(destiny), "Hello World")   
                   
    def run(self):
        threading.Thread(target=self.listen_for_messages).start()
    
        time.sleep(1)
        
        # self.send_message_through_test(6, 3)
        
        self.start_communication()

        # self.start_wrong_communication()
        
        
class Main:
    def __init__(self, num_instances):

        self.all_server_addresses = {i: f'127.0.0.{i}' for i in range(1, num_instances + 1)}
        self.servers = [ServerPC(i, self.all_server_addresses) for i in range(1, num_instances + 1)]

    def start_servers(self):
        for server in self.servers:
            threading.Thread(target=server.run).start()

if __name__ == "__main__":
    main_instance = Main(6)
    main_instance.start_servers()
