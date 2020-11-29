#!/bin/bash

sudo apt install -y libgmp-dev libmpfr-dev libmpc-dev python3 python3-dev python3-pip
pip3 install -r requirements.txt
pip3 install .

