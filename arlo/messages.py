import json


class Message:
    def __init__(self, dictionary):
        self.dictionary = dictionary

    def __getitem__(self, key):
        return self.dictionary[key]

    def __setitem__(self, key, value):
        self.dictionary[key] = value

    def __contains__(self, item):
        return item in self.dictionary

    def toNetworkMessage(self):
        msgJson = json.dumps(self.dictionary, separators=(',', ':'))
        length = len(msgJson)
        final = f"L:{length} {msgJson}"
        return str.encode(final)

    def toJSON(self):
        return json.dumps(self.dictionary, separators=(',', ':'))

    def __repr__(self):
        return json.dumps(self.dictionary, separators=(',', ':'))

    def __str__(self):
        return json.dumps(self.dictionary, indent=4)

    @staticmethod
    def from_json(json_data):
        if (json_data is not None and json_data != "None"):
            return Message(json.loads(json_data))
        else:
            return None


# ID is an incrementing number
# FROM CAMERA
REGISTRATION = {
    "Type": "registration",
    "ID": 1,
    "SystemSerialNumber": "YOURSERIAL",
    "SystemModelNumber": "VMC4030P",
    "SystemFirmwareVersion": "1.125.15.0_35_1191",
    "UpdateSystemModelNumber": "VMC4030P",
    "CommProtocolVersion": 1,
    "BatPercent": 89,
    "SignalStrengthIndicator": 4,
    "LogFrequency": 2,
    "BatTech": "Rechargeable",
    "ChargerTech": "None",
    "ChargingState": "Off",
    "ThermalShutdownRechargeMaxTemp": 60,
    "Temperature": 20,
    "InterfaceVersion": 1,
    "Capabilities": ["IRLED", "PirMotion", "NightVision", "Temperature", "BatteryLevel", "Microphone", "Speaker", "SignalStrength", "Solar", "BatteryCharging", "H.264Streaming", "JPEGSnapshot", "AutomatedStop", "BEC", "RaParams"],
    "HardwareRevision": "H3",
    "Sync": False,
    "BattChargeMinTemp": 0,
    "BattChargeMaxTemp": 60,
    "ThermalShutdownMinTemp": -20,
    "ThermalShutdownMaxTemp": 74,
    "BootSeconds": 4
}
# FROM CAMERA
STATUS = {
    "Type": "status",
    "ID": 2,
    "SystemFirmwareVersion": "1.125.15.0_35_1191",
    "HardwareRevision": "H3",
    "SystemSerialNumber": "YOURSERIAL",
    "UpdateSystemModelNumber": "VMC4030P",
    "BatPercent": 89,
    "BatTech": "Rechargeable",
    "ChargerTech": "None",
    "ChargingState": "Off",
    "WifiCountryDetails": "AT/36",
    "Bat1Volt": 7.814,
    "Temperature": 20,
    "Battery1CaliVoltage": 7.814,
    "SignalStrengthIndicator": 4,
    "Streamed": 0,
    "UserStreamed": 0,
    "MotionStreamed": 0,
    "IRLEDsOn": 0,
    "PoweredOn": 17,
    "CameraOnline": 1,
    "CameraOffline": 16,
    "WifiConnectionCount": 1,
    "WifiConnectionAttempts": 1,
    "PIREvents": 0,
    "FailedStreams": 0,
    "FailedUpgrades": 0,
    "SnapshotCount": 0,
    "LogFrequency": 2,
    "CriticalBatStatus": 0,
    "ISPOn": 15, "TimeAtPlug": 0,
    "TimeAtUnPlug": 0,
    "PercentAtPlug": 0,
    "PercentAtUnPlug": 0,
    "ISPWatchdogCount": 0,
    "ISPWatchdogCount2": 0,
    "SecsPerPercentCurr": 0,
    "SecsPerPercentAvg": 0,
    "DdrFailCnt": 0,
    "RtcpDiscCnt": 0,
    "DhcpFCnt": 48,
    "RegFCnt": 340,
    "TxErr": 0,
    "TxFail": 0,
    "TxPhyE1": 0,
    "TxPhyE2": 0
}

# FROM CAMERA
ALERT = {
    "Type": "alert",
    "ID": 7,
    "AlertType": "pirMotionAlert",
    "PIRMotion": {
            "Triggered": True,
            "TriggerLevel": 7970,
            "TriggerRtpTime": 0,
            "TriggerSysTime": 1,
            "zones": [],
            "MdZones": 0,
            "MdPrevZones": 0,
            "PirTrigger": 0,
            "z0Intensity": 0,
            "z0Counter": 0,
            "z1Intensity": 0,
            "z1Counter": 0,
            "z2Intensity": 0,
            "z2Counter": 0,
            "z3Intensity": 0,
            "z3Counter": 0
    }
}
# FROM CAMERA - SMART ENABLED?
ALERT_SMART = {
    "Type": "alert",
    "ID": -1,
    "AlertType": "pirMotionAlert",
    "PIRMotion": {
            "Triggered": True,
            "TriggerLevel": 0,
            "TriggerRtpTime": 0,
            "TriggerSysTime": 2857,
            "zones": [],
            "MdZones": 1,
            "MdPrevZones": 0,
            "PirTrigger": 2,
            "z0Intensity": 40,
            "z0Counter": 320,
            "z1Intensity": 0,
            "z1Counter": 0,
            "z2Intensity": 0,
            "z2Counter": 0,
            "z3Intensity": 0,
            "z3Counter": 0
    }
}

