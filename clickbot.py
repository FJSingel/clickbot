#!/usr/bin/python
usage = '''clickbot.py [OPTION]... MODE 
Executes the bot MODE (See MODE list) with the following options:
    -i (iteration_limit): Number of item iteration before termination (eg: potions to be made)
    -t (time_limit): Amount of time before termination in minutes
    -l (lag_constant): Multiplies wait times by this factor for laggy days
    -f (click_frequency): Determines number of seconds between clicks for Clicking MODE'''

modes = '''
MODES
0: Measure coordinates
1: Ivy
2: Superglass
3: Alching
4: Combining
5: HoM Div Clicks
6: Smithing
7: Idling
8: Herblore Dirty
9: Herblore clean
10: Fletching
11: Clicking
12: Archeology
'''

import pyautogui, sys, time, random, getopt;
from datetime import datetime, timedelta

LAG_CONSTANT = 1.0;
iteration_limit = 10000;
second_limit = 5*60*60;
start_second = int(time.time());
iteration_count = 0;
click_frequency = 60;
end_time = start_second;

def main(argv):
	global iteration_limit, second_limit, LAG_CONSTANT, end_time, click_frequency;
	# I know this is terrible. Should put methods into a list later

	try:
		opts, args = getopt.getopt(argv, "l:i:t:f:")
	except (IndexError, getopt.GetoptError):
		help();

	for o, a in opts:
		print(o);
		if o in "-l":
			LAG_CONSTANT = float(a);
		elif o in "-i":
			iteration_limit = int(a);
		elif o in "-f":
			click_frequency = int(a);
		elif o in "-t":
			second_limit = int(a) * 60.0;

	end_time += second_limit;

	print("Staring with the following parameters:");
	print("Lag constant: {}".format(LAG_CONSTANT));
	print("Max iterations: {}".format(iteration_limit));
	print("Time limit: {} seconds".format(second_limit));

	which = int(args[0]);
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
	elif which == 6:
		Smithing();
	elif which == 7:
		Idling();
	elif which == 8:
		Herblore(True);
	elif which == 9:
		Herblore(False);
	elif which == 10:
		Fletching();
	elif which == 11:
		print("Wait between clicks: {} seconds".format(click_frequency));
		Clicking();
	elif which == 12:
		print("Coming Soon");
	else:
		help();

	termination_message();

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
		while (time.time() < end_time):
			fuzz_factor = random.random()/4 + .875
			pyautogui.moveTo(x, y, fuzz_factor, pyautogui.easeInOutQuad)
			pyautogui.click();
			time.sleep(60*fuzz_factor)
	except KeyboardInterrupt:
		print("Clicking done\n")

def Superglass():
	global iteration_limit, end_time, second_limit;
	iteration_count = 0;
	print("Press CTRL+C to quit glassing")
	time.sleep(1)
	try:		
		while (time.time() < end_time) and (iteration_count < iteration_limit):
			open_bank();
			withdraw_preset('2');
			cast_superglass();
	except KeyboardInterrupt:
		print("Clicking done\n")

#Lol, this gets you banned. Leave alching to the noobs.
def Alching():
	global iteration_limit, end_time, second_limit;
	iteration_count = 0;
	print("Press CTRL+C to quit alching");
	try:		
		while (time.time() < end_time) and (iteration_count < iteration_limit):
			pyautogui.moveTo(1735, 750, .5, pyautogui.easeInOutQuad)
			pyautogui.click();
			pyautogui.click();
			time.sleep(fuzz_time(2, .15));
			iteration_count += 1;
			print("Iterations: {}/{}".format(iteration_count, iteration_limit));
			print("Time remaining: {}".format(end_time - time.time()));
	except KeyboardInterrupt:
		print("Clicking done\n")

def Combining():
	global iteration_limit, end_time, second_limit;
	iteration_count = 0;
	print("Press CTRL+C to quit combining")
	time.sleep(1)
	try:		
		while (time.time() < end_time) and (iteration_count < iteration_limit):
			open_bank();
			withdraw_preset('1');
			press_hotkey('1');
			pyautogui.press('space');
			time.sleep(fuzz_time(16, .1));
			iteration_count += 14;
			print("Iterations: {}/{}".format(iteration_count, iteration_limit));
			print("Time remaining: {}".format(end_time - time.time()));
	except KeyboardInterrupt:
		print("Clicking done\n")

