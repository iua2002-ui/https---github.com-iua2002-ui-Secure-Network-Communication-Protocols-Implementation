#!/usr/bin/env python3
import socket
import argparse
import random
from pathlib import Path
from typing import Tuple


def send_common_info(sock: socket.socket, server_address: str, server_port: int) -> Tuple[int, int]:
    try:
        sock.connect((server_address, server_port))
        base = random.randint(1, 100)
        prime_modulus = random.choice([17, 23, 31, 41, 43, 47, 53, 59, 61, 67])
        message = f"{base} {prime_modulus}"
        sock.sendall(message.encode())
        return base, prime_modulus
    except Exception as e:
        print(f"Error while sending common info: {e}")
        raise

def dh_exchange_client(server_address: str, server_port: int) -> Tuple[int, int, int, int]:
    try:
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
            base, prime_modulus = send_common_info(sock, server_address, server_port)
            print("Base proposal successful.")
            print(f"Base int is {base}")
            print(f"Modulus is {prime_modulus}")
            private_key = random.randint(1, prime_modulus - 1)
            public_key = (base ** private_key) % prime_modulus
            print(f"Secret is {private_key}")
            sock.sendall(str(public_key).encode())
            server_public_key = int(sock.recv(1024).decode())
            print(f"Int received from peer is {server_public_key}")
            shared_secret = (server_public_key ** private_key) % prime_modulus
            print(f"Shared secret is {shared_secret}")
            return base, prime_modulus, private_key, shared_secret
    except Exception as e:
        print(f"Error during key exchange: {e}")
        raise

def main(args):
    if args.seed:
        random.seed(args.seed)
    dh_exchange_client(args.address, args.port)

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "-a",
        "--address",
        default="127.0.0.1",
        help="The address the client will connect to.",
    )
    parser.add_argument(
        "-p",
        "--port",
        default=8000,
        type=int,
        help="The port the client will connect to.",
    )
    parser.add_argument(
        "--seed",
        dest="seed",
        type=int,
        help="Random seed to make the exchange deterministic.",
    )
    arguments = parser.parse_args()
    main(arguments)