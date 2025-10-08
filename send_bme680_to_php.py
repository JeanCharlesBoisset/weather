import time
import board
import adafruit_bme680
import requests

# Server configuration
HOST = "http://jeancharlesboisset.net"
PATH = "/IoT/readGetEnv.php"
URL = f"{HOST}{PATH}"

def read_bme680():
    i2c = board.I2C()  # Uses SCL/SDA pins
    bme = adafruit_bme680.Adafruit_BME680_I2C(i2c, address=0x77)

    # Optional calibration offsets (fine-tune if needed)
    bme.sea_level_pressure = 1013.25

    temperature = round(bme.temperature, 1)
    humidity = round(bme.humidity, 1)
    pressure = round(bme.pressure, 1)
    gas = round(bme.gas / 1000.0, 2)  # Convert to kΩ

    return temperature, humidity, pressure, gas

def send_data(temp, hum, press, gas):
    payload = {
        "temperature": temp,
        "humidity": hum,
        "pressure": press,
        "gas": gas
    }
    try:
        response = requests.get(URL, params=payload, timeout=10)
        print(f"Sent: T={temp}°C, H={hum}%, P={press} hPa, Gas={gas} kΩ → {response.text}")
    except Exception as e:
        print("Error sending data:", e)

def main_loop():
    while True:
        try:
            t, h, p, g = read_bme680()
            send_data(t, h, p, g)
        except Exception as e:
            print("Error:", e)
        time.sleep(300)  # every 5 minutes

if __name__ == "__main__":
    print("Starting BME680 Adafruit script...")
    main_loop()
