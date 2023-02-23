#STUDENT NAME: MWAI MARTIN KIBIRU
#STUDENT NUMBER: 3035716804
#DEVELOPMENT PLATFORM: WINDOWS 11, VS CODE.
#PYTHON VERSION: PYTHON 3.11.2


import socket
import time
import struct


def tcp_test(host, port):
    # Create a socket object
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    # Connect the socket to the server
    client_socket.connect((host, port))

    # Test 1: large transfer
    print("Start test1 - large transfer")
    data = b'0' * 1000000
    start_time = time.perf_counter()
    client_socket.sendall(data * 200)
    received_data = client_socket.recv(200000000)
    elapsed_time = time.perf_counter() - start_time
    print("From server to client")
    print(f"Received total: {len(received_data)} bytes")
    print("From client to server")
    print("* " * 20)
    start_time = time.perf_counter()
    client_socket.sendall(b'1' * 10000)
    client_socket.recv(1024)
    elapsed_time = time.perf_counter() - start_time
    print(f"Sent total: 10000 bytes")
    print(f"Elapsed time: {elapsed_time:.5f} s")
    print(f"Throughput (from client to server): {len(b'1' * 10000) / elapsed_time / 10 ** 6:.3f} Mb/s")

    # Test 2: small transfer
    print("\nStart test2 - small transfer")
    data = b'0' * 10000
    start_time = time.perf_counter()
    client_socket.sendall(data)
    received_data = client_socket.recv(1024)
    elapsed_time = time.perf_counter() - start_time
    print("From server to client")
    print(f"Received total: {len(received_data)} bytes")
    print("From client to server")
    print(f"Sent total: {len(data)} bytes")
    print(f"Elapsed time: {elapsed_time:.5f} s")
    print(f"Throughput (from client to server): {len(data) / elapsed_time / 10 ** 6:.3f} Mb/s")

    # Close the socket
    client_socket.close()


def udp_test(host, port):
    # Create a socket object
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

    # Test 3: UDP ping-pong
    print("\nStart test3 - UDP pingpong")
    total_rtt = 0
    for i in range(5):
        data = struct.pack('i', i)
        client_socket.sendto(data, (host, port))
        start_time = time.perf_counter()
        client_socket.settimeout(1)
        try:
            data, addr = client_socket.recvfrom(1024)
            rtt = time.perf_counter() - start_time
            print(f"Reply from {addr[0]}: time = {rtt:.4f} s")
            total_rtt += rtt
        except socket.timeout:
            print("Request timed out")
    avg_rtt = total_rtt / 5
    print(f"Average RTT: {avg_rtt:.5f} s")
    # Close the socket
    client_socket.close()


def main():
    # Set the host and port for the server
    host = '192.168.0.148'
    port = 55555

    # TCP test
    print("Start as client node")
    print(f"Client has connected to server at: {host}, {port}")
    print(f"Client's address: {socket.gethostbyname(socket.gethostname())}, {port}")
    tcp_socket = tcp_test(host, port)
    

    tcp_port = tcp_socket.getsockname()[1]  # get the assigned port number for TCP socket

    # UDP test
    udp_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    udp_socket.bind((host, tcp_port))  # set the same port number for UDP socket as TCP socket
    print(f"UDP socket is bound to {host}, {tcp_port}")
    udp_test(host, tcp_port)

    # Close the sockets
    tcp_socket.close()
    udp_socket.close()

