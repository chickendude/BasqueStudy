'''
maybe i can send a list with the verb name and tense you want to study for that verb.

'''

import re
from collections import OrderedDict
from random import randrange

NOR = ('NI','HI','HURA','GU','ZU','ZUEK','HAIEK')
NORI = ('NERI','HIRI','HARI','GURI','ZURI','ZUEI','HAIEI')
NORK = ('NIK','HIK','HARK','GUK','ZUK','ZUEK','HAIEK')

IMPOSSIBLE = ( ('NI',('NERI','GURI')),
		('HI',('HIRI','ZURI','ZUEI')),
		('HURA',()),
		('GU',('NIRI','GURI')),
		('ZU',('HIRI','ZURI','ZUEI')),
		('ZUEK',('HIRI','ZURI','ZUEI')),
		('HAIEK',()) )

VERBTYPES = []
EXIT = ('exit','quit','q','x')

def clrScr(prompt=''):
	# Clear the screen
	print("\033c", end="")


def numMenu(prompt,num,acceptableStrings=''):
	'''	Displays a menu, waits for a prompt, and returns the selected
		value. Repeats until a valid number is input.
		
		Inputs: prompt = the text to prompt the user
				num = the number of menu items (ie max legitimate number)
	'''
	# Repeat until a valid selection has been made (0 - max)
	prompt += "\n  {}. Exit".format(num+1)
	while True:
		clrScr()
		selection = input(prompt+"\n")
		if selection:
			if selection.lower() in acceptableStrings:
				return selection.lower()
			if selection.lower() in EXIT:
				return False
			try:
				value = int(selection)
			except:
				# On exception, set value to an invalid number
				value = -1
			if value <= num and value > 0:
				return value
			if value == num+1:
				return False

def buildNorNori(nor,nori,tense):
	''' Returns the conjugated form of a verb based on it's inputs
	'''
	stem = nor
	suffix = nori
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

def multi_runTest(verbList,tense):
	score = 0
	grade = test = ""
	while True:
		# Pick a random verb in the list of verbs
		verb = randrange(0,len(verbList))
		clrScr()
		print("*{}* - {} tense:\n{}".format(verbList[verb]['name'],tense,grade))
		# Handle verbs of type NOR
		if verbList[verb]['type'] == 'nor':
			# Randomly select the galdegaia
			nor = randrange(0,len(NOR))
			test = "{}".format(NOR[nor])
			selection = input(test+"\n")
			answer = verbList[verb]['tenses'][tense]['nor'][nor]

		# Handle verbs of type NOR-NORI
		if verbList[verb]['type'] == 'nor-nori':
			# Randomly select the galdegaiak
			nor = randrange(0,len(NOR))
			nori = randrange(0,len(NORI))
			while NORI[nori] in IMPOSSIBLE[nor][1]:
				nori = randrange(0,len(NORI))
			test = "{} + {}".format(NOR[nor],NORI[nori])
			selection = input(test+"\n")
			nor = verbList[verb]['tenses'][tense]['nor'][nor]
			nori = verbList[verb]['tenses'][tense]['nori'][nori]
			answer = buildNorNori(nor,nori,tense)

		# Handle verbs of type ZER-NORK
		if verbList[verb]['type'] == 'zer-nork':
			# Randomly select the galdegaia
			zer = randrange(0,2)
			nork = randrange(0,len(NORK))
			person = ('singular','plural')
			test = "{} ({})".format(NORK[nork],person[zer])
			selection = input(test+"\n")
			answer = verbList[verb]['tenses'][tense][person[zer]][nork]

		# Handle verbs of type NORK
		if verbList[verb]['type'] == 'nork':
			# Randomly select the galdegaia
			nork = randrange(0,len(NORK))
			test = "{}".format(NORK[nork])
			selection = input(test+"\n")
			answer = verbList[verb]['tenses'][tense]['nork'][nork]

		# If user types 'exit', exit routine
		if selection in EXIT:
			return
		if selection.lower() == answer:
			score += 1
			grade = "{} correct!".format(score)
		else:
			grade = "* Incorrect: {} (you typed {}) - {} - {}".format(answer,selection,verbList[verb]['name'],test)

