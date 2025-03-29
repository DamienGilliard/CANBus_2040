"""
This code is a very basic publisher: it sends a message to the CAN bus and lights up the onboard LED it is sent.
"""
import board
import busio
import digitalio
import neopixel
import microcontroller_module
import usb_cdc

# Use CAN_CS, which is predefined for GPIO19 on the microcontroller
cs = digitalio.DigitalInOut(board.CAN_CS)
cs.direction = digitalio.Direction.OUTPUT

# Initialize Serial Peripheral Interface (SPI)
spi = busio.SPI(board.SCK, board.MOSI, board.MISO)

can_controller = microcontroller_module.CANController(spi, cs, can_dict_path="CAN_table.csv")

# Listening to the USB port to receive commands from pc via USB
usb = usb_cdc.data
usb.timeout = 0.2
print("usb connected: ", usb.connected)

data = None

while True:
    can_controller.signal_standby_led()
    if usb.connected:
        data = usb.readline().decode("utf-8").strip()
    if data:
        if data == "turn on relay":
            usb.write("turning relay on!".encode("utf-8"))
            can_controller.send_message(id=0x100, message=0x01)
            data = None
            
        elif data == "turn off relay":
            usb.write("turning relay off!".encode("utf-8"))
            can_controller.send_message(id=0x100, message=0x00)
            data = None
