import glob

csv_list = glob.glob("/home/dabooto/PycharmProjects/GoogleParser/*.csv")

for filename in csv_list:
    with open(filename, 'r') as file:
        lines = file.readlines()
        for line in range(len(lines)-2):
            if lines[line] == lines[line+2]:
                print(filename, "was soft-blocked on GS! RETRY!")
                break