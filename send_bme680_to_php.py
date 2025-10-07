import bme680
import time
import requests

HOST = "http://jeancharlesboisset.net"
PATH = "/IoT/readGetEnv.php"
URL = f"{HOST}{PATH}"

def read_bme680():
    sensor = bme680.BME680(bme680.I2C_ADDR_SECONDARY)  # Use 0x77 instead of 0x76

    sensor.set_humidity_oversample(bme680.OS_2X)
    sensor.set_pressure_oversample(bme680.OS_4X)
    sensor.set_temperature_oversample(bme680.OS_8X)
    sensor.set_filter(bme680.FILTER_SIZE_3)
    sensor.set_gas_status(bme680.ENABLE_GAS_MEAS)

    print("Reading BME680... waiting for gas stabilization.")
    sensor.set_gas_heater_temperature(320)
    sensor.set_gas_heater_duration(150)
    sensor.select_gas_heater_profile(0)

    time.sleep(1)

    if sensor.get_sensor_data():
        if sensor.data.heat_stable:
            temperature = round(sensor.data.temperature, 1)
            humidity = round(sensor.data.humidity, 1)
            pressure = round(sensor.data.pressure, 1)
            gas = round(sensor.data.gas_resistance / 1000.0, 2)  # in kOhms
            return temperature, humidity, pressure, gas
        else:
            raise RuntimeError("Gas sensor not heat stable yet")
    else:
        raise RuntimeError("Failed to read BME680")

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
        time.sleep(300)  # every 5 min

if __name__ == "__main__":
    main_loop()
