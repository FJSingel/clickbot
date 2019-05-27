#!/usr/bin/python
modes = '''
Modes
0: Measure coordinates
1: Ivy
2: Superglass
3: Alching
4: Combining
5: HoM Div Clicks
6: Smithing
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
	elif which == 4:
		Combining();
	elif which == 5:
		HallClicking();
	else:
		print(modes);

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
	print("Press CTRL+C to quit glassing")
	time.sleep(1)
	try:		
		while True:
			pyautogui.moveTo(953, 450, .5, pyautogui.easeInOutQuad)
			pyautogui.click();
			time.sleep(fuzz_time(1.1, .25));
			pyautogui.keyDown('1');
			pyautogui.keyUp('1');
			time.sleep(fuzz_time(1.1, .25));
			pyautogui.keyDown('2');
			pyautogui.keyUp('2');
			time.sleep(fuzz_time(2.1, .25));
	except KeyboardInterrupt:
		print("Clicking done\n")

def Alching():
	print("Press CTRL+C to quit alching")
	try:		
		while True:
			pyautogui.moveTo(1735, 835, .5, pyautogui.easeInOutQuad)
			pyautogui.click();
			pyautogui.click();
			time.sleep(fuzz_time(2, .15));
	except KeyboardInterrupt:
		print("Clicking done\n")

def Combining():
	print("Press CTRL+C to quit combining")
	time.sleep(1)
	try:		
		while True:
			pyautogui.moveTo(953, 450, .5, pyautogui.easeInOutQuad)
			pyautogui.click();
			time.sleep(fuzz_time(1.1, .25));
			pyautogui.keyDown('1');
			pyautogui.keyUp('1');
			time.sleep(fuzz_time(1.1, .25));
			pyautogui.keyDown('1');
			pyautogui.keyUp('1');
			time.sleep(fuzz_time(1.1, .25));
			pyautogui.press('space');	
			time.sleep(fuzz_time(17, .25));
	except KeyboardInterrupt:
		print("Clicking done\n")

def HallClicking():
	print("Press CTRL+C to quit clicking")
	try:		
		while True:
			try:
				mouseOver = pyautogui.locateCenterOnScreen('FadedMems.png');
				pyautogui.click();
				print(mouseOver)
			except Exception as e:
				print("Not found")
			time.sleep(.2);
	except KeyboardInterrupt:
		print("Clicking done\n")

def fuzz_time(min_time, pct_increase):
	fuzz_factor = (random.random() * pct_increase) + 1;
	return (min_time * fuzz_factor);

if __name__ == "__main__":
	try:
		main(sys.argv[1:])
	except IndexError:
		print (modes);
