import pandas as pd
import os
import fileinput

items = 12
# thereisfaulty = None
# newline = None
for file in os.listdir("/home/dabooto/PycharmProjects/GoogleParser/backup"):
    if file.endswith(".csv"):
        f = open(file, 'r')
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



        print(file)
        print('data starts in line: '+ str(index))
        print('file has ' + str(lenalllines) + ' lines')
        if index < lenalllines:
            for n, line in enumerate(fileinput.input(file, inplace=True), start=index):
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
                    print(line)
            # if thereisfaulty == True:
            #     print(faultyline)
            #     print(newline)
            #     thereisfaulty = False

            read_file = pd.read_table(file, sep="|", names=labels)
            read_file.to_excel ("./excel/"+file[:-4]+".xlsx", index = None, header=False)
