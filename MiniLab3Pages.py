"""
[[
	Surface:	MiniLab3
	Developer:	Farès MEZDOUR
	Version:	1.0.1

    Copyright (c) 2022 Farès MEZDOUR
]]
"""

from MiniLab3Display import MiniLabDisplay
import device

# MIT License
# Copyright (c) 2020 Ray Juang

class MiniLabPagedDisplay:
    def __init__(self, display):
        self._display = display
        
        # String line 1
        self._line1 = {}
        
        # String line 2
        self._line2 = {}
        
        # Active page to display or None for default display
        self._active_page = None
        
        # Temporary page to display or None for default display
        self._ephemeral_page = None
        
        # Timestamp after which to switch back to active page.
        self._page_expiration_time_ms = 0
        
        # Last timestamp in milliseconds in which the text was updated.
        self._last_update_ms = 0
        
        self._page_type = 2
        self._value = 0

    def SetPageLines(self, page_name, page_type=2, value=0, line1=None, line2=None):
        self._page_type = page_type
        self._value = value
        if line1 is not None:
            self._line1[page_name] = lambda: line1
        if line2 is not None:
            self._line2[page_name] = lambda: line2
        if self._active_page == page_name:
            self._update_display()


    def SetActivePage(self, page_name, expires=None):
        if expires is not None:
            self._ephemeral_page = page_name
            self._page_expiration_time_ms = MiniLabDisplay.time_ms() + expires
        else:
            self._active_page = page_name
        self._update_display()
        


    def display(self):
        return self._display

    def _update_display(self):
        active_page = self._active_page
        self._last_update_ms = MiniLabDisplay.time_ms()
        if self._last_update_ms < self._page_expiration_time_ms:
            active_page = self._ephemeral_page
        else :
            self._page_type = 10

        if active_page is not None:
            line1 = None
            line2 = None
            if active_page in self._line1:
                line1 = self._line1[active_page]()
            if active_page in self._line2:
                line2 = self._line2[active_page]()
            #print(self._page_type)
            self._display.SetLines(self._page_type, self._value, line1=line1, line2=line2)

    def Refresh(self):
        self._update_display()
        self._display.Refresh(self._page_type, self._value)
