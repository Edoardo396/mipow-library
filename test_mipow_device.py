import unittest
import mipow_device as mipow
import time


dev = None #mipow.MipowDevice("12:5E:4B:11:AC:E6")


class MyTestCase(unittest.TestCase):

    def test_colors(self):
        dev.set_color(mipow.Color(0, 255, 128, 23))
        time.sleep(3)

    def test_effect_pulse(self):
        dev.set_effect(mipow.Effect.PULSE, 100, mipow.Color(0, 255, 0, 0))
        time.sleep(3)
        dev.set_effect(mipow.Effect.RAINBOW_FADE, 100)

## MUST RUN AS SUDO!
    def test_scan(self):
        mipow.MipowDevice.scan_devices()


if __name__ == '__main__':
    unittest.main()