def runTest(verb,tense):
	''' verb is the verb's dictionary entry
		tense is the tense id
	'''
	score = 0
	grade = test = ""
	while True:
		clrScr()
		print("{} - {} tense:\n{}".format(verb['name'],tense,grade))
		# Handle verbs of type NOR
		if verb['type'] == 'nor':
			# Randomly select the galdegaia
			nor = randrange(0,len(NOR))
			test = "{}".format(NOR[nor])
			selection = input(test+"\n")
			answer = verb['tenses'][tense]['nor'][nor]
	
		# Handle verbs of type NOR-NORI
		if verb['type'] == 'nor-nori':
			# Randomly select the galdegaiak
			nor = randrange(0,len(NOR))
			nori = randrange(0,len(NORI))
			while NORI[nori] in IMPOSSIBLE[nor][1]:
				nori = randrange(0,len(NORI))
			test = "{} + {}".format(NOR[nor],NORI[nori])
			selection = input(test+"\n")
			nor = verb['tenses'][tense]['nor'][nor]
			nori = verb['tenses'][tense]['nori'][nori]
			answer = buildNorNori(nor,nori,tense)

		# Handle verbs of type ZER-NORK
		if verb['type'] == 'zer-nork':
			# Randomly select the galdegaia
			zer = randrange(0,2)
			nork = randrange(0,len(NORK))
			person = ('singular','plural')
			test = "{} ({})".format(NORK[nork],person[zer])
			selection = input(test+"\n")
			answer = verb['tenses'][tense][person[zer]][nork]

		# Handle verbs of type NORK
		if verb['type'] == 'nork':
			# Randomly select the galdegaia
			nork = randrange(0,len(NORK))
			test = "{}".format(NORK[nork])
			selection = input(test+"\n")
			answer = verb['tenses'][tense]['nork'][nork]

		# If user types 'exit', exit routine
		if selection in EXIT:
			return
		if selection.lower() == answer:
			score += 1
			grade = "{} correct!".format(score)
		else:
			grade = "* Incorrect: {} (you typed {}) - {} - {}".format(answer,selection,verb['name'],test)

def pickTense(verb):
	'''	Let's you choose the tense of the verb you want to study.
		Afterwards runs runTest().
	'''
	# Now we select the verb tense we want to study
	counter = 0
	string = "{}:\nWhat tense would you like to work on?".format(verb['name'])
	tenseList = []
	for tense in sorted(verb['tenses'].keys(),reverse = True):
		counter += 1
		string += "\n  "+str(counter)+". "+str(tense.capitalize())
		tenseList.append(tense)
	selection = numMenu(string,len(verb['tenses']))
	if selection:
		runTest(verb,tenseList[selection-1])
	else:
		return

def multi_pickTense(verbs,verbtype):
	# Build new list of verbs out of the verb type asked for
	verbList = [verbs[i] for i in range(len(verbs)) if verbs[i]['type'] == verbtype]

	# Find all the matching (intersecting) tenses
	tenseList = set()
	for verb in verbList:
		# Set tenseList to the first verbs tense list
		if not tenseList:
			tenseList = set(verb['tenses'].keys())
		tenseList = tenseList.intersection(verb['tenses'].keys())
	tenseList = sorted(tenseList,reverse = True)
	string = "{} verbs:\nWhat tense would you like to work on?".format(verbtype)
	counter = 0
	for tense in tenseList:
		counter += 1
		string += "\n  "+str(counter)+". "+str(tense.capitalize())
	selection = numMenu(string,len(tenseList))
	if selection:
		multi_runTest(verbList,tenseList[selection-1])
	else:
		return


if __name__ == '__main__':
	# Make a list of dictionary values, each entry is a separate verb read from verbs.lst
	verbs = []
	with open('verbs.lst', encoding='utf-8') as file:
		for line in file:
			line = line.strip('\n')
			tabs = line.count("\t")
			if tabs == 0 and line.strip() != '':	# Skip blank/empty lines
				if ':' in line:
					verbtype = line[:-1]
					VERBTYPES.append(verbtype)
				else:
					verbs.append({})
					# Set verb name and verb type
					verbs[-1]['name'] = line
					verbs[-1]['type'] = verbtype
					verbs[-1]['tenses'] = {}
			if tabs == 1:
				verbtense = line.strip()
				verbs[-1]['tenses'][verbtense] = {}
			if tabs == 2:
				galdegaia, verbforms = line.strip().split(': ')
				verbs[-1]['tenses'][verbtense][galdegaia] = verbforms.strip().split(', ')
	while True:
		counter = 0
		string = "Please pick a verb:"
		verbtype = ""
		for verb in verbs:
			counter += 1
			if verbtype != verb['type']:
				verbtype = verb['type']
				string += "\n"+verbtype.upper()+":"
			string += "\n  "+str(counter)+". "+verb['name'].title()
		selection = numMenu(string,len(verbs),VERBTYPES)
		# Check if we are testing on a verb type or individual verb
		if selection in VERBTYPES:
			multi_pickTense(verbs,selection)
		else:
			if selection:
				pickTense(verbs[selection-1])
			else:
				quit()
