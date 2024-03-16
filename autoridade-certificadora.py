from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.asymmetric import ec
import socket

# Configurações do servidor
HOST = '127.0.0.8'  # Endereço IP do servidor
PORT = 12345        # Porta do servidor

# Lista para armazenar pares de chaves
key_pairs = []

# Cria um socket UDP
udp_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

# Associa o socket ao endereço e porta especificados
udp_socket.bind((HOST, PORT))

print("Servidor UDP iniciado.")

# Gerar 6 pares de chaves ECC
for i in range(1, 7):
    private_key = ec.generate_private_key(ec.SECP256R1(), default_backend())
    public_key = private_key.public_key()
    key_pairs.append((f"PC {i}", private_key, public_key))

def verificarAssinatura(numeroPC):
    if 1 <= numeroPC <= len(key_pairs):
        pair_id, private_key, public_key = key_pairs[numeroPC - 1]
        
        # Mensagem a ser verificada
        message = b"Exemplo de mensagem para assinar"
        
        # Assinatura correspondente
        signature = private_key.sign(message, ec.ECDSA(hashes.SHA256()))
        print(signature)
        
        # Verificar a assinatura
        try:
            public_key.verify(signature, message, ec.ECDSA(hashes.SHA256()))
            print(f"Assinatura válida para o par de chaves {pair_id}.")
        except:
            print(f"Assinatura inválida para o par de chaves {pair_id}.")
    else:
        print("Este PC não existe.")


while True:
    verificarAssinatura(8)
    print(key_pairs)


    # Recebe os dados do cliente e o endereço do cliente
    data, addr = udp_socket.recvfrom(1024)
    print(f"Mensagem recebida de {addr}: {data.decode()}")

    # Envia uma resposta ao cliente
    response = "Mensagem recebida com sucesso!"
    udp_socket.sendto(response.encode(), addr)
