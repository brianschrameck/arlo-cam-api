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

    def send_initial_register_set(self, wifi_country_code, video_anti_flicker_rate=None, pir_start_state="Armed", pir_start_sensitivity=30):
        registerSet = Message(copy.deepcopy(arlo.messages.AUDIO_DOORBELL_INITIAL_REGISTER_SET))
        self.send_message(registerSet)

        registerSet = Message(copy.deepcopy(arlo.messages.AUDIO_DOORBELL_SECOND_REGISTER_SET))
        registerSet['SetValues']['WifiCountryCode'] = wifi_country_code
        self.send_message(registerSet)
        self.set_pir_settings(pir_start_state, pir_start_sensitivity, 30)

    def arm(self, args):
        register_set = Message(copy.deepcopy(arlo.messages.REGISTER_SET))

        pir_target_state = args['PIRTargetState']
        pir_start_sensitivity = args.get('PIRStartSensitivity') or 30

        self.validate_arm_args(pir_target_state, pir_start_sensitivity)

        register_set["SetValues"] = {
            "PIRTargetState": pir_target_state,
            "PIRStartSensitivity": pir_start_sensitivity,
        }

        return self.send_message(register_set)