def HallClicking():
	print("Press CTRL+C to quit clicking")
	try:		
		while (time.time() < end_time):
			try:
				mouseOver = pyautogui.locateCenterOnScreen('FadedMems.png');
				pyautogui.click();
				print(mouseOver)
			except Exception as e:
				print("Not found")
			time.sleep(.2);
	except KeyboardInterrupt:
		print("Clicking done\n")

def Smithing():
	print("Not yet Implemented:")

def Idling():
	print("Press CTRL+C to quit idling")
	try:		
		while True:
			try:
				pyautogui.keyDown('left');
				time.sleep(fuzz_time(.1, 3));
				pyautogui.keyUp('left');
				time.sleep(fuzz_time(120, 1));
			except Exception as e:
				print("Not found")
			time.sleep(.2);
	except KeyboardInterrupt:
		print("Idling done\n")

'''
Note: This requires preset 1 to have a 9/9/9 split of Dirty Herb/Vial/Ingredient on 1
Keys 1-3 need to be clean-mix-mix
Do World 84 By the Combat Academy Chest
'''
def Herblore(cleaning):
	global iteration_limit, end_time, second_limit;
	iteration_count = 0;
	print("Press CTRL+C to quit herblore")
	time.sleep(1)
	try:		
		while (time.time() < end_time) and (iteration_count < iteration_limit):
			open_bank();
			withdraw_preset('1');
			press_hotkey('1');
			if cleaning:
				press_hotkey('1');
				pyautogui.press('space');	
				time.sleep(fuzz_time(6, .25));
			press_hotkey('1');
			pyautogui.press('space');	
			time.sleep(fuzz_time(12, .25));
			press_hotkey('3');
			pyautogui.press('space');	
			time.sleep(fuzz_time(10, .25));
			iteration_count += 9
			print("Iterations: {}/{}".format(iteration_count, iteration_limit));
			print("Time remaining: {}".format(end_time - time.time()));
	except KeyboardInterrupt:
		print("Clicking done\n")

def Fletching():
	global iteration_limit, end_time, second_limit;
	iteration_count = 0;
	print("Press CTRL+C to quit fletching")
	time.sleep(1)
	try:		
		while (time.time() < end_time) and (iteration_count < iteration_limit):
			open_bank();
			withdraw_preset('1');
			press_hotkey('1');
			press_hotkey('4');

			pyautogui.press('space');	
			time.sleep(fuzz_time(26, .20));
			press_hotkey('5');
			pyautogui.press('space');	
			time.sleep(fuzz_time(15, .25));
			iteration_count += 14;
			print("Iterations: {}/{}".format(iteration_count, iteration_limit));
			print("Time remaining: {}".format(end_time - time.time()));
	except KeyboardInterrupt:
		print("Clicking done\n")

def Clicking():
	global iteration_limit, end_time, second_limit, click_frequency;
	iteration_count = 0;
	print("Locking mouse coordinates in 3 seconds");
	time.sleep(3);
	x,y = pyautogui.position();
	print("Press CTRL+C to quit clicking")
	time.sleep(1)
	try:		
		while (time.time() < end_time) and (iteration_count < iteration_limit):
			pyautogui.moveTo(x, y, .5, pyautogui.easeInOutQuad)
			pyautogui.click();
			wait = fuzz_time(click_frequency, .1)
			time.sleep(wait);
			iteration_count += 1;
			print("Iterations: {}/{}".format(iteration_count, iteration_limit));
			print("Time remaining: {}".format(end_time - time.time()));
	except KeyboardInterrupt:
		print("Clicking done\n")

'''=====================Helper Methods====================='''

def fuzz_time(min_time, pct_increase):
	fuzz_factor = (random.random() * pct_increase) + 1;
	return (min_time * fuzz_factor * LAG_CONSTANT);

def open_bank():
	pyautogui.moveTo(922, 514, .5, pyautogui.easeInOutQuad)
	pyautogui.click();
	time.sleep(fuzz_time(1.1, .25));

def withdraw_preset(preset):
	pyautogui.keyDown(preset);
	pyautogui.keyUp(preset);
	time.sleep(fuzz_time(1.1, .25));

def press_hotkey(hotkey):
	pyautogui.keyDown(hotkey);
	pyautogui.keyUp(hotkey);
	time.sleep(fuzz_time(1.1, .25));

def cast_superglass():
	pyautogui.keyDown('6');
	pyautogui.keyUp('6');
	time.sleep(fuzz_time(2.1, .25));

def help():
	print(usage);
	print(modes);

def termination_message():
	print("Consider logging off until {}".format(datetime.now() + timedelta(minutes=15)))

if __name__ == "__main__":
	try:
		main(sys.argv[1:])
	except IndexError:
		help();
