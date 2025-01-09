import board
import busio
import digitalio
import adafruit_mcp2515

# Use CAN_CS, which is predefined for GPIO19
cs = digitalio.DigitalInOut(board.CAN_CS)
cs.direction = digitalio.Direction.OUTPUT

# Initialize SPI
spi = busio.SPI(board.SCK, board.MOSI, board.MISO)

# Initialize MCP2515
mcp = adafruit_mcp2515.MCP2515(spi, cs)

print("MCP2515 initialized successfully!")
