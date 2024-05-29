#!/usr/bin/python3

import time;
import serial
from serial import Serial
import requests
import re

url = "https://jcboisset.000webhostapp.com/api/readGetEIFK.php"
serial_port = '/dev/tty.usbmodem1301'
#serial_port = '/dev/ttyACM0'
baud_rate = 9600
write_to_file_path = 'data_'+time.asctime( time.localtime(time.time()) ).replace(" ", "_")+'.txt'
output_file = open(write_to_file_path, "w")
output_file.write("Time, TemperatureDHT22C, HumidityDHT22Percentage, DustConcentrationUgM3, COValueAU, TemperatureBME680C,PressureBME680HPa,HumidityBME680Percentage,GasBME680KOhm\n")
output_file.close()

ser = serial.Serial(serial_port, baud_rate)
while True:
    output_file = open(write_to_file_path, "a")
    line = ser.readline()
    line = line.decode("utf-8")
    out = time.strftime("%D:%H:%M:%S",time.localtime())+','+line
    #time.sleep(60)
    output_file.write(out)
    print(line)
    print('---')
    lineStr = re.split(',|\r', line)[:8]
    print(lineStr)
    print('####')
    if len(lineStr)==8:
        params = {
            'TemperatureDHT22C': float(lineStr[0]),
            'HumidityDHT22Percentage': float(lineStr[1]),
            'DustConcentrationUgM3': float(lineStr[2]),
            'COValueAU': float(lineStr[3]),
            'TempBMEC': float(lineStr[4]),
            'PressureBME680HPa': float(lineStr[5]),
            'HumidityBME680Percentage': float(lineStr[6]),
            'GasBME680KOhm': float(lineStr[7])
        }
        print(params)
        response = requests.get(url, params=params)
        print(response.text)
    output_file.close()