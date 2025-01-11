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
    # victory LED
    pixel = neopixel.NeoPixel(board.NEOPIXEL, 1)
    pixel.brightness = .5
    for i in range(100):
        pixel.fill((255*math.sin(i/10), 255*math.cos(i/10), 50))
        time.sleep(0.05)

except Exception as e:
    print("MCP2515 not detected")
    print(e)

pixel.fill((0, 0, 0))
    
