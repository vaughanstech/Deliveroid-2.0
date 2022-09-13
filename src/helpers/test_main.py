import RPi.GPIO as GPIO
import time
import spidev
import os
import sys
from pick import pick
from getkey import getkey, key
from lib_nrf24 import NRF24

def DeliveroidRemoteControl():
	GPIO.setwarnings(False)
	GPIO.setmode(GPIO.BCM)
	bashClearCommand = "clear"
	pipes = [[0xE8, 0xE8, 0xF0, 0xF0, 0xE1], [0xF0, 0xF0, 0xF0, 0xF0, 0xE1]]

	radio = NRF24(GPIO, spidev.SpiDev())
	radio.begin(0, 17, 4000000)

	radio.setPayloadSize(32)
	radio.setChannel(0x5A)
	radio.setDataRate(NRF24.BR_1MBPS)
	radio.setPALevel(NRF24.PA_MAX)

	radio.setAutoAck(True)
	radio.enableDynamicPayloads()
	radio.enableAckPayload()

	radio.openWritingPipe(pipes[0])
	radio.openReadingPipe(1, pipes[1])
	radio.printDetails()
	os.system(bashClearCommand)

	print("Deliveroid is in Inside Mode:")
	print("Controls:\n")
	print("_________________")
	print("w = FORWARD\t|")
	print("a = LEFT   \t|")
	print("s = REVERSE\t|")
	print("d = RIGHT  \t|")
	print("x = STOP   \t|__________________")
	print("q = QUIT MODE\t| z = QUIT CONTROL|")
	option1 = list("FORWARD")
	option2 = list("REVERSE")
	option3 = list("RIGHT")
	option4 = list("LEFT")
	option5 = list("STOP")
	# option = int(input("Please choose the mode of operation:\n1. Move motors forward\n2. Move motors reverse\n3. Move motors right\n4. Move motors left\n5. stop\n>> "))
	print("Choose an option: ")
	key = getkey()

	if (key == 'w'):
		option = option1
	elif (key == 's'):
		option = option2
	elif (key == 'd'):
		option = option3
	elif (key == 'a'):
		option = option4
	elif (key == 'x'):
		option = option5
	elif (key == 'q'):
		option = option5
		print("Stopping Operation...")
		print("Quitting...")
		main_menu()
	elif (key == 'z'):
		print("Stopping Operation...")
		option = option5
		print("Goodbye!")
		return True
	else:
		print("This options is not valid. Please retry.")
		DeliveroidRemoteControl()

	while len(option) < 32:
		option.append(0)

	while True:
		start = time.time()
		radio.write(option)
		print("Sent the command: {}".format(option))
		radio.startListening()

		while not radio.available(0):
			time.sleep(1/100)
			if time.time() - start > 1:
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
		break
	print("Cleaning GPIO")
	GPIO.cleanup()
	DeliveroidRemoteControl()

def main_menu():
	title ="""
-------------------------------------------
/        Welcome to Deliveroid 2.0        \\
/       Created by: Michael Vaughan       \\
-------------------------------------------
	 Choose Deliveroid Control
"""
	options = ["Remote Control", "Autonomous"]
	option, index = pick(options, title, indicator="=>")
	if (option == "Remote Control"):
		DeliveroidRemoteControl()

main_menu()