# FROM CAMERA - ZONE ALERT?
ALERT_ZONE = {
    "Type": "alert",
    "ID": -1,
    "AlertType": "pirMotionAlert",
    "PIRMotion": {
            "Triggered": True,
            "TriggerLevel": 0,
            "TriggerRtpTime": 0,
            "TriggerSysTime": 1823,
            "zones": ["3cfe3b01-944d-422a-9f99-34c130d23299", "b44327ff-c1c4-4208-a890-f1de0c8b5192"],
            "MdZones": 7,  # Motion Detection Zones?
            "MdPrevZones": 0,
            "PirTrigger": 1,
            "z0Intensity": 100,  # Zone 0 all zones?
            "z0Counter": 960,
            "z1Intensity": 100,  # Zone 1
            "z1Counter": 896,
            "z2Intensity": 24,  # Zone2 etc
            "z2Counter": 192,
            "z3Intensity": 0,
            "z3Counter": 0
    }
}

# FROM CAMERA
ALERT_TIMEOUT = {
    "Type": "alert",
    "ID": 9,
    "AlertType": "motionTimeoutAlert",
    "StreamDuration": 18
}

# FROM CAMERA
ALERT_AUDIO = {
    "Type": "alert",
    "ID": -1,
    "AlertType": "audioAlert",
    "AudioDetect": {
            "AudioTriggered": True,
            "AudioTriggerLevel": 2672,
            "AudioTriggerRtpTime": 0,
            "AudioTriggerSysTime": 0
    }
}

# FROM CAMERA
ALERT_AUDIO_TIMEOUT = {
    "Type": "alert",
    "ID": -1,
    "AlertType": "audioTimeoutAlert",
    "StreamDuration": 10
}

CAMERA_AUDIO_VOLUME = {
    "Type": "registerSet",
    "ID": -1,
    "SetValues": {
            "AudioSpkrVolume": 0  # 0 is 85%, 4=100%, -62=0%
    }
}

CAMERA_SPEAKER = {
    "Type": "registerSet",
    "ID": -1,
    "SetValues": {
            "AudioSpkrEnable": False
    }
}

CAMERA_MIC = {
    "Type": "registerSet",
    "ID": -1,
    "SetValues": {
            "AudioMicEnable": False
    }
}

STATUS_REQUEST = {"Type": "statusRequest", "ID": 19}

RA_PARAMS_OFF_QUALITY = {
    "Type": "raParams",
    "ID": -1,
    "Params": {
        "1080p": {
            "minbps": 102400,
            "maxbps": 1228800,
            "minQP": 24,
            "maxQP": 38,
            "vbr": True,
            "targetbps": 1024000,
            "cbrbps": 1024000
        },
        "360p": {
            "minbps": 51200,
            "maxbps": 512000,
            "minQP": 24,
            "maxQP": 38,
            "vbr": True,
            "targetbps": 409600,
            "cbrbps": 409600
        },
        "480p": {
            "minbps": 51200,
            "maxbps": 614400,
            "minQP": 24,
            "maxQP": 38,
            "vbr": True,
            "targetbps": 512000,
            "cbrbps": 512000
        },
        "720p": {
            "minbps": 51200,
            "maxbps": 1024000,
            "minQP": 24,
            "maxQP": 38,
            "vbr": True,
            "targetbps": 768000,
            "cbrbps": 768000
        }
    }
}

RA_PARAMS_LOW_QUALITY = {
    "Type": "raParams",
    "ID": -1,
    "Params": {
        "1080p": {
            "minbps": 102400,
            "maxbps": 532480,
            "minQP": 24,
            "maxQP": 38,
            "vbr": True,
            "targetbps": 409600,
            "cbrbps": 409600
        },
        "4K": {
            "minbps": 307200,
            "maxbps": 2048000,
            "minQP": 26,
            "maxQP": 38,
            "vbr": True,
            "targetbps": 1024000,
            "cbrbps": 1024000
        },
        "360p": {
            "minbps": 51200,
            "maxbps": 307200,
            "minQP": 24,
            "maxQP": 38,
            "vbr": True,
            "targetbps": 102400,
            "cbrbps": 102400
        },
        "480p": {
            "minbps": 51200,
            "maxbps": 409600,
            "minQP": 24,
            "maxQP": 38,
            "vbr": True,
            "targetbps": 307200,
            "cbrbps": 307200
        },
        "720p": {
            "minbps": 51200,
            "maxbps": 532480,
            "minQP": 24,
            "maxQP": 38,
            "vbr": True,
            "targetbps": 409600,
            "cbrbps": 409600
        }
    }
}

