#!/usr/bin/env python3
# -*- coding: utf-8 -*-

#
# SPDX-License-Identifier: GPL-3.0
#
# GNU Radio Python Flow Graph
# Title: AirBandTuner
# Author: JoeTester1965
# Copyright: MIT license
# GNU Radio version: 3.10.3.0

from packaging.version import Version as StrictVersion

if __name__ == '__main__':
    import ctypes
    import sys
    if sys.platform.startswith('linux'):
        try:
            x11 = ctypes.cdll.LoadLibrary('libX11.so')
            x11.XInitThreads()
        except:
            print("Warning: failed to XInitThreads()")

from PyQt5 import Qt
from gnuradio import eng_notation
from gnuradio import qtgui
import sip
from gnuradio import analog
from gnuradio import audio
from gnuradio import blocks
from gnuradio import filter
from gnuradio.filter import firdes
from gnuradio import gr
from gnuradio.fft import window
import sys
import signal
from argparse import ArgumentParser
from gnuradio.eng_arg import eng_float, intx
from gnuradio import zeromq
from gnuradio.fft import logpwrfft
from gnuradio.qtgui import Range, RangeWidget
from PyQt5 import QtCore
from xmlrpc.server import SimpleXMLRPCServer
import threading
import osmosdr
import time



from gnuradio import qtgui

