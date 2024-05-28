import copy

from arlo.messages import Message
import arlo.messages
from arlo.device import Device

DEVICE_PREFIXES = [
    'VMC',
    'VML',
    'ABC',
    'FB'
]


class Camera(Device):
    @property
    def port(self):
        return 4000

    def send_initial_register_set(self, wifi_country_code, video_anti_flicker_rate=None, video_quality_default='default', pir_start_state="Armed", pir_start_sensitivity=80):
        if self.model_number.startswith('VMC5040'):
            registerSet = Message(copy.deepcopy(arlo.messages.REGISTER_SET_INITIAL_ULTRA))
        elif self.model_number.startswith('FB1001'):
            registerSet = Message(copy.deepcopy(arlo.messages.REGISTER_SET_INITIAL_FLOODLIGHT))
        else:
            registerSet = Message(copy.deepcopy(arlo.messages.REGISTER_SET_INITIAL_SUBSCRIPTION))
            self.arm({"PIRTargetState": "Armed"})
        registerSet['SetValues']['WifiCountryCode'] = wifi_country_code
        registerSet['SetValues']['VideoAntiFlickerRate'] = video_anti_flicker_rate
        self.send_message(registerSet)

        if video_quality_default == 'default':
            video_quality_default = 'insane'

        self.set_quality({'quality': video_quality_default})
        self.set_pir_settings(pir_start_state, pir_start_sensitivity, 80)

    def pir_led(self, args):
        register_set = Message(copy.deepcopy(arlo.messages.REGISTER_SET))
        enabled = args['enabled']
        sensitivity = args['sensitivity']

        register_set["SetValues"] = {
            "PIREnableLED": enabled,
            "PIRLEDSensitivity": sensitivity
        }

        return self.send_message(register_set)

    def set_activity_zones(self, args):
        activity_zones = Message(copy.deepcopy(arlo.messages.ACTIVITY_ZONE_ALL))
        # TODO:Set The Co-ordinates
        return self.send_message(activity_zones)

    def unset_activity_zones(self, args):
        activity_zones = Message(copy.deepcopy(arlo.messages.ACTIVITY_ZONE_DELETE))
        return self.send_message(activity_zones)

    def set_quality(self, args):
        quality = args["quality"].lower()
        if quality == "low":
            ra_params = Message(copy.deepcopy(
                arlo.messages.RA_PARAMS_FLOODLIGHT if self.model_number.startswith('FB1001')
                else arlo.messages.RA_PARAMS_LOW_QUALITY))
            registerSet = Message(copy.deepcopy(
                arlo.messages.REGISTER_SET_LOW_QUALITY_FLOODLIGHT if self.model_number.startswith('FB1001')
                else arlo.messages.REGISTER_SET_LOW_QUALITY))
        elif quality == "medium":
            ra_params = Message(copy.deepcopy(
                arlo.messages.RA_PARAMS_FLOODLIGHT if self.model_number.startswith('FB1001')
                else arlo.messages.RA_PARAMS_MEDIUM_QUALITY))
            registerSet = Message(copy.deepcopy(
                arlo.messages.REGISTER_SET_MEDIUM_QUALITY_FLOODLIGHT if self.model_number.startswith('FB1001')
                else arlo.messages.REGISTER_SET_MEDIUM_QUALITY))
        elif quality == "high":
            ra_params = Message(copy.deepcopy(
                arlo.messages.RA_PARAMS_FLOODLIGHT if self.model_number.startswith('FB1001')
                else arlo.messages.RA_PARAMS_HIGH_QUALITY))
            registerSet = Message(copy.deepcopy(
                arlo.messages.REGISTER_SET_HIGH_QUALITY_FLOODLIGHT if self.model_number.startswith('FB1001')
                else arlo.messages.REGISTER_SET_HIGH_QUALITY))
        elif quality == "subscription":
            ra_params = Message(copy.deepcopy(
                arlo.messages.RA_PARAMS_FLOODLIGHT if self.model_number.startswith('FB1001')
                else arlo.messages.RA_PARAMS_SUBSCRIPTION_QUALITY))
            registerSet = Message(copy.deepcopy(
                arlo.messages.REGISTER_SET_HIGH_QUALITY_FLOODLIGHT if self.model_number.startswith('FB1001')
                else arlo.messages.REGISTER_SET_SUBSCRIPTION_QUALITY))
        elif quality == "insane":
            ra_params = Message(copy.deepcopy(
                arlo.messages.RA_PARAMS_FLOODLIGHT if self.model_number.startswith('FB1001')
                else arlo.messages.RA_PARAMS_INSANE_QUALITY))
            registerSet = Message(copy.deepcopy(
                arlo.messages.REGISTER_SET_HIGH_QUALITY_FLOODLIGHT if self.model_number.startswith('FB1001')
                else arlo.messages.REGISTER_SET_INSANE_QUALITY))
        else:
            return False

        return self.send_message(ra_params) and self.send_message(registerSet)

    def arm(self, args):
        register_set = Message(copy.deepcopy(arlo.messages.REGISTER_SET))

        pir_target_state = args['PIRTargetState']
        pir_start_sensitivity = args.get('PIRStartSensitivity') or 80
        pir_action = args.get('PIRAction') or 'Stream'
        video_motion_estimation_enable = args.get('VideoMotionEstimationEnable') or False
        audio_target_state = args.get('AudioTargetState') or 'Disarmed'

        self.validate_arm_args(pir_target_state, pir_start_sensitivity)

        register_set["SetValues"] = {
            "PIRTargetState": pir_target_state,
            "PIRStartSensitivity": pir_start_sensitivity,
            "PIRAction": pir_action,
            "VideoMotionEstimationEnable": video_motion_estimation_enable,
            "VideoMotionSensitivity": 80,
            "AudioTargetState": audio_target_state,
            # Unclear what this does, only set in normal traffic when 'Disarmed'
            "DefaultMotionStreamTimeLimit": 10
        }

        return self.send_message(register_set)

    def set_user_stream_active(self, active):
        register_set = Message(copy.deepcopy(arlo.messages.REGISTER_SET))
        register_set['SetValues']['UserStreamActive'] = int(active)
        return self.send_message(register_set)

    def snapshot_request(self, url):
        _snapshot_request = Message(copy.deepcopy(arlo.messages.SNAPSHOT))
        _snapshot_request['DestinationURL'] = url
        return self.send_message(_snapshot_request)
