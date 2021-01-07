#-*- coding: utf-8 -*-
import codecs
import os, sys, string
from io import open
from glob import glob
import glob
import numpy as np

#Wprowadz informacje o reaktorze i kasecie
reaktor = input("Typ reaktora: ")
kaseta = input("Typ kasety paliwowej: ")
lkaset = input("Liczba kaset paliwowych danego typu w rdzeniu: ")
NCore = int(lkaset)


# 1. Szukanie plikow .plt w glownym katalogu oraz podkatalogach
PLTfilesMain = []
PLTfilesMain = glob.glob("*.plt")
PLTfilesMain.sort()

PLTfilesSub = []
start_dir = os.getcwd()
file_name = '*.plt'
pattern   = file_name

for dir,_,_ in os.walk(start_dir):
    PLTfilesSub.extend(glob.glob(os.path.join(dir,pattern)))

NoOfItems = len(PLTfilesMain)
del PLTfilesSub[:NoOfItems]

PLTfilesSub.sort()

# 2. wybor plotow

NList = [0, 2, 3, 4, 5, 7, 8, 9]
N = int()

resultsLaTeXName = 'Tabele_LateX_'+str(reaktor)+'_'+str(kaseta)+'.tex'
resultsLaTeX = open(resultsLaTeXName, 'a+')

