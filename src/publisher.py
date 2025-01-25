"""
This code is a very basic publisher: it sends a message to the CAN bus and lights up the onboard LED it is sent.
"""
import board
import busio
import digitalio
import neopixel
import time
import adafruit_mcp2515
import usb_cdc
import math

# Use CAN_CS, which is predefined for GPIO19
cs = digitalio.DigitalInOut(board.CAN_CS)
cs.direction = digitalio.Direction.OUTPUT

# Initialize Serial Peripheral Interface (SPI)
spi = busio.SPI(board.SCK, board.MOSI, board.MISO)

# Initialize MCP2515
try:
    mcp = adafruit_mcp2515.MCP2515(spi, cs)
    print("MCP2515 detected, and device baudrate: ", mcp.baudrate)
except Exception as e:
    print("MCP2515 not detected")
    print(e)

# Listening to the USB port
usb = usb_cdc.data
usb.timeout = 0.2
print("usb connected: ", usb.connected)

# Visual feedback on the microcontroller's board
normal_led = digitalio.DigitalInOut(board.D13)
normal_led.direction = digitalio.Direction.OUTPUT
rgb_led = neopixel.NeoPixel(board.NEOPIXEL, 1)
rgb_led.brightness = 0.5

timer = adafruit_mcp2515.canio.Timer(timeout=2)
data = None

while True:
    if usb.connected:
        data = usb.readline().decode("utf-8").strip()
    if data:
        if data == "turn on relay":
            usb.write("turning relay on!".encode("utf-8"))
            listener = mcp.listen()
            my_message = adafruit_mcp2515.canio.Message(id=0x100, data=bytes([0x01]))
            mcp.send(my_message)
            data = None
            

        elif data == "turn off relay":
            usb.write("turning relay off!".encode("utf-8"))
            listener = mcp.listen()
            my_message = adafruit_mcp2515.canio.Message(id=0x100, data=bytes([0x00]))
            mcp.send(my_message)
            data = None

    # Reset the data to avoid looping over the same data
    data = None

    # Blink the normal led to let the user know the program is running even if no victory led is shown
    normal_led.value = not normal_led.value