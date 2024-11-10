# internal imports
from sys import stderr, stdout
from src.torchecking import torchecker


# external imports
import time
import urwid
import subprocess
import codecs
import os
import shlex
import sys
import logging
import multiprocess as multiprocessing
import queue

def button(self, t, fn):
        w = urwid.Button(t, fn)
        w = urwid.AttrWrap(w, 'button normal', 'button select')
        return w

# RESEARCH_HEADER_ASCII = """ _____            _____                                _     
# |  __ \          / ____|                              | |    
# | |__) |   ___  | (___     ___    __ _   _ __    ___  | |__  
# |  _  /   / _ \  \___ \   / _ \  / _` | | '__|  / __| | '_ \ 
# | | \ \  |  __/  ____) | |  __/ | (_| | | |    | (__  | | | |
# |_|  \_\  \___| |_____/   \___|  \__,_| |_|     \___| |_| |_|
# © Dario Contrino, Jerome Kaspar
# """
RESEARCH_HEADER_ASCII = """   ____     __  __ _____   __   ______
  / __ \   / / / //_  _/  / /  /_   _/
 / / / /  / / / /  / /   / /    / /   
/ /_/ /  / /_/ / _/ /_  / /___ / /    
\___\_\ /_____/ /____/ /_____//_/     
© Dario Contrino, Jerome Kaspar
"""

HOW_TO_USE = """How to Use:
#1 Wähle die gewünschten Zeiträume aus (Enter oder Mausklick)
#2 Gebe die Queries ein
<<'phrase, words'>> -> "phrase" words
<<', words'>> -> words
#3 Starte den automatisierten Parser"""

connected_to_tor = torchecker.torCheck()

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
         [2016, 2020],
         [2021, 2025]]

logging.basicConfig(
    level=logging.DEBUG,
    format="%(asctime)-4s %(processName)s %(message)s", 
    datefmt="%H:%M:%S",
    filename='tory.log',
)

def update_time(stop_event, msg_queue):
    """send timestamp to queue every second"""
    logging.info('start')
    while not stop_event.wait(timeout=0.5):
        msg_queue.put( time.strftime('time %X') )
    logging.info('stop')

# class BoxButton(urwid.WidgetWrap):
#     """ Taken from https://stackoverflow.com/a/65871001/778272
#     """
#     def __init__(self, label, on_click):
#         self.label_widget = urwid.SelectableIcon("[ " + str(label) + " ]")
#         self.widget = urwid.Padding(self.label_widget)
#         self.hidden_button = urwid.Button('hidden button', on_click)
#         super(BoxButton, self).__init__(self.widget)

#     def selectable(self):
#         return True

#     def keypress(self, *args, **kwargs):
#         return self.hidden_button.keypress(*args, **kwargs)

#     def mouse_event(self, *args, **kwargs):
#         return self.hidden_button.mouse_event(*args, **kwargs)
    
#     def set_label(self, label):
#         return self.label_widget.set_text("[ " + str(label) + " ]")

class GraphView(urwid.WidgetWrap):
    """
    A class responsible for providing the application's interface and
    graph display.
    """

    palette = [
        ('normal_text', 'white', 'dark blue'),
        ('normal_bold_text', 'white', 'dark red', 'bold'),
        ('button_normal','light gray', 'light blue', 'standout'),
        ('button_select','white', 'light green', 'bold'),
        ('footer', 'white', 'dark red'),
        ('banner', 'black', 'light gray'),
        ('streak', 'black', 'dark red'),
        ('bg', 'black', 'dark blue'),
        ('progress_start', 'black', 'white'),
        ('progress_end', 'white', 'light green'),
        ('tor_correct', 'white', 'dark green'),
        ('tor_false', 'white', 'dark red')
    ]