RA_PARAMS_MEDIUM_QUALITY = {
    "Type": "raParams",
    "ID": -1,
    "Params": {
        "1080p": {
            "minbps": 102400,
            "maxbps": 640000,
            "minQP": 24,
            "maxQP": 38,
            "vbr": True,
            "targetbps": 512000,
            "cbrbps": 512000
        },
        "4K": {
            "minbps": 307200,
            "maxbps": 3072000,
            "minQP": 26,
            "maxQP": 38,
            "vbr": True,
            "targetbps": 1536000,
            "cbrbps": 2048000
        },
        "360p": {
            "minbps": 51200,
            "maxbps": 409600,
            "minQP": 24,
            "maxQP": 38,
            "vbr": True,
            "targetbps": 204800,
            "cbrbps": 204800
        },
        "480p": {
            "minbps": 51200,
            "maxbps": 409600,
            "minQP": 24,
            "maxQP": 38,
            "vbr": True,
            "targetbps": 409600,
            "cbrbps": 409600
        },
        "720p": {
            "minbps": 51200,
            "maxbps": 599040,
            "minQP": 24,
            "maxQP": 38,
            "vbr": True,
            "targetbps": 460800,
            "cbrbps": 460800
        }
    }
}

RA_PARAMS_HIGH_QUALITY = {
    "Type": "raParams",
    "ID": -1,
    "Params": {
        "1080p": {
            "minbps": 102400,
            "maxbps": 819200,
            "minQP": 35,
            "maxQP": 40,
            "vbr": True,
            "targetbps": 614400,
            "cbrbps": 614400
        },
        "4K": {
            "minbps": 307200,
            "maxbps": 5120000,
            "minQP": 26,
            "maxQP": 38,
            "vbr": True,
            "targetbps": 3072000,
            "cbrbps": 3072000
        },
        "360p": {
            "minbps": 51200,
            "maxbps": 512000,
            "minQP": 24,
            "maxQP": 38,
            "vbr": True,
            "targetbps": 409600,
            "cbrbps": 409600
        },
        "480p": {
            "minbps": 51200,
            "maxbps": 614400,
            "minQP": 24,
            "maxQP": 38,
            "vbr": True,
            "targetbps": 512000,
            "cbrbps": 512000
        },
        "720p": {
            "minbps": 51200,
            "maxbps": 665600,
            "minQP": 24,
            "maxQP": 38,
            "vbr": True,
            "targetbps": 512000,
            "cbrbps": 512000
        }
    }
}

# Subscription quality is a slightly higher quality observed
# when ArloSmart subscription was enabled.
RA_PARAMS_SUBSCRIPTION_QUALITY = {
    "Type": "raParams",
    "ID": -1,
    "Params": {
        "1080p": {
            "minbps": 102400,
            "maxbps": 1228800,
            "minQP": 24,
            "maxQP": 38,
            "vbr": True,
            "targetbps": 1024000,
            "cbrbps": 1024000
        },
        "4K": {
            "minbps": 307200,
            "maxbps": 10240000,
            "minQP": 1,
            "maxQP": 1,
            "vbr": False,
            "targetbps": 10240000,
            "cbrbps": 10240000
        },
        "360p": {
            "minbps": 51200,
            "maxbps": 512000,
            "minQP": 24,
            "maxQP": 38,
            "vbr": True,
            "targetbps": 409600,
            "cbrbps": 409600
        },
        "480p": {
            "minbps": 51200,
            "maxbps": 614400,
            "minQP": 24,
            "maxQP": 38,
            "vbr": True,
            "targetbps": 512000,
            "cbrbps": 512000
        },
        "720p": {
            "minbps": 51200,
            "maxbps": 1024000,
            "minQP": 24,
            "maxQP": 38,
            "vbr": True,
            "targetbps": 768000,
            "cbrbps": 768000
        }
    }
}

# No promises this will work...
RA_PARAMS_INSANE_QUALITY = {
    "Type": "raParams",
    "ID": -1,
    "Params": {
        "1080p": {
            "minbps": 204800,
            "maxbps": 2097152,
            "minQP": 12,
            "maxQP": 24,
            "vbr": True,
            "targetbps": 2048000,
            "cbrbps": 2048000
        },
        "4K": {
            "minbps": 614400,
            "maxbps": 10240000,
            "minQP": 1,
            "maxQP": 1,
            "vbr": False,
            "targetbps": 10240000,
            "cbrbps": 10240000
        },
        "360p": {
            "minbps": 51200,
            "maxbps": 512000,
            "minQP": 24,
            "maxQP": 38,
            "vbr": True,
            "targetbps": 409600,
            "cbrbps": 409600
        },
        "480p": {
            "minbps": 51200,
            "maxbps": 614400,
            "minQP": 24,
            "maxQP": 38,
            "vbr": True,
            "targetbps": 512000,
            "cbrbps": 512000
        },
        "720p": {
            "minbps": 51200,
            "maxbps": 1024000,
            "minQP": 24,
            "maxQP": 38,
            "vbr": True,
            "targetbps": 768000,
            "cbrbps": 768000
        }
    }
}


