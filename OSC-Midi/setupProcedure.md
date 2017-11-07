
> Download Raspbian_server_For_zero_H2+_V0_1
> Burn it into an SD card (with Etcher)
> put the SD card on the OrangePi 
> Login to Orange Pi:
    $ ssh root@orangePiIPaddr
    password(orangepi)

# Resize fileSystem to take all sd card space available
sudo fs_resize

# reboot the Pic
sudo reboot

# Set OrangePi datetime  (and avoid ssl certificate bugs...)
date -s '2017-09-20 12:34:56'

# Update sytem
sudo apt-get update
sudo apt-get upgrade

# Install KX Studio repo
sudo apt-get install apt-transport-https software-properties-common wget
wget https://launchpad.net/~kxstudio-debian/+archive/kxstudio/+files/kxstudio-repos_9.4.6~kxstudio1_all.deb
# add --no-check-certificate if you get errors...
sudo dpkg -i kxstudio-repos_9.4.6~kxstudio1_all.deb


# Install dependancies
sudo apt-get install git python3 python3-dev virtualenv mongodb build-essential libasound2-dev alsa-utils jackd2 
sudo apt-get install libjack-dev

# enable mod usb midi
insmod /lib/modules/3.4.39/snd-usbmidi-lib.ko
insmod /lib/modules/3.4.39/snd-hwdep.ko 
insmod /lib/modules/3.4.39/sndspdif.ko
insmod /lib/modules/3.4.39/snd-usb-audio.ko

# Get the git project repository
git clone https://github.com/Silhm/bcf-scribble-strips.git


# create the virtual env named orange (TBD)
virtualenv -p python3 orangepiEnv
# Startworking on this new Env
source ~/orangepiEnv/bin/activate

# install requirements 
pip install -r bcf-scribble-strips/OSC-Midi/pythonPgm/requirements.txt


# run Setup
cd bcf-scribble-strips/OSC-Midi/pythonPgm/ 
python setup.py




