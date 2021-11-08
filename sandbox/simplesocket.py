'''
Created on 2 Dec 2014

@author: up45
'''

import os
import socket

board_ip_address = os.getenv("PERCIVAL_CARRIER_IP")
board_ip_port = 10001

def bytes_to_str(byte_list):
    return "".join([chr(b) for b in byte_list])

def main():
    #numbers = [0x00, 0xEC, 0x00, 0x00, 0x00, 0x00,
    #           0x00, 0xEC, 0x00, 0x02, 0x00, 0x00]
    numbers = [0x01, 0x40, 0x00, 0x00, 0x00, 0x00] # Header Settings Carrier shortcut

    msg = bytes_to_str(numbers)
    
    client_sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client_sock.settimeout(2.0)
    client_sock.connect((board_ip_address, board_ip_port))
    print("Sending message: ", numbers)
    print(" as string:      ", [msg])
    client_sock.send(msg)
    
    print("Waiting for response...")
    
    try:
        response = client_sock.recv(1024)
    except:
        client_sock.close()
        raise
        
    print("Got response (%dbytes): "%len(response), [response]) 
    print(" which means: ", [ord(r) for r in response])
    print("  and in hex:", " ".join([hex(ord(r))for r in response]))

    client_sock.close()
    
if __name__ == '__main__':
    main()