#  Destination URL includes serial number
# Camera will POST with a multipart form containing file parameter.
# Will not include temp.jpg in URL
SNAPSHOT = {
    "Type": "fullSnapshot",
    "ID": -1,
    "DestinationURL": "http://172.14.1.1/snapshot/YOURSERIAL_d293116d/temp.jpg"
}

REGISTER_SET_USER_STREAM_ACTIVE = {
    "Type": "registerSet",
    "ID": -1,
    "SetValues": {
            "UserStreamActive": 0  # 0 Active 1 Disabled
    }
}

# Generic registerSet
REGISTER_SET = {
    "Type": "registerSet",
    "ID": -1,
    "SetValues": {}
}

# Enable/Disable motion sensitivity
REGISTER_SET_PIR = {
    "Type": "registerSet",
    "ID": -1,
    "SetValues": {
            "PIREnableLED": True,
            "PIRLEDSensitivity": 80
    }
}

REGISTER_SET_ARMED = {
    "Type": "registerSet",
    "ID": -1,
    "SetValues": {
            "PIRTargetState": "Armed",
            "PIRStartSensitivity": 80,
            "PIRAction": "Stream",
            "VideoMotionEstimationEnable": True,
            "VideoMotionSensitivity": 80,
            "AudioTargetState": "Disarmed"
    }
}

REGISTER_SET_DISARMED = {
    "Type": "registerSet",
    "ID": -1,
    "SetValues": {
            "PIRTargetState": "Disarmed",
            "AudioTargetState": "Disarmed",
            "VideoMotionEstimationEnable": False,
            "DefaultMotionStreamTimeLimit": 10
    }
}
REGISTER_SET_ARM_AUDIO = {
    "Type": "registerSet",
    "ID": 12,
    "SetValues": {
            "PIRTargetState": "Armed",
            "PIRStartSensitivity": 80,
            "PIRAction": "Stream",
            "AudioTargetState": "Armed",
            "AudioStartSensitivity": 2,
            "AudioAction": "Stream",
            "VideoMotionEstimationEnable": True,
            "VideoMotionSensitivity": 80
    }
}

REGISTER_SET_LOW_QUALITY = {
    "Type": "registerSet",
    "ID": -1,
    "SetValues": {
        "VideoOutputResolution": "720p",
        "VideoTargetBitrate": 400,
        "HEVCVideoOutputResolution": "2160p",
        "HEVCVideoTargetBitrate": 1000,
    }
}

REGISTER_SET_MEDIUM_QUALITY = {
    "Type": "registerSet",
    "ID": -1,
    "SetValues": {
        "VideoOutputResolution": "1080p",
        "VideoTargetBitrate": 600,
        "HEVCVideoOutputResolution": "2160p",
        "HEVCVideoTargetBitrate": 1500,
    }
}

REGISTER_SET_HIGH_QUALITY = {
    "Type": "registerSet",
    "ID": -1,
    "SetValues": {
        "VideoOutputResolution": "1080p",
        "VideoTargetBitrate": 1250,
        "HEVCVideoOutputResolution": "2160p",
        "HEVCVideoTargetBitrate": 3000,
    }
}

REGISTER_SET_SUBSCRIPTION_QUALITY = {
    "Type": "registerSet",
    "ID": -1,
    "SetValues": {
        "VideoOutputResolution": "1080p",
        "VideoTargetBitrate": 1250,
        "HEVCVideoOutputResolution": "2160p",
        "HEVCVideoTargetBitrate": 6000,
    }
}

# No promises this will work...
REGISTER_SET_INSANE_QUALITY = {
    "Type": "registerSet",
    "ID": -1,
    "SetValues": {
        "VideoOutputResolution": "1080p",
        "VideoTargetBitrate": 2000,
        "HEVCVideoOutputResolution": "2160p",
        "HEVCVideoTargetBitrate": 8000,
    }
}

REGISTER_SET_INITIAL = {
    "Type": "registerSet",
    "ID": -1,
    "SetValues": {
        "AudioMicVolume": 4,
        "AudioSpkrEnable": False,
        "VideoExposureCompensation": 0,
        "VideoMirror": False,
        "VideoFlip": False,
        "VideoWindowStartX": 0,
        "VideoWindowStartY": 0,
        "VideoWindowEndX": 1280,
        "VideoWindowEndY": 720,
        "MaxMissedBeaconTime": 30,
        "MaxStreamTimeLimit": 1800,
        "VideoAntiFlickerRate": 50,
        "WifiCountryCode": "EU",
        "NightVisionMode": True,
        "HdrControl": "off",
        "MaxUserStreamTimeLimit": 1800,
        "MaxMotionStreamTimeLimit": 120,
        "VideoMode": "superWide",
        "JPEGOutputResolution": "",
        "ChargeNotificationLed": 0,  # Battery Fully Charged Indicator
        "AudioMicAGC": 0,
        "VideoOutputResolution": "1080p",
        "VideoTargetBitrate": 1000,  # 600 originally
        "Audio0EncodeFormat": 0,
        "Audio1EncodeFormat": 1,
        "ArloSmart": True,  # False originally
        "AlertBackoffTime": 0,
        "PIRTargetState": "Disarmed",
        "AudioTargetState": "Disarmed",
        "VideoMotionEstimationEnable": False,
        "DefaultMotionStreamTimeLimit": 10
    }
}

