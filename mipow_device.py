import bluepy.btle as bp
import bluepy
from enum import Enum

class Color:
    white = 0
    red = 0
    green = 0
    blue = 0

    def __init__(self, white, red, blue, green):
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


class MipowDevice:

    SET_COLOR_HANDLE = 0x001b
    SET_EFFECT_HANDLE = 0x0019

    device_address = ""
    device = None

    def __init__(self, address):
        self.device_address = address
        self.device = bp.Peripheral(address)

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.device.disconnect()

    def set_color(self, color: Color):
        value = bytes([color.white, color.red, color.green, color.blue])
        print(value)
        self.device.writeCharacteristic(self.SET_COLOR_HANDLE, value, False)

    def set_effect(self, effect: Effect, speed, color: Color = None):
        color = MipowDevice.color_if_none(color)

        if effect == Effect.STATIC:
            self.set_color(color)
            return

        effect_code = effect.value - 1
        speed = 255 - round(speed * (255/100))
        self.device.writeCharacteristic(self.SET_EFFECT_HANDLE, bytes([color.white, color.red, color.green,
                                                                       color.blue, effect_code, 0, speed, 0]))

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














