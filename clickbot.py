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
2: Superglass (Risky)
3: Alching (Risky)
4: Combining
5: HoM Div Clicks
6: Smithing (Smithing)
7: Idling
8: Clean Herbs w/ Cape (Risky)
9: Herblore clean
10: Fletching
11: Clicking
12: Graceful Archeology
13: Deposit Archaeology
14: Agility
15: Cooking/Firemaking
16: Fishing
17: Jellyfishing
18: Firemaking
19: Divomatic
20: Manufacturing
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
	elif which == 15:
		Cooking();
	elif which == 16:
		Fishing();
	elif which == 17:
		Jellyfishing();
	elif which == 18:
		Firemaking();
	elif which == 19:
		DivOMatic();
	elif which == 20:
		Manufacturing();
	elif which == 69:
		Sandbox();
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
			time.sleep(fuzz_time(11, .1));
			#time.sleep(fuzz_time(16, .1));
			iteration_count += 14;
			log_progress(iteration_count, iteration_limit, end_time);
	except KeyboardInterrupt:
		logging.info("Clicking done\n")

# About 20k/hour, but gets you banned. 2Hours at Invention Guild
def Cleaning():
	global iteration_limit, end_time, second_limit;
	iteration_count = 0;
	logging.info("Press CTRL+C to quit cleaning")
	time.sleep(1)
	try:		
		while (time.time() < end_time) and (iteration_count < iteration_limit):
			open_bank();
			withdraw_preset('1');
			press_hotkey('6');
			pyautogui.press('space');
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
				pyautogui.keyDown('0');
				time.sleep(fuzz_time(.1, 3));
				pyautogui.keyUp('0');
				time.sleep(fuzz_time(10, 1));
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
	logging.info("Note: This will also press 6 regularly for Elven Shard for Imp Souled");
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
			if iteration_count % 4 == 0:
				press_hotkey('6'); #Ancient Elven Ritual Shard goes in 6
			iteration_count += 1;
			log_progress(iteration_count, iteration_limit, end_time);
	except KeyboardInterrupt:
		logging.info("Clicking done\n")

def DepositArchaeology():
	global iteration_limit, end_time, second_limit;
	iteration_count = 0;
	seconds_to_cart = 6;
	logging.info("This will lock two mouse coordinates to run between: A Materials Cart and a surveying point. Your inventory will fill with relics.");
	logging.info("You have 3 seconds to hover your mouse over the survey point when standing next to Materials Cart.");
	time.sleep(3);
	surveyx,surveyy = pyautogui.position();
	pyautogui.click();
	logging.info("You have 6 seconds to hover your mouse over the Materials Cart when standing next to survey point.");
	time.sleep(seconds_to_cart);
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
			time.sleep(fuzz_time(seconds_to_cart, .1));
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
			clickOn(893, 608, 2.2); #start
			clickOn(856, 507, 2.2); #cliff
			clickOn(861, 570, 2.5); #cliff
			clickOn(586, 655, 5); #vine
			clickOn(1620, 320, 4); #walk
			clickOn(875, 550, 1.4); #Climb over root
			clickOn(1700, 340, 5); #walk
			clickOn(994, 553, 3); #vine
			clickOn(1740, 380, 6); #walk
			clickOn(950, 640, 2.5); #cliff
			clickOn(1660, 904, 4.6); #tree hop?
			clickOn(1887, 350, 7); #walk
			clickOn(1000, 500, 2); #cliff
			pyautogui.keyDown("f"); #Freedom
			pyautogui.keyUp("f");
			clickOn(1790, 390, 6);
			clickOn(950, 580, 3.3); #Climb cliff face by dino
			clickOn(1800, 285, 4); #walk
			clickOn(1000, 500, 2.3); #block
			clickOn(1370, 510, 5);
			clickOn(1200, 540, 3);
			clickOn(1800, 213, 5); #I think this is the NE movement to a ruins block climb
			clickOn(1111, 500, 3.5); #Climbing ruins
			clickOn(1810, 139, 5.5); #Long run to east vines kinda loose
			clickOn(950, 400, 4);
			clickOn(975, 42, 6);
			clickOn(1200, 444, 4);
			clickOn(1200, 167, 6.3);
			clickOn(1325, 68, 5.5);
			clickOn(1100, 275, 4.5);
			clickOn(1214, 600, 3);
			pyautogui.keyDown("f"); #Freedom
			pyautogui.keyUp("f");
			clickOn(1841, 285, 5.3);
			clickOn(1020, 540, 1.5);
			pyautogui.keyDown("="); #Surge
			pyautogui.keyUp("=");
			time.sleep(1.5);
			clickOn(1820, 250, 4); #walk
			clickOn(1040, 550, 3); #vine
			clickOn(1234, 476, 4); #vine
			clickOn(1117, 450, 3); #root
			clickOn(1035, 200, 4); #root
			clickOn(1250, 283, 3); #block
			clickOn(1725, 163, 4.2); #walk
			clickOn(960, 420, 2.2); #sunken
			clickOn(333, 45, 6); #root
			clickOn(173, 136, 7); #vine onto WC Jungle mesa
			clickOn(1720, 165, 5); #walk
			clickOn(960, 467, 3.3); #vine
			clickOn(787, 53, 6); #vine
			clickOn(922, 408, 3); #root
			clickOn(350, 450, 4.5); #Begin ruined wall by herby
			clickOn(650, 507, 3.5);
			clickOn(733, 520, 2.7); #Get off HW wall
			clickOn(733, 520, 3);
			clickOn(608, 36, 4);
			clickOn(742, 413, 3.5); #Bone bridge
			clickOn(717, 480, 4);
			clickOn(721, 576, 2.7);
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

