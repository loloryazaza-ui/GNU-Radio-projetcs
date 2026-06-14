#!/usr/bin/env python3
# -*- coding: utf-8 -*-

#
# SPDX-License-Identifier: GPL-3.0
#
# GNU Radio Python Flow Graph
# Title: Not titled yet
# Author: Mikhail
# GNU Radio version: 3.10.12.0

from PyQt5 import Qt
from gnuradio import qtgui
from PyQt5 import QtCore
from gnuradio import analog
from gnuradio import audio
from gnuradio import blocks
from gnuradio import filter
from gnuradio.filter import firdes
from gnuradio import gr
from gnuradio.fft import window
import sys
import signal
from PyQt5 import Qt
from argparse import ArgumentParser
from gnuradio.eng_arg import eng_float, intx
from gnuradio import eng_notation
import sip
import threading



class AM_project(gr.top_block, Qt.QWidget):

    def __init__(self):
        gr.top_block.__init__(self, "Not titled yet", catch_exceptions=True)
        Qt.QWidget.__init__(self)
        self.setWindowTitle("Not titled yet")
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

        self.settings = Qt.QSettings("gnuradio/flowgraphs", "AM_project")

        try:
            geometry = self.settings.value("geometry")
            if geometry:
                self.restoreGeometry(geometry)
        except BaseException as exc:
            print(f"Qt GUI: Could not restore geometry: {str(exc)}", file=sys.stderr)
        self.flowgraph_started = threading.Event()

        ##################################################
        # Variables
        ##################################################
        self.samp_rate = samp_rate = int(2000000)
        self.freq = freq = 100e6
        self.decim = decim = 16
        self.TX_RF = TX_RF = 0
        self.TX_IF = TX_IF = 0
        self.RX_if = RX_if = 0
        self.RX_amp_on = RX_amp_on = 0
        self.RX_BB = RX_BB = 0

        ##################################################
        # Blocks
        ##################################################

        self.qtgui_sink_x_0_0 = qtgui.sink_c(
            1024, #fftsize
            window.WIN_BLACKMAN_hARRIS, #wintype
            0, #fc
            samp_rate, #bw
            "RX output", #name
            True, #plotfreq
            True, #plotwaterfall
            True, #plottime
            True, #plotconst
            None # parent
        )
        self.qtgui_sink_x_0_0.set_update_time(1.0/10)
        self._qtgui_sink_x_0_0_win = sip.wrapinstance(self.qtgui_sink_x_0_0.qwidget(), Qt.QWidget)

        self.qtgui_sink_x_0_0.enable_rf_freq(False)

        self.top_layout.addWidget(self._qtgui_sink_x_0_0_win)
        self.freq_xlating_fir_filter_xxx_0 = filter.freq_xlating_fir_filter_fcc(decim, firdes.low_pass(1,samp_rate,samp_rate/(2*decim), 2000), 48e3, samp_rate)
        self.blocks_wavfile_source_0 = blocks.wavfile_source('./WASP.mp3', True)
        self.blocks_repeat_0 = blocks.repeat(gr.sizeof_float*1, 16)
        self.blocks_multiply_xx_0 = blocks.multiply_vff(1)
        self.blocks_multiply_const_vxx_1 = blocks.multiply_const_ff(0.5)
        self.blocks_multiply_const_vxx_0 = blocks.multiply_const_ff(1.2)
        self.blocks_float_to_complex_0 = blocks.float_to_complex(1)
        self.blocks_complex_to_mag_0 = blocks.complex_to_mag(1)
        self.blocks_complex_to_float_0 = blocks.complex_to_float(1)
        self.blocks_add_const_vxx_0 = blocks.add_const_ff(1)
        self.band_pass_filter_0 = filter.fir_filter_fff(
            1,
            firdes.band_pass(
                1,
                48e3,
                500,
                6e3,
                400,
                window.WIN_HAMMING,
                6.76))
        self.audio_sink_0 = audio.sink(48000, '', True)
        self.analog_sig_source_x_0 = analog.sig_source_f(samp_rate, analog.GR_COS_WAVE, 48000, 0.5, 0, 0)
        self.analog_agc_xx_0 = analog.agc_cc((6.25e-4), 1.0, 1.0, 65536)
        self._TX_RF_range = qtgui.Range(0, 1, 1, 0, 200)
        self._TX_RF_win = qtgui.RangeWidget(self._TX_RF_range, self.set_TX_RF, "'TX_RF'", "counter_slider", float, QtCore.Qt.Horizontal)
        self.top_layout.addWidget(self._TX_RF_win)
        self._TX_IF_range = qtgui.Range(0, 47, 1, 0, 200)
        self._TX_IF_win = qtgui.RangeWidget(self._TX_IF_range, self.set_TX_IF, "'TX_IF'", "counter_slider", float, QtCore.Qt.Horizontal)
        self.top_layout.addWidget(self._TX_IF_win)
        self._RX_if_range = qtgui.Range(0, 40, 8, 0, 200)
        self._RX_if_win = qtgui.RangeWidget(self._RX_if_range, self.set_RX_if, "'RX_if'", "counter_slider", float, QtCore.Qt.Horizontal)
        self.top_layout.addWidget(self._RX_if_win)
        self._RX_amp_on_range = qtgui.Range(0, 1, 1, 0, 200)
        self._RX_amp_on_win = qtgui.RangeWidget(self._RX_amp_on_range, self.set_RX_amp_on, "'RX_amp_on'", "counter_slider", float, QtCore.Qt.Horizontal)
        self.top_layout.addWidget(self._RX_amp_on_win)
        self._RX_BB_range = qtgui.Range(0, 62, 2, 0, 200)
        self._RX_BB_win = qtgui.RangeWidget(self._RX_BB_range, self.set_RX_BB, "'RX_BB'", "counter_slider", float, QtCore.Qt.Horizontal)
        self.top_layout.addWidget(self._RX_BB_win)


        ##################################################
        # Connections
        ##################################################
        self.connect((self.analog_agc_xx_0, 0), (self.blocks_complex_to_mag_0, 0))
        self.connect((self.analog_sig_source_x_0, 0), (self.blocks_multiply_xx_0, 1))
        self.connect((self.band_pass_filter_0, 0), (self.blocks_multiply_const_vxx_1, 0))
        self.connect((self.blocks_add_const_vxx_0, 0), (self.blocks_multiply_xx_0, 0))
        self.connect((self.blocks_complex_to_float_0, 0), (self.freq_xlating_fir_filter_xxx_0, 0))
        self.connect((self.blocks_complex_to_mag_0, 0), (self.band_pass_filter_0, 0))
        self.connect((self.blocks_float_to_complex_0, 0), (self.blocks_complex_to_float_0, 0))
        self.connect((self.blocks_float_to_complex_0, 0), (self.qtgui_sink_x_0_0, 0))
        self.connect((self.blocks_multiply_const_vxx_0, 0), (self.blocks_add_const_vxx_0, 0))
        self.connect((self.blocks_multiply_const_vxx_1, 0), (self.audio_sink_0, 0))
        self.connect((self.blocks_multiply_xx_0, 0), (self.blocks_float_to_complex_0, 1))
        self.connect((self.blocks_multiply_xx_0, 0), (self.blocks_float_to_complex_0, 0))
        self.connect((self.blocks_repeat_0, 0), (self.blocks_multiply_const_vxx_0, 0))
        self.connect((self.blocks_wavfile_source_0, 0), (self.blocks_repeat_0, 0))
        self.connect((self.freq_xlating_fir_filter_xxx_0, 0), (self.analog_agc_xx_0, 0))


    def closeEvent(self, event):
        self.settings = Qt.QSettings("gnuradio/flowgraphs", "AM_project")
        self.settings.setValue("geometry", self.saveGeometry())
        self.stop()
        self.wait()

        event.accept()

    def get_samp_rate(self):
        return self.samp_rate

    def set_samp_rate(self, samp_rate):
        self.samp_rate = samp_rate
        self.analog_sig_source_x_0.set_sampling_freq(self.samp_rate)
        self.freq_xlating_fir_filter_xxx_0.set_taps(firdes.low_pass(1,self.samp_rate,self.samp_rate/(2*self.decim), 2000))
        self.qtgui_sink_x_0_0.set_frequency_range(0, self.samp_rate)

    def get_freq(self):
        return self.freq

    def set_freq(self, freq):
        self.freq = freq

    def get_decim(self):
        return self.decim

    def set_decim(self, decim):
        self.decim = decim
        self.freq_xlating_fir_filter_xxx_0.set_taps(firdes.low_pass(1,self.samp_rate,self.samp_rate/(2*self.decim), 2000))

    def get_TX_RF(self):
        return self.TX_RF

    def set_TX_RF(self, TX_RF):
        self.TX_RF = TX_RF

    def get_TX_IF(self):
        return self.TX_IF

    def set_TX_IF(self, TX_IF):
        self.TX_IF = TX_IF

    def get_RX_if(self):
        return self.RX_if

    def set_RX_if(self, RX_if):
        self.RX_if = RX_if

    def get_RX_amp_on(self):
        return self.RX_amp_on

    def set_RX_amp_on(self, RX_amp_on):
        self.RX_amp_on = RX_amp_on

    def get_RX_BB(self):
        return self.RX_BB

    def set_RX_BB(self, RX_BB):
        self.RX_BB = RX_BB




def main(top_block_cls=AM_project, options=None):

    qapp = Qt.QApplication(sys.argv)

    tb = top_block_cls()

    tb.start()
    tb.flowgraph_started.set()

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
