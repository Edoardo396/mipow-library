import bluepy
import bluepy.btle as bp


class MipowDevice:

    device_address = ""
    device = None

    def __init__(self, address):
        self.device_address = address
        self.device = bp.Peripheral(address)

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.device.disconnect()
        print("disconnected")

    def set_color(self, white, red, green, blue):
        value = bytes([white, red, green, blue])
        print(value)
        self.device.writeCharacteristic(0x001b, value, False)

    def reconnect(self):
        self.device.connect(self.device_address)














