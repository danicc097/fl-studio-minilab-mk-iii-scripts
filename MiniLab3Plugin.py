"""
[[
	Surface:	MiniLab3
	Developer:	Farès MEZDOUR
	Version:	1.0.1

    Copyright (c) 2022 Farès MEZDOUR
]]
"""

import device
import plugins
import channels
import ui
import midi

PARAM_ID = {
            '14':1,
            '15':2,
            '30':3,
            '31':4,
            '86':1,
            '87':2,
            '89':3,
            '90':4,
            '110':5,
            '111':6,
            '116':7,
            '117':8
            }
            
KNOB_ID = (
            86,
            87,
            89,
            90,
            110,
            111,
            116,
            117
            )

KNOB_HW_VALUE = [
                0,
                0,
                0,
                0,
                0,
                0,
                0,
                0,
                ]

# Global variable

#ABSOLUTE VALUE
ABSOLUTE_VALUE = 64

def Plugin(event, clef) :

    recognized_plugin = False
    plugin_name = ui.getFocusedPluginName()
    
    global ABSOLUTE_VALUE
    
    if plugin_name == 'FLEX' :
        recognized_plugin = True
        ## FLEX ##
    
        PARAM_MAP = {
                '14':10,
                '15':11,
                '30':12,
                '31':13,
                '86':21,
                '87':22,
                '89':25,
                '90':30,
                '110':0,
                '111':2,
                '116':3,
                '117':4,
                '1':-1
                }
                
    elif plugin_name == 'FPC' :
        recognized_plugin = True
        ## FPC ##
    
        PARAM_MAP = {
                '14':8,
                '15':9,
                '30':10,
                '31':11,
                '86':4,
                '87':5,
                '89':6,
                '90':7,
                '110':0,
                '111':1,
                '116':2,
                '117':3,
                '1':-1
                }
                
    elif plugin_name == 'FL Keys' :
        recognized_plugin = True
        ## FL Keys ##
        
        PARAM_MAP = {
                '14':5,
                '15':4,
                '30':3,
                '31':2,
                '86':0,
                '87':1,
                '89':14,
                '90':13,
                '110':12,
                '111':7,
                '116':11,
                '117':10,
                '1':-1
                }
                
    elif plugin_name == 'Sytrus' :
        recognized_plugin = True
        ## SYTRUS ##
        
        PARAM_MAP = {
                '14':11,
                '15':12,
                '30':13,
                '31':14,
                '86':18,
                '87':19,
                '89':1,
                '90':16,
                '110':3,
                '111':4,
                '116':5,
                '117':6,
                '1':-1
                }
                
                
    elif plugin_name == 'GMS' :
        recognized_plugin = True
        ## GMS ##
              
        PARAM_MAP = {
                '14':32,
                '15':33,
                '30':45,
                '31':46,
                '86':56,
                '87':58,
                '89':57,
                '90':60,
                '110':24,
                '111':25,
                '116':26,
                '117':27,
                '1':-1
                }
                
                
    elif plugin_name == 'Harmless' :
        recognized_plugin = True
        ## HARMLESS ##
        
        PARAM_MAP = {
                '14':65,
                '15':66,
                '30':79,
                '31':80,
                '86':54,
                '87':59,
                '89':91,
                '90':97,
                '110':26,
                '111':27,
                '116':28,
                '117':31,
                '1':-1
                }

                
    elif plugin_name == 'Harmor' :
        recognized_plugin = True
        ## HARMOR ##
                
        PARAM_MAP = {
                '14':34,
                '15':37,
                '30':27,
                '31':28,
                '86':52,
                '87':57,
                '89':438,
                '90':443,
                '110':772,
                '111':773,
                '116':774,
                '117':776,
                '1':-1
                }
    
    elif plugin_name == 'Morphine' :
        recognized_plugin = True
        ## MORPHINE ##
    
        PARAM_MAP = {
                '14':30,
                '15':31,
                '30':32,
                '31':33,
                '86':6,
                '87':7,
                '89':14,
                '90':17,
                '110':1,
                '111':8,
                '116':15,
                '117':19,
                '1':124
                }
                
    elif plugin_name == '3x Osc' :
        recognized_plugin = True
        ## 3X OSC ##
    
        PARAM_MAP = {
                '14':6,
                '15':7,
                '30':13,
                '31':14,
                '86':1,
                '87':8,
                '89':15,
                '90':20,
                '110':2,
                '111':9,
                '116':16,
                '117':0,
                '1':-1
                }
                
    elif plugin_name == 'Fruity DX10' :
        recognized_plugin = True
        ## FRUITY DX10 ##
        
                
        PARAM_MAP = {
                '14':5,
                '15':6,
                '30':7,
                '31':8,
                '86':11,
                '87':21,
                '89':13,
                '90':10,
                '110':0,
                '111':1,
                '116':2,
                '117':-1,
                '1':-1
                }

    
    elif plugin_name == 'BASSDRUM' :
        recognized_plugin = True
        ## BASSDRUM ##
    
        PARAM_MAP = {
                '14':16,
                '15':17,
                '30':18,
                '31':0,
                '86':2,
                '87':8,
                '89':7,
                '90':6,
                '110':1,
                '111':4,
                '116':3,
                '117':5,
                '1':-1
                }
                
    elif plugin_name == 'Fruit kick' :
        recognized_plugin = True
        ## FRUIT KICK ##
        
        PARAM_MAP = {
                '14':-1,
                '15':-1,
                '30':-1,
                '31':-1,
                '86':0,
                '87':1,
                '89':2,
                '90':3,
                '110':4,
                '111':5,
                '116':-1,
                '117':-1,
                '1':-1
                }
                
    elif plugin_name == 'MiniSynth' :
        recognized_plugin = True
        ## MINISYNTH ##
    
        PARAM_MAP = {
                '14':21,
                '15':22,
                '30':23,
                '31':24,
                '86':8,
                '87':9,
                '89':19,
                '90':20,
                '110':12,
                '111':13,
                '116':14,
                '117':15,
                '1':-1
                }
                
    elif plugin_name == 'PoiZone' :
        recognized_plugin = True
        ## POIZONE ##
    
        PARAM_MAP = {
                '14':22,
                '15':23,
                '30':24,
                '31':25,
                '86':18,
                '87':19,
                '89':9,
                '90':46,
                '110':11,
                '111':12,
                '116':13,
                '117':14,
                '1':-1
                }
                
    elif plugin_name == 'Sakura' :
        recognized_plugin = True
        ## Sakura ##
    
        PARAM_MAP = {
                '14':12,
                '15':13,
                '30':14,
                '31':15,
                '86':8,
                '87':9,
                '89':19,
                '90':20,
                '110':21,
                '111':22,
                '116':23,
                '117':24,
                '1':-1
                }
                
    elif plugin_name == 'Fruity Envelope Controller' :
        recognized_plugin = True
        ## Fruity Envelope Controller ##
    
        PARAM_MAP = {
                '14':3,
                '15':4,
                '30':5,
                '31':6,
                '86':88,
                '87':89,
                '89':7,
                '90':2,
                '110':0,
                '111':1,
                '116':8,
                '117':9,
                '1':-1
                }
                            
    elif plugin_name == 'Fruity Keyboard Controller' :
        recognized_plugin = True
        ## Fruity Keyoard Controller ##
    
        PARAM_MAP = {
                '14':0,
                '15':1,
                '30':-1,
                '31':-1,
                '86':-1,
                '87':-1,
                '89':-1,
                '90':-1,
                '110':-1,
                '111':-1,
                '116':-1,
                '117':-1,
                '1':-1
                }
                
    
    elif plugin_name == 'Ogun' :
        recognized_plugin = True
        ## Ogun ##
    
        PARAM_MAP = {
                '14':49,
                '15':50,
                '30':51,
                '31':52,
                '86':17,
                '87':18,
                '89':25,
                '90':39,
                '110':5,
                '111':6,
                '116':7,
                '117':8,
                '1':-1
                }
    
    elif plugin_name == 'BooBass' :
        recognized_plugin = True
        ## BooBass ##
    
        PARAM_MAP = {
                '14':-1,
                '15':-1,
                '30':-1,
                '31':-1,
                '86':0,
                '87':1,
                '89':2,
                '90':-1,
                '110':-1,
                '111':-1,
                '116':-1,
                '117':-1,
                '1':-1
                }
    
    elif plugin_name == 'SimSynth Live' :
        recognized_plugin = True
        ## SimSynth ##
    
        PARAM_MAP = {
                '14':17,
                '15':18,
                '30':19,
                '31':20,
                '86':11,
                '87':12,
                '89':15,
                '90':16,
                '110':22,
                '111':23,
                '116':24,
                '117':25,
                '1':-1
                }
    
    elif plugin_name == 'Autogun' :
        recognized_plugin = True
        ## Autogun ##
    
        PARAM_MAP = {
                '14':-1,
                '15':-1,
                '30':-1,
                '31':-1,
                '86':0,
                '87':-1,
                '89':-1,
                '90':-1,
                '110':-1,
                '111':-1,
                '116':-1,
                '117':-1,
                '1':-1
                }
    
    elif plugin_name == 'PLUCKED!' :
        recognized_plugin = True
        ## Plucked! ##
    
        PARAM_MAP = {
                '14':-1,
                '15':-1,
                '30':-1,
                '31':-1,
                '86':0,
                '87':1,
                '89':2,
                '90':3,
                '110':4,
                '111':-1,
                '116':-1,
                '117':-1,
                '1':-1
                }
    
    elif plugin_name == 'BeepMap' :
        recognized_plugin = True
        ## BeepMap ##
    
        PARAM_MAP = {
                '14':-1,
                '15':-1,
                '30':-1,
                '31':-1,
                '86':0,
                '87':1,
                '89':2,
                '90':3,
                '110':4,
                '111':5,
                '116':6,
                '117':-1,
                '1':-1
                }
                
    elif plugin_name == 'ToxicBiohazard' :
        recognized_plugin = True
        ## Toxic Biohazard ##
    
        PARAM_MAP = {
                '14':3,
                '15':4,
                '30':5,
                '31':6,
                '86':15,
                '87':16,
                '89':10,
                '90':1,
                '110':19,
                '111':20,
                '116':21,
                '117':22,
                '1':-1
                }
    
    elif plugin_name == 'Fruity Dance' :
        recognized_plugin = True
        ## Fruity Dance ##
    
        PARAM_MAP = {
                '14':-1,
                '15':-1,
                '30':-1,
                '31':-1,
                '86':0,
                '87':1,
                '89':2,
                '90':3,
                '110':4,
                '111':5,
                '116':6,
                '117':-1,
                '1':-1
                }
    
    elif plugin_name == 'Drumaxx' :
        recognized_plugin = True
        ## Fruity Dance ##
    
        PARAM_MAP = {
                '14':706,
                '15':717,
                '30':718,
                '31':705,
                '86':0,
                '87':44,
                '89':88,
                '90':132,
                '110':176,
                '111':220,
                '116':264,
                '117':308,
                '1':-1
                }
    
    elif plugin_name == 'Drumpad' :
        recognized_plugin = True
        ## Fruity Dance ##
    
        PARAM_MAP = {
                '14':2,
                '15':3,
                '30':4,
                '31':5,
                '86':13,
                '87':15,
                '89':18,
                '90':24,
                '110':14,
                '111':16,
                '116':19,
                '117':25,
                '1':-1
                }
                
    elif plugin_name == 'Slicex' :
        recognized_plugin = True
        ## Fruity Dance ##
    
        PARAM_MAP = {
                '14':2,
                '15':3,
                '30':4,
                '31':5,
                '86':13,
                '87':15,
                '89':18,
                '90':24,
                '110':14,
                '111':16,
                '116':19,
                '117':25,
                '1':-1
                }
                
    elif plugin_name == 'SoundFont Player' :
        recognized_plugin = True
        ## Fruity Dance ##
    
        PARAM_MAP = {
                '14':5,
                '15':6,
                '30':7,
                '31':8,
                '86':12,
                '87':4,
                '89':2,
                '90':3,
                '110':9,
                '111':10,
                '116':11,
                '117':-1,
                '1':-1
                }
                
    elif plugin_name == 'Fruity granulizer' :
        recognized_plugin = True
        ## Fruity Dance ##
    
        PARAM_MAP = {
                '14':8,
                '15':9,
                '30':10,
                '31':11,
                '86':0,
                '87':1,
                '89':2,
                '90':3,
                '110':7,
                '111':4,
                '116':5,
                '117':6,
                '1':-1
                }
    
    elif plugin_name == 'Sawer' :
        recognized_plugin = True
        ## Fruity Dance ##
    
        PARAM_MAP = {
                '14':2,
                '15':3,
                '30':4,
                '31':5,
                '86':27,
                '87':28,
                '89':11,
                '90':18,
                '110':32,
                '111':33,
                '116':34,
                '117':35,
                '1':73
                }
                
    elif plugin_name == 'Transistor Bass' :
        recognized_plugin = True
        ## Fruity Dance ##
    
        PARAM_MAP = {
                '14':28,
                '15':29,
                '30':30,
                '31':31,
                '86':2,
                '87':4,
                '89':5,
                '90':6,
                '110':0,
                '111':1,
                '116':7,
                '117':8,
                '1':-1
                }
                
    else :
        
        PARAM_MAP = {
                '14':-1,
                '15':-1,
                '30':-1,
                '31':-1,
                '86':-1,
                '87':-1,
                '89':-1,
                '90':-1,
                '110':-1,
                '111':-1,
                '116':-1,
                '117':-1,
                '1':-1
                }
              
    if clef != 0 : 
        #print("clef = ",clef)    
        if recognized_plugin :
            cle = str(clef)
            PLUGIN_PARAM = PARAM_MAP.get(cle)
            if PLUGIN_PARAM != -1 :
                mapped = 1
                value = event.data2/127
                plugins.setParamValue(value,PLUGIN_PARAM ,channels.selectedChannel())
                event.handled = False
                parameter = plugins.getParamName(PLUGIN_PARAM, channels.selectedChannel())
                value = str(round(100*plugins.getParamValue(PLUGIN_PARAM, channels.selectedChannel())))
            else :
                mapped = 0
                if event.data1 in KNOB_ID :
                    parameter = "Knob "
                else :
                    parameter = "Fader "
                
                parameter = parameter + str(PARAM_ID.get(cle))
                value = str(event.data2)
        else :
            cle = str(clef)
            mapped = 0
            if event.data1 in KNOB_ID :
                parameter = "Knob "
            else :
                parameter = "Fader "
                
            parameter = parameter + str(PARAM_ID.get(cle))
            value = str(event.data2)
            
        return parameter, value, mapped
            
    else :
        #print("clef = 0")
        if recognized_plugin :

            mapped = 1
            hw_temp = []
            for i in PARAM_MAP.keys() :
                PLUGIN_PARAM = PARAM_MAP[i]
                #print(PLUGIN_PARAM)
                HW_VALUE = plugins.getParamValue(PLUGIN_PARAM, channels.selectedChannel())
                hw_temp.append(HW_VALUE)
                
            for j in range (8) : 
                KNOB_HW_VALUE[j] = hw_temp[j]
                #print(KNOB_HW_VALUE)
            
            hw_temp = []
            
            
            
        else :
            mapped = 0

        return KNOB_HW_VALUE, mapped
    
    
    


    # UTILITY 



# def RelativeToAbsolute(event) :
        # global ABSOLUTE_VALUE
        # if event.data2 < 64 :
            # ABSOLUTE_VALUE += 2*event.data2
        # else :
            # ABSOLUTE_VALUE -= 2*(event.data2-64)
        # if ABSOLUTE_VALUE > 127 :
            # ABSOLUTE_VALUE = 127
        # elif ABSOLUTE_VALUE < 0 :
            # ABSOLUTE_VALUE = 0
        # return ABSOLUTE_VALUE