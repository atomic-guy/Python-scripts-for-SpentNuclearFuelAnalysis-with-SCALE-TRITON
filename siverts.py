#-*- coding: utf-8 -*-
import codecs
import os, sys, string
from io import open
from glob import glob
import glob
import numpy as np


Inhalation  = {'am241': 9.6e-5, 'am243': 9.6e-5, 'ba140': 1.0e-9, 'ce141': 9.3e-10, 'ce143': 2.7e-10, 'ce144': 4.0e-8, 'cm242': 3.3e-6, 'cm243': 6.9e-5, 'cm244': 5.7e-5, 'cs134': 6.6e-9, 'cs135': 6.9e-10, 'cs137': 4.6e-9, 'eu154': 5.3e-8, 'eu155': 6.9e-9, 'eu156': 3.4e-9, 'i129': 3.6e-8, 'i135': 3.2e-10, 'mo99': 2.2e-10, 'nb95': 5.7e-10, 'nd147': 2.1e-9, 'np237': 5.0e-5, 'pm148': 2.0e-9, 'pr143': 2.2e-9, 'pu238': 1.1e-4, 'pu239': 1.2e-4, 'pu240': 1.2e-4, 'pu241': 2.3e-6, 'pu242': 1.1e-4, 'rh105': 8.2e-11, 'ru103': 4.8e-10, 'ru106': 7.9e-9, 'sb125': 1.4e-9, 'se79': 1.1e-9, 'sm151': 4.0e-9, 'sm153': 6.3e-10, 'sn126': 1.1e-8, 'sr90': 2.4e-8, 'tc99': 2.9e-10, 'u234': 5.6e-7, 'u236': 5.3e-7, 'zr93': 2.5e-8, 'zr95': 2.5e-9, 'pm147': 5.0e-9, 'pm149': 6.7e-10, 'sm147': 9.6e-6, 'pd107': 2.5e-11, 'cd113': 1.2e-7, 'u235': 5.2e-7, 'u238': 5.0e-7}

Ingestion  = {'am241':  2.0e-7, 'am243': 2.0e-7, 'ba140': 2.6e-9, 'ce141': 7.1e-10, 'ce143': 1.1e-9, 'ce144': 5.2e-9, 'cm242': 1.2e-8, 'cm243': 1.5e-7, 'cm244': 1.2e-7, 'cs134': 1.9e-8, 'cs135': 2.0e-9, 'cs137': 1.3e-8, 'eu154': 2.0e-9, 'eu155': 3.2e-10, 'eu156': 2.2e-9, 'i129':  1.1e-7, 'i135': 9.3e-10, 'mo99': 6.0e-10, 'nb95': 5.8e-10, 'nd147': 1.1e-9, 'np237': 1.1e-7, 'pm148': 2.7e-9, 'pr143': 1.2e-9, 'pu238': 2.3e-7, 'pu239': 2.5e-7, 'pu240': 2.5e-7, 'pu241': 4.8e-9, 'pu242': 2.4e-7, 'rh105': 3.7e-10, 'ru103': 7.3e-10, 'ru106': 7.0e-9, 'sb125': 1.1e-9, 'se79': 2.9e-9, 'sm151': 9.8e-11, 'sm153': 7.4e-10, 'sn126': 4.7e-9, 'sr90': 2.8e-8, 'tc99': 6.4e-10, 'u234': 4.9e-8, 'u236': 4.7e-8, 'zr93': 1.1e-9, 'zr95': 9.5e-10, 'pm147': 2.6e-10, 'pm149': 9.9e-10, 'sm147': 4.9e-8, 'pd107': 3.7e-11, 'cd113': 2.5e-8, 'u235': 4.7e-8, 'u238': 4.5e-8}

