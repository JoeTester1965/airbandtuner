import zmq
import numpy as np
import time
import matplotlib.pyplot as plt
import pmt
from xmlrpc.client import ServerProxy
import logging
import sys  

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s",
    handlers=[
        #logging.FileHandler("logfile.log"),
        logging.StreamHandler(sys.stdout)
    ]
)


s = ServerProxy('http://localhost:50240')

test = None

while test is None:
    try:
        test = s.get_samp_rate()
    except:
        time.sleep(1)
        logging.info("Waiting to connect to gnuradio sketch ...")
        pass

logging.info("Connected gnuradio sketch")

samp_rate = s.get_samp_rate()
tuning_freq = s.get_tuning_freq()
fft_resolution = s.get_fft_resolution()
carrier_squelch = s.get_carrier_squelch()
hold_seconds = s.get_hold_seconds()
audio_gain = s.get_audio_gain()

zmq_pub_sink_context = zmq.Context()
zmq_pub_sink = zmq_pub_sink_context.socket(zmq.SUB)
zmq_pub_sink.connect("tcp://127.0.0.1:50242")
zmq_pub_sink.setsockopt(zmq.SUBSCRIBE, b'')

zmq_push_message_sink_context = zmq.Context()
zmq_push_message_sink = zmq_push_message_sink_context.socket (zmq.PUSH)
zmq_push_message_sink.bind ("tcp://127.0.0.1:50241")


last_index = -1
last_time_tuned = time.time()
last_time_had_audio = time.time()
update_ui_seconds = 1
last_time_updated_ui = time.time()

while True:
    if zmq_pub_sink.poll(10) != 0:
        msg = zmq_pub_sink.recv()
        message_size = len(msg)
        data = np.frombuffer(msg, dtype=np.float32, count=fft_resolution)
        most_powerful_index = np.argmax(data)
        power = data[most_powerful_index]
        if  (time. time() - last_time_tuned ) > hold_seconds:
            if power > carrier_squelch:
                last_time_had_audio = time.time()
                last_time_tuned = time.time()
                frequency = tuning_freq - (samp_rate/2) + (most_powerful_index * (samp_rate/fft_resolution))
                offset = frequency - tuning_freq
                if most_powerful_index != last_index:
                    zmq_push_message_sink.send(pmt.serialize_str((pmt.cons(pmt.intern("freq"), pmt.to_pmt(float(offset))))))
                    logging.info("Tuned to am channel %.2f", frequency/1000000)
                    s.set_audio_gain(audio_gain)
                    last_index = most_powerful_index
            else:
                if (time. time() - last_time_had_audio ) > hold_seconds:
                    last_time_had_audio = time. time()
                    s.set_audio_gain(0)
    
    if  (time.time() - last_time_updated_ui) > update_ui_seconds:
        last_time_updated_ui = time.time()
        carrier_squelch = s.get_carrier_squelch()
        tuning_freq = s.get_tuning_freq()
        hold_seconds = s.get_hold_seconds()