# Register set specific to the Arlo Ultra
REGISTER_SET_INITIAL_ULTRA = {
    "Type": "registerSet",
    "ID": -1,
    "SetValues": {
        "AlertBackoffTime": 0,
        "ArloSmart": True,
        "Audio0EncodeFormat": 0,
        "Audio1EncodeFormat": 1,
        "AudioMicAGC": 0,  # automatic gain control
        "AudioMicWNS": 0,   # reduce wind noise
        "ChargeNotificationLed": 1,  # LED when charged
        "CvrModeEnabled": False,
        "EpochBsTime": 1610925182,
        "HdrControl": "auto",    # auto HDR enabled
        "HEVCVideoOutputResolution": "2160p",
        "HEVCVideoTargetBitrate": 3000,
        "IRCutState": "engaged",  # color night vision
        "IRLedState": "off",     # ??
        "JPEGOutputResolution": "",
        "MaxMissedBeaconTime": 30,
        "MaxMotionStreamTimeLimit": 120,
        "MaxSensorRequired": True,  # ??
        "MaxStreamTimeLimit": 1800,
        "MaxUserStreamTimeLimit": 1800,
        "NightModeGrey": 0,  # ??
        "NightModeLightSourceAlert": 1,  # enable (1)/disable (0) spotlight at night
        "NightVisionMode": False,  # night vision enabled
        "SpotlightIntensityAlert": 100,  # spotlight brightness - DOESN'T WORK even in the Arlo app
        "SpotlightModeAlert": 0,  # spotlight behavior: (0) Constant, (1) Flash, (2) Pulsate
        "VideoAntiFlickerRate": 60,  # hz
        "VideoExposureCompensation": 0,
        "VideoFlip": False,
        "VideoMirror": False,
        "VideoMode": "superWide",
        "VideoOutputResolution": "1080p",
        "VideoSmartZoom": "off",  # automatic zoom and tracking
        "VideoTargetBitrate": 1250,
        "VideoWindowEndX": 1280,
        "VideoWindowEndY": 720,
        "VideoWindowStartX": 0,
        "VideoWindowStartY": 0,
        "WifiCountryCode": "US",
    }
}

REGISTER_SET_INITIAL_SUBSCRIPTION = {
    "Type": "registerSet",
    "ID": -1,
    "SetValues": {
        "AlertBackoffTime": 0,
        "ArloSmart": True,
        "Audio0EncodeFormat": 0,
        "Audio1EncodeFormat": 1,
        "AudioMicAGC": 0,
        "ChargeNotificationLed": 0,
        "HdrControl": "auto",
        "JPEGOutputResolution": "",
        "MaxMissedBeaconTime": 30,
        "MaxMotionStreamTimeLimit": 300,
        "MaxStreamTimeLimit": 1800,
        "MaxUserStreamTimeLimit": 1800,
        "NightModeGrey": 0,
        "NightModeLightSourceAlert": 1,
        "NightVisionMode": True,
        "SpotlightIntensityAlert": 100,
        "SpotlightModeAlert": 0,
        "VideoAntiFlickerRate": 60,
        "VideoExposureCompensation": 0,
        "VideoFlip": False,
        "VideoMirror": False,
        "VideoMode": "superWide",
        "VideoOutputResolution": "1080p",
        "VideoTargetBitrate": 1000,
        "VideoWindowEndX": 1280,
        "VideoWindowEndY": 720,
        "VideoWindowStartX": 0,
        "VideoWindowStartY": 0,
        "WifiCountryCode": "US",
    }
}

REGISTER_SET_INITIAL_VID_DOORBELL = {
    "Type": "registerSet",
    "ID": -1,
    "SetValues": {
        "CallEnableLED": True, # LED on Call Accepted
        "EnableCLI": False,
        "LEDPirStatus": True, # Breathe LED on Motion Detection
        "LogCOMM": 0,
        "LogFrequency": 2,
        "LogLevel": 1,
        "SilentMode": False,
        "StreamingLedEnabled": True, # LED on Live Streaming & Recording
        "TradChimePlayDur": 0,
        "TraditionalChime": False
    }
}