Intake = {'am241': 9.6e-5, 'am243': 9.6e-5, 'ba140': 2.6e-9, 'ce141': 9.3e-10, 'ce143': 1.1e-9, 'ce144': 4.0e-8, 'cm242': 3.3e-6, 'cm243': 6.9e-5, 'cm244': 5.7e-5, 'cs134': 1.9e-8, 'cs135': 2.0e-9, 'cs137': 1.3e-8, 'eu154': 5.3e-8, 'eu155': 6.9e-9, 'eu156': 3.4e-9, 'i129': 1.1e-7, 'i135': 9.3e-10, 'mo99': 6.0e-10, 'nb95': 5.8e-10, 'nd147': 2.1e-9, 'np237': 5.0e-5, 'pm148': 2.7e-9, 'pr143': 2.2e-9, 'pu238': 1.1e-4, 'pu239': 1.2e-4, 'pu240': 1.2e-4, 'pu241': 2.3e-6, 'pu242': 1.1e-4, 'rh105': 3.7e-10, 'ru103': 7.3e-10, 'ru106': 7.9e-9, 'sb125': 1.4e-9, 'se79': 2.9e-9, 'sm151': 4.0e-9, 'sm153': 7.4e-10, 'sn126': 1.1e-8, 'sr90': 2.8e-8, 'tc99': 6.4e-10, 'u234': 5.6e-7, 'u236': 5.3e-7, 'zr93': 2.5e-8, 'zr95': 2.5e-9, 'pm147': 5.0e-9, 'pm149': 9.9e-10, 'sm147': 9.6e-6, 'pd107': 3.7e-11, 'cd113': 1.2e-7, 'u235': 5.2e-7, 'u238': 5.0e-7}


#Wprowadz informacje o reaktorze i kasecie
reaktor = input("Typ reaktora: ")
kaseta = input("Typ kasety paliwowej: ")


NList = [2, 7]

for N in NList:
    CaseFileName = 'ResultsTable_'+str(reaktor)+'_'+str(kaseta)+'_Case'+str(N)+'.txt'
    resultsFileName = 'ResultsTable_'+str(reaktor)+'_'+str(kaseta)+'_Case'+str(N)+'_Radiotoxicity-Sv.txt'
    resultsFile = open(resultsFileName, 'a+')

    file = open(CaseFileName)
    file2 = open(CaseFileName)

    FirstLine = file.readlines()[0]
    FirstLineSplitted = FirstLine.split()
    FirstLineSplitted.insert(0,unicode(''))

    FileListOfLines = file2.readlines()[1:]
    
    TableInhalation = []
    TableInhalation.append(FirstLineSplitted)

    TableIngestion = []
    TableIngestion.append(FirstLineSplitted)

    TableIntake = []
    TableIntake.append(FirstLineSplitted)

    for line in FileListOfLines:
        TLine = line.split()
        Isotope = TLine[0]
        TLine.pop(0)
        TLine = [float(i) for i in TLine]

        if Isotope in Inhalation:

            InhInd = Inhalation[Isotope]
            InhIndx = float(InhInd)
            TLineInh = [i * InhIndx for i in TLine]
            TLineInh = [unicode('{:.4e}'.format(i)) for i in TLineInh]
            TLineInh.insert(0,Isotope)
            TableInhalation.append(TLineInh)

            IngInd = Ingestion[Isotope]
            IngIndx = float(IngInd)
            TLineIng = [i * IngIndx for i in TLine]
            TLineIng = [unicode('{:.4e}'.format(i)) for i in TLineIng]
            TLineIng.insert(0,Isotope)
            TableIngestion.append(TLineIng)

            IntInd = Intake[Isotope]
            IntIndx = float(IntInd)
            TLineInt = [i * IntIndx for i in TLine]
            TLineInt = [unicode('{:.4e}'.format(i)) for i in TLineInt]
            TLineInt.insert(0,Isotope)
            TableIntake.append(TLineInt)

    #zapis tabel do pliku
    L1 = '\n'+'Inhalation'+'\n'
    resultsFile.write(unicode(L1))
    col_width1 = max(len(word) for item in TableInhalation for word in item) + 2
    for item in TableInhalation:
        resultsFile.write("".join(word.ljust(col_width1) for word in item))
        resultsFile.write(unicode('\n'))    

    L2 = '\n'+'Ingestion'+'\n'
    resultsFile.write(unicode(L2))
    col_width2 = max(len(word) for item in TableIngestion for word in item) + 2
    for item in TableIngestion:
        resultsFile.write("".join(word.ljust(col_width2) for word in item))
        resultsFile.write(unicode('\n'))    

    L3 = '\n'+'Intake'+'\n'
    resultsFile.write(unicode(L3))
    col_width3 = max(len(word) for item in TableIntake for word in item) + 2
    for item in TableIntake:
        resultsFile.write("".join(word.ljust(col_width3) for word in item))
        resultsFile.write(unicode('\n'))  

    resultsFile.close()