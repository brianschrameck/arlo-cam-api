import copy

from arlo.messages import Message
import arlo.messages
from arlo.camera import Camera

DEVICE_PREFIXES = [
    'AVD'
]


class VideoDoorbell(Camera):
    @property
    def port(self):
        return 4000

    def _get_quality_messages(self, quality):
        quality = quality.lower()
        if quality == '720sq':
            return (
                Message(copy.deepcopy(arlo.messages.RA_PARAMS_VID_DOORBELL)),
                Message(copy.deepcopy(arlo.messages.REGISTER_SET_720SQ))
            )
        elif quality == '1080sq':
            return (
                Message(copy.deepcopy(arlo.messages.RA_PARAMS_VID_DOORBELL)),
                Message(copy.deepcopy(arlo.messages.REGISTER_SET_1080SQ))
            )
        elif quality == '1536sq':
            return (
                Message(copy.deepcopy(arlo.messages.RA_PARAMS_VID_DOORBELL)),
                Message(copy.deepcopy(arlo.messages.REGISTER_SET_1536SQ))
            )

        return None, None

    def get_ra_params_for_register_set(self, set_values):
        insane_values = arlo.messages.REGISTER_SET_1536SQ_INSANE.get('SetValues', {})
        if all(set_values.get(key) == value for key, value in insane_values.items()):
            return Message(copy.deepcopy(arlo.messages.RA_PARAMS_VID_DOORBELL_INSANE))

        for register_set in [
            arlo.messages.REGISTER_SET_720SQ,
            arlo.messages.REGISTER_SET_1080SQ,
            arlo.messages.REGISTER_SET_1536SQ,
        ]:
            quality_values = register_set.get('SetValues', {})
            if all(set_values.get(key) == value for key, value in quality_values.items()):
                return Message(copy.deepcopy(arlo.messages.RA_PARAMS_VID_DOORBELL))

        return None

    def build_default_register_set(self, wifi_country_code=None, video_anti_flicker_rate=None, video_quality_default=None):
        bootstrap_defaults = self.get_bootstrap_defaults()
        wifi_country_code = wifi_country_code or bootstrap_defaults['WifiCountryCode']
        video_anti_flicker_rate = video_anti_flicker_rate if video_anti_flicker_rate is not None else bootstrap_defaults['VideoAntiFlickerRate']
        video_quality_default = video_quality_default or bootstrap_defaults['VideoQualityDefault']

        registerSet = Message(copy.deepcopy(arlo.messages.REGISTER_SET_INITIAL_2_VID_DOORBELL))
        registerSet['SetValues']['WifiCountryCode'] = wifi_country_code
        registerSet['SetValues']['VideoAntiFlickerRate'] = video_anti_flicker_rate

        if video_quality_default == 'default':
            video_quality_default = '1536sq'

        _, quality_register_set = self._get_quality_messages(video_quality_default)
        if quality_register_set is not None:
            registerSet['SetValues'].update(copy.deepcopy(quality_register_set['SetValues']))

        return registerSet

    def send_initial_register_set(self, wifi_country_code, video_anti_flicker_rate=None, video_quality_default='default'):
        registerSet = Message(copy.deepcopy(arlo.messages.REGISTER_SET_INITIAL_VID_DOORBELL))
        self.send_message(registerSet, 4100)

        if self.default_register_set is None:
            self.set_default_register_set(
                self.build_default_register_set(
                    wifi_country_code,
                    video_anti_flicker_rate,
                    video_quality_default
                )
            )

        return self.send_default_register_set()

    def set_quality(self, args):
        ra_params, registerSet = self._get_quality_messages(args['quality'])
        if ra_params is None or registerSet is None:
            return False

        result = self.send_message(ra_params) and self.send_message(registerSet)
        if result:
            self.update_default_register_set(registerSet['SetValues'])

        return result

    def arm(self, args, persist_default=True):
        pir_target_state = args['PIRTargetState']
        pir_start_sensitivity = args.get('PIRStartSensitivity') or 80

        set_values = {
            'PIRTargetState': pir_target_state,
            'PIRStartSensitivity': pir_start_sensitivity,
        }

        return self.send_register_set_values(set_values, persist_default=persist_default)
