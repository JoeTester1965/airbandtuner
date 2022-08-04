#!/bin/bash
python3 airbandtuner.py 2>/dev/null &
sleep 1
python3 airbandtunerclient.py
