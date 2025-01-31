#!/usr/bin/env python3
import socket
import argparse
import random
from pathlib import Path
from typing import Tuple



def receive_common_info(client_socket: socket.socket) -> Tuple[int, int]:
    try:
        data = client_socket.recv(1024).decode()
        base, prime_modulus = map(int, data.split())
        return base, prime_modulus
    except Exception as e:
        print(f"Error while receiving common info: {e}")
        raise

def dh_exchange_server(server_address: str, server_port: int) -> Tuple[int, int, int, int]:
    try:
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as server_socket:
            server_socket.bind((server_address, server_port))
            server_socket.listen(1)
            print(f"Server listening on {server_address}:{server_port}")
            client_socket, addr = server_socket.accept()
            print(f"Connection established with {addr}")
            base, prime_modulus = receive_common_info(client_socket)
            print(f"Base int is {base}")
            print(f"Modulus is {prime_modulus}")
            private_key = random.randint(1, prime_modulus - 1)
            public_key = (base ** private_key) % prime_modulus
            print(f"Secret is {private_key}")
            client_socket.sendall(str(public_key).encode())
            client_public_key = int(client_socket.recv(1024).decode())
            print(f"Int received from peer is {client_public_key}")
            shared_secret = (client_public_key ** private_key) % prime_modulus
            print(f"Shared secret is {shared_secret}")
            client_socket.close()
            return base, prime_modulus, private_key, shared_secret
    except Exception as e:
        print(f"Error during key exchange: {e}")
        raise

def main(args):
    dh_exchange_server(args.address, args.port)

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "-a",
        "--address",
        default="127.0.0.1",
        help="The address the server will bind to.",
    )
    parser.add_argument(
        "-p",
        "--port",
        default=8000,
        type=int,
        help="The port the server will listen on.",
    )
    arguments = parser.parse_args()
    main(arguments)