REGISTER_SET_INITIAL_2_VID_DOORBELL = {
    "Type": "registerSet",
    "ID": -1,
    "SetValues": {
        "AlertBackoffTime": 0,
        "ArloSmart": True,
        "Audio0EncodeFormat": 0,
        "Audio1EncodeFormat": 1,
        "EpochBsTime": 1679235744,
        "HdrControl": "auto",
        "MaxMissedBeaconTime": 10,
        "MaxStreamTimeLimit": 1800,
        "NightVisionMode": True,
        "PIRAction": "Snapshot",
        "PIRStartSensitivity": 80,
        "PIRTargetState": "Armed",
        "VideoAntiFlickerRate": 60,
        "VideoExposureCompensation": 0,
        "VideoFlip": False,
        "VideoMirror": False,
        "VideoMotionEstimationEnable": True,
        "VideoMotionSensitivity": 80,
        "VideoOutputResolution": "1536sq",
        "VideoTargetBitrate": 750,
        "VideoWindowEndX": 1536,
        "VideoWindowEndY": 1536,
        "VideoWindowStartX": 0,
        "VideoWindowStartY": 0,
        "WifiCountryCode": "US"
    }
}

RA_PARAMS_VID_DOORBELL = {
    "Type": "raParams",
    "ID": 2,
    "Params": {
        "1080sq": {
            "minbps": 51200,
            "maxbps": 1024000,
            "minQP": 24,
            "maxQP": 38,
            "vbr": True,
            "targetbps": 768000,
            "cbrbps": 768000
        },
        "1536sq": {
            "minbps": 102400,
            "maxbps": 1228800,
            "minQP": 24,
            "maxQP": 38,
            "vbr": True,
            "targetbps": 1024000,
            "cbrbps": 1024000
        },
        "720sq": {
            "minbps": 51200,
            "maxbps": 614400,
            "minQP": 24,
            "maxQP": 38,
            "vbr": True,
            "targetbps": 512000,
            "cbrbps": 512000
        }
    }
}

REGISTER_SET_720SQ = {
    "Type": "registerSet",
    "ID": -1,
    "SetValues": {
        "VideoOutputResolution": "720sq",
        "VideoTargetBitrate": 400,
    }
}

REGISTER_SET_1080SQ = {
    "Type": "registerSet",
    "ID": -1,
    "SetValues": {
        "VideoOutputResolution": "1080sq",
        "VideoTargetBitrate": 500,
    }
}

REGISTER_SET_1536SQ = {
    "Type": "registerSet",
    "ID": -1,
    "SetValues": {
        "VideoOutputResolution": "1536sq",
        "VideoTargetBitrate": 750,  # 750 originally
    }
}

REGISTER_SET_TURNED_OFF = {
    "Type": "registerSet",
    "ID": -1,
    "SetValues": {
        "VideoExposureCompensation": 0,
        "VideoMirror": False,
        "VideoFlip": False,
        "VideoWindowStartX": 0,
        "VideoWindowStartY": 0,
        "VideoWindowEndX": 1274,
        "VideoWindowEndY": 718,
        "MaxMissedBeaconTime": 30,
        "MaxStreamTimeLimit": 1800,
        "VideoAntiFlickerRate": 60,
        "WifiCountryCode": "US",
        "NightVisionMode": True,
        "IRLedState": "off",
        "IRCutState": "engaged",
        "HdrControl": "off",
        "MaxUserStreamTimeLimit": 1800,
        "MaxMotionStreamTimeLimit": 120,
        "VideoMode": "superWide",
        "JPEGOutputResolution": "",
        "ChargeNotificationLed": 0,
        "AudioMicAGC": 0,
        "VideoOutputResolution": "1080p",
        "VideoTargetBitrate": 1000,
        "Audio0EncodeFormat": 0,
        "Audio1EncodeFormat": 1,
        "ArloSmart": True,
        "AlertBackoffTime": 0
    }
}

RESPONSE = {
    "Type": "response",
    "ID": -1,
    "Response": "Ack"
}

ACTIVITY_ZONE = {
    "Type": "motionZone",
    "ID": -1,
    "intrZone": [
        {
            "name": "Zone 2",
            "id": "5461bdfe-ab83-4b58-8325-848dd2c30dda",
            "coords": [{"x": 0.264449, "y": 0.3}, {"x": 0.864449, "y": 0.3}, {"x": 0.864449, "y": 1}, {"x": 0.264449, "y": 1}],
            "color": 41210
        }
    ]
}
ACTIVITY_ZONE_ALL = {
    "Type": "motionZone",
    "ID": -1,
    "intrZone": [
        {
            "name": "Zone 3",
            "id": "2d10c7b1-72c7-4a42-8500-f75dbbbc860d",
            "coords": [{"x": 0.1, "y": 0.1}, {"x": 0.7, "y": 0.1}, {"x": 0.7, "y": 0.8}, {"x": 0.1, "y": 0.8}],
            "color": 15790130
        },
        {
            "name": "Zone 2",
            "id": "4a9b190b-eae2-49eb-93f8-3e924f13a179",
            "coords": [{"x": 0.1, "y": 0.1}, {"x": 0.7, "y": 0.1}, {"x": 0.7, "y": 0.8}, {"x": 0.1, "y": 0.8}],
            "color": 41210
        },
        {
            "name": "Zone 1",
            "id": "e8c8412d-5700-4567-9709-84c8b6bcd893",
            "coords": [{"x": 0.1, "y": 0.1}, {"x": 0.7, "y": 0.1}, {"x": 0.7, "y": 0.8}, {"x": 0.1, "y": 0.8}],
            "color": 8524960
        }
    ]
}

