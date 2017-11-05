#!/usr/bin/python2.7
# -*- coding:utf-8 -*-

import os

from sets import Set
import time

class UtilData(object):
    def __init__(self):
        self.corpusDir = "./data/corpus/"
        self.ENCODE = 'utf-8'
        self.LINE_START = "<"
        self.LINE_END = ">"

    def analyzeCorpus(self):
        totalPoems = 0
        for filePath in os.listdir(self.corpusDir):
            if filePath.endswith('.txt') or filePath.endswith('.all'):
                fin = open(self.corpusDir + filePath)
                lines = fin.readlines()
                totalPoems += len(lines)
                print "****{:10d} poems in {:}".format(len(lines), filePath)
        print "****{:10d} poems in total".format(totalPoems)

    def prepareVocabularyDic(self):
        print "Start preparing vocabularyDic........"
        corpus = []
        corpus.append(self.LINE_START)
        corpus.append(self.LINE_END)
        for filePath in os.listdir(self.corpusDir):
            if filePath.endswith('.txt') or filePath.endswith('.all'):
                print "processing file {:}".format(filePath)
                fin = open(self.corpusDir + filePath)
                charList = fin.read().decode(self.ENCODE).split()# only chinese characters
                corpus += charList
        wordList = list( Set( corpus ) )
        vocabularyDic = {}
        for i in xrange(len(wordList)):
            vocabularyDic[wordList[i]] = i
        print "****Vocabulary size : {:d}".format(len(vocabularyDic))
        print "Finish preparing vocabularyDic........"
        return vocabularyDic

    def prepareNPLMData(self, WINDOW_SIZE):
        print "Start preparing data for NPLM ........"
        print "Start timer"
        start = time.time()
        vocabularyDic = self.prepareVocabularyDic()
        print "Making input-label pairs........"
        windowData = []
        for filePath in os.listdir(self.corpusDir):
            if filePath.endswith('.txt') or filePath.endswith('.all'):
                print "processing file {:}".format(filePath)
                fin = open(self.corpusDir + filePath)
                lines = fin.readlines()
                for line in lines:
                    cleanedLine = line.decode(self.ENCODE).split() # decode and delete space and eol
                    for i in xrange(len(cleanedLine)):
                        center = vocabularyDic[ cleanedLine[i] ]
                        context = []
                        for j in range(i - WINDOW_SIZE, i + WINDOW_SIZE + 1):
                            if j != i:
                                if j < 0:
                                    context.append(vocabularyDic[self.LINE_START])
                                elif j >= len(cleanedLine):
                                    context.append(vocabularyDic[self.LINE_END])
                                else:
                                    context.append(vocabularyDic[cleanedLine[j]])
                        windowData.append((context, center))
        trainData = zip(*windowData[0 : len(windowData) - 2000])#(inputs, labels)
        validData = zip(*windowData[len(windowData) - 2000 : len(windowData) - 1000])#(inputs, labels)
        testData = zip(*windowData[len(windowData) - 1000 : len(windowData)])#(inputs, labels)

        end = time.time()
        print "****{:d} datum in total".format(len(windowData))
        print "****Time cost {:} seconds".format(end - start)
        print "Finish preparing data for NPLM"

        return vocabularyDic, trainData, validData, testData

    def prepareSkipGramData(self, WINDOW_SIZE):
        print "Start preparing data for SkipGram ........"
        print "Start timer"
        start = time.time()
        vocabularyDic = self.prepareVocabularyDic()
        print "Making input-label pairs........"
        windowData = []
        for filePath in os.listdir(self.corpusDir):
            if filePath.endswith('.txt') or filePath.endswith('.all'):
                print "processing file {:}".format(filePath)
                fin = open(self.corpusDir + filePath)
                lines = fin.readlines()
                for line in lines:
                    cleanedLine = line.decode(self.ENCODE).split() # decode and delete space and eol
                    for i in xrange(len(cleanedLine)):
                        center = vocabularyDic[ cleanedLine[i] ]
                        for j in range(i - WINDOW_SIZE, i + WINDOW_SIZE + 1):
                            if j != i:
                                if j < 0:
                                    windowData.append((center, vocabularyDic[self.LINE_START]))
                                elif j >= len(cleanedLine):
                                    windowData.append(( center, vocabularyDic[self.LINE_END]))
                                else:
                                    windowData.append((center, vocabularyDic[cleanedLine[j]]))
        trainData = zip(*windowData[0 : len(windowData) - 2000])#(inputs, labels)
        validData = zip(*windowData[len(windowData) - 2000 : len(windowData) - 1000])#(inputs, labels)
        testData = zip(*windowData[len(windowData) - 1000 : len(windowData)])#(inputs, labels)


        end = time.time()
        print "****{:d} datum in total".format(len(windowData))
        print "****Time cost {:} seconds".format(end - start)
        print "Finish preparing data for SkipGram"

        return vocabularyDic, trainData, validData, testData


if __name__ == "__main__":
    utilData = UtilData()
    utilData.analyzeCorpus()
    utilData.prepareVocabularyDic()
    utilData.prepareNPLMData(1)
    utilData.prepareSkipGramData(1)