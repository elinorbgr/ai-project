#!/usr/bin/ipython

import nltk
import random
from random import randint
#TODO
# tagsList = getTags(word)
# (isWordInCorrectForm, newWord) = setWordInTheCorrectForm(newWord, form)


def file_len(f):
	for i, l in enumerate(f):
		pass
		return i + 1


def getRandomProverb():
	proverbsFile = open('proverbsList','r')
	proverbsList = proverbsFile.readlines()
	line = randint(0,len(proverbsList)-1)
	proverb = proverbsList[line];
	proverbsFile.close()
	return proverb[0:-1]

def computeModificationRate(initialLProverb,lProverb):
	diffWords=0
	for a,b in zip(initialLProverb,lProverb):
		if a!=b:
			diffWords = diffWords + 1
	return float(diffWords)/len(initialLProverb)

def getTags(word):
	l = nltk.pos_tag([word])
	tags = [ t for (w,t) in l]
	return tags

def fillLists(words):
	l=dict()
	for w in words:
		tags = getTags(w)
		for t in tags:
			if l.keys().count(t)==0:
				l[t] = []
			l[t].append(w)
	return l

def getRandomWordFromModifMask(modifMask,proverb):
	nWordUnmodified = modifMask.count(False)
	if nWordUnmodified==0:
		return False
	nWord = randint(0,nWordUnmodified)
	index = 0
	for i,m,w in zip(range(0,len(modifMask)),modifMask, proverb):
		if m==False:
			index = index + 1
		if index==nWord:
			return (i, w)
	return (False, None)

def pickUpWordFromEntitiesLists(entitiesList,form):
	if entitiesList.keys().count(form)==0:
		return (False, None)
	else:
		return (True, random.choice(entitiesList[form]))

def setWordInTheCorrectForm(word, form):
	return (True,(word,form))

def shuffle(x):
	x = list(x)
	random.shuffle(x)
	return x

def generateProverb(theme, rate=0.5):
	# Load Background Corpus
	backgroundGraph = nltk.text.ContextIndex([word.lower( ) for word in nltk.corpus.brown.words( )])

	# Build background graph from the theme
	words = backgroundGraph.similar_words(theme,100)
	entitiesList = fillLists(words)

	# Get a proverb
	proverb = getRandomProverb()
	print(proverb)
	lProverb = nltk.pos_tag(nltk.word_tokenize(proverb))
	initialLProverb = lProverb

	modif = [False]*len(lProverb)

	# Main loop of the algorithm

	permutation = shuffle(range(0,len(lProverb)))
	for i in permutation:
	
		if computeModificationRate(initialLProverb,lProverb) > rate:
			break

		# Pick up a random word from the proverb
		(index, word) = (i,lProverb[i])


		# Pick up a word from the background graph
		(finded, newWord) = pickUpWordFromEntitiesLists(entitiesList,word[1])

		# Replace if the word can be put in the right form
		if finded:
			(isWordInCorrectForm, newWord) = setWordInTheCorrectForm(newWord, word[1])
			if isWordInCorrectForm:
				modif[index] = True
				lProverb[index] = newWord

		print(str(word) + " -> " + str(newWord))


	print(proverb)

	newProverb = ' '.join([w for (w,t) in lProverb])
	print(newProverb)

	return newProverb


