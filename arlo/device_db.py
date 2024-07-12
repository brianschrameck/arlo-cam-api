import threading
import sqlite3
import functools

from arlo.messages import Message
from arlo.device_factory import DeviceFactory
from arlo.device import Device


class DeviceDB:
    sqliteLock = threading.Lock()

    def synchronized(wrapped):
        @functools.wraps(wrapped)
        def _wrapper(*args, **kwargs):
            with DeviceDB.sqliteLock:
                return wrapped(*args, **kwargs)
        return _wrapper

    @staticmethod
    @synchronized
    def from_db_serial(serial):
        with sqlite3.connect('arlo.db') as conn:
            c = conn.cursor()
            c.execute("SELECT * FROM devices WHERE serialnumber = ?", (serial,))
            result = c.fetchone()
            return DeviceDB.from_db_row(result)

    @staticmethod
    @synchronized
    def register_set_from_db_serial(serial: str):
        with sqlite3.connect('arlo.db') as conn:
            c = conn.cursor()
            c.execute("SELECT set_values FROM register_sets WHERE serialnumber = ?", (serial,))
            result = c.fetchone()
            if result is not None:
                return Message.from_json(result[0])
            else:
                return None

    @staticmethod
    @synchronized
    def from_db_ip(ip):
        with sqlite3.connect('arlo.db') as conn:
            c = conn.cursor()
            c.execute("SELECT * FROM devices WHERE ip = ?", (ip,))
            result = c.fetchone()
            return DeviceDB.from_db_row(result)

    @staticmethod
    def from_db_row(row):
        if row is not None:
            (ip, _, _, registration, status, friendly_name) = row
            _registration = Message.from_json(registration)

            device = DeviceFactory.createDevice(ip, _registration)
            if device is None:
                return None

            device.status = Message.from_json(status)
            device.friendly_name = friendly_name
            return device
        else:
            return None

    @staticmethod
    @synchronized
    def persist(device: Device):
        with sqlite3.connect('arlo.db') as conn:
            c = conn.cursor()
            # Remove the IP for any redundant device that has the same IP...
            c.execute("UPDATE devices SET ip = 'UNKNOWN' WHERE ip = ? AND serialnumber <> ?",
                      (device.ip, device.serial_number))
            c.execute("REPLACE INTO devices VALUES (?,?,?,?,?,?)", (device.ip, device.serial_number,
                      device.hostname, repr(device.registration), repr(device.status), device.friendly_name))
            conn.commit()

    @staticmethod
    @synchronized
    def persist_register_set(serial: str, register_set: Message):
        with sqlite3.connect('arlo.db') as conn:
            c = conn.cursor()
            # retrieve the existing register set and overwrite any of it's values with the new register set values
            # this is to ensure that we don't lose any values that are not in the new register set
            c.execute("SELECT set_values FROM register_sets WHERE serialnumber = ?", (serial,))
            register_set_result = c.fetchone()
            if register_set_result is not None:
                existing_register_set= Message.from_json(register_set_result[0])
                for key in register_set['SetValues']:
                    existing_register_set['SetValues'][key] = register_set['SetValues'][key]
                register_set = existing_register_set

            c.execute("REPLACE INTO register_sets VALUES (?,?)", (serial, register_set.toJSON()))
            conn.commit()

    @staticmethod
    @synchronized
    def delete(device: Device):
        with sqlite3.connect('arlo.db') as conn:
            c = conn.cursor()
            # Remove the IP for any redundant device that has the same IP...
            c.execute("DELETE FROM devices WHERE ip = ? AND serialnumber = ?",
                      (device.ip, device.serial_number))            
            conn.commit()
            return True