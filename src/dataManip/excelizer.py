from csv import QUOTE_NONE
import pandas as pd
import os
import fileinput

items = 12
directory = os.path.abspath(os.path.realpath(__file__)[:-len(os.path.basename(__file__))] + "../../") + '/'
for file in os.listdir(directory):
    if file.endswith(".csv"):
        f = open(directory+str(file), 'r')
        lines = f.readlines()
        f.close()
        labels = None
        index = 1
        lenalllines = len(lines)
        for line in lines:
            if len(line.split("|")) == items:
                labels = line.split("|")
                break
            else:
                index += 1
        
        print(file, "has index =", index, "and lenalllines = ", lenalllines)
        if index >= lenalllines:
            print("NOT PASSED")
        elif index < lenalllines:
            print("#"*5, "PASSED", "#"*5)
            for n, line in enumerate(fileinput.input(directory+str(file), inplace=True), start=index):
                if len(line.split('|')) > items:
                    line = '|'.join(line.split('|')[:items])
                    print(line)
                else:
                    print(line)

            read_file = pd.read_table(directory+str(file), sep="|", names=labels, quoting=QUOTE_NONE)
            if not os.path.exists(os.path.join(directory, "excel/")):
                os.mkdir(os.path.join(directory, "excel/"))
            read_file.to_excel(directory+"excel/"+file[:-4]+".xlsx", index = None, header=False)