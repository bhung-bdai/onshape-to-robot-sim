#!/usr/bin/bash
sudo apt-get update -y
sudo apt-get install ros-humble-ros-gz -y
sudo apt-get update -y
sudo apt-get install lsb-release wget gnupg -y

sudo wget https://packages.osrfoundation.org/gazebo.gpg -O /usr/share/keyrings/pkgs-osrf-archive-keyring.gpg
echo "deb [arch=$(dpkg --print-architecture) signed-by=/usr/share/keyrings/pkgs-osrf-archive-keyring.gpg] http://packages.osrfoundation.org/gazebo/ubuntu-stable $(lsb_release -cs) main" | sudo tee /etc/apt/sources.list.d/gazebo-stable.list > /dev/null
sudo apt-get update -y
sudo apt install libgz-math13-dev -y

sudo apt-get install python3-pip wget lsb-release gnupg curl -y
sudo sh -c 'echo "deb http://packages.osrfoundation.org/gazebo/ubuntu-stable `lsb_release -cs` main" > /etc/apt/sources.list.d/gazebo-stable.list'
wget http://packages.osrfoundation.org/gazebo.key -O - | sudo apt-key add -
sudo apt-get update -y

sudo apt install libsdformat13-dev libsdformat13 -y

pip install -e .