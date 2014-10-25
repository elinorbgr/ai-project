import pickle
from operator import itemgetter
import itertools
import math
import copy

class BackgroundGraph:

    #constructor
    def __init__(self, nameCurrentGraph):
        #variables initialization
        self.nameCurrentGraph = nameCurrentGraph
        self.graph={}
        #Graph completion
        self.loadFileGraph()

    def addlistWords(self, listWords):
        # extract sentences
        indices = [i for i, x in enumerate(listWords) if x == "."]
        indices = [0]+indices
        listSentences = [listWords[indices[i - 1]:x] for i, x in enumerate(indices)][1:]
        # add sentences
        l = len(listSentences)
        for i,s in enumerate(listSentences):
            print(100.0*i/l)
            self.addSentence(s)

    def addSentence(self, sentence):
        for x,y in itertools.product(sentence,sentence):
            self.addWords(x,y)

    #load a graph from an existing file
    def loadFileGraph(self):
        try:
            file= open(self.nameCurrentGraph, 'rb')
            try:
                self.graph = pickle.load(file)
            except:
                print("The file doesn't contain a graph")
            file.close()
        except IOError:
            print("File couldn't be opened ! Graph will start empty")

    #save the current graph to a file        
    def saveFileGraph(self):
        file= open(self.nameCurrentGraph, 'wb')
        pickle.dump(self.graph, file)
        file.close()

    #add a new or existing combination of 2 words to the graph
    def addWords(self, word1, word2):
        w1 = (word1 in self.graph)
        w2 = word2 in self.graph
        if (word1 in self.graph) == False:
            self.graph[word1] = {}
        if (word2 in self.graph) == False:
            self.graph[word2] = {}

        if (word2 in self.graph[word1]):
            self.graph[word1][word2] += 1
        else:
            self.graph[word1][word2] = 1

        if (word1 in self.graph[word2]):
            self.graph[word2][word1] += 1
        else:
            self.graph[word2][word1] = 1

    #get the N closest neighbors        
    def getNeighbors(self, word, N):
        l=list(self.graph[word].items())
        l.sort(key=itemgetter(1),reverse=True)
        if N<len(l): return [l[i][0] for i in range(N)] 
        else:   return [l[i][0] for i in range(len(l))]

    #give the proximity between 2 words
    def prox(self, word1, word2):
        return self.graph[word1][word2]


    def normalize(self):
        compt_back={}
        compt_rel={}
        LLR={}
        #background and relative frequencies calculus
        tot_mot = 0
        for mot1, dic in self.graph.items():
            compt_rel[mot1] = {}
            tot_curr_mot = sum(dic.values())
            compt_back[mot1]=tot_curr_mot 
            tot_mot+= tot_curr_mot
            for mot2, nb_assoc in dic.items():
                compt_rel[mot1][mot2] = nb_assoc/(tot_curr_mot+0.0)
        for mot, val_abs in compt_back.items():
            compt_back[mot] = val_abs / (tot_mot + 0.0)
        #final likelihood calculus
        LLR = copy.deepcopy(compt_rel)
        for mot1, dic in compt_rel.items():
            for mot2, freq in dic.items():
                p11=compt_rel[mot1][mot2]*compt_back[mot1]
                if p11<=0:   p11=10**-15
                k11=self.graph[mot1][mot2]
                p11n=compt_back[mot1]*compt_back[mot2]
                p12=compt_back[mot2]-p11
                if p12<=0:   p12=10**-15
                k12=sum(self.graph[mot2].values())-k11
                p12n=compt_back[mot2]-p11n
                if p12n<=0:   p12n=10**-15
                p21=compt_back[mot1]-p11
                if p21<=0:   p21=10**-15
                k21=sum(self.graph[mot1].values())-k11
                p21n=compt_back[mot1]-p11n
                if p21n<=0:   p21n=10**-15
                p22=1-(p11+p12+p21)
                if p22<=0:   p22=10**-15
                p22n=1-(p11n+p12n+p21n)
                if p22n<=0:   p22n=10**-15
                k22=tot_mot
                #print(p11,k11,p11n,p12,k12,p12n,p21,k21,p21n,p22,p22n,k22)
                LLR[mot1][mot2]= -2* ( k11*math.log(p11n/p11)+k12*math.log(p12n/p12)+ k21*math.log(p21n/p21)+ k22*math.log(p22n/p22))
        self.graph=LLR

            
            

##########################
#CODE TESTING            #
##########################
    
#Graph creation
graph = BackgroundGraph("Test")

#Graph filling
graph.addWords("chien", "chat")
graph.addWords("souris", "chat")
graph.addWords("laisse", "chien")
graph.addWords("souris", "chat")
graph.addWords("chat", "chien")
graph.addWords("poisson", "chat")

#graph printing
print(graph.graph)

#closest neighbors
print(graph.getNeighbors("chat", 2))

#proximity between 2 words
print(graph.prox("chat", "poisson"))

graph.normalize()
print(graph.graph)

print(graph.prox("chat", "poisson"))
print(graph.getNeighbors("chat", 2))

"""
#serialization
graph.saveFileGraph()

#load preexisting graph from a file
graph2 = BackgroundGraph("Test")
print(graph2.graph)
"""
            
