"""
[[
	Surface:	MiniLab3
	Developer:	Farès MEZDOUR
	Version:	1.0.1

    Copyright (c) 2022 Farès MEZDOUR
]]
"""

import channels

# This script contains the strings of the V Collection software

V_COL = ['Analog Lab V',
         'Augmented STRINGS',
         'Aurmented VOICES',
         'Augmented GRAND PIANO'
         'ARP 2600 V3',
         'B-3 V2',
         'Buchla Easel V',
         'Clavinet V',
         'CMI V',
         'CS-80 V3',
         'CS-80 V4',
         'CZ V',
         'DX7 V',
         'Emulator II V',
         'Farfisa V',
         'Jun-6 V',
         'Jup-8 V4',
         'KORG MS-20 V',
         'Matrix-12 V2',
         'Mellotron V',
         'Mini V3',
         'Modular V3',
         'OP-Xa V',
         'Piano V2',
         'Piano V3',
         'Pigments',
         'Prophet V3',
         'Prophet-VS V',
         'Prophet-5 V',
         'SEM V2',
         'Solina V2',
         'SQ80 V',
         'Stage-73 V2',
         'Synclavier V',
         'Synthi V',
         'Vocoder V',
         'Vox Continental V2',
         'Wurli V2'
         ]
         

class ArturiaVCOLLECTION() :
    
    def __init__(self) :
        self._v_col = []
    
    def v_col_aff(self) :
        print(self._v_col)
        return self._v_col
   
    def AddVST(self) :
        string = channels.getChannelName(channels.channelNumber())
        present = False
        for i in self._v_col :
            if string == i :
                present = True
        if present == False and string in V_COL :
            self._v_col.append(string)

    