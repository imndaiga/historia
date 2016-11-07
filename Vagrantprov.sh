#!/usr/bin/env bash

apt-get update

# Install git for version control, pip for install python packages
echo 'Installing git, python3.4...'
apt-get install git python3.4 python3.4-dev -q -y
wget -q https://bootstrap.pypa.io/get-pip.py
python3 get-pip.py

# Install python package dependancies from requirements.txt
echo 'Installing python packages...'
pip3 install -r /vagrant/requirements.txt

# Some useful aliases for getting started
printf "\nUseful Aliases:\n" >> ~vagrant/.bashrc
printf "alias runserver='python3 /vagrant/manage.py runserver -h 0.0.0.0'\n" >> ~vagrant/.bashrc

echo "Vagrant install complete."
echo "Now try logging in:"
echo "    $ vagrant ssh"