#!/usr/bin/python

import nltk
import random
import sys
import os
from random import randint
from collections import defaultdict

import lt
#TODO
# tagsList = getTags(word)
# (isWordInCorrectForm, newWord) = setWordInTheCorrectForm(newWord, form)

def distance(proverb1, proverb2):
    return float(sum(1 for (a,b) in zip(proverb1, proverb2) if a != b)) / len(proverb1)

def corresponding(lt_tag, nltk_tag):
    return (
        (nltk_tag.startswith("JJ") and lt_tag.startswith("adj"))
        or (nltk_tag.startswith("VB") and lt_tag.startswith("v"))
        or (nltk_tag.startswith("MD") and lt_tag.startswith("v"))
        or (nltk_tag.startswith("NNP") and lt_tag.startswith("v"))
        or (nltk_tag.startswith("N") and lt_tag.startswith("n"))
        or (nltk_tag.startswith("CC") and lt_tag.startswith("cnj"))
        or (nltk_tag.startswith("IN") and lt_tag.startswith("cnj"))
        or (nltk_tag.startswith("CD") and lt_tag.startswith("num"))
        or (nltk_tag.startswith("DT") and lt_tag.startswith("det"))
        or (nltk_tag.startswith("MD") and lt_tag.startswith("vaux"))
        or (nltk_tag.startswith("PDT") and lt_tag.startswith("predet"))
        or (nltk_tag.startswith("PR") and lt_tag.startswith("prn"))
        or (nltk_tag.startswith("RB") and lt_tag.startswith("adv"))
        or (nltk_tag.startswith("RP") and lt_tag.startswith("pr"))
        )

class ProverbGenerator:

    def __init__(self):
        # FST analyser
        self.analyser = lt.Analyser()

        # Proverb list
        with open('proverbsList','r') as pfile:
            self.proverbsList = [line.rstrip() for line in pfile]

        # background graph
        self.backgroundGraph = nltk.text.ContextIndex(
            [word.lower() for word in nltk.corpus.gutenberg.words()]
        )

    def randomProverb(self):
        return self.proverbsList[randint(0,len(self.proverbsList)-1)]

    def categorize_words(self, words):
        d = defaultdict(list)
        for w in words:
            for (base, tags) in self.analyser.analyse(w):
                d[tags[0]].append(base)
        return d

    def analyse_proverb(self, proverb):
        pos_tagged = nltk.pos_tag(proverb)
        print(pos_tagged)
        analysis = []

        for (w,pos) in zip(proverb, pos_tagged):
            a = self.analyser.analyse(w)
            if len(a) == 1:
                analysis.append(a[0][1])
            else:
                keep = None
                for b in a:
                    if corresponding(b[1][0], pos[1]):
                        keep = b
                if keep is None:
                    keep = a[0]
                analysis.append(keep[1])

        return analysis

    def generate(self, theme, rate=0.5):
        # disabel over verbosity
        old_stdout = sys.stdout
        sys.stdout = open(os.devnull, 'w')
        similar_words = self.backgroundGraph.similar_words(theme, 100)
        sys.stdout = old_stdout

        categories = self.categorize_words(similar_words)
        
        base_proverb = nltk.word_tokenize(self.randomProverb())
        base_analysis = self.analyse_proverb(base_proverb)

        new_proverb = [ base_proverb[i] for i in range(len(base_proverb))]

        permutation = list(range(0,len(base_proverb)))
        random.shuffle(permutation)
        for i in permutation:
            if len(categories[base_analysis[i][0]]) == 0 or distance(base_proverb, new_proverb) > rate:
                continue

            if (base_analysis[i][0].startswith("prn")
             or base_analysis[i][0].startswith("det")
             or base_analysis[i][0].startswith("num")):
                continue

            new_word = random.choice(categories[base_analysis[i][0]])

            new_proverb[i] = self.analyser.generate(new_word, base_analysis[i])

        for ((a,b),c) in zip(zip(base_proverb,new_proverb),base_analysis):
            print(a,b,c)

        print(" ".join(base_proverb))
        print(" ".join(new_proverb))
