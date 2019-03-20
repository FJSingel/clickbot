#!/usr/bin/python
'''
Modes
0: Measures coordinates
1: Ivy
2: Superglass
3: Alching
'''

import pyautogui, sys, time, random

def main(argv):
	# I know this is terrible. Should put methods into a list later
	which = int(argv[0])
	if which == 0:
		Measure();
	elif which == 1:
		Ivy();
	elif which == 2:
		Superglass();
	elif which == 3:
		Alching();
	else:
		print("Number not deefined yet")

def Measure():
	try:
		while True:
			x,y = pyautogui.position();
			positionString = "X:" + str(x) + " Y:" + str(y)
			print(positionString)
			time.sleep(.5)
	except KeyboardInterrupt:
		print("Coordinates are " + positionString)

def Ivy():
	print("Click to select coordinates for Ivy")
	try:
		positionString = ""
		x = 0
		y = 0
		while True:
			x,y = pyautogui.position();
			positionString = "X:" + str(x) + " Y:" + str(y)
			print(positionString)
			time.sleep(.5)
	except KeyboardInterrupt:
		print("Coordinates are " + positionString)
	print("Press CTRL+C to quit")
	try:
		while True:
			fuzz_factor = random.random()/4 + .875
			pyautogui.moveTo(x, y, fuzz_factor, pyautogui.easeInOutQuad)
			pyautogui.click();
			time.sleep(60*fuzz_factor)
	except KeyboardInterrupt:
		print("Clicking done\n")

def Superglass():
	print("Glass")

def Alching():
	print("Alch")

if __name__ == "__main__":
	main(sys.argv[1:])