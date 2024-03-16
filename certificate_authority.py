from os import urandom
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.asymmetric import ec
import socket
from socket import socket, AF_INET, SOCK_DGRAM

from encrypter import encrypt_message
from log_message import log_message

# Configurações do servidor
HOST = '127.0.0.8'  # Endereço IP do servidor
PORT = 10311        # Porta do servidor

# Lista para armazenar pares de chaves
key_pairs = {}

servers = ["127.0.0.1",
           "127.0.0.2",
           "127.0.0.3",
           "127.0.0.4",
           "127.0.0.5",
           "127.0.0.6",
        ]

servers_port = 10311

def verificarAssinatura(server):
    if server in key_pairs:
        public_key = key_pairs[server]
        
        # Mensagem a ser verificada
        message = b"Exemplo de mensagem para assinar"
        
        # Assinatura correspondente
        signature = private_key.sign(message, ec.ECDSA(hashes.SHA256()))
        print(signature)
        
        # Verificar a assinatura
        try:
            public_key.verify(signature, message, ec.ECDSA(hashes.SHA256()))
            print(f"Assinatura válida para o par de chaves {pair_id}.")
            return "OK"
        except:
            print(f"Assinatura inválida para o par de chaves {pair_id}.")
            return "NOK"
    else:
        print("Este PC não existe.")

def instantiate_pc(server):
    private_key = ec.generate_private_key(ec.SECP256R1(), default_backend())
    public_key = private_key.public_key()
    key_pairs[server] = public_key
    
    return private_key;

with socket(AF_INET, SOCK_DGRAM) as sock:
    server_id = (HOST, PORT)

    sock.bind(server_id)
    log_message("[Certificate_Authority] Servidor UDP iniciado.")    
    
    for server in servers:
        private_key = instantiate_pc(server)
        private_message = f"PRIVATE_KEY-{private_key}"
        sock.sendto(private_message.encode(), (server, PORT))
        log_message(f"[Certificate_Authority] Chave privada enviada para {server}")
         
    log_message("[Certificate_Authority] Chaves privadas enviadas para todos os servidores.")
    log_message(f"[Certificate_Authority] public keys: {key_pairs}")
    
    while True:
        try:
            message, address = sock.recvfrom(1024)
            decoded_message = message.decode()
            log_message(f"[Certificate_Authority] Mensagem recebida de {address}: {decoded_message}")
            
            result = verificarAssinatura()
            log_message(f"[Certificate_Authority] Enviando resposta para {address}: {result}")
            
            # OK / NOK
            sock.sendto(result.encode(), address)
        except Exception as e:
            log_message(f"[Certificate_Authority] Error: {e}")
            continue
        