for N in NList:

    ResultsTable = []

    MainFile = PLTfilesMain[N]
    SubFileList = [s for s in PLTfilesSub if MainFile in s]
    SubFileList.sort()
    
    IsoColumn = []
    BurnColumn = []
    
    #czytaj kolumne izotopow oraz kolumne dla momentu zakonczenia wypalania t = 0
    BurnFile = open(SubFileList[0])
    BurnColumnFile = BurnFile.readlines()[5:]
    for item in BurnColumnFile:
        lineSplitted = item.split()
        toIsoColumn = lineSplitted[0]
        toBurnCoulumn = lineSplitted[2]
        IsoColumn.append(toIsoColumn)
        BurnColumn.append(toBurnCoulumn)

    IsoColumn[0] = 'Izotop'
    BurnColumn[0] = '0'
    
    DecayColumns = []
   
    #czytaj kolumny t > 0
    for file in SubFileList:       
        file2 = open(file)
        FileLines = file2.readlines()[6:]
        DecayColumn = []
        for line in FileLines:        
            FileLinesSplit = line.split()
            toDecayColumn = FileLinesSplit[3]
            DecayColumn.append(toDecayColumn)
        DecayColumns.append(DecayColumn)

    for item in DecayColumns:
        item.insert(0,unicode('0'))

    DecayColumns[0][0] = unicode('1')
    DecayColumns[1][0] = unicode('10')
    DecayColumns[2][0] = unicode('100')
    DecayColumns[3][0] = unicode('1000')
    DecayColumns[4][0] = unicode('10000')
    DecayColumns[5][0] = unicode('100000')
    DecayColumns[6][0] = unicode('10000000')

    ResultsTable.insert(0, IsoColumn)
    ResultsTable.insert(1, BurnColumn)

    for item in DecayColumns:
        ResultsTable.append(item)

    
    ResultsTable = map(list, zip(*ResultsTable))

    #zapis do pliku
    firstFile = PLTfilesMain[N]
    f1 = open(firstFile).readlines()
    line1 = f1[0]
    line2 = f1[1]
    line3 = f1[2]

    resultsFileName = 'ResultsTable_Case'+str(N)+'.txt'
    resultsFile = open(resultsFileName, 'a+')
    resultsFile.write(unicode(line1))
    resultsFile.write(unicode(line2))
    resultsFile.write(unicode(line3))
    col_width = max(len(word) for item in ResultsTable for word in item) + 2
    for item in ResultsTable:
        resultsFile.write("".join(word.ljust(col_width) for word in item))
        resultsFile.write(unicode('\n'))

    resultsFile.close()
    
    #tabela do LaTeX:
    # - nowa tabela

    del ResultsTable[-2:]

    ResultsTableLaTeX = []
    FirstLine = ResultsTable[0]

    FirstLine[0] = ' '
    FirstLine[1] = '\\textcolor{myGreen}{0 y}'
    FirstLine[2] = '\\textcolor{myBlue}{1 y}'
    FirstLine[3] = '\\textcolor{myBlue}{10 y}'
    FirstLine[4] = '\\textcolor{myBlue}{100 y}'
    FirstLine[5] = '\\textcolor{myBlue}{1.000 y}'
    FirstLine[6] = '\\textcolor{myBlue}{10.000 y}'
    FirstLine[7] = '\\textcolor{myBlue}{100.000 y}'
    FirstLine[8] = '\\textcolor{myBlue}{1 mln y}'

    ResultsTable.pop(0)
    for item in ResultsTable:
        ix = ResultsTable.index(item)
        firstColumn = '\\textbf{'+str(ResultsTable[ix][0])+'}'
        lastColumns = ResultsTable[ix][-8:]
        lastColumns.insert(0,firstColumn)
        ResultsTableLaTeX.append(lastColumns)

    ResultsTableLaTeX = [[x.replace('.',',') for x in l] for l in ResultsTableLaTeX]

    # - captions
    caption = str()
    if N == 0:
        caption = "\\textbf{Reaktor "+str(reaktor)+" - Kaseta "+str(kaseta)+"} - Zale\\.zno\\'s\\'c masy [g] wybranych aktywnowc\\'ow od czasu - \\textcolor{myGreen}{od momentu zako\\'nczenia wypalania} \\textcolor{myBlue}{do miliona lat sk\\l{}adowania} paliwa (y - lata)".decode("utf8")
    if N == 1:
        caption = "\\textbf{Reaktor "+str(reaktor)+" - Kaseta "+str(kaseta)+"} - Zale\\.zno\\'s\\'c masy [kg] wybranych aktywnowc\\'ow od czasu - \\textcolor{myGreen}{od momentu zako\\'nczenia wypalania} \\textcolor{myBlue}{do miliona lat sk\\l{}adowania} paliwa (y - lata)".decode("utf8")
    if N == 2:
        caption = "\\textbf{Reaktor "+str(reaktor)+" - Kaseta "+str(kaseta)+"} - Zale\\.zno\\'s\\'c aktywno\\'sci [Bq] wybranych aktywnowc\\'ow od czasu - \\textcolor{myGreen}{od momentu zako\\'nczenia wypalania} \\textcolor{myBlue}{do miliona lat sk\\l{}adowania} paliwa (y - lata)".decode("utf8")
    if N == 3:
        caption = "\\textbf{Reaktor "+str(reaktor)+" - Kaseta "+str(kaseta)+"} - Zale\\.zno\\'s\\'c radiotoksyczno\\'sci [H2OM - ilo\\'s\\'c $m^{3}$ wody, aby rozcie\\'nczy\\'c izotop do poziomu okre\\'slonego w \\textit{Radioactivity Concentration Guides}] wybranych aktywnowc\\'ow od czasu - \\textcolor{myGreen}{od momentu zako\\'nczenia wypalania} \\textcolor{myBlue}{do miliona lat sk\\l{}adowania} paliwa (y - lata)".decode("utf8")
    if N == 4:
        caption = "\\textbf{Reaktor "+str(reaktor)+" - Kaseta "+str(kaseta)+"} - Zale\\.zno\\'s\\'c mocy cieplnej [W] wybranych aktywnowc\\'ow od czasu - \\textcolor{myGreen}{od momentu zako\\'nczenia wypalania} \\textcolor{myBlue}{do miliona lat sk\\l{}adowania} paliwa (y - lata)".decode("utf8")
    if N == 5:
        caption = "\\textbf{Reaktor "+str(reaktor)+" - Kaseta "+str(kaseta)+"} - Zale\\.zno\\'s\\'c masy [g] wybranych produkt\\'ow rozszczepienia od czasu - \\textcolor{myGreen}{od momentu zako\\'nczenia wypalania} \\textcolor{myBlue}{do miliona lat sk\\l{}adowania} paliwa (y - lata)".decode("utf8")
    if N == 6:
        caption = "\\textbf{Reaktor "+str(reaktor)+" - Kaseta "+str(kaseta)+"} - Zale\\.zno\\'s\\'c masy [kg] wybranych produkt\\'ow rozszczepienia od czasu - \\textcolor{myGreen}{od momentu zako\\'nczenia wypalania} \\textcolor{myBlue}{do miliona lat sk\\l{}adowania} paliwa (y - lata)".decode("utf8")
    if N == 7:
        caption = "\\textbf{Reaktor "+str(reaktor)+" - Kaseta "+str(kaseta)+"} - Zale\\.zno\\'s\\'c aktywno\\'sci [Bq] wybranych produkt\\'ow rozszczepienia od czasu - \\textcolor{myGreen}{od momentu zako\\'nczenia wypalania} \\textcolor{myBlue}{do miliona lat sk\\l{}adowania} paliwa (y - lata)".decode("utf8")
    if N == 8:
        caption = "\\textbf{Reaktor "+str(reaktor)+" - Kaseta "+str(kaseta)+"} - Zale\\.zno\\'s\\'c radiotoksyczno\\'sci [H2OM - ilo\\'s\\'c $m^{3}$ wody, aby rozcie\\'nczy\\'c izotop do poziomu okre\\'slonego w \\textit{Radioactivity Concentration Guides}] wybranych produkt\\'ow rozszczepienia od czasu - \\textcolor{myGreen}{od zako\\'nczenia wypalania} \\textcolor{myBlue}{do mln lat sk\\l{}adowania} paliwa (y - lata)".decode("utf8")
    if N == 9:
        caption = "\\textbf{Reaktor "+str(reaktor)+" - Kaseta "+str(kaseta)+"} - Zale\\.zno\\'s\\'c mocy cieplnej [W] wybranych produkt\\'ow rozszczepienia od czasu - \\textcolor{myGreen}{od momentu zako\\'nczenia wypalania} \\textcolor{myBlue}{do miliona lat sk\\l{}adowania} (y - lata)".decode("utf8")

    label = str(reaktor)+'_'+str(kaseta)+'_'+str(N)
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

    for item in ResultsTableLaTeX:
        LineFromTable = ' & '.join(item)
        LineToWrite = LineFromTable + '\\\\ \\hline'+'\n'
        resultsLaTeX.write(LineToWrite)

