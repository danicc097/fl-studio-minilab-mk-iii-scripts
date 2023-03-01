# name=MiniLab 3 DEV
# supportedHardwareIds=00 20 6B 02 00 04 04

"""
[[
	Surface:	MiniLab3
	Developer:	Farès MEZDOUR
	Version:	1.0.1

    Copyright (c) 2022 Farès MEZDOUR
]]
"""


import time
import ui
import channels
import patterns
import plugins
import device




from MiniLab3Process import MiniLabMidiProcessor
from MiniLab3Return import MiniLabLightReturn
from MiniLab3Display import MiniLabDisplay
from MiniLab3Pages import MiniLabPagedDisplay
from MiniLab3Connexion import MiniLabConnexion
import ArturiaVCOL

## CONSTANT

TEMP = 0.5
COLOUR = [0x10,0x11,0x04,0x05,0x14,0x7F,0x01]
PORT_MIDICC_ANALOGLAB = 10

#-----------------------------------------------------------------------------------------

# This is the master class. It will run the init lights pattern
# and call the others class to process MIDI events


class MidiControllerConfig :

    def __init__(self):
        self._lightReturn = MiniLabLightReturn()
        self._display = MiniLabDisplay()
        self._paged_display = MiniLabPagedDisplay(self._display)
        self._connexion = MiniLabConnexion()
        self._disp = 0


    def LightReturn(self) :
        return self._lightReturn

    def display(self):
        return self._display

    def paged_display(self):
        return self._paged_display

    def connexion(self) :
        return self._connexion

    def Idle(self):
        self._paged_display.Refresh()

    def Sync(self):
        # Update display

        active_index = channels.selectedChannel()
        channel_name = channels.getChannelName(active_index)
        for i in range(len(channel_name)) :
            if (ord(channel_name[i]) not in range(0,127)) :
                str1 = channel_name[0:i]
                str2 = channel_name[i+1::]
                channel_name = str1 + '?' + str2
        pattern_number = patterns.patternNumber()
        pattern_name = patterns.getPatternName(pattern_number)

        if active_index != -1 :
            self._paged_display.SetPageLines(
                'main',
                10,
                line1='%d-%s' % (active_index + 1, channel_name),
                line2='%s' % pattern_name
                )
            self.paged_display().SetActivePage('main', 1500)

        else :
            self._paged_display.SetPageLines(
                'main',
                10,
                line1='No Selection',
                line2='%s' % pattern_name
                )
            self.paged_display().SetActivePage('main', 1500)


#----------------------------------------------------------------------------------------

# Function called for each event


def OnMidiMsg(event) :
    # print(event)
    if _processor.ProcessEvent(event):
        event.handled = False


# Function called when FL Studio is starting

def OnInit():
    print('Loaded MIDI script for Arturia MiniLab 3')
    init()
    _mk3.LightReturn().init()
    _mk3.Sync()
    _mk3.paged_display().SetPageLines('welcome', 10, line1=ui.getProgTitle(), line2="Connected")
    _mk3.paged_display().SetActivePage('welcome', expires=1500)
    _mk3.paged_display().SetActivePage('main')
    print("### Messages successfully sent to MINILAB3 ###")



def init() :

    # Connxexion
    global _mk3
    _mk3 = MidiControllerConfig()
    global _processor
    _processor = MiniLabMidiProcessor(_mk3)
    _mk3.connexion().DAWConnexion()
    print("### Successfully created class objects ###")

    global old_pitch
    old_pitch = 0



# Handles the script when FL Studio closes

def OnDeInit():
    # Deconnxexion
    # _mk3.paged_display().SetPageLines('goodbye1', 12, line1=ui.getProgTitle(), line2="Disconnected")
    # _mk3.paged_display().SetActivePage('goodbye1', 1500)
    _mk3.connexion().DAWDisconnection()
    #_mk3.connexion().ArturiaDisconnection()
    time.sleep(2)
    return


# Function called when Play/Pause button is ON

def OnUpdateBeatIndicator(value):
    _mk3.LightReturn().ProcessPlayBlink(value)
    _mk3.LightReturn().ProcessRecordBlink(value)


# Function called at refresh, flag value changes depending on the refresh type

def OnRefresh(flags) :
    _mk3.LightReturn().RecordReturn()
    _mk3.LightReturn().PlayReturn()
    _mk3.LightReturn().LoopReturn()

    if plugins.isValid(channels.selectedChannel()) :
        string = plugins.getPluginName(channels.selectedChannel())
        if string in ArturiaVCOL.V_COL :
        #     _mk3.connexion().ArturiaConnexion()
        # else :
            if not ui.getFocused(5) :
                _mk3.connexion().ArturiaDisconnection()
            else :
                _mk3.connexion().ArturiaConnexion()
        # else :
        #     if not ui.getFocused(5) :
        #         _mk3.connexion().ArturiaDisconnection()
        else :
            _mk3.connexion().ArturiaDisconnection()
    else :
        _mk3.connexion().ArturiaDisconnection()


    #print("flags : ", flags)
    if flags not in [4,256,260,4608] :
        _mk3.Sync()



# Function called time to time mainly to update the beat indicator

def OnIdle():
    _mk3.Idle()


def OnPitchBend(event) :
    global old_pitch

    pitch = (event.data2-64)*(200/64)
    if pitch == 0: # releasing press
        if old_pitch > 0:
            ui.up()
        else:
            ui.down()
    old_pitch = pitch

    if channels.selectedChannel(1) != -1 :
        if plugins.isValid(channels.selectedChannel()) :
            if plugins.getPluginName(channels.selectedChannel()) not in ArturiaVCOL.V_COL :
                channels.setChannelPitch(channels.selectedChannel(),(event.data2-64)*(200/64),1)
                event.handled = True
            else :
                device.forwardMIDICC(event.status + (event.data1 << 8) + (event.data2 << 16) + (PORT_MIDICC_ANALOGLAB << 24))
                event.handled = True
