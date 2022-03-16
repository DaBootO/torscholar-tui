from csv import QUOTE_NONE
import pandas as pd
import os
import fileinput

items = 12
# thereisfaulty = None
# newline = None
# directory = "/home/dabooto/PycharmProjects/GoogleParser/SendToShared/"
directory = os.path.realpath(__file__)[:-len(os.path.basename(__file__))]
# print(directory)
for file in os.listdir(directory):
    # print(directory+str(file))
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



        # print(file)
        # print('data starts in line: '+ str(index))
        # print('file has ' + str(lenalllines) + ' lines')
        print(file, "has index =", index, "and lenalllines = ", lenalllines)
        if index >= lenalllines:
            print("\033[93m", "NOT PASSED", "\033[0m")
        if index < lenalllines:
            print("#"*5, "PASSED", "#"*5)
            for n, line in enumerate(fileinput.input(directory+str(file), inplace=True), start=index):
                if len(line.split('|')) > items:
                    line = '|'.join(line.split('|')[:items])
                    # thereisfaulty = True
                    # faultyline = line
                    # string = line
                    # char = "|"
                    #
                    # string2 = ''
                    # length = len(string)
                    #
                    # for i in range(length):
                    #     if (string[i] == char):
                    #         string2 = string[0:i] + string[i + 1:length]
                    # print(string2)
                    # newline = string2
                    print(line)
                else:
                    if line != '':
                        print(line)
            # if thereisfaulty == True:
            #     print(faultyline)
            #     print(newline)
            #     thereisfaulty = False

            read_file = pd.read_table(directory+str(file), sep="|", names=labels, quoting=QUOTE_NONE)
            if not os.path.exists(os.path.join(directory, "excel/")):
                os.mkdir(os.path.join(directory, "excel/"))
            read_file.to_excel(directory+"excel/"+file[:-4]+".xlsx", index = None, header=False)
