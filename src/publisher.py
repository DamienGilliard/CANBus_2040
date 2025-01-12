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
        data = usb.read()
    if data:
        print(data)
        usb.write("recieved!".encode("utf-8"))
        listener = mcp.listen()
        my_message = adafruit_mcp2515.canio.Message(id=0, data=data)
        
        if mcp.send(my_message):
            # If message sent, victory led:
            for i in range(100):
                rgb_led.fill((255*math.sin(i/10), 255*math.cos(i/10), 50))
                time.sleep(0.05)
            rgb_led.fill((0, 0, 0))

    # Reset the data to avoid looping over the same data
    data = None

    # Blink the normal led to let the user know the program is running even if no victory led is shown
    if timer.expired:
        normal_led.value = True
        time.sleep(0.1)
        normal_led.value = False
        time.sleep(0.1)
