import RPi.GPIO as GPIO
from lib_nrf24 import NRF24
import time
import spidev

GPIO.setmode(GPIO.BCM)

# setting sending and receiving addresses
pipes = [[0xE8, 0xE8, 0xF0, 0xF0, 0xE1], [0xF0, 0xF0, 0xF0, 0xF0, 0xE1]]

radio = NRF24(GPIO, spidev.SpiDev())
radio.begin(0, 17, 4000000)

radio.setPayloadSize(32)
radio.setChannel(0x76)
radio.setDataRate(NRF24.BR_1MBPS)
radio.setPALevel(NRF24.PA_MIN)


radio.setAutoAck(True)
radio.enableDynamicPayloads()
radio.enableAckPayload()

radio.openWritingPipe(pipes[0])
radio.openReadingPipe(1, pipes[1])
radio.printDetails()

message = list("GETSTRING")
while len(message) < 32:
	message.append(0)

while True:
	# creating command to signal the Arduino to do something
	start = time.time()
	radio.write(message)
	print("Sent the message: {}".format(message))
	radio.startListening()
	
	# if the command is not doing anything on the Arduino time out
	while not radio.available(0):
		time.sleep(1/100)
		if time.time() - start > 2:
			print("Timed out.")
			break

	# creating buffer for the returned message from the Arduino
	receivedMessage = []
	radio.read(receivedMessage, radio.getDynamicPayloadSize())
	print("Received: {}".format(receivedMessage))

	print("translating our received Message into unicode characters...")
	string = ""

	# decode the message sent from the Arduino to human readable text
	for n in receivedMessage:
		if (n >= 32 and n <= 126):
			string += chr(n)
	print("Our received message decodes to: {}".format(string))
	
	# once the command has finished executing on the Arduino stop listening so another command may be sent
	radio.stopListening()
	time.sleep(1)
