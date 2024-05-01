#!/usr/bin/env python3
# -*- coding: utf-8 -*-

#
# SPDX-License-Identifier: GPL-3.0
#
# GNU Radio Python Flow Graph
# Title: AirBandTuner
# Author: JoeTester1965
# Copyright: MIT license
# GNU Radio version: 3.10.7.0

from packaging.version import Version as StrictVersion
from PyQt5 import Qt
from gnuradio import qtgui
from gnuradio import analog
from gnuradio import audio
from gnuradio import blocks
from gnuradio import eng_notation
from gnuradio import filter
from gnuradio.filter import firdes
from gnuradio import gr
from gnuradio.fft import window
import sys
import signal
from PyQt5 import Qt
from argparse import ArgumentParser
from gnuradio.eng_arg import eng_float, intx
from gnuradio import network
from gnuradio import soapy
from gnuradio import zeromq
from gnuradio.fft import logpwrfft
from gnuradio.qtgui import Range, RangeWidget
from PyQt5 import QtCore
from xmlrpc.server import SimpleXMLRPCServer
import threading
import sip



class airbandtuner(gr.top_block, Qt.QWidget):

    def __init__(self):
        gr.top_block.__init__(self, "AirBandTuner", catch_exceptions=True)
        Qt.QWidget.__init__(self)
        self.setWindowTitle("AirBandTuner")
        qtgui.util.check_set_qss()
        try:
            self.setWindowIcon(Qt.QIcon.fromTheme('gnuradio-grc'))
        except BaseException as exc:
            print(f"Qt GUI: Could not set Icon: {str(exc)}", file=sys.stderr)
        self.top_scroll_layout = Qt.QVBoxLayout()
        self.setLayout(self.top_scroll_layout)
        self.top_scroll = Qt.QScrollArea()
        self.top_scroll.setFrameStyle(Qt.QFrame.NoFrame)
        self.top_scroll_layout.addWidget(self.top_scroll)
        self.top_scroll.setWidgetResizable(True)
        self.top_widget = Qt.QWidget()
        self.top_scroll.setWidget(self.top_widget)
        self.top_layout = Qt.QVBoxLayout(self.top_widget)
        self.top_grid_layout = Qt.QGridLayout()
        self.top_layout.addLayout(self.top_grid_layout)

        self.settings = Qt.QSettings("GNU Radio", "airbandtuner")

        try:
            if StrictVersion(Qt.qVersion()) < StrictVersion("5.0.0"):
                self.restoreGeometry(self.settings.value("geometry").toByteArray())
            else:
                self.restoreGeometry(self.settings.value("geometry"))
        except BaseException as exc:
            print(f"Qt GUI: Could not restore geometry: {str(exc)}", file=sys.stderr)

        ##################################################
        # Variables
        ##################################################
        self.tuning_freq = tuning_freq = 135e6
        self.samp_rate = samp_rate = 1920000
        self.ppm = ppm = 0
        self.hold_seconds = hold_seconds = 3
        self.gain = gain = 35
        self.fft_resolution = fft_resolution = 4096
        self.decimation = decimation = 40
        self.carrier_squelch = carrier_squelch = (-40)
        self.audio_gain = audio_gain = 126
        self.AudioStreamPort = AudioStreamPort = 7355
        self.AudioStreamIP = AudioStreamIP = '127.0.0.1'

        ##################################################
        # Blocks
        ##################################################

        self._tuning_freq_range = Range(108e6, 137e6, 1000000, 135e6, 200)
        self._tuning_freq_win = RangeWidget(self._tuning_freq_range, self.set_tuning_freq, "'tuning_freq'", "counter_slider", float, QtCore.Qt.Horizontal)
        self.top_grid_layout.addWidget(self._tuning_freq_win, 0, 0, 1, 1)
        for r in range(0, 1):
            self.top_grid_layout.setRowStretch(r, 1)
        for c in range(0, 1):
            self.top_grid_layout.setColumnStretch(c, 1)
        self._samp_rate_tool_bar = Qt.QToolBar(self)
        self._samp_rate_tool_bar.addWidget(Qt.QLabel("'samp_rate'" + ": "))
        self._samp_rate_line_edit = Qt.QLineEdit(str(self.samp_rate))
        self._samp_rate_tool_bar.addWidget(self._samp_rate_line_edit)
        self._samp_rate_line_edit.returnPressed.connect(
            lambda: self.set_samp_rate(int(str(self._samp_rate_line_edit.text()))))
        self.top_grid_layout.addWidget(self._samp_rate_tool_bar, 4, 0, 1, 1)
        for r in range(4, 5):
            self.top_grid_layout.setRowStretch(r, 1)
        for c in range(0, 1):
            self.top_grid_layout.setColumnStretch(c, 1)
        self._ppm_tool_bar = Qt.QToolBar(self)
        self._ppm_tool_bar.addWidget(Qt.QLabel("'ppm'" + ": "))
        self._ppm_line_edit = Qt.QLineEdit(str(self.ppm))
        self._ppm_tool_bar.addWidget(self._ppm_line_edit)
        self._ppm_line_edit.returnPressed.connect(
            lambda: self.set_ppm(int(str(self._ppm_line_edit.text()))))
        self.top_grid_layout.addWidget(self._ppm_tool_bar, 4, 1, 1, 1)
        for r in range(4, 5):
            self.top_grid_layout.setRowStretch(r, 1)
        for c in range(1, 2):
            self.top_grid_layout.setColumnStretch(c, 1)
        self._gain_range = Range(0, 49, 1, 35, 200)
        self._gain_win = RangeWidget(self._gain_range, self.set_gain, "'gain'", "counter_slider", float, QtCore.Qt.Horizontal)
        self.top_grid_layout.addWidget(self._gain_win, 0, 1, 1, 1)
        for r in range(0, 1):
            self.top_grid_layout.setRowStretch(r, 1)
        for c in range(1, 2):
            self.top_grid_layout.setColumnStretch(c, 1)
        self._AudioStreamPort_tool_bar = Qt.QToolBar(self)
        self._AudioStreamPort_tool_bar.addWidget(Qt.QLabel("'AudioStreamPort'" + ": "))
        self._AudioStreamPort_line_edit = Qt.QLineEdit(str(self.AudioStreamPort))
        self._AudioStreamPort_tool_bar.addWidget(self._AudioStreamPort_line_edit)
        self._AudioStreamPort_line_edit.returnPressed.connect(
            lambda: self.set_AudioStreamPort(int(str(self._AudioStreamPort_line_edit.text()))))
        self.top_grid_layout.addWidget(self._AudioStreamPort_tool_bar, 3, 1, 1, 1)
        for r in range(3, 4):
            self.top_grid_layout.setRowStretch(r, 1)
        for c in range(1, 2):
            self.top_grid_layout.setColumnStretch(c, 1)
        self._AudioStreamIP_tool_bar = Qt.QToolBar(self)
        self._AudioStreamIP_tool_bar.addWidget(Qt.QLabel("'AudioStreamIP'" + ": "))
        self._AudioStreamIP_line_edit = Qt.QLineEdit(str(self.AudioStreamIP))
        self._AudioStreamIP_tool_bar.addWidget(self._AudioStreamIP_line_edit)
        self._AudioStreamIP_line_edit.returnPressed.connect(
            lambda: self.set_AudioStreamIP(str(str(self._AudioStreamIP_line_edit.text()))))
        self.top_grid_layout.addWidget(self._AudioStreamIP_tool_bar, 3, 0, 1, 1)
        for r in range(3, 4):
            self.top_grid_layout.setRowStretch(r, 1)
        for c in range(0, 1):
            self.top_grid_layout.setColumnStretch(c, 1)
        self.zeromq_pull_msg_source_0 = zeromq.pull_msg_source('tcp://127.0.0.1:50241', 100, False)
        self.zeromq_pub_sink_1 = zeromq.pub_sink(gr.sizeof_float, fft_resolution, 'tcp://127.0.0.1:50242', 100, False, (-1), '', True, True)
        self.xmlrpc_server_0 = SimpleXMLRPCServer(('localhost', 50240), allow_none=True)
        self.xmlrpc_server_0.register_instance(self)
        self.xmlrpc_server_0_thread = threading.Thread(target=self.xmlrpc_server_0.serve_forever)
        self.xmlrpc_server_0_thread.daemon = True
        self.xmlrpc_server_0_thread.start()
        self.soapy_rtlsdr_source_0 = None
        dev = 'driver=rtlsdr'
        stream_args = ''
        tune_args = ['']
        settings = ['']

        def _set_soapy_rtlsdr_source_0_gain_mode(channel, agc):
            self.soapy_rtlsdr_source_0.set_gain_mode(channel, agc)
            if not agc:
                  self.soapy_rtlsdr_source_0.set_gain(channel, self._soapy_rtlsdr_source_0_gain_value)
        self.set_soapy_rtlsdr_source_0_gain_mode = _set_soapy_rtlsdr_source_0_gain_mode

        def _set_soapy_rtlsdr_source_0_gain(channel, name, gain):
            self._soapy_rtlsdr_source_0_gain_value = gain
            if not self.soapy_rtlsdr_source_0.get_gain_mode(channel):
                self.soapy_rtlsdr_source_0.set_gain(channel, gain)
        self.set_soapy_rtlsdr_source_0_gain = _set_soapy_rtlsdr_source_0_gain

        def _set_soapy_rtlsdr_source_0_bias(bias):
            if 'biastee' in self._soapy_rtlsdr_source_0_setting_keys:
                self.soapy_rtlsdr_source_0.write_setting('biastee', bias)
        self.set_soapy_rtlsdr_source_0_bias = _set_soapy_rtlsdr_source_0_bias

        self.soapy_rtlsdr_source_0 = soapy.source(dev, "fc32", 1, 'remote=192.168.1.50,driver=remote,remote:timeout=100000,remote:driver=rtlsdr,rtl=0',
                                  stream_args, tune_args, settings)

        self._soapy_rtlsdr_source_0_setting_keys = [a.key for a in self.soapy_rtlsdr_source_0.get_setting_info()]

        self.soapy_rtlsdr_source_0.set_sample_rate(0, samp_rate)
        self.soapy_rtlsdr_source_0.set_frequency(0, tuning_freq)
        self.soapy_rtlsdr_source_0.set_frequency_correction(0, ppm)
        self.set_soapy_rtlsdr_source_0_bias(bool(False))
        self._soapy_rtlsdr_source_0_gain_value = gain
        self.set_soapy_rtlsdr_source_0_gain_mode(0, bool(False))
        self.set_soapy_rtlsdr_source_0_gain(0, 'TUNER', gain)
        self.qtgui_vector_sink_f_0 = qtgui.vector_sink_f(
            fft_resolution,
            (tuning_freq - (samp_rate/2)),
            (samp_rate/fft_resolution),
            'Frequency',
            'Power',
            'Radio spectrum',
            1, # Number of inputs
            None # parent
        )
        self.qtgui_vector_sink_f_0.set_update_time(0.10)
        self.qtgui_vector_sink_f_0.set_y_axis((-140), 10)
        self.qtgui_vector_sink_f_0.enable_autoscale(False)
        self.qtgui_vector_sink_f_0.enable_grid(False)
        self.qtgui_vector_sink_f_0.set_x_axis_units('Hz')
        self.qtgui_vector_sink_f_0.set_y_axis_units('dB')
        self.qtgui_vector_sink_f_0.set_ref_level(0)


        labels = ['', '', '', '', '',
            '', '', '', '', '']
        widths = [1, 1, 1, 1, 1,
            1, 1, 1, 1, 1]
        colors = ["blue", "red", "green", "black", "cyan",
            "magenta", "yellow", "dark red", "dark green", "dark blue"]
        alphas = [1.0, 1.0, 1.0, 1.0, 1.0,
            1.0, 1.0, 1.0, 1.0, 1.0]

        for i in range(1):
            if len(labels[i]) == 0:
                self.qtgui_vector_sink_f_0.set_line_label(i, "Data {0}".format(i))
            else:
                self.qtgui_vector_sink_f_0.set_line_label(i, labels[i])
            self.qtgui_vector_sink_f_0.set_line_width(i, widths[i])
            self.qtgui_vector_sink_f_0.set_line_color(i, colors[i])
            self.qtgui_vector_sink_f_0.set_line_alpha(i, alphas[i])

        self._qtgui_vector_sink_f_0_win = sip.wrapinstance(self.qtgui_vector_sink_f_0.qwidget(), Qt.QWidget)
        self.top_layout.addWidget(self._qtgui_vector_sink_f_0_win)
        self.network_udp_sink_0 = network.udp_sink(gr.sizeof_short, 1, AudioStreamIP, AudioStreamPort, 0, 1472, False)
        self.logpwrfft_x_0 = logpwrfft.logpwrfft_c(
            sample_rate=samp_rate,
            fft_size=fft_resolution,
            ref_scale=2,
            frame_rate=10,
            avg_alpha=1.0,
            average=False,
            shift=True)
        self._hold_seconds_range = Range(1, 30, 1, 3, 200)
        self._hold_seconds_win = RangeWidget(self._hold_seconds_range, self.set_hold_seconds, "'hold_seconds'", "counter_slider", int, QtCore.Qt.Horizontal)
        self.top_grid_layout.addWidget(self._hold_seconds_win, 2, 1, 1, 1)
        for r in range(2, 3):
            self.top_grid_layout.setRowStretch(r, 1)
        for c in range(1, 2):
            self.top_grid_layout.setColumnStretch(c, 1)
        self.freq_xlating_fir_filter_xxx_0 = filter.freq_xlating_fir_filter_ccc(decimation,  firdes.low_pass(1,samp_rate,samp_rate/decimation/8,1000), 0, samp_rate)
        self._carrier_squelch_range = Range((-90), (-20), 1, (-40), 200)
        self._carrier_squelch_win = RangeWidget(self._carrier_squelch_range, self.set_carrier_squelch, "'carrier_squelch'", "counter_slider", int, QtCore.Qt.Horizontal)
        self.top_grid_layout.addWidget(self._carrier_squelch_win, 2, 0, 1, 1)
        for r in range(2, 3):
            self.top_grid_layout.setRowStretch(r, 1)
        for c in range(0, 1):
            self.top_grid_layout.setColumnStretch(c, 1)
        self.blocks_float_to_short_0 = blocks.float_to_short(1, audio_gain)
        self.blocks_endian_swap_0 = blocks.endian_swap(2)
        self.audio_sink_0 = audio.sink(44100, '', True)
        self.analog_feedforward_agc_cc_0 = analog.feedforward_agc_cc(1024, 1.0)
        self.analog_am_demod_cf_0 = analog.am_demod_cf(
        	channel_rate=(samp_rate/decimation),
        	audio_decim=1,
        	audio_pass=4000,
        	audio_stop=4500,
        )


        ##################################################
        # Connections
        ##################################################
        self.msg_connect((self.zeromq_pull_msg_source_0, 'out'), (self.freq_xlating_fir_filter_xxx_0, 'freq'))
        self.connect((self.analog_am_demod_cf_0, 0), (self.audio_sink_0, 0))
        self.connect((self.analog_am_demod_cf_0, 0), (self.blocks_float_to_short_0, 0))
        self.connect((self.analog_feedforward_agc_cc_0, 0), (self.analog_am_demod_cf_0, 0))
        self.connect((self.blocks_endian_swap_0, 0), (self.network_udp_sink_0, 0))
        self.connect((self.blocks_float_to_short_0, 0), (self.blocks_endian_swap_0, 0))
        self.connect((self.freq_xlating_fir_filter_xxx_0, 0), (self.analog_feedforward_agc_cc_0, 0))
        self.connect((self.logpwrfft_x_0, 0), (self.qtgui_vector_sink_f_0, 0))
        self.connect((self.logpwrfft_x_0, 0), (self.zeromq_pub_sink_1, 0))
        self.connect((self.soapy_rtlsdr_source_0, 0), (self.freq_xlating_fir_filter_xxx_0, 0))
        self.connect((self.soapy_rtlsdr_source_0, 0), (self.logpwrfft_x_0, 0))


    def closeEvent(self, event):
        self.settings = Qt.QSettings("GNU Radio", "airbandtuner")
        self.settings.setValue("geometry", self.saveGeometry())
        self.stop()
        self.wait()

        event.accept()

    def get_tuning_freq(self):
        return self.tuning_freq

    def set_tuning_freq(self, tuning_freq):
        self.tuning_freq = tuning_freq
        self.qtgui_vector_sink_f_0.set_x_axis((self.tuning_freq - (self.samp_rate/2)), (self.samp_rate/self.fft_resolution))
        self.soapy_rtlsdr_source_0.set_frequency(0, self.tuning_freq)

    def get_samp_rate(self):
        return self.samp_rate

    def set_samp_rate(self, samp_rate):
        self.samp_rate = samp_rate
        Qt.QMetaObject.invokeMethod(self._samp_rate_line_edit, "setText", Qt.Q_ARG("QString", str(self.samp_rate)))
        self.freq_xlating_fir_filter_xxx_0.set_taps( firdes.low_pass(1,self.samp_rate,self.samp_rate/self.decimation/8,1000))
        self.logpwrfft_x_0.set_sample_rate(self.samp_rate)
        self.qtgui_vector_sink_f_0.set_x_axis((self.tuning_freq - (self.samp_rate/2)), (self.samp_rate/self.fft_resolution))
        self.soapy_rtlsdr_source_0.set_sample_rate(0, self.samp_rate)

    def get_ppm(self):
        return self.ppm

    def set_ppm(self, ppm):
        self.ppm = ppm
        Qt.QMetaObject.invokeMethod(self._ppm_line_edit, "setText", Qt.Q_ARG("QString", str(self.ppm)))
        self.soapy_rtlsdr_source_0.set_frequency_correction(0, self.ppm)

    def get_hold_seconds(self):
        return self.hold_seconds

    def set_hold_seconds(self, hold_seconds):
        self.hold_seconds = hold_seconds

    def get_gain(self):
        return self.gain

    def set_gain(self, gain):
        self.gain = gain
        self.set_soapy_rtlsdr_source_0_gain(0, 'TUNER', self.gain)

    def get_fft_resolution(self):
        return self.fft_resolution

    def set_fft_resolution(self, fft_resolution):
        self.fft_resolution = fft_resolution
        self.qtgui_vector_sink_f_0.set_x_axis((self.tuning_freq - (self.samp_rate/2)), (self.samp_rate/self.fft_resolution))

    def get_decimation(self):
        return self.decimation

    def set_decimation(self, decimation):
        self.decimation = decimation
        self.freq_xlating_fir_filter_xxx_0.set_taps( firdes.low_pass(1,self.samp_rate,self.samp_rate/self.decimation/8,1000))

    def get_carrier_squelch(self):
        return self.carrier_squelch

    def set_carrier_squelch(self, carrier_squelch):
        self.carrier_squelch = carrier_squelch

    def get_audio_gain(self):
        return self.audio_gain

    def set_audio_gain(self, audio_gain):
        self.audio_gain = audio_gain
        self.blocks_float_to_short_0.set_scale(self.audio_gain)

    def get_AudioStreamPort(self):
        return self.AudioStreamPort

    def set_AudioStreamPort(self, AudioStreamPort):
        self.AudioStreamPort = AudioStreamPort
        Qt.QMetaObject.invokeMethod(self._AudioStreamPort_line_edit, "setText", Qt.Q_ARG("QString", str(self.AudioStreamPort)))

    def get_AudioStreamIP(self):
        return self.AudioStreamIP

    def set_AudioStreamIP(self, AudioStreamIP):
        self.AudioStreamIP = AudioStreamIP
        Qt.QMetaObject.invokeMethod(self._AudioStreamIP_line_edit, "setText", Qt.Q_ARG("QString", str(self.AudioStreamIP)))




def main(top_block_cls=airbandtuner, options=None):

    if StrictVersion("4.5.0") <= StrictVersion(Qt.qVersion()) < StrictVersion("5.0.0"):
        style = gr.prefs().get_string('qtgui', 'style', 'raster')
        Qt.QApplication.setGraphicsSystem(style)
    qapp = Qt.QApplication(sys.argv)

    tb = top_block_cls()

    tb.start()

    tb.show()

    def sig_handler(sig=None, frame=None):
        tb.stop()
        tb.wait()

        Qt.QApplication.quit()

    signal.signal(signal.SIGINT, sig_handler)
    signal.signal(signal.SIGTERM, sig_handler)

    timer = Qt.QTimer()
    timer.start(500)
    timer.timeout.connect(lambda: None)

    qapp.exec_()

if __name__ == '__main__':
    main()
