import socket
import sys
import copy
import time

from abc import ABC, abstractproperty, abstractmethod
from arlo.messages import Message
from arlo.socket import ArloSocket
import arlo.messages
from helpers.safe_print import s_print


class Device(ABC):

    @abstractproperty
    def port(self):
        pass

    def __init__(self, ip, registration):
        self.registration = registration
        self.ip = ip
        self.id = 0
        self.serial_number = registration["SystemSerialNumber"]
        self.hostname = f"{registration['SystemModelNumber']}-{self.serial_number[-5:]}"
        self.status = {}
        self.friendly_name = self.serial_number
        self.model_number = registration['SystemModelNumber']
        self.pir_start_state = None
        self.pir_start_sensitivity = None

    def __getitem__(self, key):
        return self.registration[key]

    def send_message(self, message: Message, port=None):
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:

            sock.settimeout(5.0)
            try:
                sock.connect((self.ip, port or self.port))
            except OSError as msg:
                print('Connection to camera failed: {msg}')
                return False

            result = False
            try:
                arloSock = ArloSocket(sock)
                self.id += 1
                message['ID'] = self.id
                s_print(f">[{self.ip}][{self.id}] {message.toNetworkMessage()}")
                arloSock.send(message)
                ack = arloSock.receive()
                if (ack != None):
                    if (ack['ID'] == message['ID']):
                        s_print(f"<[{self.ip}][{self.id}] {ack.toNetworkMessage()}")
                        if ('Response' in ack and ack['Response'] != "Ack"):
                            result = False
                        else:
                            result = True
            except:
                print(f'Exception: {sys.exc_info()}')
            finally:
                return result

    @abstractmethod
    def send_initial_register_set(self, wifi_country_code, video_anti_flicker_rate=None):
        ...

    def status_request(self):
        _status_request = Message(copy.deepcopy(arlo.messages.STATUS_REQUEST))
        return self.send_message(_status_request)

    def set_pir_settings(self, pir_start_state, pir_start_sensitivity, pir_start_sensitivity_default):
        # set PIR state and PIR Sensitivity if they're not using defaults
        if pir_start_state is None:
            pir_start_state = 'Armed'
        if pir_start_sensitivity is None:
            pir_start_state_sensivitity = pir_start_sensitivity_default

        update_pir_settings = False
        if pir_start_state != 'Armed':
            update_pir_settings = True
        if pir_start_sensitivity != pir_start_sensitivity_default:
            update_pir_settings = True

        if update_pir_settings:
            s_print(f"{self.friendly_name} - Setting custom PIR state: {pir_start_state}, PIR sensitivity: {pir_start_sensitivity}")
            self.arm({'PIRTargetState': pir_start_state, 'PIRStartSensitivity': pir_start_sensitivity})

    def validate_arm_args(self, pir_target_state, pir_start_sensitivity):
        if pir_target_state not in ['Armed', 'Disarmed']:
            s_print(f'{self.friendly_name} - Invalid PIR state value: {pir_target_state}')
            raise ValueError(f'ERROR: Invalid PIR state value: {pir_target_state}. Valid values: Armed, Disarmed')

        if pir_start_sensitivity < 0 or pir_start_sensitivity > 100:
            s_print(f'{self.friendly_name} - Invalid PIR sensitivity value: {pir_start_sensitivity}')
            raise ValueError(f'ERROR: Invalid PIR sensitivity value: {pir_start_sensitivity}. Valid values: 0-100')

    def arm(self, args):
        ...

    def mic_request(self, enabled):
        register_set = Message(copy.deepcopy(arlo.messages.REGISTER_SET))
        set_values = {
            'AudioMicEnable': enabled
        }
        register_set['AudioMicEnable'] = set_values
        return self.send_message(register_set)

    def speaker_request(self, enabled):
        register_set = Message(copy.deepcopy(arlo.messages.REGISTER_SET))
        set_values = {
            'AudioSpkrEnable': enabled
        }
        register_set['SetValues'] = set_values
        return self.send_message(register_set)

    def register_set(self, set_values):
        register_set = copy.deepcopy(arlo.messages.REGISTER_SET)
        register_set['SetValues'] = set_values
        register_set_message = Message(register_set)
        return self.send_message(register_set_message)

    def send_message_dict(self, message_dict):
        message = Message(message_dict)
        return self.send_message(message)

    def send_epoch_bs_time(self):
        register_set = Message(copy.deepcopy(arlo.messages.REGISTER_SET))
        set_values = {
            'EpochBsTime': int(time.time())
        }
        register_set['SetValues'] = set_values
        return self.send_message(register_set)
