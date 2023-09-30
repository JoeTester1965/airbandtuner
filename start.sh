#!/bin/bash
python3 airbandtuner.py 2>/dev/null &
cvlc --demux=rawaud --rawaud-channels=1 --rawaud-samplerate=48000 udp://@:7355 --sout '#transcode{vcodec=none,acodec=mp3,ab=128,channels=1,samplerate=44100}:std{access=http,mux=mp3,dst=:8087}' &
python3 airbandtunerclient.py &