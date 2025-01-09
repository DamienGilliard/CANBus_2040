# Setup

Adafruit [provides a library](https://github.com/adafruit/Adafruit_CircuitPython_MCP2515) for the CAN controller, that can be installed as follows: 

1) Setup the Microcontroller, for example using [Thonny](https://thonny.org/):
* press and hold the *Boot* button while plugging the usb-c cable to your computer with Thonny installed.
* in the botton right corner of the Thonny IDE, click on "Local Python 3" and select "configure interpreter"
* Choose "CircuitPython" as interpreter, and the "RP2040 CAN" as Port. Circuit python will be installed if it is not already. (Note: I believe MicroPython can also be used, basic code using the MCP2515 works, but further validation is needed)
* You are good to go !

2) Install the `adafruit_mcp2515` library:
* Download the [repository](https://github.com/adafruit/Adafruit_CircuitPython_MCP2515).
* Using thonny, move the `adafruit_mcp2515` folder to the microcontroller:
<p align="center"> <img src="./assets/img/install_Adafruit_lib.png" width=50% />

3) Test the library:
* execute the [`basic_test.py`](./src/basic_test.py) code. Check that you are using the microcontroller as interpreter. If you get this, it worked:
```bash
>>> %Run -c $EDITOR_CONTENT
MCP2515 initialized successfully!
>>> 
```