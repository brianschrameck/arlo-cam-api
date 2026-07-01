import copy

from arlo.messages import Message
import arlo.messages
from arlo.device import Device

DEVICE_PREFIXES = [
    'AAD'
]


class AudioDoorbell(Device):
    @property
    def port(self):
        return 4100

    def build_default_register_set(self, wifi_country_code=None, video_anti_flicker_rate=None, video_quality_default=None):
        bootstrap_defaults = self.get_bootstrap_defaults()
        wifi_country_code = wifi_country_code or bootstrap_defaults['WifiCountryCode']

        registerSet = Message(copy.deepcopy(arlo.messages.AUDIO_DOORBELL_SECOND_REGISTER_SET))
        registerSet['SetValues']['WifiCountryCode'] = wifi_country_code
        return registerSet

    def send_initial_register_set(self, wifi_country_code, video_anti_flicker_rate=None):
        registerSet = Message(copy.deepcopy(arlo.messages.AUDIO_DOORBELL_INITIAL_REGISTER_SET))
        self.send_message(registerSet)

        if self.default_register_set is None:
            self.set_default_register_set(self.build_default_register_set(wifi_country_code))

        return self.send_default_register_set()

    def arm(self, args, persist_default=True):
        pir_target_state = args['PIRTargetState']
        pir_start_sensitivity = args.get('PIRStartSensitivity') or 30

        set_values = {
            "PIRTargetState": pir_target_state,
            "PIRStartSensitivity": pir_start_sensitivity,
        }

        return self.send_register_set_values(set_values, persist_default=persist_default)
