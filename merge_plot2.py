#-*- coding: utf-8 -*-
import codecs
import os, sys, string
from io import open
from glob import glob
import glob

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

resultsLaTeX = open('Tabele_LateX_APR1400_B2.tex', 'a+')

for N in NList:

    ResultsTable = []

    MainFile = PLTfilesMain[N]
    SubFileList = [s for s in PLTfilesSub if MainFile in s]
    SubFileList.sort()

    MainFileRead = open(MainFile)
    MainListOfLines = MainFileRead.readlines()[5:]
    
    #czytaj pierwsza linie z MainFile:
    FirstLine = MainListOfLines[0]
    FirstLineSplit = FirstLine.split()
    firstWord = "Izotop"
    FirstLineSplit.insert(0,firstWord)
    ResultsTable.insert(0,FirstLineSplit)
    LastTime = float(FirstLineSplit[-1])

    #czytaj kloejne linie z MainFile:
    MainListOfLines.pop(0)
    for item in MainListOfLines:
        TLine = item.split()
        ResultsTable.append(TLine)

    #czytaj pierwsza linie z SubFile:
    for subfile in SubFileList:
        SubFileRead = open(subfile)
        SubListOfLines = SubFileRead.readlines()[5:]
        FirstLineSub = SubListOfLines[0]
        FirstLineSubSplit = FirstLineSub.split()
        toAppend = float(FirstLineSubSplit[2])
        TimeToAppend = str(LastTime + toAppend) 
        ResultsTable[0].append(TimeToAppend)

        SubListOfLines.pop(0)
        for item in SubListOfLines:
            indx = SubListOfLines.index(item)
            Place = indx + 1
            TLine = item.split()
            ValueToAppend = TLine[3]
            ResultsTable[Place].append(ValueToAppend)

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

    ResultsTableLaTeX = []
    firstTxT = ResultsTable[0][0]
    FirstLine = ResultsTable[0][-8:]
    FirstLine.insert(0,firstTxT)

    FirstLine[0] = ' '
    BurnTime = FirstLine[1]
    FirstLine[1] = str(float(BurnTime))+' d'
    FirstLine[1] = FirstLine[1].replace('.',',')
    FirstLine[2] = '1 y'
    FirstLine[3] = '10 y'
    FirstLine[4] = '100 y'
    FirstLine[5] = '1.000 y'
    FirstLine[6] = '10.000 y'
    FirstLine[7] = '100.000 y'
    FirstLine[8] = '1 mln y'

    ResultsTable.pop(0)
    for item in ResultsTable:
        ix = ResultsTable.index(item)
        firstColumn = '\\textbf{'+str(ResultsTable[ix][0])+'}'
        lastColumns = ResultsTable[ix][-8:]
        lastColumns.insert(0,firstColumn)
        ResultsTableLaTeX.append(lastColumns)

    del ResultsTableLaTeX[-2:]

    ResultsTableLaTeX = [[x.replace('.',',') for x in l] for l in ResultsTableLaTeX]

    # - captions
    caption = str()
    if N == 0:
        caption = "\\textbf{Reaktor APR1400 - Kaseta B2} - Zale\\.zno\\'s\\'c masy [g] wybranych aktywnowc\\'ow od czasu - od momentu zako\\'nczenia wypalania do miliona lat składowania paliwa (d - dni, y - lata)".decode("utf8")
    if N == 1:
        caption = "\\textbf{Reaktor APR1400 - Kaseta B2} - Zale\\.zno\\'s\\'c masy [kg] wybranych aktywnowc\\'ow od czasu - od momentu zako\\'nczenia wypalania do miliona lat składowania paliwa (d - dni, y - lata)".decode("utf8")
    if N == 2:
        caption = "\\textbf{Reaktor APR1400 - Kaseta B2} - Zale\\.zno\\'s\\'c aktywno\\'sci [Bq] wybranych aktywnowc\\'ow od czasu - od momentu zako\\'nczenia wypalania do miliona lat składowania paliwa (d - dni, y - lata)".decode("utf8")
    if N == 3:
        caption = "\\textbf{Reaktor APR1400 - Kaseta B2} - Zale\\.zno\\'s\\'c radiotoksyczno\\'sci [H2OM - ilo\\'s\\'c metr\\'ow sze\\'sciennych wody, aby rozcie\\'nczy\\'c izotop do poziomu okre\\'slonego w \\textit{Radioactivity Concentration Guide}] wybranych aktywnowc\\'ow od czasu - od momentu zako\\'nczenia wypalania do miliona lat składowania paliwa (d - dni, y - lata)".decode("utf8")
    if N == 4:
        caption = "\\textbf{Reaktor APR1400 - Kaseta B2} - Zale\\.zno\\'s\\'c mocy cieplnej [W] wybranych aktywnowc\\'ow od czasu - od momentu zako\\'nczenia wypalania do miliona lat składowania paliwa (d - dni, y - lata)".decode("utf8")
    if N == 5:
        caption = "\\textbf{Reaktor APR1400 - Kaseta B2} - Zale\\.zno\\'s\\'c masy [g] wybranych produkt\\'ow rozszczepienia od czasu - od momentu zako\\'nczenia wypalania do miliona lat składowania paliwa (d - dni, y - lata)".decode("utf8")
    if N == 6:
        caption = "\\textbf{Reaktor APR1400 - Kaseta B2} - Zale\\.zno\\'s\\'c masy [kg] wybranych produkt\\'ow rozszczepienia od czasu - od momentu zako\\'nczenia wypalania do miliona lat składowania paliwa (d - dni, y - lata)".decode("utf8")
    if N == 7:
        caption = "\\textbf{Reaktor APR1400 - Kaseta B2} - Zale\\.zno\\'s\\'c aktywno\\'sci [Bq] wybranych produkt\\'ow rozszczepienia od czasu - od momentu zako\\'nczenia wypalania do miliona lat składowania paliwa (d - dni, y - lata)".decode("utf8")
    if N == 8:
        caption = "\\textbf{Reaktor APR1400 - Kaseta B2} - Zale\\.zno\\'s\\'c radiotoksyczno\\'sci [H2OM - ilo\\'s\\'c metr\\'ow sze\\'sciennych wody, aby rozcie\\'czy\\'c izotop do poziomu okre\\'slonego w \\textit{Radioactivity Concentration Guide}] wybranych produkt\\'ow rozszczepienia od czasu - od momentu zako\\'nczenia wypalania do miliona lat składowania paliwa (d - dni, y - lata)".decode("utf8")
    if N == 9:
        caption = "\\textbf{Reaktor APR1400 - Kaseta B2} - Zale\\.zno\\'s\\'c mocy cieplnej [W] wybranych produkt\\'ow rozszczepienia od czasu - od momentu zako\\'nczenia wypalania (d - dni, y - lata)".decode("utf8")

    label = 'EPR_A1_'+str(N)
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

resultsLaTeX.close()