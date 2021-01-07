#-*- coding: utf-8 -*-
import codecs
import os, sys, string
from io import open
from glob import glob
import glob
import numpy as np


RCG = {'am241': 2e5,
 'am243': 2e5,
 'ba140': 2e7, 
 'ce141': 6e7,
 'ce143': 5e7, 
 'ce144': 8e6,
 'cm242': 8e6,
 'cm243': 3e5,
 'cm244': 3e5,
 'cs134': 9e6, 
 'cs135': 1e8, 
 'cs137': 1e7, 
 'eu154': 3e7,
 'eu155': 2e8,
 'eu156': 2e7,
 'i129':  4e5, 
 'i135':  6e7,  
 'mo99':  2e8,  
 'nb95':  1e8,  
 'nd147': 4e7,
 'np237': 1e4,
 'pm148': 2e7, 
 'pr143': 4e7,
 'pu238': 1e7,
 'pu239': 9e6,
 'pu240': 9e6,
 'pu241': 4e8,
 'pu242': 9e6,
 'rh105': 1e8,  
 'ru103': 8e7,  
 'ru106': 8e6,
 'sb125': 9e7,
 'se79':  2e8, 
 'sm151': 5e8,
 'sm153': 7e7,  
 'sn126': 1e7,
 'sr90':  2e7, 
 'tc99':  2e8,  
 'u234':  1e7,
 'u236':  1e7,
 'zr93':  2e8,
 'zr95':  7e7,
 'pm147': 2e8,
 'pm149': 5e7,
 'sm147': 2e6,
 'pd107': 1e9,
 'cd113': 9e5,
 'u235': 1e7,
 'u238': 1e7}


#Wprowadz informacje o reaktorze i kasecie
reaktor = input("Typ reaktora: ")
kaseta = input("Typ kasety paliwowej: ")


NList = [2, 7]

for N in NList:
    CaseFileName = 'ResultsTable_Case'+str(N)+'.txt'
    resultsFileName = 'ResultsTable_Case'+str(N)+'_Radiotoxicity-RCG.txt'
    resultsFile = open(resultsFileName, 'a+')

    file = open(CaseFileName)
    file2 = open(CaseFileName)

    FirstLine = file.readlines()[3]
    FirstLineSplitted = FirstLine.split()

    FileListOfLines = file2.readlines()[4:]
    del FileListOfLines[-2:]
    
    TableRCG = []
    TableRCG.append(FirstLineSplitted)

    for line in FileListOfLines:
        TLine = line.split()
        Isotope = TLine[0]
        TLine.pop(0)
        TLine = [float(i) for i in TLine]

        if Isotope in RCG:

            RCGInd = RCG[Isotope]
            RCGIndx = float(RCGInd)
            TLineRCG = [i / RCGIndx for i in TLine]
            TLineRCG = [unicode('{:.4e}'.format(i)) for i in TLineRCG]
            TLineRCG.insert(0,Isotope)
            TableRCG.append(TLineRCG)

    #zapis tabel do pliku
    L1 = 'RCG'+'\n'
    resultsFile.write(unicode(L1))
    col_width1 = max(len(word) for item in TableRCG for word in item) + 2
    for item in TableRCG:
        resultsFile.write("".join(word.ljust(col_width1) for word in item))
        resultsFile.write(unicode('\n'))    


    resultsFile.close()