ACTIVITY_ZONE_DELETE = {
    "Type": "motionZone",
    "ID": -1,
    "intrZone": []
}

# FROM DOORBELL
AUDIO_DOORBELL_STATUS = {
    "Bat1Volt": 2667,
    "BatPercent": 82,
    "BatTech": "Primary",
    "ButtonEvents": 327,
    "CriticalBatStatus": False,
    "FailedStreams": 0,
    "FailedUpgrades": 0,
    "HardwareRevision": "1.4",
    "Hibernate": True,
    "ID": 31581,
    "LogFrequency": 2,
    "PIREvents": 0,
    "SignalStrengthIndicator": 0,
    "SystemFirmwareVersion": "1.2.0.0_320_401",
    "SystemSerialNumber": "YOURSERIAL",
    "Type": "status",
    "WifiConnectionAttempts": 1,
    "WifiConnectionCount": 1,
    "WifiCountryRegion": 5
}

# FROM DOORBELL
AUDIO_DOORBELL_REGISTRATION = {
    "BCC": "64_CHAR_HEXADECIMAL_STRING",  # what is this?
    "BatPercent": 86,
    "BatTech": "Primary",
    "Capabilities": [
        "BatteryLevel",
        "SignalStrength",
        "Microphone",
        "Speaker",
        "PirMotion"
    ],
    "CommProtocolVersion": 1,
    "HardwareRevision": "1.4",
    "ID": 31580,
    "InterfaceVersion": 1,
    "LogFrequency": 2,
    "RtpPort": 5000,
    "SKU": "AAD1001-100NAS",
    "SignalStrengthIndicator": 4,
    "Sync": False,
    "SystemFirmwareVersion": "1.2.0.0_320_401",
    "SystemModelNumber": "AAD1001",
    "SystemSerialNumber": "YOURSERIAL",
    "Type": "registration"
}

# TO DOORBELL
AUDIO_DOORBELL_INITIAL_REGISTER_SET = {
    "Type": "registerSet",
    "ID": 2,
    "SetValues": {
        "PIRTargetState": "Armed",
        "PIRStartSensitivity": 30
    }
}

# TO DOORBELL
AUDIO_DOORBELL_SECOND_REGISTER_SET = {
    "Type": "registerSet",
    "ID": 1,
    "SetValues": {
        "BeaconLostTime": 10,
        "WifiCountryCode": "US",
        "AudioSpkrEnable": True,
        "AudioSpkrVolume": 85,
        "AudioMicEnable": True,
        "AudioMicVolume": 0,
        "HibernateTimer": 3600,
        "IdleTimer": 15,
        "LEDStatus": True,
        "TraditionalChime": False,
        "SilentMode": False,
        "LogFrequency": 2,
        "LogCOMM": 0,
        "LogLevel": 1,
        "EnableCLI": False
    }
}

# FROM DOORBELL 849
AUDIO_DOORBELL_BUTTON_PRESS = {
    "Type": "alert",
    "ID": 31607,
    "SystemSerialNumber": "YOURSERIAL",
    "AlertType": "buttonPressAlert",
    "ButtonPress": {
        "Triggered": True
    }
}

# 864 RST

# TO DOORBELL 873
AUDIO_DOORBELL_END_OF_CALL = {
    "Type": "rtpBye",
    "ID": 48,
    "Streams": [1],
    "EndOfCall": True
}

# TO DOORBELL
AUDIO_DOORBELL_RTP_INVITE = {
    "Type": "rtpInvite",
    "ID": 59,
    "AudioStream": {
        "PayloadType": 97,
        "PayloadTypeString": "OPUS",
        "Bitrate": 32000,
        "ID": 2
    },
    "buttonPressed": True
}

# FROM DOORBELL
AUDIO_DOORBELL_RTP_RESPONSE = {
    "Type": "response",
    "ID": 59,
    "SystemSerialNumber": "YOURSERIAL",
    "Response": "Ack",
    "AudioStream": {
        "PayloadType": 97,
        "PayloadTypeString": "OPUS",
        "Bitrate": 32000,
        "Port": 8000,  # send audio to doorbell here
        "ID": 2
    }
}

# TO DOORBELL
AUDIO_DOORBELL_RTP_REQUEST = {
    "Type": "rtpRequest",
    "ID": 60,
    "AudioStream": {
        "PayloadType": 97,
        "PayloadTypeString": "OPUS",
        "Port": 53046,  # audio from doorbell gets sent here
        "ID": 3
    }
}

# FROM DOORBELL
AUDIO_DOORBELL_RTP_RESPONSE_2 = {
    "Type": "response",
    "ID": 60,
    "SystemSerialNumber": "YOURSERIAL",
    "Response": "Ack",
    "AudioStream": {
        "PayloadType": 97,
        "PayloadTypeString": "OPUS",
        "Bitrate": 32000,
        "Port": 8000,  # send audio to doorbell here
        "ID": 3
    }
}

