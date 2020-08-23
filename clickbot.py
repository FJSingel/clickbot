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
8: Clean Herbs w/ Cape
9: Herblore clean
10: Fletching
11: Clicking
12: Graceful Archeology
13: Deposit Archaeology
14: Agility
'''

import pyautogui, sys, time, random, getopt, logging;
from datetime import datetime, timedelta

console = logging.StreamHandler(sys.stdout);
console.setLevel(logging.INFO);

logging.basicConfig(
	level=logging.DEBUG,
	format='%(asctime)s %(message)s',
	handlers=[
		logging.FileHandler("clickbot.log"),
		console
	]
)

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
		logging.debug(o);
		if o in "-l":
			LAG_CONSTANT = float(a);
		elif o in "-i":
			iteration_limit = int(a);
		elif o in "-f":
			click_frequency = int(a);
		elif o in "-t":
			second_limit = int(a) * 60.0;

	end_time += second_limit;

	logging.debug("===Staring with the following parameters===\n"
		+ "\tLag constant: {}\n".format(LAG_CONSTANT)
		+ "\tMax iterations: {}\n".format(iteration_limit)
		+ "\tTime limit: {} seconds".format(second_limit)
	);

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
		Cleaning();
	elif which == 9:
		Herblore(False);
	elif which == 10:
		Fletching();
	elif which == 11:
		logging.debug("Wait between clicks: {} seconds".format(click_frequency));
		Clicking();
	elif which == 12:
		GracefulArchaeology();
	elif which == 13:
		DepositArchaeology();
	elif which == 14:
		Agility();
	else:
		help();

	termination_message();

def Measure():
	try:
		while True:
			x,y = pyautogui.position();
			positionString = "X:" + str(x) + " Y:" + str(y)
			logging.info(positionString)
			time.sleep(2)
	except KeyboardInterrupt:
		logging.info("Coordinates are " + positionString)

def Ivy():
	logging.info("Click to select coordinates for Ivy")
	try:
		positionString = ""
		x = 0
		y = 0
		while True:
			x,y = pyautogui.position();
			positionString = "X:" + str(x) + " Y:" + str(y)
			logging.info(positionString)
			time.sleep(.5)
	except KeyboardInterrupt:
		logging.info("Coordinates are " + positionString)
	logging.info("Press CTRL+C to quit")
	try:
		while (time.time() < end_time):
			fuzz_factor = random.random()/4 + .875
			pyautogui.moveTo(x, y, fuzz_factor, pyautogui.easeInOutQuad)
			pyautogui.click();
			time.sleep(60*fuzz_factor)
	except KeyboardInterrupt:
		logging.info("Clicking done\n")

def Superglass():
	global iteration_limit, end_time, second_limit;
	iteration_count = 0;
	logging.info("Press CTRL+C to quit glassing")
	time.sleep(1)
	try:		
		while (time.time() < end_time) and (iteration_count < iteration_limit):
			open_bank();
			withdraw_preset('2');
			cast_superglass();
	except KeyboardInterrupt:
		logging.info("Clicking done\n")

#Lol, this gets you banned. Leave alching to the noobs.
def Alching():
	global iteration_limit, end_time, second_limit;
	iteration_count = 0;
	logging.info("Press CTRL+C to quit alching");
	try:		
		while (time.time() < end_time) and (iteration_count < iteration_limit):
			pyautogui.moveTo(1735, 750, .5, pyautogui.easeInOutQuad)
			pyautogui.click();
			pyautogui.click();
			time.sleep(fuzz_time(2, .15));
			iteration_count += 1;
			log_progress(iteration_count, iteration_limit, end_time);
	except KeyboardInterrupt:
		logging.info("Clicking done\n")

def Combining():
	global iteration_limit, end_time, second_limit;
	iteration_count = 0;
	logging.info("Press CTRL+C to quit combining")
	time.sleep(1)
	try:		
		while (time.time() < end_time) and (iteration_count < iteration_limit):
			open_bank();
			withdraw_preset('1');
			press_hotkey('1');
			pyautogui.press('space');
			time.sleep(fuzz_time(16, .1));
			iteration_count += 14;
			log_progress(iteration_count, iteration_limit, end_time);
	except KeyboardInterrupt:
		logging.info("Clicking done\n")

def Cleaning():
	global iteration_limit, end_time, second_limit;
	iteration_count = 0;
	logging.info("Press CTRL+C to quit cleaning")
	time.sleep(1)
	try:		
		while (time.time() < end_time) and (iteration_count < iteration_limit):
			open_bank();
			withdraw_preset('1');
			press_hotkey('2');
			pyautogui.press('space');
			time.sleep(fuzz_time(5, .1));
			iteration_count += 28;
			log_progress(iteration_count, iteration_limit, end_time);
	except KeyboardInterrupt:
		logging.info("Cleaning done\n")


def HallClicking():
	logging.info("Press CTRL+C to quit clicking")
	try:		
		while (time.time() < end_time):
			try:
				mouseOver = pyautogui.locateCenterOnScreen('FadedMems.png');
				pyautogui.click();
				logging.info(mouseOver)
			except Exception as e:
				logging.info("Not found")
			time.sleep(.2);
	except KeyboardInterrupt:
		logging.info("Clicking done\n")

def Smithing():
	logging.info("Not yet Implemented:")

def Idling():
	logging.info("Press CTRL+C to quit idling")
	try:		
		while True:
			try:
				pyautogui.keyDown('left');
				time.sleep(fuzz_time(.1, 3));
				pyautogui.keyUp('left');
				time.sleep(fuzz_time(120, 1));
			except Exception as e:
				logging.info("Not found")
			time.sleep(.2);
	except KeyboardInterrupt:
		logging.info("Idling done\n")

'''
Note: This requires preset 1 to have a 9/9/9 split of Dirty Herb/Vial/Ingredient on 1
Keys 1-3 need to be clean-mix-mix
Do World 84 By the Combat Academy Chest
'''
def Herblore(cleaning):
	global iteration_limit, end_time, second_limit;
	iteration_count = 0;
	logging.info("Press CTRL+C to quit herblore")
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
			iteration_count += 9;
			log_progress(iteration_count, iteration_limit, end_time);
	except KeyboardInterrupt:
		logging.info("Clicking done\n")

def Fletching():
	global iteration_limit, end_time, second_limit;
	iteration_count = 0;
	logging.info("Press CTRL+C to quit fletching")
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
			log_progress(iteration_count, iteration_limit, end_time);
	except KeyboardInterrupt:
		logging.info("Clicking done\n")

def Clicking():
	global iteration_limit, end_time, second_limit, click_frequency;
	iteration_count = 0;
	logging.info("Locking mouse coordinates in 3 seconds");
	time.sleep(3);
	x,y = pyautogui.position();
	logging.info("Press CTRL+C to quit clicking");
	time.sleep(1);
	try:		
		while (time.time() < end_time) and (iteration_count < iteration_limit):
			pyautogui.moveTo(x, y, .5, pyautogui.easeInOutQuad);
			pyautogui.click();
			wait = fuzz_time(click_frequency, .1);
			time.sleep(wait);
			iteration_count += 1;

			log_progress(iteration_count, iteration_limit, end_time);
	except KeyboardInterrupt:
		logging.info("Clicking done\n")

#Note: This also works for Mining, but got me banned once
def GracefulArchaeology():
	global iteration_limit, end_time, second_limit;
	iteration_count = 0;
	logging.info("Note: You need a charged Grace of the Elves and Autoscreener for this to work");
	logging.info("Locking mouse coordinates in 3 seconds");
	time.sleep(3);
	x,y = pyautogui.position();
	logging.info("Press CTRL+C to quit Archeologing with Grace")
	time.sleep(1)
	try:		
		while (time.time() < end_time) and (iteration_count < iteration_limit):
			pyautogui.moveTo(x, y, .5, pyautogui.easeInOutQuad)
			pyautogui.click();
			time.sleep(fuzz_time(15, .4));
			iteration_count += 1;
			log_progress(iteration_count, iteration_limit, end_time);
	except KeyboardInterrupt:
		logging.info("Clicking done\n")

def DepositArchaeology():
	global iteration_limit, end_time, second_limit;
	iteration_count = 0;
	logging.info("This will lock two mouse coordinates to run between: A Materials Cart and a surveying point. Your inventory will fill with relics.");
	logging.info("You have 3 seconds to hover your mouse over the survey point when standing next to Materials Cart.");
	time.sleep(3);
	surveyx,surveyy = pyautogui.position();
	pyautogui.click();
	logging.info("You have 6 seconds to hover your mouse over the Materials Cart when standing next to survey point.");
	time.sleep(6);
	cartx,carty = pyautogui.position();
	pyautogui.click();
	logging.info("Press CTRL+C to quit Deposit Archeologing")
	time.sleep(3)
	try:		
		while (time.time() < end_time) and (iteration_count < iteration_limit):
			pyautogui.moveTo(surveyx, surveyy, .5, pyautogui.easeInOutQuad)
			pyautogui.click();
			time.sleep(fuzz_time(60, .1));
			pyautogui.moveTo(cartx, carty, .5, pyautogui.easeInOutQuad)
			pyautogui.click();
			time.sleep(fuzz_time(4, .1));
			iteration_count += 1;
			log_progress(iteration_count, iteration_limit, end_time);
	except KeyboardInterrupt:
		logging.info("Clicking done\n");

def Agility():
	global iteration_limit, end_time, second_limit;
	iteration_count = 0;
	logging.info("This runs counterclockwise around the Anachronia Agility Course.");
	logging.info("To prepare, set your Map corner to (1528, 446) and Anticipate to F.");
	logging.info("Press CTRL+C to quit Agility.")
	time.sleep(3)
	clickOn(1550, 83, 1);
	pyautogui.keyDown("up");
	time.sleep(.5);
	pyautogui.keyUp("up");
	try:		
		while (time.time() < end_time) and (iteration_count < iteration_limit):
			pyautogui.keyDown("-"); #Excalibur for health
			pyautogui.keyUp("-");
			clickOn(893, 608, 2);
			clickOn(856, 507, 2);
			clickOn(861, 570, 2);
			clickOn(586, 655, 5);
			clickOn(1620, 320, 5);
			clickOn(875, 550, 1);
			clickOn(1700, 340, 5.3);
			clickOn(994, 553, 3);
			clickOn(1740, 380, 6);
			clickOn(950, 640, 2.5);
			clickOn(1660, 904, 6);
			clickOn(1887, 350, 7);
			clickOn(1000, 500, 2);
			pyautogui.keyDown("f");
			pyautogui.keyUp("f");
			clickOn(1790, 390, 7);
			clickOn(950, 580, 3);
			clickOn(1800, 285, 4);
			clickOn(1000, 500, 2);
			clickOn(1370, 510, 5);
			clickOn(1200, 540, 3);
			clickOn(1800, 213, 6);
			clickOn(1111, 500, 3.5);
			clickOn(1810, 139, 6); #Long run to east vines kinda loose
			clickOn(950, 400, 4);
			clickOn(975, 42, 6);
			clickOn(1200, 444, 4);
			clickOn(1200, 167, 6);
			clickOn(1325, 68, 5.5);
			clickOn(1100, 275, 4.5);
			clickOn(1214, 600, 3.5);
			pyautogui.keyDown("f");
			pyautogui.keyUp("f");
			clickOn(1841, 285, 6.2);
			clickOn(1020, 540, 1.1);
			pyautogui.keyDown("=");
			pyautogui.keyUp("=");
			time.sleep(.6);
			clickOn(1820, 250, 4);
			clickOn(1040, 550, 3);
			clickOn(1234, 476, 4);
			clickOn(1117, 450, 3);
			clickOn(1035, 200, 4);
			clickOn(1250, 283, 3);
			clickOn(1725, 163, 4);
			clickOn(960, 420, 2);
			clickOn(333, 45, 6);
			clickOn(173, 136, 7);
			clickOn(1720, 165, 5);
			clickOn(960, 467, 3);
			clickOn(787, 53, 6);
			clickOn(922, 408, 3);
			clickOn(350, 450, 5);
			clickOn(650, 507, 3.5);
			clickOn(733, 520, 3);
			clickOn(733, 520, 3);
			clickOn(608, 36, 4);
			clickOn(742, 413, 3.5); #Bone bridge
			clickOn(717, 480, 4);
			clickOn(721, 576, 3);
			clickOn(1642, 88, 7);
			clickOn(868, 555, 2);
			clickOn(644, 488, 3);
			clickOn(1629, 300, 4.5);
			clickOn(950, 570, 1.5);
			clickOn(950, 830, 2.5);
			clickOn(950, 732, 2);
			clickOn(1661, 275, 3);
			clickOn(865, 547, 3); #Tunnel
			clickOn(806, 493, 3);
			clickOn(950, 881, 3);
			clickOn(631, 785, 4);
			clickOn(1033, 951, 3);
			clickOn(1065, 618, 3);
			clickOn(1677, 424, 8);
			clickOn(1715, 310, 3);
			iteration_count += 1;
			log_progress(iteration_count, iteration_limit, end_time);
	except KeyboardInterrupt:
		logging.info("Clicking done\n");

'''=====================Helper Methods====================='''
def clickOn(x, y, length):
	pyautogui.moveTo(x, y, .5, pyautogui.easeInOutQuad)
	pyautogui.click();
	time.sleep(fuzz_time(2.0 * length, .1));

def fuzz_time(min_time, pct_increase):
	fuzz_factor = (random.random() * pct_increase) + 1;
	return (min_time * fuzz_factor * LAG_CONSTANT);

def open_bank():
	pyautogui.moveTo(955, 650, .5, pyautogui.easeInOutQuad);
	pyautogui.click();
	time.sleep(fuzz_time(1.1, .25));

def withdraw_preset(preset):
	pyautogui.keyDown(preset);
	pyautogui.keyUp(preset);
	time.sleep(fuzz_time(1, .25));

def press_hotkey(hotkey):
	pyautogui.keyDown(hotkey);
	pyautogui.keyUp(hotkey);
	time.sleep(fuzz_time(1, .25));

def cast_superglass():
	pyautogui.keyDown('6');
	pyautogui.keyUp('6');
	time.sleep(fuzz_time(2.1, .25));

def help():
	print(usage);
	print(modes);
	termination_message();

def log_progress(iteration_count, iteration_limit, end_time):
	logging.info("Iterations: {}/{}".format(iteration_count, iteration_limit));
	logging.info("Time remaining: {}".format(end_time - time.time()));

def termination_message():
	logging.info("Consider logging off for 15 minutes to lessen ban likelihood.")

if __name__ == "__main__":
	try:
		main(sys.argv[1:])
	except IndexError:
		help();
