import time
import adafruit_dht
import board

dht_device = adafruit_dht.DHT11(board.D17, use_pulseio=True)
max_retries = 20
retry_delay = 8  # seconds

for attempt in range(max_retries):
    try:
        temperature = dht_device.temperature
        #temperature_f = temperature * (9 / 5) + 32  # Convert to Fahrenheit

        humidity = dht_device.humidity

        print(f'{{"Temperature": {temperature}, "Humidity": {humidity}}}')
        # print("Temp:{:.1f} C / {:.1f} F    Humidity: {}%".format(temperature, temperature_f, humidity))
        break  # Exit the loop if successful
    except RuntimeError as err:
        print(f"Attempt {attempt + 1} failed: {err.args[0]}")
        time.sleep(retry_delay)
else:
    print("Failed to read from DHT11 sensor after several attempts.")