'''
Need to stand by Prif GE desk by bonfire
'''
def Cooking():
	global iteration_limit, end_time, second_limit;
	iteration_count = 0;
	seconds_to_fire = 3;
	logging.info("You have 3 seconds to hover your mouse over the Bonfire point when standing next to Bank.");
	time.sleep(3);
	firex,firey = pyautogui.position();
	pyautogui.click();
	logging.info("You have 3 seconds to hover your mouse over the Bank when standing next to bonfire.");
	time.sleep(3);
	bankx,banky = pyautogui.position();
	pyautogui.click();
	logging.info("Press CTRL+C to quit Cooking")
	time.sleep(3)
	try:		
		while (time.time() < end_time) and (iteration_count < iteration_limit):
			press_hotkey('1');
			pyautogui.moveTo(firex, firey, .5, pyautogui.easeInOutQuad)
			pyautogui.click();
			time.sleep(fuzz_time(seconds_to_fire, .1));			
			pyautogui.press('space');
			time.sleep(fuzz_time(64, .1));
			press_hotkey('7'); #Try to send an urn if possible
			pyautogui.moveTo(bankx, banky, .5, pyautogui.easeInOutQuad)
			pyautogui.click();
			time.sleep(fuzz_time(seconds_to_fire, .1));
			iteration_count += 28;
			log_progress(iteration_count, iteration_limit, end_time);
	except KeyboardInterrupt:
		logging.info("Cooking done\n");
'''
Fishing in Menaphos VIP area
'''
def Fishing():
	global iteration_limit, end_time, second_limit;
	iteration_count = 0;
	try:
		while (time.time() < end_time) and (iteration_count < iteration_limit):
			scan_for_vip_fishing();
			time.sleep(fuzz_time(70, .1));
			press_hotkey('space');
			press_hotkey('7'); #Put your decorated Urn here
			open_vip_bank();
			press_hotkey('1');
			iteration_count += 25;
			log_progress(iteration_count, iteration_limit, end_time);
	except KeyboardInterrupt:
		logging.info("Fishing done\n");

def Jellyfishing():
	global iteration_limit, end_time, second_limit;
	iteration_count = 0;
	logging.info("Just stand on the NW most corner of the chest boat.");
	clickOn(1550, 83, 1);
	try:
		while (time.time() < end_time) and (iteration_count < iteration_limit):
			for x in range(6):
				scan_for_jellyfish();
				time.sleep(fuzz_time(20, .1));
			press_hotkey('7'); #Put your decorated Urn here	
			clickOn(1086, 569, 1);
			press_hotkey('1');
			iteration_count += 25;
			log_progress(iteration_count, iteration_limit, end_time);
	except KeyboardInterrupt:
		logging.info("Fishing done\n");

def DivOMatic():
	global iteration_limit, end_time, second_limit;
	iteration_count = 0;
	try:
		while (time.time() < end_time) and (iteration_count < iteration_limit):
			find_and_click_on_wisp();
			iteration_count += 1;
			log_progress(iteration_count, iteration_limit, end_time);
	except KeyboardInterrupt:
		logging.info("Divining done\n");

'''
Creates things at an invention table, but mostly Divine Charges
Augs take 3 seconds each (-f = 180)
Charges 2.4 seconds each (-f = 144)
Siphons 1.8 seconds each (-f = 108)
'''
def Manufacturing():
	global iteration_limit, end_time, second_limit, click_frequency;
	iteration_count = 0;
	logging.info("Press CTRL+C to quit manufacturing")
	time.sleep(1)
	try:		
		while (time.time() < end_time) and (iteration_count < iteration_limit):
			clickOn(950, 470, 1);
			pyautogui.press('space');
			time.sleep(fuzz_time(click_frequency, .05));
			iteration_count += 60;
			log_progress(iteration_count, iteration_limit, end_time);
	except KeyboardInterrupt:
		logging.info("Manufacturing done\n")

'''
Just whatever you feel like testing goes here
'''
def Sandbox():
	reset_to_spring();

