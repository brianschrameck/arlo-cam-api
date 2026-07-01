import socket
import sys
import copy
import time
import yaml

from abc import ABC, abstractmethod
from arlo.messages import Message
from arlo.socket import ArloSocket
import arlo.messages
from helpers.safe_print import s_print


class Device(ABC):
    _bootstrap_defaults = None

    @property
    @abstractmethod
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
        self.default_register_set = None

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
            
            return result

    @abstractmethod
    def send_initial_register_set(self, wifi_country_code, video_anti_flicker_rate=None):
        ...

    def status_request(self):
        _status_request = Message(copy.deepcopy(arlo.messages.STATUS_REQUEST))
        return self.send_message(_status_request)

    def arm(self, args):
        ...

    def mic_request(self, enabled):
        set_values = {
            'AudioMicEnable': enabled
        }
        return self.send_register_set_values(set_values)

    def speaker_request(self, enabled):
        set_values = {
            'AudioSpkrEnable': enabled
        }
        return self.send_register_set_values(set_values)

    def register_set(self, set_values):
        return self.send_register_set_values(set_values)

    def send_message_dict(self, message_dict):
        message = Message(message_dict)
        return self.send_message(message)

    def send_epoch_bs_time(self):
        set_values = {
            'EpochBsTime': int(time.time())
        }
        return self.send_register_set_values(set_values, persist_default=False)

    def send_register_set_values(self, set_values, persist_default=True):
        register_set = copy.deepcopy(arlo.messages.REGISTER_SET)
        register_set['SetValues'] = set_values
        register_set_message = Message(register_set)
        result = self.send_message(register_set_message)
        if result and persist_default:
            self.update_default_register_set(set_values)
        return result

    def set_default_register_set(self, register_set: Message):
        if register_set is None:
            self.default_register_set = None
            return

        if isinstance(register_set, Message):
            register_set_dict = register_set.dictionary
        else:
            register_set_dict = register_set

        self.default_register_set = Message(copy.deepcopy(register_set_dict))

    def update_default_register_set(self, set_values):
        if set_values is None:
            return

        if self.default_register_set is None:
            self.ensure_default_register_set()

        if self.default_register_set is None:
            self.default_register_set = Message(copy.deepcopy(arlo.messages.REGISTER_SET))

        if 'SetValues' not in self.default_register_set or self.default_register_set['SetValues'] is None:
            self.default_register_set['SetValues'] = {}

        self.default_register_set['SetValues'].update(copy.deepcopy(set_values))
        self.persist()

    def persist(self):
        from arlo.device_db import DeviceDB
        DeviceDB.persist(self)

    @classmethod
    def get_bootstrap_defaults(cls):
        if cls._bootstrap_defaults is not None:
            return cls._bootstrap_defaults

        defaults = {
            "WifiCountryCode": "US",
            "VideoAntiFlickerRate": 60,
            "VideoQualityDefault": "default"
        }
        try:
            with open('config.yaml') as file:
                config = yaml.load(file, Loader=yaml.FullLoader) or {}
                defaults["WifiCountryCode"] = config.get('WifiCountryCode', defaults["WifiCountryCode"])
                defaults["VideoAntiFlickerRate"] = config.get('VideoAntiFlickerRate', defaults["VideoAntiFlickerRate"])
                defaults["VideoQualityDefault"] = config.get('VideoQualityDefault', defaults["VideoQualityDefault"])
        except Exception:
            pass

        cls._bootstrap_defaults = defaults
        return cls._bootstrap_defaults

    def ensure_default_register_set(self):
        if self.default_register_set is None:
            default_register_set = self.build_default_register_set()
            if default_register_set is not None:
                self.set_default_register_set(default_register_set)

    def build_default_register_set(self, wifi_country_code=None, video_anti_flicker_rate=None, video_quality_default=None):
        return None

    def get_ra_params_for_register_set(self, set_values):
        return None

    def send_default_register_set(self):
        if self.default_register_set is None:
            return True

        set_values = self.default_register_set['SetValues'] if 'SetValues' in self.default_register_set else {}
        if set_values is None:
            set_values = {}
        ra_params = self.get_ra_params_for_register_set(set_values)
        if ra_params is not None and not self.send_message(ra_params):
            return False

        register_set = Message(copy.deepcopy(self.default_register_set.dictionary))
        return self.send_message(register_set)