class airbandtuner(gr.top_block, Qt.QWidget):

    def __init__(self):
        gr.top_block.__init__(self, "AirBandTuner", catch_exceptions=True)
        Qt.QWidget.__init__(self)
        self.setWindowTitle("AirBandTuner")
        qtgui.util.check_set_qss()
        try:
            self.setWindowIcon(Qt.QIcon.fromTheme('gnuradio-grc'))
        except:
            pass
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
        except:
            pass

        ##################################################
        # Variables
        ##################################################
        self.tuning_freq = tuning_freq = 135e6
        self.samp_rate = samp_rate = 1.92e6
        self.rtl_ppm = rtl_ppm = (-1)
        self.rtl_device_arguments = rtl_device_arguments = ''
        self.hold_seconds = hold_seconds = 5
        self.gain = gain = 45
        self.fft_resolution = fft_resolution = 4096
        self.decimation = decimation = 40
        self.carrier_squelch = carrier_squelch = (-40)
        self.audio_squelch = audio_squelch = (-8)
        self.audio_gain = audio_gain = 1.0

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
        self._rtl_ppm_tool_bar = Qt.QToolBar(self)
        self._rtl_ppm_tool_bar.addWidget(Qt.QLabel("'rtl_ppm'" + ": "))
        self._rtl_ppm_line_edit = Qt.QLineEdit(str(self.rtl_ppm))
        self._rtl_ppm_tool_bar.addWidget(self._rtl_ppm_line_edit)
        self._rtl_ppm_line_edit.returnPressed.connect(
            lambda: self.set_rtl_ppm(int(str(self._rtl_ppm_line_edit.text()))))
        self.top_grid_layout.addWidget(self._rtl_ppm_tool_bar, 1, 1, 1, 1)
        for r in range(1, 2):
            self.top_grid_layout.setRowStretch(r, 1)
        for c in range(1, 2):
            self.top_grid_layout.setColumnStretch(c, 1)
        self._rtl_device_arguments_tool_bar = Qt.QToolBar(self)
        self._rtl_device_arguments_tool_bar.addWidget(Qt.QLabel("'rtl_device_arguments'" + ": "))
        self._rtl_device_arguments_line_edit = Qt.QLineEdit(str(self.rtl_device_arguments))
        self._rtl_device_arguments_tool_bar.addWidget(self._rtl_device_arguments_line_edit)
        self._rtl_device_arguments_line_edit.returnPressed.connect(
            lambda: self.set_rtl_device_arguments(str(str(self._rtl_device_arguments_line_edit.text()))))
        self.top_grid_layout.addWidget(self._rtl_device_arguments_tool_bar, 1, 0, 1, 1)
        for r in range(1, 2):
            self.top_grid_layout.setRowStretch(r, 1)
        for c in range(0, 1):
            self.top_grid_layout.setColumnStretch(c, 1)
        self._gain_range = Range(0, 49, 1, 45, 200)
        self._gain_win = RangeWidget(self._gain_range, self.set_gain, "'gain'", "counter_slider", int, QtCore.Qt.Horizontal)
        self.top_grid_layout.addWidget(self._gain_win, 0, 1, 1, 1)
        for r in range(0, 1):
            self.top_grid_layout.setRowStretch(r, 1)
        for c in range(1, 2):
            self.top_grid_layout.setColumnStretch(c, 1)
        self._audio_squelch_range = Range((-30), 0, 1, (-8), 200)
        self._audio_squelch_win = RangeWidget(self._audio_squelch_range, self.set_audio_squelch, "'audio_squelch'", "counter_slider", int, QtCore.Qt.Horizontal)
        self.top_grid_layout.addWidget(self._audio_squelch_win, 2, 1, 1, 1)
        for r in range(2, 3):
            self.top_grid_layout.setRowStretch(r, 1)
        for c in range(1, 2):
            self.top_grid_layout.setColumnStretch(c, 1)
        self.zeromq_pull_msg_source_0 = zeromq.pull_msg_source('tcp://127.0.0.1:50241', 100, False)
        self.zeromq_pub_sink_1 = zeromq.pub_sink(gr.sizeof_float, fft_resolution, 'tcp://127.0.0.1:50242', 100, False, (-1), '')
        self.xmlrpc_server_0 = SimpleXMLRPCServer(('localhost', 50240), allow_none=True)
        self.xmlrpc_server_0.register_instance(self)
        self.xmlrpc_server_0_thread = threading.Thread(target=self.xmlrpc_server_0.serve_forever)
        self.xmlrpc_server_0_thread.daemon = True
        self.xmlrpc_server_0_thread.start()
        self.rtlsdr_source_0 = osmosdr.source(
            args="numchan=" + str(1) + " " + rtl_device_arguments
        )
        self.rtlsdr_source_0.set_sample_rate(samp_rate)
        self.rtlsdr_source_0.set_center_freq(tuning_freq, 0)
        self.rtlsdr_source_0.set_freq_corr(rtl_ppm, 0)
        self.rtlsdr_source_0.set_dc_offset_mode(2, 0)
        self.rtlsdr_source_0.set_iq_balance_mode(2, 0)
        self.rtlsdr_source_0.set_gain_mode(False, 0)
        self.rtlsdr_source_0.set_gain(gain, 0)
        self.rtlsdr_source_0.set_if_gain(1, 0)
        self.rtlsdr_source_0.set_bb_gain(1, 0)
        self.rtlsdr_source_0.set_antenna('', 0)
        self.rtlsdr_source_0.set_bandwidth(0, 0)
        self.qtgui_vector_sink_f_0 = qtgui.vector_sink_f(
            fft_resolution,
            (tuning_freq - (samp_rate/2)),
            (samp_rate/fft_resolution),
            'Frequency',
            'Power',
            "",
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
        self.logpwrfft_x_0 = logpwrfft.logpwrfft_c(
            sample_rate=samp_rate,
            fft_size=fft_resolution,
            ref_scale=2,
            frame_rate=10,
            avg_alpha=1.0,
            average=False,
            shift=True)
        self._hold_seconds_range = Range(1, 30, 1, 5, 200)
        self._hold_seconds_win = RangeWidget(self._hold_seconds_range, self.set_hold_seconds, "'hold_seconds'", "counter_slider", int, QtCore.Qt.Horizontal)
        self.top_grid_layout.addWidget(self._hold_seconds_win, 4, 1, 1, 1)
        for r in range(4, 5):
            self.top_grid_layout.setRowStretch(r, 1)
        for c in range(1, 2):
            self.top_grid_layout.setColumnStretch(c, 1)
        self.freq_xlating_fir_filter_xxx_0 = filter.freq_xlating_fir_filter_ccc(decimation,  firdes.low_pass(1,samp_rate,samp_rate/decimation/8,1000), 0, samp_rate)
        self._carrier_squelch_tool_bar = Qt.QToolBar(self)
        self._carrier_squelch_tool_bar.addWidget(Qt.QLabel("'carrier_squelch'" + ": "))
        self._carrier_squelch_line_edit = Qt.QLineEdit(str(self.carrier_squelch))
        self._carrier_squelch_tool_bar.addWidget(self._carrier_squelch_line_edit)
        self._carrier_squelch_line_edit.returnPressed.connect(
            lambda: self.set_carrier_squelch(int(str(self._carrier_squelch_line_edit.text()))))
        self.top_grid_layout.addWidget(self._carrier_squelch_tool_bar, 2, 0, 1, 1)
        for r in range(2, 3):
            self.top_grid_layout.setRowStretch(r, 1)
        for c in range(0, 1):
            self.top_grid_layout.setColumnStretch(c, 1)
        self.blocks_multiply_const_vxx_0 = blocks.multiply_const_ff(audio_gain)
        self.audio_sink_0 = audio.sink(48000, '', True)
        self.analog_pwr_squelch_xx_0 = analog.pwr_squelch_cc(audio_squelch, (1e-4), 1024, False)
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
        self.connect((self.analog_am_demod_cf_0, 0), (self.blocks_multiply_const_vxx_0, 0))
        self.connect((self.analog_feedforward_agc_cc_0, 0), (self.analog_pwr_squelch_xx_0, 0))
        self.connect((self.analog_pwr_squelch_xx_0, 0), (self.analog_am_demod_cf_0, 0))
        self.connect((self.blocks_multiply_const_vxx_0, 0), (self.audio_sink_0, 0))
        self.connect((self.freq_xlating_fir_filter_xxx_0, 0), (self.analog_feedforward_agc_cc_0, 0))
        self.connect((self.logpwrfft_x_0, 0), (self.qtgui_vector_sink_f_0, 0))
        self.connect((self.logpwrfft_x_0, 0), (self.zeromq_pub_sink_1, 0))
        self.connect((self.rtlsdr_source_0, 0), (self.freq_xlating_fir_filter_xxx_0, 0))
        self.connect((self.rtlsdr_source_0, 0), (self.logpwrfft_x_0, 0))


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
        self.rtlsdr_source_0.set_center_freq(self.tuning_freq, 0)

    def get_samp_rate(self):
        return self.samp_rate

    def set_samp_rate(self, samp_rate):
        self.samp_rate = samp_rate
        self.freq_xlating_fir_filter_xxx_0.set_taps( firdes.low_pass(1,self.samp_rate,self.samp_rate/self.decimation/8,1000))
        self.logpwrfft_x_0.set_sample_rate(self.samp_rate)
        self.qtgui_vector_sink_f_0.set_x_axis((self.tuning_freq - (self.samp_rate/2)), (self.samp_rate/self.fft_resolution))
        self.rtlsdr_source_0.set_sample_rate(self.samp_rate)

    def get_rtl_ppm(self):
        return self.rtl_ppm

    def set_rtl_ppm(self, rtl_ppm):
        self.rtl_ppm = rtl_ppm
        Qt.QMetaObject.invokeMethod(self._rtl_ppm_line_edit, "setText", Qt.Q_ARG("QString", str(self.rtl_ppm)))
        self.rtlsdr_source_0.set_freq_corr(self.rtl_ppm, 0)

    def get_rtl_device_arguments(self):
        return self.rtl_device_arguments

    def set_rtl_device_arguments(self, rtl_device_arguments):
        self.rtl_device_arguments = rtl_device_arguments
        Qt.QMetaObject.invokeMethod(self._rtl_device_arguments_line_edit, "setText", Qt.Q_ARG("QString", str(self.rtl_device_arguments)))

    def get_hold_seconds(self):
        return self.hold_seconds

    def set_hold_seconds(self, hold_seconds):
        self.hold_seconds = hold_seconds

    def get_gain(self):
        return self.gain

    def set_gain(self, gain):
        self.gain = gain
        self.rtlsdr_source_0.set_gain(self.gain, 0)

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
        Qt.QMetaObject.invokeMethod(self._carrier_squelch_line_edit, "setText", Qt.Q_ARG("QString", str(self.carrier_squelch)))

    def get_audio_squelch(self):
        return self.audio_squelch

    def set_audio_squelch(self, audio_squelch):
        self.audio_squelch = audio_squelch
        self.analog_pwr_squelch_xx_0.set_threshold(self.audio_squelch)

    def get_audio_gain(self):
        return self.audio_gain

    def set_audio_gain(self, audio_gain):
        self.audio_gain = audio_gain
        self.blocks_multiply_const_vxx_0.set_k(self.audio_gain)




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