'''
Need to stand by Prif GE desk by bonfire
'''
def Firemaking():
	global iteration_limit, end_time, second_limit;
	iteration_count = 0;
	seconds_to_fire = 3;
	logging.info("You have 3 seconds to hover your mouse over the Bonfire point when standing next to Bank.");
	time.sleep(3);
	firex,firey = pyautogui.position();
	pyautogui.click();
	logging.info("You have 3 seconds to hover your mouse over the Bank when standing next to bonfire.");
	time.sleep(3);
	bankx,banky = pyautogui.position();
	pyautogui.click();
	logging.info("Press CTRL+C to quit Blazing")
	time.sleep(3)
	try:		
		while (time.time() < end_time) and (iteration_count < iteration_limit):
			press_hotkey('1');
			pyautogui.moveTo(firex, firey, .5, pyautogui.easeInOutQuad)
			pyautogui.click();
			time.sleep(fuzz_time(115, .1));
			pyautogui.moveTo(bankx, banky, .5, pyautogui.easeInOutQuad)
			pyautogui.click();
			time.sleep(fuzz_time(seconds_to_fire, .1));		
			iteration_count += 28;
			log_progress(iteration_count, iteration_limit, end_time);
	except KeyboardInterrupt:
		logging.info("Blazing done\n");

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

def open_vip_bank():
	# mouseOver = pyautogui.locateCenterOnScreen('VIPChestSample.png');
	mouseOver = pyautogui.locateCenterOnScreen('ChectSpareSample.png');
	if mouseOver == None:
		logging.error("Chest not found");
		raise Exception;
	pyautogui.moveTo(mouseOver[0], mouseOver[1], .5, pyautogui.easeInOutQuad);
	pyautogui.click();
	time.sleep(fuzz_time(4, .25));

def scan_for_vip_fishing():
	x_coords = [1200, 1240, 1280, 1320, 1360, 1400, 1440, 1480];
	found = False;
	for x in x_coords:
		pyautogui.moveTo(x, 625, .5, pyautogui.easeInOutQuad);
		mouseOver = pyautogui.locateCenterOnScreen('FishBait.png');
		if mouseOver != None:
			pyautogui.click();
			found = True;
			break;
	if found == False:
		logging.error("Fish not found");
		raise Exception;

def scan_for_jellyfish():
	jelly_coords = [[532,504],[800,450],[1408,505]];
	jelly_pics = ["BlueJellyFish.png", "GreenJellyFish.png"];
	found = False;
	while found == False:
		for pic in jelly_pics:
			if found == True:
				break;
			for x, y in jelly_coords:
				pyautogui.moveTo(x, y, .5, pyautogui.easeInOutQuad);
				mouseOver = pyautogui.locateCenterOnScreen(pic);
				if mouseOver != None:
					pyautogui.click();
					found = True;
					break;

def find_and_click_on_wisp():
	clicked = False;
	while not clicked:
		clicked = click_on_wisp();
	wait_for_no_image('DivXP.png');

def click_on_wisp():
	mouseOver = wait_for_image('LuminousWispSample.png');
	pyautogui.moveTo(mouseOver[0], mouseOver[1], .1, pyautogui.easeInOutQuad);
	pyautogui.click();
	logging.info("Clicking on Wisp.");
	time.sleep(fuzz_time(3.5, .25));

	 #See if we're getting xp. If not, try again.
	mouseOver = pyautogui.locateCenterOnScreen('DivXP.png');
	if mouseOver == None:
		logging.info("Click failed. Searching again...");
		return False;
	return True;

def wait_for_image(image):
	mouseOver = pyautogui.locateCenterOnScreen(image);
	attempt_no = 0;
	while mouseOver == None:
		misses = 0;
		attempt_no += 1;
		logging.info("Could not find " + image + ". Searching again...");
		time.sleep(.5);
		mouseOver = pyautogui.locateCenterOnScreen(image);
		if attempt_no % 5 == 0:
			misses += reset_to_spring(misses);
			if misses == 5:
				raise Exception("Cannot reset successfully. Terminating.");
	return mouseOver;

def wait_for_no_image(image):
	mouseOver = pyautogui.locateCenterOnScreen(image);
	if mouseOver != None:
		logging.info(image + " found. Searching again...");
		time.sleep(4);
		wait_for_no_image(image);
	else:
		logging.info(image + " not found. Continuing...");

'''The Spring map image is cropped because if a wisp crosses 
the section we're looking for, we won't be able to find it.'''
def reset_to_spring(misses):
	logging.info("Attempting to locate spring to recenter...");
	mouseOver = pyautogui.locateCenterOnScreen("SpringCenter.png");
	if mouseOver == None:
		logging.info("Spring not found.");
		return misses + 1;
	pyautogui.moveTo(mouseOver[0], mouseOver[1], .4, pyautogui.easeInOutQuad);
	pyautogui.click();
	return 0;

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