AUDIO_DOORBELL_END_OF_CALL_1 = {
    "Type": "rtpBye",
    "ID": 61,
    "Streams": [3, 2],
    "EndOfCall": True
}

AUDIO_DOORBELL_END_OF_CALL = {
    "Type": "rtpBye",
    "ID": 62,
    "Streams": [3],
    "EndOfCall": False
}

AUDIO_DOORBELL_END_OF_CALL = {
    "Type": "rtpBye",
    "ID": 62,
    "Streams": [2],
    "EndOfCall": False
}

REGISTER_SET_INITIAL_FLOODLIGHT = {
    "Type": "registerSet",
    "ID": 2,
    "SetValues": {
        "AlertBackoffTime": 0,
        "ArloSmart": True,
        "Audio0EncodeFormat": 0,
        "Audio1EncodeFormat": 1,
        "AudioMicAGC": 0,
        "AudioMicVolume": 4,
        "AudioMicWNS": 0,
        "AudioSpkrEnable": True,
        "AudioTargetState": "Disarmed",
        "ChargeNotificationLed": 1,
        "CvrModeEnabled": False,
        "DefaultMotionStreamTimeLimit": 28,
        "DuskToDawnThrshVal": 26, # Dusk to Dawn Sensor setting; unclear what the range is
        "EpochBsTime": 1679206967,
        "HdrControl": "auto",
        "HEVCVideoOutputResolution": "1440p",
        "HEVCVideoTargetBitrate": 1000,
        "JPEGOutputResolution": "",
        "MaxMissedBeaconTime": 10,
        "MaxMotionStreamTimeLimit": 300,
        "MaxSensorRequired": True,
        "MaxStreamTimeLimit": 1800,
        "MaxUserStreamTimeLimit": 1800,
        "NightModeLightSourceAlert": 1,
        "NightVisionMode": True,
        "PIRAction": "Stream+Spotlight", # turn on floodlight with motion
        "PIRStartSensitivity": 95,
        "PIRTargetState": "Armed",
        "SpotlightDurationManual": 300, # floodlight duration when manually activated
        "SpotlightIntensityAlert": 12593, # floodlight brightness when motion detected, 25700 == 100%
        "SpotlightIntensityManual": 12593, # floodlight brightness when manually activated, 25700 == 100%
        "SpotlightModeAlert": 0, # floodlight behavior when motion detected: (0) Constant , (1) Flash, (2) Pulsate if the same as spotlight cam (unclear if (1) Flash is supported)
        "SpotlightModeManual": 0, # floodlight behavior when manually activated: (0) Constant, (2) Pulsate if the same as spotlight cam (unclear if (1) Flash is supported)
        "VideoAntiFlickerRate": 60,
        "VideoExposureCompensation": 0,
        "VideoFlip": False,
        "VideoMirror": False,
        "VideoMode": "wide",
        "VideoMotionEstimationEnable": False,
        "VideoOutputResolution": "1080p",
        "VideoSmartZoom": "off",
        "VideoTargetBitrate": 750,
        "VideoWindowEndX": 1280,
        "VideoWindowEndY": 720,
        "VideoWindowStartX": 0,
        "VideoWindowStartY": 0,
        "WifiCountryCode": "US"
    }
}

RA_PARAMS_FLOODLIGHT = {
    "Type": "raParams",
    "ID": 3,
    "Params": {
        "1080p": {
            "minbps": 102400,
            "maxbps": 1024000,
            "minQP": 24,
            "maxQP": 38,
            "vbr": True,
            "targetbps": 768000,
            "cbrbps": 768000
        },
        "2K": {
            "minbps": 307200,
            "maxbps": 2048000,
            "minQP": 26,
            "maxQP": 38,
            "vbr": True,
            "targetbps": 1024000,
            "cbrbps": 1024000
        },
        "720p": {
            "minbps": 51200,
            "maxbps": 768000,
            "minQP": 24,
            "maxQP": 38,
            "vbr": True,
            "targetbps": 512000,
            "cbrbps": 614400
        }
    }
}

REGISTER_SET_LOW_QUALITY_FLOODLIGHT = {
    "Type": "registerSet",
    "ID": -1,
    "SetValues": {
        "VideoOutputResolution": "720p",
        "VideoTargetBitrate": 400,
        "HEVCVideoOutputResolution": "1440p",
        "HEVCVideoTargetBitrate": 1000,
    }
}

REGISTER_SET_MEDIUM_QUALITY_FLOODLIGHT = {
    "Type": "registerSet",
    "ID": -1,
    "SetValues": {
        "VideoOutputResolution": "1080p",
        "VideoTargetBitrate": 500,
        "HEVCVideoOutputResolution": "1440p",
        "HEVCVideoTargetBitrate": 1000,
    }
}

REGISTER_SET_HIGH_QUALITY_FLOODLIGHT = {
    "Type": "registerSet",
    "ID": -1,
    "SetValues": {
        "VideoOutputResolution": "1080p",
        "VideoTargetBitrate": 750,
        "HEVCVideoOutputResolution": "1440p",
        "HEVCVideoTargetBitrate": 1000,
    }
}