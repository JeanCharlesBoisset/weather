import serial
import time
import requests

DEVICE = "/dev/ttyUSB0"
HOST = "http://jeancharlesboisset.net"
PATH = "/IoT/readGetEnv.php"
URL = f"{HOST}{PATH}"

def wake_sensor(ser):
    # Command to wake up the sensor
    cmd = bytearray([0xAA, 0xB4, 0x06, 0x01] + [0x00]*10)
    cmd.append(sum(cmd[2:]) % 256)
    cmd.append(0xAB)
    ser.write(cmd)

def sleep_sensor(ser):
    # Command to put sensor to sleep
    cmd = bytearray([0xAA, 0xB4, 0x06, 0x00] + [0x00]*10)
    cmd.append(sum(cmd[2:]) % 256)
    cmd.append(0xAB)
    ser.write(cmd)

def read_sds011(port=DEVICE):
    with serial.Serial(port, baudrate=9600, timeout=5) as ser:
        wake_sensor(ser)
        time.sleep(30)  # allow sensor to stabilize

        # Wait for valid data
        while True:
            if ser.read(1) == b'\xAA':
                data = ser.read(9)
                if len(data) == 9 and data[0] == 0xC0 and data[-1] == 0xAB:
                    pm25 = (data[1] + data[2] * 256) / 10.0
                    pm10 = (data[3] + data[4] * 256) / 10.0
                    break
        sleep_sensor(ser)
        return pm25, pm10

def send_data(pm25, pm10):
    payload = {
        "pm25": pm25,
        "pm10": pm10
    }
    try:
        response = requests.get(URL, params=payload, timeout=10)
        print(f"PM2.5 = {pm25}, PM10 = {pm10} → {response.text}")
    except Exception as e:
        print("Error sending data:", e)

def main_loop():
    while True:
        try:
            pm25, pm10 = read_sds011()
            send_data(pm25, pm10)
        except Exception as e:
            print("Sensor read/send failed:", e)
        time.sleep(300)  # 5 minutes between readings

if __name__ == "__main__":
    main_loop()
