import threading
import sqlite3
import functools
import json
import ast

from arlo.messages import Message
from arlo.device_factory import DeviceFactory
from arlo.device import Device


class DeviceDB:
    sqliteLock = threading.RLock()
    schemaChecked = False

    def synchronized(wrapped):
        @functools.wraps(wrapped)
        def _wrapper(*args, **kwargs):
            with DeviceDB.sqliteLock:
                return wrapped(*args, **kwargs)
        return _wrapper

    @staticmethod
    @synchronized
    def ensure_schema():
        if DeviceDB.schemaChecked:
            return

        with sqlite3.connect('arlo.db') as conn:
            c = conn.cursor()
            camera_table = c.execute(
                "SELECT tbl_name FROM sqlite_schema WHERE type='table' AND tbl_name='camera'"
            ).fetchall()
            devices_table = c.execute(
                "SELECT tbl_name FROM sqlite_schema WHERE type='table' AND tbl_name='devices'"
            ).fetchall()

            if camera_table != [] and devices_table == []:
                c.execute('ALTER TABLE camera RENAME TO devices')

            c.execute(
                "CREATE TABLE IF NOT EXISTS devices ("
                "ip text, serialnumber text, hostname text, "
                "registration text, status text, register_set text, friendlyname text)"
            )

            columns = [row[1] for row in c.execute("PRAGMA table_info(devices)").fetchall()]
            if 'registration' not in columns:
                c.execute("ALTER TABLE devices ADD COLUMN registration text")
                # Legacy layout stored registration in status and status in register_set.
                c.execute(
                    "UPDATE devices SET registration = status, status = register_set, register_set = NULL "
                    "WHERE registration IS NULL"
                )

            c.execute("CREATE UNIQUE INDEX IF NOT EXISTS idx_device_serialnumber ON devices (serialnumber)")
            c.execute("CREATE UNIQUE INDEX IF NOT EXISTS idx_device_ip ON devices (ip)")
            c.execute("CREATE UNIQUE INDEX IF NOT EXISTS idx_device_friendlyname ON devices (friendlyname)")
            c.execute("CREATE UNIQUE INDEX IF NOT EXISTS idx_device_hostname ON devices (hostname)")
            conn.commit()

        DeviceDB.schemaChecked = True

    @staticmethod
    def _to_json(value):
        if value is None:
            return None

        if isinstance(value, Message):
            return value.toJSON()

        if isinstance(value, str):
            return value

        return json.dumps(value, separators=(',', ':'))

    @staticmethod
    def _to_message(value):
        if value is None or value == "None":
            return None

        try:
            return Message(json.loads(value))
        except Exception:
            pass

        try:
            parsed = ast.literal_eval(value)
            if isinstance(parsed, dict):
                return Message(parsed)
        except Exception:
            pass

        return None

    @staticmethod
    @synchronized
    def from_db_serial(serial):
        DeviceDB.ensure_schema()
        with sqlite3.connect('arlo.db') as conn:
            c = conn.cursor()
            c.execute(
                "SELECT ip, serialnumber, hostname, registration, status, register_set, friendlyname "
                "FROM devices WHERE serialnumber = ?",
                (serial,)
            )
            result = c.fetchone()
            return DeviceDB.from_db_row(result)

    @staticmethod
    @synchronized
    def from_db_ip(ip):
        DeviceDB.ensure_schema()
        with sqlite3.connect('arlo.db') as conn:
            c = conn.cursor()
            c.execute(
                "SELECT ip, serialnumber, hostname, registration, status, register_set, friendlyname "
                "FROM devices WHERE ip = ?",
                (ip,)
            )
            result = c.fetchone()
            return DeviceDB.from_db_row(result)

    @staticmethod
    def from_db_row(row):
        if row is not None:
            (ip, _, _, registration, status, register_set, friendly_name) = row
            _registration = DeviceDB._to_message(registration)
            if _registration is None:
                # Legacy fallback
                _registration = DeviceDB._to_message(status)
            if _registration is None:
                return None

            device = DeviceFactory.createDevice(ip, _registration)
            if device is None:
                return None

            device.status = DeviceDB._to_message(status)
            device.default_register_set = DeviceDB._to_message(register_set)
            device.friendly_name = friendly_name
            return device
        else:
            return None

    @staticmethod
    @synchronized
    def persist(device: Device):
        DeviceDB.ensure_schema()
        with sqlite3.connect('arlo.db') as conn:
            c = conn.cursor()
            # Remove the IP for any redundant device that has the same IP...
            c.execute("UPDATE devices SET ip = 'UNKNOWN' WHERE ip = ? AND serialnumber <> ?",
                      (device.ip, device.serial_number))
            c.execute(
                "REPLACE INTO devices "
                "(ip, serialnumber, hostname, registration, status, register_set, friendlyname) "
                "VALUES (?,?,?,?,?,?,?)",
                (
                    device.ip,
                    device.serial_number,
                    device.hostname,
                    DeviceDB._to_json(device.registration),
                    DeviceDB._to_json(device.status),
                    DeviceDB._to_json(device.default_register_set),
                    device.friendly_name
                )
            )
            conn.commit()

    @staticmethod
    @synchronized
    def delete(device: Device):
        DeviceDB.ensure_schema()
        with sqlite3.connect('arlo.db') as conn:
            c = conn.cursor()
            # Remove the IP for any redundant device that has the same IP...
            c.execute("DELETE FROM devices WHERE ip = ? AND serialnumber = ?",
                      (device.ip, device.serial_number))            
            conn.commit()
            return True
