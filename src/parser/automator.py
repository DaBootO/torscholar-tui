import subprocess
import shlex
import sys
import random
import time
import os
import asyncio
import pdb
def execute(cmd, stdout_subproc=subprocess.PIPE, stderr_subproc=subprocess.STDOUT):
    process = subprocess.Popen(shlex.split(cmd, posix=False), shell=False, stdout=stdout_subproc, stderr=stderr_subproc)
    # process = subprocess.Popen('for i in $(seq 50); do echo -n "$i "; sleep 0.005; done', shell=True, stdout=stdout_subproc, stderr=stderr_subproc)
    # lines = []
    # Poll process for new output until finished
    # while True:
        
    #     # nextline = process.stdout.readline()
    #     if process.poll()  is not None:
    #         break
        # print(fcntl.fcntl(stdout_subproc, fcntl.F_GETFL))
        
        # lines.append(nextline.decode())
        # sys.stdout.write()
        # os.fdopen(stdout_subproc, 'w')
        # sys.stdout.flush()
        # # print(type(stdout_subproc))
        # os.write(stdout_subproc, b'')

    # output = process.communicate()[0]
    # output = process.communicate(timeout=0.2)[0]
    # while True:
    #     if process.poll() is not None:
    #         break
    exitCode = process.returncode
    
    if (exitCode == 0):
        return
        # return lines
    else:
        raise subprocess.CalledProcessError(exitCode, cmd)

def main(years=[], queries=[], stdout_external=subprocess.PIPE, stderr_external=subprocess.STDOUT):
    queries = [
    ["choice of", "welding process", "choice_of_welding_process"]
    ]
    
    if years == [] or queries == []:
        print("Input years and queries!")
        sys.exit(1)
    
    
    present_files = os.listdir()
    automator_dir = os.path.realpath(__file__)[:-len(os.path.basename(__file__))]
    filetemplate = '%s_%s-%s.csv'
    check_template = '%s_%s-%s.csv'
    
    while len(queries) != 0:
        query = queries.pop()
        if not isinstance(query, list):
            query = [q.strip() for q in query.split('"') if q !='']
        if "choice of" in query or "selOFORFOR" in query:
            search_type = 1
            if not isinstance(query, list):
                query.append((query[0]+' '+query[1]).replace(' ', '_'))
            ## SEL OF OR FOR
            commandtemplate = 'python3 -u ' + automator_dir + 'torscholar.py -t --csv-header --no-patents --after=%s --before=%s -p "%s" -A "%s"'
        else:
            search_type = 2
            if not isinstance(query, list):
                query.append((query[0]).replace(' ', '_'))
            ### REST
            commandtemplate = 'python3 -u ' + automator_dir + 'torscholar.py -t --csv-header --no-patents --after=%s --before=%s -p "%s"'
                
        for year in years:
            # if (check_template % (query[1], year[0], year[1])) in present_files:
            #     print(filetemplate % (query[1], year[0], year[1]), " already exists! continuing...")
            #     continue
            if search_type == 1:
                command = commandtemplate % (year[0], year[1], query[0], query[1])
            else:
                command = commandtemplate % (year[0], year[1], query[0])
            # print(command)
            
            # lines = execute(command)
            # pdb.set_trace()
            lines = execute(command, stdout_subproc=stdout_external, stderr_subproc=stderr_external)
            return lines
            # if search_type == 1:
            #     with open(filetemplate % (query[2], year[0], year[1]), 'w') as f:
            #         f.writelines(lines)
            # else:
            #     with open(filetemplate % (query[1], year[0], year[1]), 'w') as f:
            #         f.writelines(lines)


            # time.sleep(random.randint(1, 3))
if __name__ == '__main__':
    main()