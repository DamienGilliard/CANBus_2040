"""
This code is a very basic listener: it listens to the CAN bus and lights up the onboard LED when a message is received.
the small red led is also used to indicate that the program is running.
"""
import board
import busio
import digitalio
import analogio
import microcontroller_module

# Use CAN_CS, which is predefined for GPIO19
cs = digitalio.DigitalInOut(board.CAN_CS)
cs.direction = digitalio.Direction.OUTPUT

relay_pin = digitalio.DigitalInOut(board.A1)
relay_pin.direction = digitalio.Direction.OUTPUT

# Initialize Serial Peripheral Interface (SPI)
spi = busio.SPI(board.SCK, board.MOSI, board.MISO)

can_controller = microcontroller_module.CANController(spi, cs, can_dict_path="CAN_table.csv")

while True:
    message = can_controller.listen()
    can_controller.signal_standby_led()
    if message is not None:
        command = message.data[0]
        print(f"Received command: {command}")

        if command == 0x01:
            relay_pin.value = True
            can_controller.signal_success_led(0.05)
        elif command == 0x00:
            relay_pin.value = False
            can_controller.signal_success_led(0.05)
