import unittest
import mipow_device as mipow
import time

dev = mipow.MipowDevice("12:5E:4B:11:AC:E6")


class MyTestCase(unittest.TestCase):

    def test_colors(self):
        dev.effect = mipow.Effect.STATIC
        dev.color = mipow.Color(0, 0, 0, 0)
        time.sleep(2)
        dev.color = mipow.Color(255, 0, 0, 0)
        time.sleep(2)
        dev.color = mipow.Color(0, 255, 0, 0)
        time.sleep(2)
        dev.color = mipow.Color(0, 0, 255, 0)
        time.sleep(2)
        dev.color = mipow.Color(0, 0, 0, 255)
        time.sleep(2)

    def test_effects(self):
        dev.effect_speed = 100
        dev.color = mipow.Color(0, 0, 255, 0)
        dev.effect = mipow.Effect.FLASH
        dev.update_remote()
        time.sleep(7)
        dev.color = mipow.Color(0, 255, 0, 0)
        dev.effect = mipow.Effect.PULSE
        dev.update_remote()
        time.sleep(7)
        dev.effect = mipow.Effect.RAINBOW
        dev.update_remote()
        time.sleep(7)
        dev.effect = mipow.Effect.RAINBOW_FADE

    def test_update(self):
        dev.update_local()

    def test_off_on(self):
        dev.effect = mipow.Effect.PULSE
        dev.color = mipow.Color(255,0,128,0)
        dev.effect_speed = 100
        dev.update_remote()
        time.sleep(2)
        dev.turn_off()
        time.sleep(5)
        dev.turn_on()



""" MUST RUN AS SUDO!
    def test_scan(self):
        mipow.MipowDevice.scan_devices()
"""

if __name__ == '__main__':
    unittest.main()
