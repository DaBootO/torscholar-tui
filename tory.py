# internal imports
from sys import stderr, stdout
from types import coroutine
from src.torchecking import torchecker
from src.parser import automator


# external imports
import time
import urwid
import subprocess
import codecs
import os
import shlex
import sys
import asyncio
import pdb

def button(self, t, fn):
        w = urwid.Button(t, fn)
        w = urwid.AttrWrap(w, 'button normal', 'button select')
        return w

RESEARCH_HEADER_ASCII = """ _____            _____                                _     
|  __ \          / ____|                              | |    
| |__) |   ___  | (___     ___    __ _   _ __    ___  | |__  
|  _  /   / _ \  \___ \   / _ \  / _` | | '__|  / __| | '_ \ 
| | \ \  |  __/  ____) | |  __/ | (_| | | |    | (__  | | | |
|_|  \_\  \___| |_____/   \___|  \__,_| |_|     \___| |_| |_|
"""

HOW_TO_USE = """How to use:
#1 wähle die gewünschten Zeiträume aus (Enter)
#2 gebe die Queries ein (für Format siehe Readme)
#3 starte den automatisierten Parser"""

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
         [2016, 2020]]

class GraphView(urwid.WidgetWrap):
    """
    A class responsible for providing the application's interface and
    graph display.
    """

    palette = [
        ('normal_text', 'white', 'dark blue'),
        ('normal_bold_text', 'white', 'dark red', 'bold'),
        ('button normal','light gray', 'dark blue', 'standout'),
        ('button select','white', 'dark green'),
        ('footer', 'white', 'dark red'),
        ('banner', 'black', 'light gray'),
        ('streak', 'black', 'dark red'),
        ('bg', 'black', 'dark blue'),
        ('progress_start', 'black', 'white'),
        ('progress_end', 'white', 'dark gray'),
        ('tor_correct', 'white', 'dark green'),
        ('tor_false', 'white', 'dark red')
    ]

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

    def exit_on_q(self, key):
        if key in ('q', 'Q'):
            raise urwid.ExitMainLoop()

    def saveLines(self, data):
        self.pipelines.append(data)
    
    def addText2TextWidget(self, widget, updateText):
        try:
            widget.set_text(str(widget.text) + "\n" + codecs.decode(updateText, "UTF-8"))
        except(TypeError):
            widget.set_text(str(widget.text) + "\n" + updateText)

    def update_text(self, read_data):
        self.addText2TextWidget(self.right_text_box, read_data)
        # self.saveLines(read_data)

    def execute(self, cmd, stdout_subproc=subprocess.PIPE, stderr_subproc=subprocess.STDOUT):
        process = subprocess.Popen(shlex.split(cmd, posix=False), shell=False, stdout=stdout_subproc, stderr=stderr_subproc)
        while process.poll() is None:
            # self.main_window().sizing()
            size = self.loopie.screen.get_cols_rows()
            self.loopie.screen.draw_screen(size, self.main_frame.render(size))
        
        # output = process.communicate()[0]
        # self.loopie.draw_screen()
        # output = process.communicate(timeout=1.0)[0]
        # while True:
        #     if process.poll() is not None:
        #         break
        exitCode = process.returncode
        
        if (exitCode == 0):
            return
            # return lines
        else:
            raise subprocess.CalledProcessError(exitCode, cmd)
        
    def automator(self, years=[], queries=[], stdout_external=subprocess.PIPE, stderr_external=subprocess.STDOUT):
        queries = [
        ["choice of", "welding process", "choice_of_welding_process"],
        ["choice of", "weldinglingidasndiasdj process", "choice_of_welding_process"]
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
                commandtemplate = 'python3 -u ' + automator_dir + 'src/parser/torscholar.py -t --csv-header --no-patents --after=%s --before=%s -p "%s" -A "%s"'
            else:
                search_type = 2
                if not isinstance(query, list):
                    query.append((query[0]).replace(' ', '_'))
                ### REST
                commandtemplate = 'python3 -u ' + automator_dir + 'src/parser/torscholar.py -t --csv-header --no-patents --after=%s --before=%s -p "%s"'
                    
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
                lines = self.execute(command, stdout_subproc=stdout_external, stderr_subproc=stderr_external)
                # if search_type == 1:
                #     with open(filetemplate % (query[2], year[0], year[1]), 'w') as f:
                #         f.writelines(lines)
                # else:
                #     with open(filetemplate % (query[1], year[0], year[1]), 'w') as f:
                #         f.writelines(lines)


                # time.sleep(random.randint(1, 3))
    
    def call_the_automator(self):
        self.years = []
        for cb in self.yearlist:
            if cb.state == True:
                self.years.append(cb.get_label().split('-'))
        # pipe = automator.main(years=self.years, stdout_external=self.stdout, stderr_external=self.stderr)
        pipe = self.automator(years=self.years, stdout_external=self.stdout, stderr_external=self.stderr)

    def on_animate_button(self, button):
        """Toggle started state and button text."""
        if self.started: # stop animation
            button.set_label("Start")
            self.started = False
        else:
            if not self.connected_to_tor:
                self.started = False
                self.update_text("Connect to tor first!")
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
        for year in years:
            text = str(year[0])+'-'+str(year[1])
            self.checkboxlist.append(urwid.CheckBox(text))
        self.yearlist = self.checkboxlist

        checkbox_walker = urwid.SimpleFocusListWalker([left_fill, div1] + self.checkboxlist)
        left_side = urwid.LineBox(urwid.ListBox(checkbox_walker))

        mid_txt = urwid.Text(('banner', u'Queries eingeben'), align='center')
        mid_fill = urwid.BoxAdapter(urwid.Filler(mid_txt, valign='top'), height=1)
        div2 = urwid.Divider()

        self.query_box = urwid.Edit(multiline=True)

        middle_walker = urwid.SimpleFocusListWalker([mid_fill, div2, self.query_box])
        middle_box = urwid.LineBox(urwid.ListBox(middle_walker))
        
        self.right_txt = urwid.Text(('banner', u'Outputfeld Subprozesse'), align='center')
        self.right_text_box = urwid.Text(u'')
        self.butty = urwid.Button(u"Start", on_press=self.on_animate_button)
        self.on_animate_button(self.butty)
        self.butty_padding = urwid.Padding(self.butty, align='center')
        self.right_walker = urwid.SimpleFocusListWalker([self.butty_padding, self.right_txt, self.right_text_box])
        self.right_side = urwid.LineBox(urwid.ListBox(self.right_walker))

        mid = urwid.Columns([('weight', 1, left_side), ('weight', 2, middle_box), ('weight', 3, self.right_side)])

        pg_bar = urwid.ProgressBar('progress_start', 'progress_end')
        bottom = urwid.LineBox(urwid.Filler(pg_bar))


        simple_walk = urwid.SimpleFocusListWalker([('weight', 2, top), ('weight', 5, mid), ('weight', 1, bottom)])
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
        # self.aloop = asyncio.get_event_loop()
        # ev_loop = urwid.AsyncioEventLoop(loop=self.aloop)
        # self.loop = urwid.MainLoop(self.view, self.view.palette, unhandled_input=self.view.exit_on_q, event_loop=ev_loop)
        screen = urwid.raw_display.Screen()
        self.loop = urwid.MainLoop(self.view, self.view.palette, unhandled_input=self.view.exit_on_q, screen=screen)
        stdout = self.loop.watch_pipe(self.view.update_text)
        stderr = self.loop.watch_pipe(self.view.update_text)
        self.view.stdout = stdout
        self.view.stderr = stderr
        self.view.loopie = self.loop
        self.loop.run()


def main():
    GraphController().main()

if '__main__'==__name__:
    main()