### queue bekommt message rein von subprozess
### 

    def __init__(self, controller):
        self.loopie = urwid.MainLoop
        self.controller = controller
        self.started = True
        self.start_time = None
        self.offset = 0
        self.last_offset = None
        self.connected_to_tor = torchecker.torCheck()
        self.stdout = None
        self.stderr = None
        self.yearlist = None
        self.pipelines = []
        urwid.WidgetWrap.__init__(self, self.main_window())
        self.proc_pool = None
        self.current_proc_num = 0
        self.current_proc = None
        self.num_procs = None

    def check_process(self, loop, *_args):
        """add message to bottom of screen"""
        
        try:
            self.proc_pool[self.current_proc_num][0].join(timeout=0.1)
            if self.proc_pool[self.current_proc_num][0].is_alive() or self.proc_pool[self.current_proc_num][0].exitcode == None:
                loop.set_alarm_in(
                    sec=1.0,
                    callback=self.check_process,
                )
                return
            else:
                logging.info("Process #%s exited with exitcode %s" % (self.current_proc_num+1, self.proc_pool[self.current_proc_num][0].exitcode))
                # logging.info("Process #%s is of searchtype %s" % (self.current_proc_num+1, self.proc_pool[self.current_proc_num][1]))

                # self.csv_outputter(
                #     self.pipelines,
                #     self.proc_pool[self.current_proc_num][1],
                #     self.proc_pool[self.current_proc_num][2],
                #     self.proc_pool[self.current_proc_num][3]
                # )
                self.csv_outputter(
                    self.pipelines,
                    self.proc_pool[self.current_proc_num][1],
                    self.proc_pool[self.current_proc_num][2]
                )
                
                self.pg_bar.current = ((self.current_proc_num+1) * (self.pg_bar.done / float(self.num_procs)))
                
                self.clearLines()
                
                if self.current_proc_num+1 <= self.num_procs-1:
                    self.current_proc_num += 1
                    self.pool_handler(self.proc_pool)
                
        except queue.Empty:
            logging.info("queue.Empty encountered!")
            return
    
    def exit_on_q(self, key):
        if key in ('q', 'Q'):
            raise urwid.ExitMainLoop()

    def clearLines(self):
        self.pipelines = []
    
    def byte2str(self, data):
        try:
            text = codecs.decode(data, "UTF-8")
        except(TypeError):
            text = data
        except(UnicodeDecodeError):
            text = codecs.decode(data.encode(), "UTF-8")
        return text
    
    def addText2TextWidget(self, widget, updateText):
        widget.set_text(str(widget.text) + "\n" + self.byte2str(updateText))

    def saveLines(self, data):
        self.pipelines.append(data)
    
    def update_text(self, read_data):
        read_data = self.byte2str(read_data)
        self.saveLines(self.byte2str(read_data))
        if type(read_data) == bytes:
            if '|' in read_data:
                lines = read_data.split('\n')
                for l in lines:
                    if l.split('|')[0] != '':
                        self.addText2TextWidget(self.right_text_box, l.split('|')[0])
                        self.addText2TextWidget(self.right_text_box, '--')
            else:
                self.addText2TextWidget(self.right_text_box, read_data)
        else:
            self.addText2TextWidget(self.right_text_box, read_data)
    
    def csv_outputter(self, lines, query, year):
        if year != "gesamt":
            filetemplate = '%s_%s-%s.csv'
            logging.info("Outputting to .CSV as %s" % (filetemplate % (query[2], year[0], year[1])))
            with open(filetemplate % (query[2], year[0], year[1]), 'w') as f:
                f.writelines(lines)
        else:
            filetemplate = '%s_gesamt.csv'
            logging.info("Outputting to .CSV as %s" % (filetemplate % (query[2])))
            with open(filetemplate % (query[2]), 'w') as f:
                f.writelines(lines)
    
    def pool_handler(self, proc_pool):
        logging.info("Process number #%s currently running..." % (self.current_proc_num+1))
        proc = proc_pool[self.current_proc_num][0]
        proc.start()
        self.check_process(self.loopie, proc)
    
    def progger(self, proc):
        if proc.is_alive():
            self.loopie.set_alarm_in(
                sec=0.5,
                callback=self.progger
            )
        else:
            self.update_text("Process is stopped")
            
    
    def csv2excel_action(self, button):
        multiprocessing.Process(
            target=self.csv2excel_execute,
            args=[self.stdout, self.stderr],
            name="csv2excel"
        ).start()
        
    def csv2excel_execute(self, stdout_subproc=subprocess.PIPE, stderr_subproc=subprocess.STDOUT):
        this_dir = os.path.realpath(__file__)[:-len(os.path.basename(__file__))]
        process = subprocess.Popen(shlex.split(this_dir + "src/dataManip/csv2excel.sh", posix=False), shell=False, stdout=stdout_subproc, stderr=stdout_subproc)
        process.communicate()
    
    def comparator_action(self, button):
        multiprocessing.Process(
            target=self.comparator_execute,
            args=[self.stdout, self.stderr],
            name="comparator"
        ).start()
        
    def comparator_execute(self, stdout_subproc=subprocess.PIPE, stderr_subproc=subprocess.STDOUT):
        this_dir = os.path.realpath(__file__)[:-len(os.path.basename(__file__))]
        process = subprocess.Popen(shlex.split("python3 "+ this_dir + "src/dataManip/comparator.py", posix=False), shell=False, stdout=stdout_subproc, stderr=stdout_subproc)
        process.communicate()
    
    def merge_action(self, button):
        multiprocessing.Process(
            target=self.merge_execute,
            args=[self.stdout, self.stderr],
            name="merge"
        ).start()
        
    def merge_execute(self, stdout_subproc=subprocess.PIPE, stderr_subproc=subprocess.STDOUT):
        this_dir = os.path.realpath(__file__)[:-len(os.path.basename(__file__))]
        process = subprocess.Popen(shlex.split("python3 "+ this_dir + "src/dataManip/merger.py", posix=False), shell=False, stdout=stdout_subproc, stderr=stdout_subproc)
        process.communicate()
    
    def authoring_action(self, button):
        # self.csv2escel_execute(self.stdout, self.stderr)
        multiprocessing.Process(
            target=self.authoring_execute,
            args=[self.stdout, self.stderr],
            name="authoring"
        ).start()
        
    def authoring_execute(self, stdout_subproc=subprocess.PIPE, stderr_subproc=subprocess.STDOUT):
        this_dir = os.path.realpath(__file__)[:-len(os.path.basename(__file__))]
        process = subprocess.Popen(shlex.split(this_dir + "src/dataManip/authoring.sh", posix=False), shell=False, stdout=stdout_subproc, stderr=stdout_subproc)
        process.communicate()
    
    def execute(self, cmd, stdout_subproc=subprocess.PIPE, stderr_subproc=subprocess.STDOUT):
        
        process = subprocess.Popen(shlex.split(cmd, posix=False), shell=False, stdout=stdout_subproc, stderr=stdout_subproc)
        process.communicate()
        
    def automator(self, years=[], queries=[], stdout_external=subprocess.PIPE, stderr_external=subprocess.STDOUT):
        
        proc_pool = []
        
        if years == [] or queries == []:
            print("Input years and queries!")
            sys.exit(1)
        
        automator_dir = os.path.realpath(__file__)[:-len(os.path.basename(__file__))]
        
        while len(queries) != 0:
            query = queries.pop()
            # if not isinstance(query, list):
            #     query = [q.strip() for q in query.split('"') if q !='']
            
            commandtemplate = 'python3 -u ' + automator_dir + 'src/parser/torscholar.py -t --csv-header --no-patents '
            year_arg = '--after=%s --before=%s'
    
            if len(query) != 3:
                print("ERROR with format! Input has to be 'PHRASE,WORDS' in template file!")
                print("The query you gave was:")
                print(query)
                continue
            
            # if  query[0] != '':
            #     if query[0] == "selOFORFOR":
            #         phrasepart = "'selection of' OR 'selection for'"
            #     else:
            #         phrasepart = query[0]
            #     phrase = ' -p "' +  phrasepart + '"'
            #     # phrase = " -p '" +  phrasepart + "'"
            # else:
            #     phrase = ''
            if  query[0] != '':
                phrase = ' -p "' +  query[0] + '"'
            else:
                phrase = ''
            if query[1] != '':
                words = ' -A "' + query[1] + '"'
            else:
                words = ''
            
            if not isinstance(query, list):
                query = [q.strip() for q in query.split('"') if q !='']
            
            # if "choice of" in query or "selOFORFOR" in query:
            #     search_type = 1
            #     if not isinstance(query, list):
            #         query.append((query[0]+' '+query[1]).replace(' ', '_'))
            #     ## SEL OF OR FOR
            #     commandtemplate = 'python3 -u ' + automator_dir + 'src/parser/torscholar.py -t --csv-header --no-patents --after=%s --before=%s -p "%s" -A "%s"'
            # else:
            #     search_type = 2
            #     if not isinstance(query, list):
            #         query.append((query[0]).replace(' ', '_'))
            #     ### REST
            #     commandtemplate = 'python3 -u ' + automator_dir + 'src/parser/torscholar.py -t --csv-header --no-patents --after=%s --before=%s -p "%s"'
            cmd = commandtemplate + phrase + words
            
            for year in years:
                # if search_type == 1:
                #     command = commandtemplate % (year[0], year[1], query[0], query[1])
                # else:
                #     command = commandtemplate % (year[0], year[1], query[0])
                
                if year != "gesamt":
                    command = (cmd + year_arg) % (year[0], year[1])
                else:
                    command = cmd
                
                proc = multiprocessing.Process(
                    target=self.execute,
                    args=[command, stdout_external, stderr_external],
                    name=command
                )
                
                # proc_pool.append([proc, search_type, query, year])
                proc_pool.append([proc, query, year])
                
        return proc_pool
    
    def call_the_automator(self):
        self.years = []
        for cb in self.yearlist:
            if cb.label == "gesamt" and cb.state == True:
                self.years = ["gesamt"]
                break
            if cb.state == True:
                self.years.append(cb.get_label().split('-'))
        
        self.queries = []
        query_all_text = self.query_box.text
        query_lines = query_all_text.split('\n')
        
        # for l in query_lines:
        #     query_text = l.split(',')
        #     query_text = [t.strip() for t in query_text]
        #     self.queries.append(query_text)
        
        for test in query_lines:
            if ',' not in test:
                self.update_text("ERROR in query: %s" % test)
                self.update_text("There needs to be a comma to seperate PHRASE from WORDS!")
                return
        
        q = [line.split(',') for line in query_lines]

        qry = []
        for querylist in q:
            tmp = []
            for query in querylist:
                tmp.append(query.strip())
            qry.append(tmp)

        for q in qry:
            if '' in q:
                filename = ''.join(q)
                q.append(filename.replace(' ', '_'))
            else:
                filename = '_'.join(q)
                q.append(filename.replace(' ', '_'))
            self.queries.append(q)
        
        proc_pool = self.automator(years=self.years, queries=self.queries, stdout_external=self.stdout, stderr_external=self.stderr)
        self.num_procs = len(proc_pool)
        
        self.update_text("There are %s process(es) waiting..." % self.num_procs)
        
        self.proc_pool = proc_pool
        self.pool_handler(proc_pool)
    
    def on_animate_button(self, button):
        """Toggle started state and button text."""
        
        if self.started: # stop animation
            # self.update_text(str(self.pipelines))
            button.set_label("Start")
            self.started = False
        else: # start animation
            if not self.connected_to_tor:
                self.started = False
                self.update_text("YOU ARE NOT CONNECTED TO TOR!")
                self.update_text("Connect to tor first!")
                self.update_text("run 'sudo service tor start'")
                return
            else:
                button.set_label("Stop")
                self.started = True
                pipe = self.call_the_automator()
    
    def checkbox(self, lbl):
        w = urwid.CheckBox(lbl)
        return w
    
    def progress_bar(self, smooth=False):
        if smooth:
            return urwid.ProgressBar('pg normal', 'pg complete',
                0, 1, 'pg smooth')
        else:
            return urwid.ProgressBar('pg normal', 'pg complete',
                0, 1)
    
    def exit_program(self, w):
        raise urwid.ExitMainLoop()
    
    def main_window(self):
        footer = urwid.AttrMap(urwid.Text(u'Press [q] / [Q] to exit...', align='center'), 'footer')
        if self.connected_to_tor:
            header = urwid.AttrMap(urwid.Text(u'You are connected to the tor network', align='center'), 'tor_correct')
        else:
            header = urwid.AttrMap(urwid.Text(u'You are !NOT! connected to the tor network! Pls fix!', align='center'), 'tor_false')

        txt_box_howto = urwid.Text((HOW_TO_USE), align='left')
        txt_box_research = urwid.Text((u''+RESEARCH_HEADER_ASCII), align='right')
        top_linebox = urwid.Columns([('weight', 1, txt_box_howto), ('weight', 2, txt_box_research)])
        top = urwid.Filler(top_linebox)
        
        left_txt = urwid.Text(('banner', u'Zeitfenster'), align='center')
        left_fill = urwid.BoxAdapter(urwid.Filler(left_txt, valign='top'), height=1)
        div1 = urwid.Divider()

        self.checkboxlist = []
        self.checkboxlist.append(urwid.CheckBox("gesamt"))
        for year in years:
            text = str(year[0])+'-'+str(year[1])
            self.checkboxlist.append(urwid.CheckBox(text))
        self.yearlist = self.checkboxlist

        checkbox_walker = urwid.SimpleFocusListWalker([left_fill, div1] + self.checkboxlist)
        left_side = urwid.LineBox(urwid.ListBox(checkbox_walker))

        mid_txt = urwid.Text(('banner', u'Query Eingabe'), align='center')
        mid_fill = urwid.BoxAdapter(urwid.Filler(mid_txt, valign='top'), height=1)
        div2 = urwid.Divider()

        self.query_box = urwid.Edit(multiline=True)

        middle_walker = urwid.SimpleFocusListWalker([mid_fill, div2, self.query_box])
        middle_box = urwid.LineBox(urwid.ListBox(middle_walker))
        
        self.right_txt = urwid.Text(('banner', u'Outputfeld Subprozesse'), align='center')
        self.right_text_box = urwid.Text(u'')
        self.right_walker = urwid.SimpleFocusListWalker([self.right_txt, self.right_text_box])
        self.right_side = urwid.LineBox(urwid.ListBox(self.right_walker))

        self.butty = urwid.Button(u"Start", self.on_animate_button)
        self.on_animate_button(self.butty)
        self.butty_attr = urwid.AttrMap(self.butty, "button_normal", focus_map="button_select")
        self.butty_csv2excel = urwid.Button(u"csv2excel", on_press=self.csv2excel_action)
        self.butty_csv2excel_attr = urwid.AttrMap(self.butty_csv2excel, "button_normal", focus_map="button_select")
        self.butty_comparator = urwid.Button(u"comparator", on_press=self.comparator_action)
        self.butty_comparator_attr = urwid.AttrMap(self.butty_comparator, "button_normal", focus_map="button_select")
        self.butty_merge = urwid.Button(u"merger", on_press=self.merge_action)
        self.butty_merge_attr = urwid.AttrMap(self.butty_merge, "button_normal", focus_map="button_select")
        self.butty_authoring = urwid.Button(u"authoring", on_press=self.authoring_action)
        self.butty_authoring_attr = urwid.AttrMap(self.butty_authoring, "button_normal", focus_map="button_select")
        self.arrow_text = urwid.Text(u'  ➤➤➤  ', align='center')
        self.button_bar = urwid.LineBox(urwid.Filler(urwid.Columns([('weight', 1, self.butty_attr),
                                                                    ('weight', 1, self.arrow_text),
                                                                    ('weight', 1, self.butty_csv2excel_attr),
                                                                    ('weight', 1, self.arrow_text),
                                                                    ('weight', 1, self.butty_comparator_attr),
                                                                    ('weight', 1, self.arrow_text),
                                                                    ('weight', 1, self.butty_merge_attr),
                                                                    ('weight', 1, self.arrow_text),
                                                                    ('weight', 1, self.butty_authoring_attr)]),
                                                    valign='middle'))
        mid = urwid.Columns([('weight', 1, left_side), ('weight', 2, middle_box), ('weight', 3, self.right_side)])

        self.pg_bar = urwid.ProgressBar('progress_start', 'progress_end')
        bottom = urwid.LineBox(urwid.Filler(self.pg_bar))
        


        # simple_walk = urwid.SimpleFocusListWalker([('weight', 2, top), ('weight', 5, mid), ('weight', 1, bottom)])
        simple_walk = urwid.SimpleFocusListWalker([('weight', 2, top), ('weight', 6, mid), ('weight', 1, self.button_bar), ('weight', 1, bottom)])
        pile = urwid.Pile(simple_walk)

        self.main_frame = urwid.Frame(pile)
        self.main_frame.set_footer(footer)
        self.main_frame.set_header(header)
        
        return self.main_frame
        
class GraphController:
    """
    A class responsible for setting up the model and view and running
    the application.
    """
    def __init__(self):
        self.view = GraphView( self )

    def main(self):
        screen = urwid.raw_display.Screen()
        self.loop = urwid.MainLoop(self.view, self.view.palette, unhandled_input=self.view.exit_on_q, screen=screen)
        stdout = self.loop.watch_pipe(self.view.update_text)
        stderr = self.loop.watch_pipe(self.view.saveLines)
        self.view.stdout = stdout
        self.view.stderr = stderr
        self.view.loopie = self.loop
        self.loop.run()


def main():
    GraphController().main()

if '__main__'==__name__:
    main()
