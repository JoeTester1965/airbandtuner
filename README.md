# airbandtuner

Will autoscan and tune into the most powerful AM broadcast up in the skies for a large frequency range wherever you tune your RTL dongle.

Audio can be heard remotely over the Internet by typing the following URL into something like VLC player:

```http://my-ip-address:AudioStreamPort```  e.g.  ```http://192.168.1.50:8087```

The audio server works using vlc to capture and rebroadcast the audio arriving in from gnuradio.

If you have issues with port conflicts, edit [start.sh](start.sh) for VLC (8087) and use gnuradio_companion to edit AudioStreamPort (7355) in airbandtuner.grc and regenerate airbandtuner.py.


# Using

First of all use gnuradio_companion to edit the following variables in airbandtuner.grc then regenerate airbandtuner.py;

- rtl_device_arguments  (leave blank if simply one USB device, otherwise use rtl_tcp=a.b.c.d etc, see [this](https://manpages.ubuntu.com/manpages/trusty/man1/rtl_tcp.1.html) for more details)
- rtl_ppm (not really needed)


Then:

```console
bash ./start.sh 
2022-08-04 08:39:23,045 [INFO] Tuned to am channel 135.43
2022-08-04 08:39:43,311 [INFO] Tuned to am channel 135.50
2022-08-04 08:39:56,755 [INFO] Tuned to am channel 135.43
2022-08-04 08:40:01,344 [INFO] Tuned to am channel 135.51
2022-08-04 08:40:09,061 [INFO] Tuned to am channel 135.50
2022-08-04 08:40:18,608 [INFO] Tuned to am channel 134.98


bash ./end.sh
```

# Dependancies

This runs on Linux, recently tested with the excellent [PiSDR](https://github.com/luigifcruz/pisdr-image) distro 6.1.

* [GNURadio](https://wiki.gnuradio.org/index.php/InstallingGR) Note: works on GNURADIO 3.10 and 3.9 but not 3.8.

* [rtl-sdr](https://www.rtl-sdr.com/rtl-sdr-quick-start-guide/) Note: On Linux just do sudo apt-get install rtl-sdr.

* [vlc](https://www.videolan.org/vlc/)

# User interface

![!](./uiscreenshot.png "")

| Item | Description |
| :-: | :-:|
| tuning_freq | Coarse tuning into the frequencies of interest, in 1MHz jumps. For example selecting 135000000 (135MHz) will let you listen in on activity within 134 MHz and 136 MHz. |
| gain | Tune this using the Power/Frequency graph in the user interface so that you see decent audio signals (the large upward spikes) appear on the graph above the noise floor. |   
| carrier_squelch | Set this to the lowest power level (as in the displayed graph) of signals you want to listen to, bigger values have a better signal to noise ratio and sound clearer. |
| hold_seconds | Do not tune into another concurrent (albeit higher signal to noise) audio channel for this interval (prevents rapid flipping between channels). |  

# Design

![!](./design.png "")

You can still run the flow graph [airbandtuner.grc](https://github.com/JoeTester1965/airbandtuner/blob/main/airbandtuner.grc) in gnuradio-companion without running [airbandtunerclient.py](https://github.com/JoeTester1965/airbandtuner/blob/main/airbandtunerclient.py) as well, it just will not auto tune into the audio. 

I decided to delegate processing of the FFT for channel selection over the network to a custom python program as unfortunately the built in GNURadio Max() block is no use as you need the index from the FFT for tuning as well as the power value. 

There are upsides to this though ...

# Future possibilities

* CSV file of useful stats e.g. frequency, timestamp, power, talk-duration (for all concurrent channels).
* Radio frequency name identification based on your location and harvested frequency name guide databases.
* Speech to text, then hooks to flights on [ADSB exchange](https://globe.adsbexchange.com)!

## Contributing

Please do email JoeTester1965 at mail dot com with any questions.

## License

[MIT](https://choosealicense.com/licenses/mit/)
