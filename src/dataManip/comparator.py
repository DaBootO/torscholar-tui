import time
import openpyxl
import os
import string
import re
from rich import print as rprint
import shutil

def dim2list(ws):
    dims = ws.dimensions.split(':')
    for i in range(len(dims)):
        dims[i] = int(re.findall('\d+', dims[i])[0])
    return dims

items = 12

letters = string.ascii_uppercase

directory = os.path.abspath(os.path.realpath(__file__)[:-len(os.path.basename(__file__))] + "../../") + '/'
directory_data = os.path.join(directory, "comparison/")
# saveto = os.path.join(directory, "data/", "output/")
# data = [] # [[name, yearlow, yearhigh, positives]]

dirs = os.listdir(directory_data)
dirs = [dir for dir in dirs if os.path.isdir(os.path.join(directory_data, dir))]

files_dict = {}
for dir in dirs:
    filelist = os.listdir(os.path.join(directory_data, dir))
    files_dict[dir] = filelist

differences = 0
file_diffs = []
for dir in files_dict.keys():
    for dir_check in files_dict.keys():
        if dir == dir_check:
            continue
        for file in files_dict[dir]:
            if file not in files_dict[dir_check]:
                differences += 1
                file_diffs.append("%s is in %s but not in %s" % (file, dir, dir_check))

if differences != 0:
    print("There are some files which are not in all directories!")
    for diff in file_diffs:
        print(diff)
else:
    print("The files in all directories overlap fully!")

title_dict = {}

full_data = {}

for dir in dirs:
    title_dict[dir] = {}
    full_data[dir] = {}
    for file in os.listdir(os.path.join(directory_data, dir)):
        if file.endswith(".xlsx"):
            full_data[dir][file] = {}
            title_dict[dir][file] = []
            print("parsing titles of %s in %s" % (file, dir))
            wb = openpyxl.load_workbook(filename=os.path.join(directory_data, dir, file))
            ws = wb.active
            dims = dim2list(ws)
            index = 1
            
            while ws['C'+str(index)].value != "title":
                index += 1
            index += 1
            while index <= dims[1]:
                article = ws['C'+str(index)].value
                title_dict[dir][file].append(article)
                data = []
                for i in range(items):
                    data.append(ws[letters[i]+str(index)].value)
                full_data[dir][file][article] = data
                index += 1

already_parsed = []
for dir in title_dict.keys():
    for dir_check in title_dict.keys():
        if dir == dir_check:
            continue
        for file in title_dict[dir].keys():
            outputs = []
            title_diffs = []
            if file in title_dict[dir_check].keys():
                for title in title_dict[dir][file]:
                    if title not in title_dict[dir_check][file]:
                        if full_data[dir][file][title] not in already_parsed:
                            already_parsed.append(full_data[dir][file][title])
                        else:
                            print("We already parsed %s! skipping..." % title)
                        outputs.append(full_data[dir][file][title])
                        title_diffs.append(title)
            else:
                print("%s exists in %s but not in %s" % (file, dir, dir_check))
                if not os.path.isdir(os.path.join(directory, "unique")):
                    os.mkdir(os.path.join(directory, "unique"))
                file_src = os.path.join(directory_data, dir, file)
                file_out = os.path.join(directory, "unique", file)
                shutil.copy(file_src, file_out)
                continue
            if len(title_diffs) > 0:
                print("There are %i differences in titles for %s in %s and %s" % (len(title_diffs), file, dir, dir_check))
                
                out_excel = openpyxl.Workbook()
                out_ws = out_excel.active
                
                row = 1
                labels = [
                "title",
                "author",
                "url",
                "year",
                "num_citations",
                "num_versions",
                "cluster_id",
                "url_pdf",
                "url_citations",
                "url_versions",
                "url_citation",
                "excerpt"]

                for lbl in range(len(labels)):
                    out_ws[letters[lbl+2]+str(row)] = labels[lbl]
                row += 1
                for i in outputs:
                    for j in range(items):
                        out_ws[letters[j]+str(row)] = i[j]
                    row += 1
                out_ws.column_dimensions['C'].width = 100.0
                out_ws.column_dimensions['D'].width = 100.0
                if not os.path.isdir(os.path.join(directory, "diffs")):
                    os.mkdir(os.path.join(directory, "diffs"))
                out_excel.save(os.path.join(os.path.join(directory, "diffs", "DIFFS"+file)))
            else:
                print("There are no differences in titles for %s in %s and %s" % (file, dir, dir_check))
                if not os.path.isdir(os.path.join(directory, "similar")):
                    os.mkdir(os.path.join(directory, "similar"))
                file_src = os.path.join(directory_data, dir, file)
                file_out = os.path.join(directory, "similar", file)
                shutil.copy(file_src, file_out)