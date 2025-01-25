import serial
import time

# Open the serial port for writing
data_sender = serial.Serial(port='/dev/cu.usbmodem103', baudrate=115200, timeout=1)

bites_sent = data_sender.write('turn on relay'.encode("utf-8"))
print(f"Bytes sent: {bites_sent}")
time.sleep(0.5)
data_sender.flush()

# Listen back to the microcontroller
received_data = data_sender.readline()
print(f"Data received: {received_data.decode('utf-8')}")

# Close the serial port
data_sender.close()