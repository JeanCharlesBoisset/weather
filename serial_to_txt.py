#!/usr/bin/python3

import time;
import serial
from serial import Serial
import requests

url = "jcboisset.000webhostapp.com/api/readGetEIFK.php"
#serial_port = '/dev/cu.usbmodem14201'
serial_port = '/dev/ttyACM0'
baud_rate = 9600
write_to_file_path = 'data_'+time.asctime( time.localtime(time.time()) ).replace(" ", "_")+'.txt'
output_file = open(write_to_file_path, "w")
output_file.write("Time, TemperatureDHT22C, HumidityDHT22Percentage, DustConcentrationUgM3, COValueAU, TemperatureBMEC,PressureBMEHPa,HumidityBMEPercentage,GasBMEKOhm\n")
output_file.close()

ser = serial.Serial(serial_port, baud_rate)
while True:
    output_file = open(write_to_file_path, "a")
    line = ser.readline()
    line = line.decode("utf-8")
    out = time.strftime("%D:%H:%M:%S",time.localtime())+','+line
    #time.sleep(60)
    output_file.write(out)
    params = {
        'TemperatureCBME680':
            
    }
    output_file.close()
