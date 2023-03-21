import socket
import sys
import copy

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

    def __getitem__(self, key):
        return self.registration[key]

    def send_message(self, message):
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:

            sock.settimeout(5.0)
            try:
                sock.connect((self.ip, self.port))
            except OSError as msg:
                print(f'Connection to camera failed: {msg}')
                return False

            result = False
            try:
                arloSock = ArloSocket(sock)
                self.id += 1
                message['ID'] = self.id
                s_print(f">[{self.ip}][{self.id}] {message['Type']}")
                arloSock.send(message)
                ack = arloSock.receive()
                if (ack != None):
                    if (ack['ID'] == message['ID']):
                        if ('Response' in ack and ack['Response'] != "Ack"):
                            s_print(f"<[{self.ip}][{self.id}] {ack['Response']}: {ack['Errors']}")
                            result = False
                        else:
                            s_print(f"<[{self.ip}][{self.id}] Ack")
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

    def arm(self, args):
        ...

    def mic_request(self, enabled):
        register_set = Message(copy.deepcopy(arlo.messages.REGISTER_SET))
        register_set['AudioMicEnable'] = enabled
        return self.send_message(register_set)

    def speaker_request(self, enabled):
        register_set = Message(copy.deepcopy(arlo.messages.REGISTER_SET))
        register_set['AudioSpkrEnable'] = enabled
        return self.send_message(register_set)

    def register_set(self, set_values):
        raw_register_set = copy.deepcopy(arlo.messages.REGISTER_SET)
        raw_register_set['SetValues'] = set_values
        register_set = Message(raw_register_set)
        return self.send_message(register_set)
