# Step By Step for Preparing Your Device

## Prerequisites

Install and customize (connect to the network) your Raspberry Pi. Any of the following models are supported: Zero, Zero W, 1A+, 1B+, 2B, 3B, 3B+, 3A+, 4B, 400, CM1, CM3, CM3+, CM4, CM4S, Zero 2 W. The best way is to use the Raspberry Pi Imager: [Raspberry Pi Imager](https://www.raspberrypi.com/software/).  
After a fresh installation, it is wise to update the operating system.
```
sudo apt update
sudo apt upgrade -y
```

To anable vnc invoke: 
```
sudo raspi-config nonint get_vnc
```
## Minimum Hardware

The minimum hardware required is a compatible camera connected to your Raspberry Pi.

### Additional Hardware

#### Temperature and Humidity Sensor DHT21 (AM2301)

See [Step-by-Step Guide 02 - sending temperature](StepByStep-02.md)

#### Button

We will be using it as a traditional ring door button, e.g., on a gate.


## Install Software

Copy the repository to your Raspberry:
```
cd /opt
sudo git clone https://github.com/MariuszFerdyn/AzureSmartDoorbellSystem.git
sudo chown -R $USER:$USER /opt/AzureSmartDoorbellSystem
```

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
on_movie_end /opt/AzureSmartDoorbellSystem/VideoUpload.sh %f >> /videos/on_movie_end.log 2>&1

############################################################
# Movie output configuration parameters
############################################################

movie_output on
movie_max_time 600
movie_quality 80
movie_codec mp4
```

### Install Azure CLI for Uploading Videos to Azure

Run the following commands to ensure all prerequisites are installed:

```
sudo apt install libffi-dev python3-dev python3-pip openssl
```

Once the prerequisites are installed, use the official Microsoft script to install the Azure CLI:

```
curl -L https://aka.ms/InstallAzureCli | bash
```

### Create an Azure Storage Account and Blob Container

1. Sign in to your Azure account:
    ```
    az login
    ```

2. Create a resource group:
    ```
    az group create --name <resource-group> --location <location>
    ```

3. Create a storage account:
    ```
    az storage account create --name <storage-account> --resource-group <resource-group> --location <location> --sku Standard_ZRS --encryption-services blob
    ```

4. Assign yourself the Storage Blob Data Contributor role:
    ```
    az ad signed-in-user show --query id -o tsv | az role assignment create --role "Storage Blob Data Contributor" --assignee @- --scope "/subscriptions/<subscription>/resourceGroups/<resource-group>/providers/Microsoft.Storage/storageAccounts/<storage-account>"
    ```

5. Create a blob container:
    ```
    az storage container create --account-name <storage-account> --name videos --auth-mode login
    ```

6. Create and display a SAS token that allows you to upload files only to the `videos` container in your storage account:

```
az storage container generate-sas \
  --account-name <storage-account> \
  --name videos \
  --permissions w \
  --expiry <YYYY-MM-DD> \
  --auth-mode login \
  --as-user \
  --output tsv
```

Replace `<storage-account>` with your storage account name and `<YYYY-MM-DD>` with your desired expiry date (e.g., `2027-12-31`).  
This SAS token grants write-only access to the `videos` container.

7. Make VideoUpload.sh executable and update it with your SAS token and storage account:

```
sudo chmod +x /opt/AzureSmartDoorbellSystem/VideoUpload.sh
```

Edit `/opt/AzureSmartDoorbellSystem/VideoUpload.sh` and replace the placeholders `<storage-account>` and `<your_sas_token>` with your actual storage account name and the SAS token you generated above.

***For now, all new videos should be uploaded to your Storage Account.***

## Notifications for New Videos

You can use standard Azure functionality to notify users about new videos by SMS, email, or other channels. One recommended approach is to use an Azure Logic App:

- **Logic Apps** can monitor your storage account for new blobs (videos) and trigger automated workflows.
- You can configure Logic Apps to send notifications via SMS (using Twilio or Azure Communication Services), email (using Outlook, Gmail, or SMTP), or even post to Microsoft Teams or Slack.
- Logic Apps can also integrate with other Azure services, databases, or custom APIs for advanced automation.

**Example workflow:**
1. Logic App is triggered when a new video is uploaded to the `videos` container.
2. The Logic App sends an email or SMS notification to the desired recipients with details about the new video.
3. Optionally, you can include a link to the video or additional metadata in the notification.

For more details, see the official documentation: [Azure Logic Apps Documentation](https://learn.microsoft.com/en-us/azure/logic-apps/)
