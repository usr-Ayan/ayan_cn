#!/usr/bin/env python3
import socket
from Crypto.Util.number import long_to_bytes, bytes_to_long
import checksum
import crc


s = socket.socket()

s.bind(('localhost', 9999))

s.listen(1)
print("Waiting for connections")

while True:
    c, addr = s.accept()
    print("Connection from {}".format(addr))
    size = bytes_to_long(c.recv(1024))
    #method = c.recv(1024).decode('utf-8')
    sum = c.recv(1024).decode('utf-8')
    checksum_data = []
    while 1:
        text = c.recv(1024).decode('utf-8')
        if 'EOF' in text:
            checksum_data.append(text.replace("EOF", ""))
            break
        checksum_data.append(text)
    received_text = ''.join(checksum_data)[:size]
    print("Data size:{}".format(size))
    print("Received Data in Checksum ={}".format(received_text))
    if checksum.Checksum.check_checksum(checksum_data, sum):
        c.send(b"Received Text, No errors found by Checksum")
    else:
        c.send(b"Error detected by Checksum")
    divisor = c.recv(1024).decode('utf-8')
    CRC_data = []
    while 1:
        text = c.recv(1024).decode('utf-8')
        if 'EOF' in text:
            CRC_data.append(text.replace("EOF", ""))
            break
        CRC_data.append(text)
    received_text = ''.join(CRC_data)[:]
    print("Received Data in CRC ={}".format(received_text))
    if crc.CRC.checkRemainder(CRC_data, divisor):
        c.send(b"Received Text, No errors found by CRC")
    else:
        c.send(b"Error detected by CRC")
    c.close()
