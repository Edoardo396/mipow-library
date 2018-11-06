import unittest
import mipow_device as mipow
import time


dev = mipow.mipow_device("12:5E:4B:11:AC:E6")


class MyTestCase(unittest.TestCase):

    def test_colors(self):
        dev.set_color(0x40, 0xb5, 0x66, 0xfa)
        time.sleep(3)




if __name__ == '__main__':
    unittest.main()