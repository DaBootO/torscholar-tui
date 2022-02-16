# import os
import subprocess
import shlex
import sys
import random
import time
import os

def execute(cmd):
    process = subprocess.Popen(shlex.split(cmd, posix=False), shell=False, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
    lines = []
    # Poll process for new output until finished
    while True:
        nextline = process.stdout.readline()
        if nextline.decode() == '' and process.poll()  is not None:
            break

        lines.append(nextline.decode())
        sys.stdout.write(nextline.decode())
        sys.stdout.flush()

    output = process.communicate(timeout=0.2)[0]
    exitCode = process.returncode

    if (exitCode == 0):
        return lines
    else:
        raise subprocess.CalledProcessError(exitCode, command, output)

present_files = os.listdir()

# years = [[1946, 1950],
#          [1951, 1955],
#          [1956, 1960],
#          [1961, 1965],
#          [1966, 1970],
#          [1971, 1975],
#          [1976, 1980],
#          [1981, 1985],
#          [1986, 1990],
#          [1991, 1995],
#          [1996, 2000],
#          [2001, 2005],
#          [2006, 2010],
#          [2011, 2015],
#          [2016, 2020]]

years = [[2001, 2005]]

querys = [
    ["choice of", "welding process", "choice_of_welding_process"]
]

###################################
# select search type              #
# 1 = SEL OF OR FOR && choice of  #
# 2 = NORMAL                      #
###################################
search_type = 1

working_directory = os.getcwd()
print(working_directory)

if search_type == 1:
    ## SEL OF OR FOR
    commandtemplate = 'python3 -u ' + working_directory + '/torscholar.py -t --csv-header --no-patents \
    --after=%s --before=%s -p "%s" -A "%s"'
else:
    # ### REST
    commandtemplate = 'python3 -u ' + working_directory + '/torscholar.py -t --csv-header --no-patents \
    --after=%s --before=%s -p "%s"'

filetemplate = working_directory + '/%s_%s-%s.csv'
check_template = '%s_%s-%s.csv'


while len(querys) != 0:
    query = querys.pop()
    for year in years:

        if (check_template % (query[1], year[0], year[1])) in present_files:
            print(filetemplate % (query[1], year[0], year[1]), " already exists! continuing...")
            continue
        if search_type == 1:
            command = commandtemplate % (year[0], year[1], query[0], query[1])
        else:
            command = commandtemplate % (year[0], year[1], query[0])
        print(command)

        lines = execute(command)
        if search_type == 1:
            with open(filetemplate % (query[2], year[0], year[1]), 'w') as f:
                f.writelines(lines)
        else:
            with open(filetemplate % (query[1], year[0], year[1]), 'w') as f:
                f.writelines(lines)


        time.sleep(random.randint(1, 3))