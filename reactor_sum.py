#-*- coding: utf-8 -*-
import codecs
import os, sys, string
from io import open
from glob import glob
import glob
import numpy as np
import matplotlib
matplotlib.use('agg')
import matplotlib.pyplot as plt
import matplotlib.ticker as ticker

reaktor = input("Typ reaktora: ")

NList = [0, 2, 3, 4, 5, 7, 8, 9]
#NList = [0]

for N in NList:
    CaseFileName = '*Case'+str(N)+'.txt'
    CaseFiles = []
    CaseFiles = glob.glob(CaseFileName)
    CaseFiles.sort()
    resultsFileName = 'Results_'+str(reaktor)+'_Case'+str(N)+'.dat'
    resultsFile = open(resultsFileName, 'a+')

    ResultsTable = []

    for file in CaseFiles:
        file2 = open(file)
        FileListOfLines = file2.readlines()[1:]
        FileLinesTable = []
        for line in FileListOfLines:
            TLine = line.split()
            TLine.pop(0)
            TLine = [float(i) for i in TLine]
            FileLinesTable.append(TLine)
        ResultsTable.append(FileLinesTable)

    ResultsArray = np.array(ResultsTable) 

    SumArray = sum(ResultsArray)
    TSUMl = SumArray.tolist()
    TSUMl = [[unicode('{:.4e}'.format(i)) for i in j] for j in TSUMl]
    TSUMl = [[x.replace('.',',') for x in l] for l in TSUMl]

    #odczytanie pierwszego wiersza
    filec = open(CaseFiles[0])
    filec2 = filec.readlines()
    filecL = filec2[0].split()
    BurnTime = filecL[0]
    
    FirstLine = []
    FirstLine.append('\\textcolor{myGreen}{0 y}')
    FirstLine.append('\\textcolor{myBlue}{1 y}')
    FirstLine.append('\\textcolor{myBlue}{10 y}')
    FirstLine.append('\\textcolor{myBlue}{100 y}')
    FirstLine.append('\\textcolor{myBlue}{1.000 y}')
    FirstLine.append('\\textcolor{myBlue}{10.000 y}')
    FirstLine.append('\\textcolor{myBlue}{100.000 y}')
    FirstLine.append('\\textcolor{myBlue}{1 mln y}')

    TSUMlLaTeX = list(TSUMl)
    TSUMlLaTeX.insert(0,FirstLine)
    print TSUMlLaTeX

    DecayLine = []
    DecayLine.append(unicode('0'))
    DecayLine.append(unicode('1'))
    DecayLine.append(unicode('10'))
    DecayLine.append(unicode('100'))
    DecayLine.append(unicode('1000'))
    DecayLine.append(unicode('10000'))
    DecayLine.append(unicode('100000'))
    DecayLine.append(unicode('10000000'))

    TSUMl.insert(0,DecayLine)
    
    IsoCol = []
    for line in FileListOfLines:
        LineSplit = line.split()
        iso = LineSplit[0]
        IsoCol.append(iso)

    #odczytanie kolumny izotopów
    IsoCol.insert(0,' ')
    for item in TSUMl:
        itemInx = TSUMl.index(item)
        toIns = IsoCol[itemInx]
        item.insert(0,toIns)
    
    #zapis tabeli do pliku
    col_width = max(len(word) for item in TSUMl for word in item) + 2
    for item in TSUMl:
        resultsFile.write("".join(word.ljust(col_width) for word in item))
        resultsFile.write(unicode('\n'))    
    
    IsoColLaTeX = []
    for item in IsoCol:
        newItem = '\\textbf{'+str(item)+'}'
        IsoColLaTeX.append(newItem)

    for item in TSUMlLaTeX:
        ixxItem = TSUMlLaTeX.index(item)
        item[0] = IsoColLaTeX[ixxItem]
    
    resultsFile.close()

    #Zapis do LaTeX

    resultsLaTeXName = 'Tabele_LateX_'+str(reaktor)+'_Total.tex'
    resultsLaTeX = open(resultsLaTeXName, 'a+')

    FirstLine.insert(0,' ')
    caption = str()
    if N == 0:
        caption = "Zale\\.zno\\'s\\'c \\textbf{masy [g]} wybranych aktywnowc\\'ow od czasu - \\textcolor{myGreen}{od momentu zako\\'nczenia wypalania} \\textcolor{myBlue}{do miliona lat sk\\l{}adowania} paliwa (y - lata) - dla pierwszegoo za\\l{}adunku rdzenia reaktora \\textbf{"+str(reaktor)+"}".decode("utf8")
    if N == 1:
        caption = "Zale\\.zno\\'s\\'c \\textbf{masy [kg]} wybranych aktywnowc\\'ow od czasu - \\textcolor{myGreen}{od momentu zako\\'nczenia wypalania} \\textcolor{myBlue}{do miliona lat sk\\l{}adowania} paliwa (y - lata) - dla pierwszego za\\l{}adunku rdzenia reaktora \\textbf{"+str(reaktor)+"}".decode("utf8")
    if N == 2:
        caption = "Zale\\.zno\\'s\\'c \\textbf{aktywno\\'sci [Bq]} wybranych aktywnowc\\'ow od czasu - \\textcolor{myGreen}{od momentu zako\\'nczenia wypalania} \\textcolor{myBlue}{do miliona lat sk\\l{}adowania} paliwa (y - lata) - dla pierwszego za\\l{}adunku rdzenia reaktora \\textbf{"+str(reaktor)+"}".decode("utf8")
    if N == 3:
        caption = "Zale\\.zno\\'s\\'c \\textbf{radiotoksyczno\\'sci} [H2OM - ilo\\'s\\'c $m^{3}$ wody, aby rozcie\\'nczy\\'c izotop do poziomu okre\\'slonego w \\textit{Radioactivity Concentration Guides}] wybranych aktywnowc\\'ow od czasu - \\textcolor{myGreen}{od momentu zako\\'nczenia wypalania} \\textcolor{myBlue}{do miliona lat sk\\l{}adowania} paliwa (y - lata) - dla pierwszego za\\l{}adunku rdzenia reaktora \\textbf{"+str(reaktor)+"}".decode("utf8")
    if N == 4:
        caption = "Zale\\.zno\\'s\\'c \\textbf{mocy cieplnej [W]} wybranych aktywnowc\\'ow od czasu - \\textcolor{myGreen}{od momentu zako\\'nczenia wypalania} \\textcolor{myBlue}{do miliona lat sk\\l{}adowania} paliwa (y - lata) - dla pierwszego za\\l{}adunku rdzenia reaktora \\textbf{"+str(reaktor)+"}".decode("utf8")
    if N == 5:
        caption = "Zale\\.zno\\'s\\'c \\textbf{masy [g]} wybranych produkt\\'ow rozszczepienia od czasu - \\textcolor{myGreen}{od momentu zako\\'nczenia wypalania} \\textcolor{myBlue}{do miliona lat sk\\l{}adowania} paliwa (y - lata) - dla pierwszego za\\l{}adunku rdzenia reaktora \\textbf{"+str(reaktor)+"}".decode("utf8")
    if N == 6:
        caption = "Zale\\.zno\\'s\\'c \\textbf{masy [kg]} wybranych produkt\\'ow rozszczepienia od czasu - \\textcolor{myGreen}{od momentu zako\\'nczenia wypalania} \\textcolor{myBlue}{do miliona lat sk\\l{}adowania} paliwa (y - lata) - dla pierwszego za\\l{}adunku rdzenia reaktora \\textbf{"+str(reaktor)+"}".decode("utf8")
    if N == 7:
        caption = "Zale\\.zno\\'s\\'c \\textbf{aktywno\\'sci [Bq]} wybranych produkt\\'ow rozszczepienia od czasu - \\textcolor{myGreen}{od momentu zako\\'nczenia wypalania} \\textcolor{myBlue}{do miliona lat sk\\l{}adowania} paliwa (y - lata) - dla pierwszego za\\l{}adunku rdzenia reaktora \\textbf{"+str(reaktor)+"}".decode("utf8")
    if N == 8:
        caption = "Zale\\.zno\\'s\\'c \\textbf{radiotoksyczno\\'sci} [H2OM - ilo\\'s\\'c $m^{3}$ wody, aby rozcie\\'nczy\\'c izotop do poziomu okre\\'slonego w \\textit{Rad. Conc. Guides}] wybranych produkt\\'ow rozszczepienia od czasu - \\textcolor{myGreen}{od zako\\'nczenia wypalania} \\textcolor{myBlue}{do mln lat sk\\l{}adowania} paliwa (y - lata) - dla pierwszego za\\l{}adunku rdzenia r. \\textbf{"+str(reaktor)+"}".decode("utf8")
    if N == 9:
        caption = "Zale\\.zno\\'s\\'c \\textbf{mocy cieplnej [W]} wybranych produkt\\'ow rozszczepienia od czasu - \\textcolor{myGreen}{od momentu zako\\'nczenia wypalania} \\textcolor{myBlue}{do miliona lat sk\\l{}adowania} paliwa (y - lata) - dla pierwszego za\\l{}adunku rdzenia reaktora \\textbf{"+str(reaktor)+"}".decode("utf8")

    label = str(reaktor)+'_Total_'+str(N)
    #zapis tabel
    L1 = '\\begin{landscape}'+'\n'+'\\begin{longtable}[h]{rllllllll}'+'\n'
