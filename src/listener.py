"""
This code is a very basic listener: it listens to the CAN bus and lights up the onboard LED when a message is received.
the small red led is also used to indicate that the program is running.
"""
import board
import busio
import digitalio
import neopixel
import time
import math
import adafruit_mcp2515

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
    
# visual feed-back on the microcontroller's board
normal_led = digitalio.DigitalInOut(board.D13)
normal_led.direction = digitalio.Direction.OUTPUT
rgb_led = neopixel.NeoPixel(board.NEOPIXEL, 1)
rgb_led.brightness = .5
    
timer = adafruit_mcp2515.canio.Timer(timeout=2)

while True:
    if timer.expired:
        normal_led.value = True
        time.sleep(0.1)
        normal_led.value = False
        time.sleep(0.1)

    listener = mcp.listen()
    message_count = listener.in_waiting()
    
    if message_count == 0:
        continue
    else:
        # If message recieved, victory led:
        for i in range(100):
            rgb_led.fill((255*math.sin(i/10), 255*math.cos(i/10), 50))
            time.sleep(0.05)