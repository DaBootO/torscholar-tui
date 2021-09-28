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
        raise subprocess.CalledProcessError(exitCode, cmd)

present_files = os.listdir()

years = [[1946, 1950],
         [1951, 1955],
         [1956, 1960],
         [1961, 1965],
         [1966, 1970],
         [1971, 1975],
         [1976, 1980],
         [1981, 1985],
         [1986, 1990],
         [1991, 1995],
         [1996, 2000],
         [2001, 2005],
         [2006, 2010],
         [2011, 2015],
         [2016, 2020]]

# years = [[2016, 2020]]

# querys = [['"choice of"', "production process", "choice_of_production_process"],
#           ['"choice of"', "manufacturing process", "choice_of_manifacturing_process"],
#           ['"selection of,OR,selection for"', "production process", "sel_OF_OR_FOR_production_process"],
#           ['"selection of,OR,selection for"', "manufacturing process", "sel_OF_OR_FOR_manifacturing_process"]]

# querys = [['"selection of,OR,selection for"', "joining process", "sel_OF_OR_FOR_joining_process"],
#           ['"selection of,OR,selection for"', "welding process", "sel_OF_OR_FOR_welding_process"],
#           ['"selection of,OR,selection for"', "welding technology", "sel_OF_OR_FOR_welding_technology"],]


# querys = [["Auswahl des Werkstoff", "Auswahl_des_Werkstoff"],
#           ["Wahl des Material", "Wahl_des_Material"],
#           ["Wahl des Materials", "Wahl_des_Materials"],
#           ["Wahl des Werkstoff", "Wahl_des_Werkstoff"],
#           ["Wahl des Werkstoffs", "Wahl_des_Werkstoffs"],
#           ["joining method selection", "joining_method_selection"],
#           ["joining technology selection", "joining_technology_selection"],
#           ["welding technology selection", "welding_technology_selection"],
#           ["Auswahl von Fügetechniken", "Auswahl_von_Fügetechniken"],
#           ["Auswahl von Fügeprozessen", "Auswahl_von_Fügeprozessen"],
#           ["Auswahl der Fügetechnologie", "Auwahl_der_Fügetechnologie"],
#           ["Auswahl der Fügetechnik", "Auswahl_der_Fügetechnik"],
#           ["Auswahl des Fügeverfahren", "Auwahl_des_Fügeverfahren"],
#           ["Auswahl des Fügeverfahrens", "Auswahl_des_Fügeverfahrens"],
#           ["Auswahl des Fügeverfahren", "Auswahl_des_Fügeverfahren"],
#           ["Auswahl der Fügeprozesse", "Auswahl_der_Fügeprozesse"],
#           ["Auswahl des Fügeprozesses", "Auswahl_des_Fügeprozesses"],
#           ["Auswahl von Schweißprozessen", "Auswahl_von_Schweißprozessen"],
#           ["Auswahl der Schweißprozesse", "Auswahl_der_Schweißprozesse"],
#           ["Auswahl des Schweißprozesses", "Auswahl_des_Schweißprozesses"],
#           ["Auswahl des Schweißprozess", "Auswahl_des_Schweißprozess"],
#           ["Wahl von Fügetechniken", "Wahl_von_Fügetechniken"],
#           ["Wahl von Fügeprozessen", "Wahl_von_Fügeprozessen"],
#           ["Wahl der Fügetechnologie", "Wahl_der_Fügetechnologie"],
#           ["Wahl der Fügetechnik", "Wahl_der_Fügetechnik"],
#           ["Wahl des Fügeverfahren", "Wahl_des_Fügeverfahren"],
#           ["Wahl des Fügeverfahrens", "Wahl_des_Fügeverfahrens"],
#           ["Wahl des Fügeverfahren", "Wahl_des_Fügeverfahren"],
#           ["Wahl der Fügeprozesse", "Wahl_der_Fügeprozesse"],
#           ["Wahl des Fügeprozesses", "Wahl_des_Fügeprozesses"],
#           ["Wahl von Schweißprozessen", "Wahl_von_Schweißprozessen"],
#           ["Wahl der Schweißprozesse", "Wahl_der_Schweißprozesse"],
#           ["Wahl des Schweißprozesses", "Wahl_des_Schweißprozesses"],
#           ["Wahl des Schweißprozess", "Wahl_des_Schweißprozess"]]
# querys = [["Auswahl von Fertigungstechnologien", "Auswahl_von_Fertigungstechnologien"],
#            ["Auswahl von Fertigungsverfahren", "Auswahl_von_Fertigungsverfahren"],
#            ["Auswahl der Fertigungstechnologie", "Auswahl_der_Fertigungstechnologie"],
#            ["Auswahl der Fertigungstechnologien", "Auswahl_von_Fertigungstechnologien"],
#            ["Wahl der Fertigungstechnologie", "Wahl_der_Fertigungstechnologie"],
#            ["Wahl der Fertigungstechnologien", "Wahl_der_Fertigungstechnologien"],
#            ["Auswahl der Fertigungstechnik", "Auswahl_der_Fertigungstechnik"],
#            ["Auswahl der Fertigungstechniken", "Auswahl_der_Fertigungstechniken"],
#            ["Wahl der Fertigungstechnik", "Wahl_der_Fertigungstechnik"],
#            ["Wahl der Fertigungstechniken", "Wahl_der_Fertigungstechniken"],
#            ["Auswahl des Fertigungsverfahrens", "Auswahl_des_Fertigungsverfahrens"],
#            ["Wahl des Fertigungsverfahrens", "Wahl_des_Fertigungsverfahrens"],
#            ["Auswahl des Produktionsverfahrens", "Auswahl_des_Produktionsverfahrens"],
#            ["Wahl des Produktionsverfahrens", "Wahl_des_Produktionsverfahrens"]]


