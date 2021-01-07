#-*- coding: utf-8 -*-
import codecs
import os, sys, string
from io import open
from glob import glob
import glob

OutputFiles = []
OutputFiles = glob.glob('*.out')
OutputFiles.sort()

keffResultsTotal = []

#Time Line
TimeLine = []
TimeFile = open(OutputFiles[0]).readlines()
for line in TimeFile:
	if 'k-eff = ' in line:
		lineTime = line.split()
		Time = unicode(lineTime[4])
		TimeLine.append(Time)
TimeLine.insert(0,' ')
TimeLine = [y.replace('d', '') for y in TimeLine]
TimeLine = [y.replace('.', ',') for y in TimeLine]

print TimeLine

for file in OutputFiles:
	keffResultsFile = []
	nameFile = str(file)
	keffResultsFile.append(nameFile)
	
	FileLines = open(file, 'r').readlines()
	for line in FileLines:
		if 'k-eff = ' in line:
			keffValue = unicode(line.split()[2])
			keffResultsFile.append(keffValue)

	keffResultsFile = [y.replace('.', ',') for y in keffResultsFile]
	keffResultsTotal.append(keffResultsFile)

KeffOutputFile = open('keff_APR1400.txt', 'a+')
keffResultsTotal.insert(0,TimeLine)

col_width = max(len(word) for item in keffResultsTotal for word in item) + 2
for item in keffResultsTotal:
    KeffOutputFile.write("".join(word.ljust(col_width) for word in item))
    KeffOutputFile.write(unicode('\n'))