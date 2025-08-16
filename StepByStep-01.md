# Step By Step for Preparing Your Device

## Prerequisites

Install and customize (connect to the network) your Raspberry Pi. Any of the following models are supported: Zero, Zero W, 1A+, 1B+, 2B, 3B, 3B+, 3A+, 4B, 400, CM1, CM3, CM3+, CM4, CM4S, Zero 2 W. The best way is to use the Raspberry Pi Imager: [Raspberry Pi Imager](https://www.raspberrypi.com/software/).  
After a fresh installation, it is wise to update the operating system.
```
sudo apt update
sudo apt upgrade -y
```
## Minimum Hardware

The minimum hardware required is a compatible camera connected to your Raspberry Pi.

### Additional Hardware

#### Temperature and Humidity Sensor DHT11 - Module + Wires

We will be using it simply to get the temperature.
- [Botland Store](https://botland.store/multifunctional-sensors/1886-temperature-and-humidity-sensor-dht11-module--5903351242448.html)
- [Anodas](https://www.anodas.lt/en/dht11-module-arduino-temperature-and-humidity-sensor)

#### Button

We will be using it as a traditional ring door button, e.g., on a gate.


## Install Software

### Camera Setup

To enable your camera module, run:
```
sudo modprobe bcm2835-v4l2
```

### Install Motion Service

The Motion service allows you to stream your camera over the internet and view it from any browser.

Install Motion:
```
sudo apt install motion
```

Start the Motion service:
```
sudo service motion start
```
If your webcam has a light, it should turn on.

### Configure Motion Software

Edit the main configuration file:
```
sudo nano /etc/motion/motion.conf
```
Make the following changes:
- `daemon = ON`
- `webcam_localhost = OFF`
- `webcam_port = 8088
- `control_port = 8089`

To ensure the Motion service starts as a daemon, edit:
```
sudo nano /etc/default/motion
```
Change:
- `start_motion_daemon=yes`

Restart the Motion service:
```
sudo service motion restart
```

### Viewing and Controlling the Camera

Open a browser on another computer on the same network and view the feed:
```
http://<your Raspi Address>:8088
```

Remotely control webcam settings:
```
http://<your Raspi Address>:8089
```

### Reconfigure the Motion software to automatically detect motion and save files to a specified path

Here are relevant excerpts of Motion’s config file at `/etc/motion/motion.conf`, with some notes. Modify the file changing parameters rather than control-c/v.

```conf
# >>> Change this to "off" because systemd starts this service
# daemon off

# >>> Make sure the `motion` group has write access - first create directory using mkdir /videos
target_dir /videos

# >>> This was where my webcam mounted, but may not be for you.
video_device /dev/video0

############################################################
# Image Processing configuration parameters
############################################################

width 1280
height 720
framerate 30

############################################################
# Motion detection configuration parameters
############################################################

# >>> I tweaked these, may tweak more... the docs are good
threshold 600
minimum_motion_frames 3
event_gap 15
pre_capture 5
post_capture 60

############################################################
# Script execution configuration parameters
############################################################

# >>> See above!
on_event_start

# >>> Explained below; handles Stream and Webhook #2
#     "%f" is a placeholder for the full path to the mp4
on_movie_end /opt/video-upload.bash %f >> /videos/on_movie_end.log 2>&1

############################################################
# Movie output configuration parameters
############################################################

movie_output on
movie_max_time 600
movie_quality 80
movie_codec mp4
```

