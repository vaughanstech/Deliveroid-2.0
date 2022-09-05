import RPi.GPIO as GPIO
import time
import spidev
import os
import sys
from lib_nrf24 import NRF24

def Deliveroid():
	GPIO.setwarnings(False)
	GPIO.setmode(GPIO.BCM)
	bashCommand = "clear"
	pipes = [[0xE8, 0xE8, 0xF0, 0xF0, 0xE1], [0xF0, 0xF0, 0xF0, 0xF0, 0xE1]]

	radio = NRF24(GPIO, spidev.SpiDev())
	radio.begin(0, 17, 4000000)

	radio.setPayloadSize(32)
	radio.setChannel(0x76)
	radio.setDataRate(NRF24.BR_1MBPS)
	radio.setPALevel(NRF24.PA_MAX)

	radio.setAutoAck(True)
	radio.enableDynamicPayloads()
	radio.enableAckPayload()

	radio.openWritingPipe(pipes[0])
	radio.openReadingPipe(1, pipes[1])
	radio.printDetails()

	print("Welcome to Deliveroid 2.0")
	option1 = list("FORWARD")
	option2 = list("REVERSE")
	option3 = list("RIGHT")
	option4 = list("LEFT")
	option5 = list("STOP")
	option = int(input("Please choose the mode of operation:\n1. Move motors forward\n2. Move motors reverse\n3. Move motors right\n4. Move motors left\n5. stop\n>> "))

	if (option == 1):
		option = option1
	elif (option == 2):
		option = option2
	elif (option == 3):
		option = option3
	elif (option == 4):
		option = option4
	elif (option == 5):
		option = option5

	while len(option) < 32:
		option.append(0)

	while True:
		start = time.time()
		radio.write(option)
		print("Sent the command: {}".format(option))
		radio.startListening()

		while not radio.available(0):
			time.sleep(1/100)
			if time.time() - start > 2:
				print("Timed out.")
				break


		receivedMessage = []
		radio.read(receivedMessage, radio.getDynamicPayloadSize())
		print("Received: {}".format(receivedMessage))

		print("Translating the received message from Deliveroid into readable text...")
		string = ""

		for n in receivedMessage:
			if (n >= 32 and n <= 126):
				string += chr(n)
		print("The received message from Deliveroid: {}".format(string))
		radio.stopListening()
		time.sleep(1)
		break
	print("Cleaning GPIO")
	GPIO.cleanup()
	Deliveroid()

Deliveroid()
