"""
[[
	Surface:	MiniLab3
	Developer:	Farès MEZDOUR
	Version:	1.0.1

    Copyright (c) 2022 Farès MEZDOUR
]]
"""

import time
import channels
import transport
import mixer
import ui
from MiniLab3Dispatch import send_to_device

# MIT License
# Copyright (c) 2020 Ray Juang

PLAY_STATUS = [0x00, 0x02]
REC_STATUS = [0x00, 0x03]

class MiniLabDisplay:
    """ Manages scrolling display of two lines so that long strings can be scrolled on each line. """
    def __init__(self):
        # Holds the text to display on first line. May exceed the 16-char display limit.
        self._line1 = ' '
        # Holds the text to display on second line. May exceed the 16-char display limit.
        self._line2 = ' '
        # Sets the kind of display
        self._page_type = ' '

        # Holds ephemeral text that will expire after the expiration timestamp. These lines will display if the
        # the expiration timestamp is > current timestamp.
        self._ephemeral_line1 = ' '
        self._ephemeral_line2 = ' '
        self._expiration_time_ms = 0

        # Holds the starting offset of where the line1 text should start.
        self._line1_display_offset = 0
        
        # Holds the starting offset of where the line2 text should start.
        self._line2_display_offset = 0
        
        # Last timestamp in milliseconds in which the text was updated.
        self._last_update_ms = 0
        
        # Minimum interval before text is scrolled
        self._scroll_interval_ms = 1000
        
        # How many characters to allow last char to scroll before starting over.
        self._end_padding = 0
        
        # Track what's currently being displayed
        self._last_payload = bytes()
        
    def _get_line1_bytes(self):
        # Get up to 32-bytes the exact chars to display for line 1.
        start_pos = self._line1_display_offset
        end_pos = start_pos + 31
        line_src = self._get_line_src(self._line1)
        if self._expiration_time_ms > self.time_ms():
            line_src = self._get_line_src(self._ephemeral_line1)
        return bytearray(line_src[start_pos:end_pos], 'ascii')

    def _get_line2_bytes(self):
        # Get up to 32-bytes the exact chars to display for line 2.
        start_pos = self._line2_display_offset
        end_pos = start_pos + 31
        line_src = self._get_line_src(self._line2)
        if self._expiration_time_ms > self.time_ms():
            line_src = self._get_line_src(self._ephemeral_line2)
        return bytearray(line_src[start_pos:end_pos], 'ascii')

    def _get_new_offset(self, start_pos, line_src):
        end_pos = start_pos + 31
        if end_pos >= len(line_src) + self._end_padding or len(line_src) <= 20:
            return 0
        else:
            return start_pos + 1

    def _update_scroll_pos(self):
        current_time_ms = self.time_ms()
        if current_time_ms >= self._scroll_interval_ms + self._last_update_ms:
            self._line1_display_offset = self._get_new_offset(self._line1_display_offset, self._line1)
            self._line2_display_offset = self._get_new_offset(self._line2_display_offset, self._line2)
            self._last_update_ms = current_time_ms

    @staticmethod
    def time_ms():
        # Get the current timestamp in milliseconds
        return time.monotonic() * 1000


    def _refresh_display(self, page_type, value):
        # Internally called to refresh the display now.
        string = []
        
        data_control = bytes([])
        data_string = bytes([0x04, 0x02, 0x60])
        data_line1 = bytes([0x01]) + self._get_line1_bytes() + bytes([0x00])
        data_line2 = bytes([0x02]) + self._get_line2_bytes() + bytes([0x00])
        #data += bytes([0x7F])
        
        if page_type == 1 :
            #print("Defaut")
            #Defaut Screen
            data_control = bytes([])
        
        elif page_type == 2 :
            #print("Two Lines")
            #Two Lines Screen
            data_control += bytes([0x1F, 0x02, 0x01, 0x00])
            
        elif page_type == 3 :
            #print("Encoder")
            #Encoder Screen
            scaled_value = int(int(value)*127/100)
            data_control += bytes([0x1F, 0x03, 0x01, scaled_value, 0x00, 0x00])
            
        elif page_type == 4 :
            #print("Fader")
            #Fader Screen
            scaled_value = int(int(value)*127/100)
            data_control += bytes([0x1F, 0x04, 0x01, scaled_value, 0x00, 0x00])
            
        elif page_type == 5 :
            #print("scroll")
            #Scroll Screen
            data_control += bytes([0x1F, 0x05, 0x01, 0x00, 0x00, 0x00])
            
        elif page_type == 10 :
            #print("Picto")
            #Picto Screen
            data_control += bytes([0x1F, 0x07, 0x01, REC_STATUS[transport.isRecording()], PLAY_STATUS[transport.isPlaying() != 0], 0x01, 0x00])
            
        
        string = data_string + data_control + data_line1 + data_line2

        #self._update_scroll_pos()
        if self._last_payload != string:
            send_to_device(string)
            #print(page_type)
            self._last_payload = string

    def ResetScroll(self):
        self._line1_display_offset = 0
        self._line2_display_offset = 0



    def SetLines(self, page_type, value, line1=None, line2=None, expires=None):
        """ Update lines on the display, or leave alone if not provided.

        :param line1:    first line to update display with or None to leave as is.
        :param line2:    second line to update display with or None to leave as is.
        :param type:     sets the type of display
        :param expires:  number of milliseconds that the line persists before expiring. Note that when an expiration
            interval is provided, lines are interpreted as a blank line if not provided.
        """
        if expires is None:
            if line1 is not None:
                self._line1 = line1
            if line2 is not None:
                self._line2 = line2
        else:
            self._expiration_time_ms = self.time_ms() + expires
            if line1 is not None:
                self._ephemeral_line1 = line1
            if line2 is not None:
                self._ephemeral_line2 = line2

        self._refresh_display(page_type, value)
        return self

    def Refresh(self, page_type, value):
        """ Called to refresh the display, possibly with updated text. """
        if self.time_ms() - self._last_update_ms >= self._scroll_interval_ms:
            self._refresh_display(page_type, value)
        return self
        
# device.midiOutSysex(bytes([0xF0, 0x00, 0x20, 0x6B, 0x7F, 0x42]) + data + bytes([0xF7]))

    def _get_line_src(self, line) :

        is_ascii = True
        for i in line :
            if ord(i) not in range (0,128) :          #Undefined char '?'
                is_ascii = False
        
        if is_ascii :
            line_src = line
        else :
            line_src = "Undefined text"
        
        return line_src