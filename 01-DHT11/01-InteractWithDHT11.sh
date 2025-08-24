#/bin/bash
sudo apt install -y python3
sudo apt install -y python3-pip
python3 -m pip install --break-system-packages  adafruit-circuitpython-dht==3.5.5
python3 InteractWithDHT11.py