#    L8 = '\\end{tabularx}'+'\n'
    L9 = '\\end{longtable}'+'\n'+'\\end{landscape}'+'\n'+'\n'
#    resultsLaTeX.write(unicode(L8))
    resultsLaTeX.write(unicode(L9))   

    #generowanie tabeli do obliczenia całego rdzenia

    ResultsTableLaTeX = [[x.replace(',','.') for x in l] for l in ResultsTableLaTeX]
    resultsFullFileName = 'ResultsTable_'+str(reaktor)+'_'+str(kaseta)+'_Case'+str(N)+'.txt'
    resultsFull = open(resultsFullFileName, 'a+')
    
    resultsFullTable = []
    for item in ResultsTableLaTeX:
        iitem = ResultsTableLaTeX.index(item)
        fullitem = []
        for i in item:
            ixx = item.index(i)
            if ixx != 0:
                full = float(i)
                full = NCore * full
                full = unicode('{:.4e}'.format(full))
                fullitem.append(full)
        resultsFullTable.append(fullitem)

    del IsoColumn[0]
    del IsoColumn[-2:] 
    for item in resultsFullTable:
        indexitem = resultsFullTable.index(item)
        Iso = IsoColumn[indexitem]
        item.insert(0,Iso)
    
    FirstLine[0] = ' '
    FirstLine[1] = '0'
    FirstLine[2] = '1'
    FirstLine[3] = '10'
    FirstLine[4] = '100'
    FirstLine[5] = '1000'
    FirstLine[6] = '10000'
    FirstLine[7] = '100000'
    FirstLine[8] = '1000000'

    FirstLine = [unicode(i) for i in FirstLine]
    resultsFullTable.insert(0,FirstLine)

    for item in resultsFullTable:
        resultsFull.write("".join(word.ljust(col_width) for word in item))
        resultsFull.write(unicode('\n'))

resultsLaTeX.close()