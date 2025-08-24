# Additional functionality - sending themerature

## Temperature and Humidity Sensor DHT21 (AM2301)

We will be using it simply to get the temperature.
- [Botland Store](https://botland.store/multifunctional-sensors/1884-temperature-and-humidity-sensor-dht21-am2301-in-5904422373269.html)
- [AVMARKET](https://www.avmarket.eu/czujniki-temperatury/6908-czujnik-temperatury-i-wilgotnosci-dht21-am2301-5903772337945.html)

## Install Software

Copy the repository to your Raspberry:
```
cd /opt
sudo git clone https://github.com/MariuszFerdyn/AzureSmartDoorbellSystem.git
sudo chown -R $USER:$USER /opt/AzureSmartDoorbellSystem
```

## Assumption

GPIO will be used as a input/output devices. Each GPIO is set as in or out, the assumption is that the system is clear and all GPIO are disabled and all are set as in. So simply clear configuration. Please check the following:
```
sudo ls -R /sys/class/gpio
```
It should be without any gpio directory - so like:

```
mf@pi1:~ $ sudo ls -R /sys/class/gpio
/sys/class/gpio:
export  gpiochip512  unexport
mf@pi1:~ $
```
Please review the Rapberry PI pinouts - the best here: https://pinout.xyz/ or for old Rasberry Pi here: https://forums.raspberrypi.com/viewtopic.php?t=250161

![Raspberry PI Pinouts](media/PiPinouts.PNG)

## Connections

### Temperature and Humidity Sensor DHT21

GND (-) - connect to Pin 6 - Ground</br>
VCC (+) - connect to Pin 1 - 3v3 V</br>
OUT - connect to Pin 11 - GPIO 17</br>


## Configure GPIO

GPIO are not configured in your Rasperry out of the box, so we need to configure them enable it. After enabling GPIO are configured as input device, so for output device we need to perform additional step.

Log in to your Raspberry Pi and perform the following.

```
sudo echo 17 > /sys/class/gpio/export
sudo echo 27 > /sys/class/gpio/export
sudo echo 22 > /sys/class/gpio/export
sudo echo out > /sys/class/gpio/gpio22/direction
sudo ls -R /sys/class/gpio/
```

## Check if Temperature and Humidity Sensor DHT11 2f working

```
cd /opt/AzureSmartDoorbellSystem
chmod 755 01-InteractWithDHT21.sh
./01-InteractWithDHT21.sh
```

This behavior is normal due to the error in nev version of library (not always temperature will be taken):
```
Attempt 1 failed: A full buffer was not returned. Try again.
Attempt 2 failed: A full buffer was not returned. Try again.
Attempt 3 failed: A full buffer was not returned. Try again.
Attempt 4 failed: A full buffer was not returned. Try again.
Attempt 5 failed: A full buffer was not returned. Try again.
Attempt 6 failed: Checksum did not validate. Try again.
Attempt 7 failed: Checksum did not validate. Try again.
Attempt 8 failed: A full buffer was not returned. Try again.
{"Temperature": 27, "Humidity": 56}
```

## Create Azure IOT Central for aquiring the temperature and display it
