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

def buildVerb(nor,nori=''):
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

def clrScr(prompt=''):
	# Clear the screen
	print("\033c", end="")


def numMenu(prompt,num):
	''' Displays a menu, waits for a prompt, and returns the selected
		value. Repeats until a valid number is input.
		
		Inputs: prompt = the text to prompt the user
				num = the number of menu items (ie max legitimate number)
	'''
	# Repeat until a valid selection has been made (0 - max)
	prompt += "\n{}. Exit".format(num+1)
	while True:
		clrScr()
		print(prompt)
		selection = input()
		if selection:
			try:
				value = int(selection)
			except:
				# On exception, set value to an invalid number
				value = num+1
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


def runTest(verb,tense):
	''' verb is the verb's dictionary entry
		tense is the tense id
	'''
	score = 0
	grade = ""
	while True:
		clrScr()
		print("Testing the {} tense of {}:\n{}".format(tense,verb['name'],grade))
		# Handle verbs of type NOR
		if verb['type'] == 'nor':
			# Randomly select the galdegaia
			nor = randrange(0,len(NOR)-1)
			selection = input("{}\n".format(NOR[nor]))
			# If user types 'exit', go back
			if selection.lower() == 'exit':
				return
			answer = verb['tenses'][tense]['nor'][nor]
	
		# Handle verbs of type NOR-NORI
		if verb['type'] == 'nor-nori':
			# Randomly select the galdegaiak
			nor = randrange(0,len(NOR)-1)
			nori = randrange(0,len(NORI)-1)
			while NORI[nori] in IMPOSSIBLE[nor][1]:
				nori = randrange(0,len(NORI)-1)
			selection = input("{} + {}\n".format(NOR[nor],NORI[nori]))
			# If user types 'exit', go back
			if selection.lower() == 'exit':
				return
			nor = verb['tenses'][tense]['nor'][nor]
			nori = verb['tenses'][tense]['nori'][nori]
			answer = buildNorNori(nor,nori,tense)

		if selection.lower() == answer:
			score += 1
			grade = "{} correct!".format(score)
		else:
			grade = "*Incorrect: " + answer

def pickTense(verb):
	# Now we select the verb tense we want to study
	counter = 0
	string = "{}:\nWhat tense would you like to work on?".format(verb['name'])
	tenseList = []
	for tense in sorted(verb['tenses'].keys(),reverse = True):
		counter += 1
		string += "\n"+str(counter)+". "+str(tense.capitalize())
		tenseList.append(tense)
	selection = numMenu(string,len(verb['tenses']))
	if selection:
		runTest(verb,tenseList[selection-1])
	else:
		return

def pickVerb(verbList):
	while True:
		counter = 0
		string = "Please pick a verb:"
		for verb in verbList:
			counter += 1
			string += "\n"+str(counter)+". "+verb['name'].capitalize()
		selection = numMenu(string,len(verbs))
		if selection:
			pickTense(verbList[selection-1])
		else:
			return


if __name__ == '__main__':
	# Make a list of dictionary values, each entry is a separate verb read from verbs.lst
	verbs = []

	with open('verbs.lst', encoding='utf-8') as file:
		for line in file:
			tabs = line.count("\t")
			if tabs == 0:
				verbname,verbtype = line.strip().split(': ')
				verbs.append({})
				# Set verb name and verb type
				verbs[-1]['name'] = verbname
				verbs[-1]['type'] = verbtype
				verbs[-1]['tenses'] = {}
			if tabs == 1:
				verbtense = line.strip()
				verbs[-1]['tenses'][verbtense] = {}
			if tabs == 2:
				galdegaia, verbforms = line.strip().split(': ')
				verbs[-1]['tenses'][verbtense][galdegaia] = verbforms.strip().split(', ')
	pickVerb(verbs)
