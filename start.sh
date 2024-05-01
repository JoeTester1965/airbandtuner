#!/bin/bash
python3 airbandtuner.py >> airbandtuner.py.log.txt 2>&1 &
python3 airbandtunerclient.py >> airbandtunerclient.py.log.txt 2>&1 &