# querys = [["Auswahl des Werkstoffs", "Auswahl_des_Werkstoffs"],
#           ["Auswahl von Werkstoffen", "Auswahl_von_Werkstoffen"],
#           ["Werkstoffauswahl", "Werkstoffauswahl"],
#           ["Materialauswahl", "Materialauswahl"],
#           ["Auswahl von Materialien", "Auswahl_von_Materialien"],
#           ["Auswahl des Materials", "Auswahl_des_Materials"],
#           ["process selection", "process_selection"],
#           ["Auswahl von Fertigungsprozessen", "Auswahl_von_Fertigungsprozessen"],
#           ["Auswahl von Herstellungsprozess", "Auswahl_von_Herstellungsprozess"],
#           ["Auswahl von Herstellungsprozessen", "Auswahl_von_Herstellungsprozessen"],
#           ["Auswahl von Herstellprozess", "Auswahl_von_Herstellprozess"]]

# querys = [
#     ["choice of material", "choice_of_material"],
#     ["choice of materials", "choice_of_materials"],
#     ["materials selection", "materials_selection"],
#     ["selection of material", "selection_of_material"],
#     ["selection of materials", "selection_of_materials"],
#     ["Auswahl von Materialien", "Auswahl_von_Materialien"],
#     ["Auswahl von Werkstoffen", "Auswahl_von_Werkstoffen"],
#     ["Auswahl des Materials", "Auswahl_des_Materials"],
#     ["Wahl des Materials", "Wahl_des_Materials"],
#     ["Auswahl des Werkstoffs", "Auswahl_des_Werkstoffs"],
#     ["Wahl des Werkstoffs", "Wahl_des_Werkstoffs"],
#     ["Auswahl des Werkstoff", "Auswahl_des_Werkstoff"],
#     ["Wahl des Werkstoff", "Wahl_des_Werkstoff"],
#     ["Materialauswahl", "Materialauswahl"],
#     ["Werkstoffauswahl", "Werkstoffauswahl"],
#     ["choice of joining method", "choice_of_joining_method"],
#     ["choice of joining process", "choice_of_joining_process"],
#     ["choice of joining technology", "choice_of_joining_technology"],
#     ["joining selection", "joining_selection"],
#     ["joining method selection", "joining_method_selection"],
#     ["joining process selection", "joining_process_selection"],
#     ["joining technology selection", "joining_technology_selection"],
#     ["welding process selection", "welding_process_selection"],
#     ["Auswahl von Fügetechnologien", "Auswahl_von_Fügetechnologien"],
#     ["Auswahl von Fügeverfahren", "Auswahl_von_Fügeverfahren"],
#     ["choice of manufacturing process", "choice_of_manufacturing_process"],
#     ["choice of production process", "choice_of_production_process"],
#     ["process selection", "process_selection"],
#     ["Auswahl von Fertigungstechnologien", "Auswahl_von_Fertigungstechnologien"],
#     ["Auswahl von Fertigungsverfahren", "Auswahl_von_Fertigungsverfahren"],
#     ["Auswahl der Fertigungstechnologie", "Auswahl_der_Fertigungstechnologie"],
#     ["Wahl der Fertigungstechnologie", "Wahl_der_Fertigungstechnologie"],
#     ["Auswahl der Fertigungstechnik", "Auswahl_der_Fertigungstechnik"],
#     ["Wahl der Fertigungstechnik", "Wahl_der_Fertigungstechnik"],
#     ["Auswahl des Fertigungsverfahrens", "Auswahl_des_Fertigungsverfahrens"],
#     ["Wahl des Fertigungsverfahrens", "Wahl_des_Fertigungsverfahrens"]]

querys = [
    ["choice of", "welding process", "choice_of_welding_process"],
    ["choice of", "welding technology", "choice_of_welding_technology"]
]

###################################
# select search type              #
# 1 = SEL OF OR FOR && choice of  #
# 2 = NORMAL                      #
###################################
search_type = 1

if search_type == 1:
    ## SEL OF OR FOR
    commandtemplate = 'python3 -u torscholar.py -t --csv-header --no-patents --after=%s --before=%s -p "%s" -A "%s"'
else:
    # ### REST
    commandtemplate = 'python3 -u torscholar.py -t --csv-header --no-patents --after=%s --before=%s -p "%s"'

filetemplate = '%s_%s-%s.csv'
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