#    L2 = '\\centering'+'\n'
    L2 = '\\caption{'+caption+' \\label{tab:'+label+'}} \\\\'+'\n'
#    L4 = '\\begin{tabularx}{\\textwidth}{rllllllll}'+'\n'
    L3 = '\\toprule'+'\n'
    L4 = '\\textbf{'+FirstLine[0]+'} & '+ '\\textbf{'+FirstLine[1]+'} & '+'\\textbf{'+FirstLine[2]+'} & '+'\\textbf{'+FirstLine[3]+'} & '+'\\textbf{'+FirstLine[4]+'} & '+'\\textbf{'+FirstLine[5]+'} & '+'\\textbf{'+FirstLine[6]+'} & '+'\\textbf{'+FirstLine[7]+'} & '+'\\textbf{'+FirstLine[8]+'}'+'\\\\'+'\n'
    L5 = '\\toprule'+'\n'+'\\endfirsthead'+'\n'+'\\multicolumn{9}{c}{\\tablename\\ \\thetable\\ -- \\textit{Kontynuacja z poprzedniej strony}} \\\\'+'\n'+'\\midrule'+'\n'
    L6 = '\\textbf{'+FirstLine[0]+'} & '+ '\\textbf{'+FirstLine[1]+'} & '+'\\textbf{'+FirstLine[2]+'} & '+'\\textbf{'+FirstLine[3]+'} & '+'\\textbf{'+FirstLine[4]+'} & '+'\\textbf{'+FirstLine[5]+'} & '+'\\textbf{'+FirstLine[6]+'} & '+'\\textbf{'+FirstLine[7]+'} & '+'\\textbf{'+FirstLine[8]+'}'+'\\\\'+'\n'
    L7 = '\\endhead'+'\n'+'\\hline \\multicolumn{9}{c}{\\textit{Kontynuacja na nast\\k{e}pnej stronie}} \\\\'+'\n'+'\\endfoot'+'\n'+'\\bottomrule'+'\n'+'\\endlastfoot'+'\n'
    resultsLaTeX.write(unicode(L1))
    resultsLaTeX.write(unicode(L2))
    resultsLaTeX.write(unicode(L3))
    resultsLaTeX.write(unicode(L4))
    resultsLaTeX.write(unicode(L5))
    resultsLaTeX.write(unicode(L6))
    resultsLaTeX.write(unicode(L7))

    TSUMlLaTeX.pop(0)
    for item in TSUMlLaTeX:
        LineFromTable = ' & '.join(item)
        LineToWrite = LineFromTable + '\\\\ \\hline'+'\n'
        resultsLaTeX.write(LineToWrite)

#    L8 = '\\end{tabularx}'+'\n'
    L9 = '\\end{longtable}'+'\n'+'\\end{landscape}'+'\n'+'\n'
#    resultsLaTeX.write(unicode(L8))
    resultsLaTeX.write(unicode(L9))   

