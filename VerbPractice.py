import re
from random import randrange

NOR = (('NI','NATZAI'),
		('HI','HATZAI'),
		('HURA','ZAI'),
		('GU','GATZAIZKI'),
		('ZU','ZATZAIZKI'),
		('ZUEK','ZATZAIZKI+TE'),
		('HAIEK','ZAIZKI'))
NORI = (('NERI','T/DA'),
		('HIRI','K'),
		('HARI','O'),
		('GURI','GU'),
		('ZURI','ZU'),
		('ZUEI','ZUE'),
		('HAIEI','E'))

NORPAST = (('NI','NINTZAI+N'),
		('HI','HINTZAI+N'),
		('HURA','ZITZAI+N'),
		('GU','GINTZAIZKI+N'),
		('ZU','ZINTZAIZKI+N'),
		('ZUEK','ZINTZAIZKI+TEN'),
		('HAIEK','ZITZAIZKI+N'))
NORIPAST = (('NERI','DA'),
		('HIRI','A'),
		('HARI','O'),
		('GURI','GU'),
		('ZURI','ZU'),
		('ZUEI','ZUE'),
		('HAIEI','E'))

IMPOSSIBLE = ( ('NI',('NERI','GURI')),
		('HI',('HIRI','ZURI','ZUEI')),
		('HURA',()),
		('GU',('NIRI','GURI')),
		('ZU',('HIRI','ZURI','ZUEI')),
		('ZUEK',('HIRI','ZURI','ZUEI')),
		('HAIEK',()) )

def buildVerbPast(nor,nori):
	''' Takes two inputs, the NOR and NORI
		and returns the conjugated form in past tense
	'''
	# Pull out the correct stem and suffix based on the pronouns
	for pron,verb in NORPAST:
		if nor == pron:
			stem = verb
	for pron,verb in NORIPAST:
		if nori == pron:
			suffix = verb
	# stem2 gets added to the end of the verb (for ZUEK)
	stem2 = ''
	if '+' in stem:
		stem,stem2 = stem.split('+')
	string = stem + suffix + stem2
	return string.lower()

def buildVerb(nor,nori):
	''' Takes two inputs, the NOR and NORI
		and returns the conjugated form
	'''
	# Pull out the correct stem and suffix based on the pronouns
	for pron,verb in NOR:
		if nor == pron:
			stem = verb
	for pron,verb in NORI:
		if nori == pron:
			suffix = verb
	# stem2 gets added to the end of the verb (for ZUEK)
	stem2 = ''
	if '+' in stem:
		stem,stem2 = stem.split('+')
	if '/' in suffix:
		suffix = suffix.split('/')
		if stem2:
			suffix = suffix[1]
		else:
			suffix = suffix[0]
	string = stem + suffix + stem2
	return string.lower()

def numMenu(prompt,num):
	''' Displays a menu, waits for a prompt, and returns the selected
		value. Repeats until a valid number is input.
		
		Inputs: prompt = the text to prompt the user
				num = the number of menu items (ie max legitimate number)
	'''
	# Repeat until a valid selection has been made (0 - max)
	while True:
		# Clear the screen
		print("\033c" + prompt)
		selection = input()
		if selection:
			try:
				value = int(selection)
			except:
				# On exception, set value to an invalid number
				value = num+1
			if value <= num:
				return value
			else:
				print("Please enter a valid selection")

if __name__ == '__main__':
	selection = numMenu("""What would you like to work on? (enter 0 at any time to quit)
1. NOR-NORI present tense
2. NOR-NORI past tense""",2)
	if selection == 0:
		quit()
	score = 0
	if selection == 1:
		# Keep asking for more 
		while True:
			nor = randrange(0,len(NOR)-1)
			nori = randrange(0,len(NORI)-1)
			while NORI[nori][0] in IMPOSSIBLE[nor][1]:
				nori = randrange(0,len(NORI)-1)
			selection = input("{} + {}\n".format(NOR[nor][0],NORI[nori][0]))
			if selection == '0':
				quit()
			answer = buildVerb(NOR[nor][0],NORI[nori][0])
			if selection.lower() == answer:
				score += 1
				print("   {} correct!".format(score))
			else:
				print("   Incorrect: " + answer)
	if selection == 2:
		# Keep asking for more 
		while True:
			nor = randrange(0,len(NORPAST)-1)
			nori = randrange(0,len(NORIPAST)-1)
			while NORIPAST[nori][0] in IMPOSSIBLE[nor][1]:
				nori = randrange(0,len(NORIPAST)-1)
			selection = input("{} + {}\n".format(NORPAST[nor][0],NORIPAST[nori][0]))
			if selection == '0':
				quit()
			answer = buildVerbPast(NORPAST[nor][0],NORIPAST[nori][0])
			if selection.lower() == answer:
				score += 1
				print("   {} correct!".format(score))
			else:
				print("   Incorrect: " + answer)
