"""
This module contains the code for interfacing with the mocrocontrollers
"""

import board
import adafruit_mcp2515
import neopixel
import time

class CANController:
    """
    This class is used to control the MCP2515 CAN controller and the RGB LED on the microcontroller board.
    """

    def __init__(self, spi, cs, can_dict_path="../can_dict.csv"):
        """
        Initializes the Controller class.

        Parameters:
        spi (SPI): The Serial Peripheral Interface (SPI) bus to use (default is board.SPI()).
        cs (DigitalInOut): The pin for the MCP2515 controller (default is board.CAN_CS).
        CAN_id (int): The CAN ID assigned to the microcontroller (default is 0x100).
        """
        self.spi = spi
        self.cs = cs
        self.mcp = self.setup_MCP2515()
        self.can_dict = self.__read_can_dictionnary(can_dict_path)
        self.rgb_led = neopixel.NeoPixel(board.NEOPIXEL, 1)

    def __read_can_dictionnary(self, csv_file_path):
        """
        Reads a CAN dictionary file (.csv) and returns the contents as a dictionary.
        the lines of the file should be structures as such:
        name, id, message, what it does

        Parameters:
        file_path (str): The path to the CAN dictionary file.

        Returns:
        dict: The contents of the CAN dictionary file as a dictionary.
        """
        with open(csv_file_path, 'r') as file:
            can_dict = {}
            for line in file:
                # Split the line into key-value pairs
                device_description, message_id, command_value, command_description = line.strip().split(',')
                can_dict[message_id] = command_description
            if not can_dict:
                self.signal_error_led()
                return None
        return can_dict

    def set_rgb_color(self, color, brightness=1.0):
        """
        Sets the color of the RGB LED on the microcontroller board.
        Parameters:
        color (tuple): A tuple containing the RGB values (0-255) for the LED color.
        brightness (float): The brightness level of the LED (0.0 to 1.0).
        """
        self.rgb_led.brightness = brightness
        self.rgb_led.fill(color)

    def signal_error_led(self, sleep_time=0.1):
        """
        Signals an error by blinking the RGB LED on the microcontroller board.
        """
        for i in range(100):
            self.set_rgb_color((255, 0, 0), 1.0)
            time.sleep(sleep_time)
            self.set_rgb_color((100, 0, 0), 0.5)
            time.sleep(sleep_time)
            
    def signal_standby_led(self, sleep_time=0.1):
        """
        Signals standby mode by blinking the RGB LED on the microcontroller board.
        """
        self.set_rgb_color((0, 0, 255), 1.0)
        time.sleep(sleep_time)
        self.set_rgb_color((0, 0, 100), 0.5)
        time.sleep(sleep_time)
            
    def signal_success_led(self, sleep_time=0.1):
        """
        Signals that a process was successful. Sort of "return 1" but visual on the microcontroller
        """
        for i in range(2):
            self.set_rgb_color((0, 255, 0), 1.0)
            time.sleep(sleep_time)
            self.set_rgb_color((0, 100, 0), 0.5)
            time.sleep(sleep_time)
            
    def setup_MCP2515(self):
        """
        Sets up the MCP2515 CAN controller on the microcontroller board.
        """
        try:
            mcp = adafruit_mcp2515.MCP2515(self.spi, self.cs)
            print("MCP2515 detected, and device baudrate: ", mcp.baudrate)
            return mcp
        except Exception as e:
            print("MCP2515 not detected")
            print(e)
            self.signal_error_led()
            return None
        
    def send_message(self, id, message):
        """
        Sends a CAN message using the MCP2515 controller.
        Parameters:
        id (int): The CAN ID of the message.
        message (Message): The CAN message to send.
        """
        try:
            self.mcp.send(message)
        except Exception as e:
            print("Error sending message:", e)
            self.signal_error_led()
            return None
        
    def listen(self):
        """
        Listens for incoming CAN messages using the MCP2515 controller.
        Returns:
        Message: The received CAN message.
        """
        try:
            listener = self.mcp.listen()
            message_count = listener.in_waiting()
            if message_count == 0:
                return None
            else:
                received_message = listener.receive()
                return received_message
        except Exception as e:
            print("Error listening for messages:", e)
            self.signal_error_led(0.5)
            return None
        
    def publish_CAN_message(self, id, data):
        """
        Publishes a CAN message using the MCP2515 controller.
        Parameters:
        id (int): The CAN ID of the message.
        data (bytes): The data to send in the message.
        """
        try:
            my_message = adafruit_mcp2515.canio.Message(id=id, data=data)
            self.mcp.send(my_message)
        except Exception as e:
            print("Error publishing CAN message:", e)
            self.signal_error_led()
            return None
        self.signal_success_led(0.05)