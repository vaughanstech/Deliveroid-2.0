import RPi.GPIO as GPIO
import time
import spidev
import os
import sys
from pynput import keyboard
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
	print("Please choose the mode of operation:\n1. Move motors forward\n2. Move motors reverse\n3. Move motors right\n4. Move motors left\n5. stop\n>> ")

	with keyboard.Events() as events:
		event = events.get(1e6)
		if (event.key == keyboard.KeyCode.from_char('w')):
			option = list("FORWARD")
		elif (event.key == keyboard.KeyCode.from_char('s')):
			option = list("REVERSE")
		elif (event.key == keyboard.KeyCode.from_char('a')):
			option = list("LEFT")
		elif (event.key == keyboard.KeyCode.from_char('d')):
			option = list("RIGHT")
		elif (event.key == keyboard.KeyCode.from_char('x')):
			option = list("STOP")

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
