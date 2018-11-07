import bluepy.btle as bp
import bluepy
from enum import Enum
import struct


class Color:
    red = 0
    green = 0
    blue = 0
    white = 0

    def __init__(self, red, green, blue, white):
        self.white = white
        self.red = red
        self.blue = blue
        self.green = green


class Effect(Enum):
    STATIC = 0
    FLASH = 1
    PULSE = 2
    RAINBOW = 3
    RAINBOW_FADE = 4


COLOR_CHARACTERISTIC_UUID = bp.UUID("0000fffc-0000-1000-8000-00805f9b34fb")
EFFECT_CHARACTERISTIC_UUID = bp.UUID("0000fffb-0000-1000-8000-00805f9b34fb")


class MipowDevice:

    def __init__(self, address):
        self._color = None  # type: Color
        self._effect = None
        self._effect_speed = 0
        self.device_address = address
        self.device = bp.Peripheral(address)
        characteristics = self.device.getCharacteristics(0x0001)
        self.color_characteristic = next(filter(lambda el: el.uuid == COLOR_CHARACTERISTIC_UUID, characteristics))
        self.effect_characteristic = next(filter(lambda el: el.uuid == EFFECT_CHARACTERISTIC_UUID, characteristics))
        self.update_local()

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.device.disconnect()

    @property
    def color(self):
        self.update_local()
        return self._color

    @color.setter
    def color(self, color: Color):
        self._color = color

    @property
    def effect(self):
        self.update_local()
        return self._effect

    @effect.setter
    def effect(self, value: Effect):
        self._effect = value

    @property
    def effect_speed(self):
        self.update_local()
        return self._effect_speed

    @effect_speed.setter
    def effect_speed(self, value):
        self._effect_speed = value

    def update_local(self):
        color_value = self.color_characteristic.read()
        effect_value = self.effect_characteristic.read()
        self._effect_speed = effect_value[6] * (100/255)

        # solid color set
        if effect_value[4] == 255:
            self._color = Color(color_value[0], color_value[1], color_value[2], color_value[3])
            self._effect = Effect.STATIC
            return

        # effect set
        if effect_value[4] != 255:
            self._color = Color(effect_value[0], effect_value[1], effect_value[2], effect_value[3])
            self._effect = Effect(effect_value[4] + 1)

    def update_remote(self):
        if self._effect == Effect.STATIC:
            self.color_characteristic.write(bytes([self._color.white, self._color.red, self._color.green, self._color.blue]))
        else:
            speed = 255 - round(self._effect_speed * (255 / 100))
            array = [self._color.white, self._color.red, self._color.green, self._color.blue,
                     self._effect.value - 1, 0, speed, 0]
            print(array)
            self.effect_characteristic.write(bytes(array))

    def disconnect(self):
        self.device.disconnect()

    def reconnect(self):
        self.disconnect()
        self.device.connect(self.device_address)

    @staticmethod
    def scan_devices():
        scanner = bp.Scanner()
        devices = scanner.scan(10.0)

        for dev in devices:
            print("Device %s (%s), RSSI=%d dB" % (dev.addr, dev.addrType, dev.rssi))
            for (adtype, desc, value) in dev.getScanData():
                print("  %s = %s" % (desc, value))

    @staticmethod
    def color_if_none(color: Color):
        if color is None:
            return Color(0, 0, 0, 0)
        else:
            return color