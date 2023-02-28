"""
[[
	Surface:	MiniLab3
	Developer:	Farès MEZDOUR
	Version:	1.0.1

    Copyright (c) 2022 Farès MEZDOUR
]]
"""

import transport
import ui
import channels
import patterns
import mixer


# This class allows FL Studio to send hint messages to Arturia KeyLab's screen

WidMixer = 0
WidChannelRack = 1
WidPlaylist = 2
WidBrowser = 4
WidPlugin = 5


class NavigationMode:
    def __init__(self, paged_display, display_ms= 1500):
        self._paged_display = paged_display
        self._display_ms = 2000
        self._modes = []
        self._active_index = 0


    def VolumeChRefresh(self, value, page_type) :
        value_disp = str(round(mixer.getTrackVolume(mixer.trackNumber())*100))
        track = str(mixer.trackNumber())
        self._paged_display.SetPageLines('Volume',
                                        page_type,
                                        value*100,
                                        line1= 'Volume - ' + track,
                                        line2= value_disp + '%'
                                        )
        self._paged_display.SetActivePage('Volume', expires=self._display_ms)


    def PanChRefresh(self, value, page_type) :
        track = str(mixer.trackNumber())
        value_disp = str(round(mixer.getTrackPan(mixer.trackNumber()) * 100))
        value_process = 100*(value+1)/2
        self._paged_display.SetPageLines('Pan',
                                        page_type,
                                        value_process,
                                        line1= 'Pan - ' + track,
                                        line2= value_disp + '%'
                                        )
        self._paged_display.SetActivePage('Pan', expires=self._display_ms)


    def StereoSepChRefresh(self, value, page_type) :
        track = str(mixer.trackNumber())
        value_disp = str(round(mixer.getTrackStereoSep(mixer.trackNumber()) * 100))
        value_process = 100*(value+1)/2
        self._paged_display.SetPageLines('Stereo',
                                        page_type,
                                        value_process,
                                        line1= 'Stereo - ' + track,
                                        line2= value_disp + '%'
                                        )
        self._paged_display.SetActivePage('Stereo', expires=self._display_ms)


    def SetRouteChRefresh(self, value, event, page_type) :
        track = str(mixer.trackNumber())
        value_disp = str(round(event.data2/127)*100)
        self._paged_display.SetPageLines('Route',
                                        page_type,
                                        value,
                                        line1= track + ' - To Master',
                                        line2= value_disp + '%'
                                        )
        self._paged_display.SetActivePage('Route', expires=self._display_ms)


    def NoPlugin(self) :
        if not ui.getFocused(WidPlugin) :
            self._paged_display.SetPageLines('NoPlugin',
                                            10,
                                            line1= 'No Plugin',
                                            line2= 'Focused'
                                            )
            self._paged_display.SetActivePage('NoPlugin', expires=self._display_ms)



    def PluginRefresh(self, parameter, value, mapped, HW_value, page_type) :
        if mapped == 1 :
            self._paged_display.SetPageLines('Param',
                                            page_type,
                                            value,
                                            line1= parameter,
                                            line2= value + "%"
                                            )
            self._paged_display.SetActivePage('Param', expires=3500)
        else :
            self._paged_display.SetPageLines('Param2',
                                            page_type,
                                            round(HW_value/127*100),
                                            line1= parameter,
                                            line2= str(HW_value)
                                            )
            self._paged_display.SetActivePage('Param2', expires=3500)


    def PlayRefresh(self) :
        if transport.isPlaying() != 0 :
            self._paged_display.SetPageLines('Play',
                                            10,
                                            line1= 'Play',
                                            line2= transport.getSongPosHint()
                                            )
            self._paged_display.SetActivePage('Play', expires=self._display_ms)
        else :
            self._paged_display.SetPageLines('Pause',
                                            10,
                                            line1= 'Pause',
                                            line2= transport.getSongPosHint()
                                            )
            self._paged_display.SetActivePage('Pause', expires=self._display_ms)


    def StopRefresh(self) :
        self._paged_display.SetPageLines('Stop',
                                        10,
                                        line1= 'Stop',
                                        line2= transport.getSongPosHint()
                                        )
        self._paged_display.SetActivePage('Stop', expires=self._display_ms)


    def RecordRefresh(self) :
        if transport.isRecording() :
            self._paged_display.SetPageLines('RecordOn',
                                            10,
                                            line1= 'Record',
                                            line2= 'ON'
                                            )
            self._paged_display.SetActivePage('RecordOn', expires=self._display_ms
            )
        else :
            self._paged_display.SetPageLines('RecordOff',
                                            10,
                                            line1= 'Record',
                                            line2= 'OFF'
                                            )
            self._paged_display.SetActivePage('RecordOff', expires=self._display_ms)


    def RewindRefresh(self) :
        self._paged_display.SetPageLines('Rewind',
                                        10,
                                        line1= 'Rewind <<',
                                        line2= transport.getSongPosHint()
                                        )
        self._paged_display.SetActivePage('Rewind', expires=self._display_ms)


    def FastForwardRefresh(self) :
        self._paged_display.SetPageLines('FastForward',
                                        10,
                                        line1= 'FastForward >>',
                                        line2= transport.getSongPosHint()
                                        )
        self._paged_display.SetActivePage('FastForward', expires=self._display_ms)


    def LoopRefresh(self) :
        if ui.isLoopRecEnabled() :
            self._paged_display.SetPageLines('LoopOn',
                                            10,
                                            line1= 'Loop Mode',
                                            line2= 'ON'
                                            )
            self._paged_display.SetActivePage('LoopOn', expires=self._display_ms)
        else :
            self._paged_display.SetPageLines('LoopOff',
                                            10,
                                            line1= 'Loop Mode',
                                            line2= 'OFF'
                                            )
            self._paged_display.SetActivePage('LoopOff', expires=self._display_ms)


    def OverdubRefresh(self) :
        self._paged_display.SetPageLines('Overdub',
                                        10,
                                        line1= 'Overdub Mode',
                                        line2= ''
                                        )
        self._paged_display.SetActivePage('Overdub', expires=self._display_ms)


    def CutRefresh(self) :
        channelnum = str(channels.channelNumber() + 1)
        patternnum = str(patterns.patternNumber())
        self._paged_display.SetPageLines('Cut',
                                        2,
                                        line1= 'Pattern ' + patternnum,
                                        line2= 'Chan ' + channelnum + ' CLEARED'
                                        )
        self._paged_display.SetActivePage('Cut', expires=self._display_ms)


    def UndoRefresh(self) :
        self._paged_display.SetPageLines('Undo',
                                        10,
                                        line1= 'Undo',
                                        line2= ''
                                        )
        self._paged_display.SetActivePage('Undo', expires=self._display_ms)


    def MetronomeRefresh(self) :
        if ui.isMetronomeEnabled() :
            self._paged_display.SetPageLines('MetroOn',
                                            10,
                                            line1= 'Metronome',
                                            line2= 'ON'
                                        )
            self._paged_display.SetActivePage('MetroOn', expires=self._display_ms)
        else :
            self._paged_display.SetPageLines('MetroOff',
                                            10,
                                            line1= 'Metronome',
                                            line2= 'OFF'
                                            )
            self._paged_display.SetActivePage('MetroOff', expires=self._display_ms)


    def Undo(self):
        # tempo = str(mixer.getCurrentTempo(0))
        self._paged_display.SetPageLines('UNDO', 10, line1= 'Undo', line2="Undo 2")
        self._paged_display.SetActivePage('UNDO', expires=self._display_ms)
        # if mixer.getCurrentTempo(0) > 99000 :
        #     tempo_str = tempo[:3]
        # else :
        #     tempo_str = tempo[:2]
        # self._paged_display.SetPageLines('Tempo',
        #                                 10,
        #                                 line1= 'Tempo',
        #                                 line2= tempo_str + ' BPM'
        #                                 )
        # self._paged_display.SetActivePage('Tempo', expires=self._display_ms)


    def SnapModeRefresh(self) :
        SNAP_MODE = {'0' : 'Line',
                     '1' : 'Cell',
                     '3' : 'None',
                     '4' : '1/6 Step',
                     '5' : '1/4 Step',
                     '6' : '1/3 Step',
                     '7' : '1/2 Step',
                     '8' : 'Step',
                     '9' : '1/6 Beat',
                     '10' : '1/4 Beat',
                     '11' : '1/3 Step',
                     '12' : '1/2 Beat',
                     '13' : 'Beat',
                     '14' : 'Bar'}
        cle = str(ui.getSnapMode())
        snap = SNAP_MODE.get(cle)
        self._paged_display.SetPageLines('Snap',
                                        10,
                                        line1= 'Snap Mode',
                                        line2= snap
                                        )
        self._paged_display.SetActivePage('Snap', expires=self._display_ms)




    def BrowserRefresh(self) :
        self._paged_display.SetPageLines('Browser',
                                        10,
                                        line1= 'Window',
                                        line2= 'BROWSER'
                                        )
        self._paged_display.SetActivePage('Browser', expires=self._display_ms)


    def ChannelRackRefresh(self) :
        self._paged_display.SetPageLines('ChannelRack',
                                        10,
                                        line1= 'Window',
                                        line2= 'CHANNEL RACK'
                                        )
        self._paged_display.SetActivePage('ChannelRack', expires=self._display_ms)




    def HintRefresh(self, string) :
        # for i in range(len(string)) : This is obsolete for chinease
        #     if (ord(string[i]) not in range(0,127)) :
        #         str1 = string[0:i]
        #         str2 = string[i+1::]
        #         string = str1 + '?' + str2
        if ui.isInPopupMenu() :
            # LABELS = {
                    # "Send to selected channel or focused plugin" : "Replace",
                    # "Open in new channel" : "New Channel",
                    # "Add to plugin database (flag as favorite)" : "Like",
                    # "Open Windows shell menu for this file" : "Windows menu",
                    # "Send file to the trash bin" : "Delete file"
                    # }
            self._paged_display.SetPageLines('Hintpopup',
                                        2,
                                        line1= 'Browser',
                                        line2= ui.getHintMsg()
                                        )
            self._paged_display.SetActivePage('Hintpopup', expires=5000)
        else :
            self._paged_display.SetPageLines('Hint',
                                            2,
                                            line1= 'Browser',
                                            line2= string
                                            )
            self._paged_display.SetActivePage('Hint', expires=3000)


    def PressRefresh(self) :
        self._paged_display.SetPageLines('Press',
                                        2,
                                        line1= 'Browser',
                                        line2= "Select an option"
                                        )
        self._paged_display.SetActivePage('Press', expires=2000)


    def BackRefresh(self) :
        self._paged_display.SetPageLines('Back',
                                        2,
                                        line1= 'Browser',
                                        line2= "Back <-"
                                        )
        self._paged_display.SetActivePage('Back', expires=1000)


    def GODMODERefresh(self, godmode) :
        if godmode :
            self._paged_display.SetPageLines('GODMODEON',
                                            10,
                                            line1= 'GODMODE',
                                            line2= 'ON'
                                            )
            self._paged_display.SetActivePage('GODMODEON', expires=self._display_ms)
        else :
            self._paged_display.SetPageLines('GODMODEOFF',
                                            10,
                                            line1= 'GODMODE',
                                            line2= 'OFF'
                                            )
            self._paged_display.SetActivePage('GODMODEOFF', expires=self._display_ms)

    def SCREENIDRefresh(self, id) :
        self._paged_display.SetPageLines('ScreenID',
                                        10,
                                        line1= 'Screen ID',
                                        line2= str(id)
                                        )
        self._paged_display.SetActivePage('ScreenID', expires=self._display_ms)
