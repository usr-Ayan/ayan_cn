#!/usr/bin/env python3
import socket
from Crypto.Util.number import bytes_to_long, long_to_bytes
import random
import time
import checksum
import helper
import crc

HOST = 'localhost'
PORT = 9999
PKT_SIZE = 8
c = socket.socket()
random.seed(time.time()) #initialize the random number generator


def single_error(text: str, number: int) -> str:
    if number == 0:
        return text
    x = random.randint(0, len(text)-1)
    if text[x] == '0':
        text = text[:x]+'1'+text[x+1:]
    else:
        text = text[:x]+'0'+text[x+1:]
    return text
def burst_error(text: str, number: int) -> str:
    if number == 0:
        return text
    for i in range(3) :
        x = random.randint(0, len(text)-1)
        if text[x] == '0':
            text = text[:x]+'1'+text[x+1:]
        else:
            text = text[:x]+'0'+text[x+1:]
    return text
def special_error(text: str) -> str:
        x = 6
        if text[x] == '0':
            text = text[:x]+'1'+text[x+1:]
        else:
            text = text[:x]+'0'+text[x+1:]
        return text

c.connect((HOST, PORT)) #establishes a connection from the client socket c to a server running on the local machine (localhost) at port 9999

text = input("Enter data:").encode('utf-8') # The encode('utf-8') method converts the string entered by the user into bytes using the UTF-8 encoding. This is useful for preparing the string for transmission over a network or for writing to a binary file.
res = input("What kind of error Do you want to insert errors?(single/Burst/special/n)")
crc_method = input("Give the CRC divisor method:")
divisor = helper.convToBinary(crc_method)
#method = input("Detection Method:(CRC/Checksum)")
enc_text = bin(bytes_to_long(text))[2:]
actual_len = len(enc_text)
if actual_len/8 == 0:
    pass
else:
    extra = '0'*(8-(actual_len % 8))
    enc_text = enc_text + extra
chunks = [enc_text[i:i+PKT_SIZE] for i in range(0, len(enc_text), PKT_SIZE)]
CRCchunks = crc.CRC.encodeData(chunks, divisor)
c.send(long_to_bytes(actual_len))
time.sleep(1)
#checksum
c.send(checksum.Checksum.generate_checksum(chunks).encode('utf-8'))
for i in chunks:
    time.sleep(1)
    if res == 'single':
        j = single_error(i, random.randint(0, 2))
        c.send(j.encode('utf-8'))
    elif res == 'Burst' :
        j = burst_error(i, random.randint(0, 2))
        c.send(j.encode('utf-8'))
    elif res == 'special' :
        j = special_error(i)
        c.send(j.encode('utf-8'))
    else:
        c.send(i.encode('utf-8'))
c.send(b'EOF')
print("Sending data FOR Checksum", enc_text)
print(chunks)
print(c.recv(1024).decode('utf-8')) 
#CRC   
c.send(divisor.encode('utf-8'))
for i in CRCchunks:
    time.sleep(1)
    if res == 'single':
        j = single_error(i, random.randint(0, 2))
        c.send(j.encode('utf-8'))
    elif res == 'Burst' :
        j = burst_error(i, random.randint(0, 2))
        c.send(j.encode('utf-8'))
    elif res == 'special' :
        j = special_error(i)
        c.send(j.encode('utf-8'))
    else:
        c.send(i.encode('utf-8'))
c.send(b'EOF')
print("Sending data FOR CRC", enc_text)
print(CRCchunks)
print(c.recv(1024).decode('utf-8')) 

