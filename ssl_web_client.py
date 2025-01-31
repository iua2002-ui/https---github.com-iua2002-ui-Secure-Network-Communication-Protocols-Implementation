#!/usr/bin/env python3
import ssl
import pprint
import socket
import argparse
from typing import Dict, Any
from pathlib import Path

def craft_http_request(host: str, path: str) -> str:
    return f"GET {path} HTTP/1.1\r\nHost: {host}\r\n\r\n"

def create_socket(host: str, port: int, use_ssl: bool) -> socket.socket | ssl.SSLSocket:
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    if use_ssl:
        # Create an SSL context
        ssl_context = ssl.create_default_context()
        # Wrap the socket with SSL
        s = ssl_context.wrap_socket(s, server_hostname=host)
    s.connect((host, port))  # Connect to the server
    return s


def get_peer_certificate(ssl_socket: ssl.SSLSocket) -> Dict[str, Any]:
    return ssl_socket.getpeercert()

def send_http_request(s: socket.socket | ssl.SSLSocket, request_string: str) -> str:
    s.sendall(request_string.encode())
    response = b""
    data = s.recv(1024)
    response += data
    return response.decode()

def main(args):
    s = create_socket(args.host, args.port, args.ssl)

    if args.ssl:
        # Check SSL handshake success
        print("SSL handshake successful:", s.version())
        
        # Get the peer certificate
        cert = get_peer_certificate(s)
        print("Peer certificate:")
        pprint.pprint(cert)

    request = craft_http_request(args.host, args.document)
    response = send_http_request(s, request)

    print("========================= HTTP Response =========================")
    print(response)
    s.close()
    
if __name__ == "__main__":
    parser = argparse.ArgumentParser()

    parser.add_argument(
        "host",
        default="www.example.com",
        type=str,
        help="The url/host we connect to",
    )

    parser.add_argument(
        "-d",
        "--document",
        default="/",
        type=str,
        help="The path to the document/webpage we want to retrieve"
    )

    parser.add_argument(
        "--ssl",
        action="store_true",
    )

    parser.add_argument(
        "-p",
        "--port",
        default=80,
        type=int,
        help="The port we connect to",
    )

    arguments = parser.parse_args()
    main(arguments)