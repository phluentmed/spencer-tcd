import serial
import struct
import time
import sys
import requests
from SerialConnection import SerialConnection
from PacketDecoder import PacketDecoder
import json

port = "/dev/ttyUSB0"
dest_ip = "http://capstone.us-east-2.elasticbeanstalk.com/patients/5c69a22fecc0cf3c45497a46"
serial_connection = SerialConnection(port)
print('Result of serial connect: %r' %serial_connection.connect())
packet_decoder = PacketDecoder.getInstance()

def tcd_network_post(payload, dest_ip):
    # payload = payload
    # dest_ip = dest_ip
    print("called tcd_network_post")
    payload = {'TCDMonitor':payload}
    print(payload)
    r = requests.put(dest_ip, data=json.dumps(payload))
    print(r.text)

while True:
    header, data = serial_connection.receive()
    (PS, PL, DID, VER, PN, CH, PT) = header
    if not data and not header:
        print('error in transmission')
    if (PT == 1):
        print("envelope packet\n")
    #numerics packet sent once a second
    elif (PT == 2):
        print('numerics packet')
        num_packet = packet_decoder.decode(header, data)
        print(num_packet)
        tcd_network_post(num_packet, dest_ip)

    #messages packet 
    elif(PT == 3):
        print("message packet")
        print(packet_decoder.decode(header, data))
    #error packet
    elif(PT == 4):
        print("error packet")
        print(packet_decoder.decode(header, data))


