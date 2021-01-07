import glob, os, sys, string
from io import open

krok = input("Podaj numer kroku: ")
name = '*' + str(krok)

file_write_name = 'compos_step_'+str(krok)+'.txt'

file_names = glob.glob(name)

with open(file_write_name, 'w') as outfile:
	for file_name in file_names:
		with open(file_name) as f:
			for line in f:
				outfile.write(line)

outfile.close()