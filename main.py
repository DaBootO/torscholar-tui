# internal imports
from sys import stderr, stdout
from GoogleParser.scholar import Error
from src.torchecking import torchecker
from src.parser import automator


# external imports
import urwid
import subprocess
import codecs

def button(self, t, fn):
        w = urwid.Button(t, fn)
        w = urwid.AttrWrap(w, 'button normal', 'button select')
        return w



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
        self.controller = controller
        self.started = True
        self.start_time = None
        self.offset = 0
        self.last_offset = None
        self.connected_to_tor = torchecker.torCheck()
        self.stdout = None
        self.stderr = None
        urwid.WidgetWrap.__init__(self, self.main_window())

    def exit_on_q(self, key):
        if key in ('q', 'Q'):
            raise urwid.ExitMainLoop()

    def addText2TextWidget(self, widget, updateText):
        try:
            widget.set_text(str(widget.text) + "\n" + codecs.decode(updateText, "UTF-8"))
        except(TypeError):
            widget.set_text(str(widget.text) + "\n" + updateText)
        
            

    def update_text(self, read_data):
        self.addText2TextWidget(self.right_text_box, read_data)

    def call_the_automator(self):
        self.years = []
        for cb in self.checkboxlist:
            if cb.get_state() == True:
                self.years.append(cb.get_label().split('-'))
        self.query_texts = [q.strip() for q in self.query_box.get_text()[0].split('\n') if q.strip() != '']
        # self.addText2TextWidget(self.right_text_box, str(self.stdout))
        # print('!'*100)
        # print(self.stdout)
        # print('!'*100)
        automator.main(self.query_texts, self.years, self.stdout, self.stderr)
        


    def on_animate_button(self, button):
        """Toggle started state and button text."""
        if self.started: # stop animation
            button.set_label("Start")
            self.started = False
        else:
            button.set_label("Stop")
            self.started = True
            self.call_the_automator()
        
        # self.addText2TextWidget(self.right_text_box, u"test"+str(self.started))

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

        txt_box_upper = urwid.Text(('banner', u'Benutzung: blab bla'), align='center')
        filler_top = urwid.Filler(txt_box_upper)
        top = urwid.LineBox(urwid.Columns([filler_top]))

        left_txt = urwid.Text(('banner', u'Zeitfenster eingeben'), align='center')
        left_fill = urwid.BoxAdapter(urwid.Filler(left_txt, valign='top'), height=1)
        div1 = urwid.Divider()

        self.checkboxlist = []
        for year in years:
            text = str(year[0])+'-'+str(year[1])
            self.checkboxlist.append(urwid.CheckBox(text))

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
        self.butty_padding = urwid.Padding(self.butty, align='center', width='pack')
        self.right_walker = urwid.SimpleFocusListWalker([self.butty_padding, self.right_txt, self.right_text_box])
        self.right_side = urwid.LineBox(urwid.ListBox(self.right_walker))


        mid = urwid.Columns([('weight', 1, left_side), ('weight', 2, middle_box), ('weight', 3, self.right_side)])



        pg_bar = urwid.ProgressBar('progress_start', 'progress_end')
        bottom = urwid.LineBox(urwid.Filler(pg_bar))


        simple_walk = urwid.SimpleFocusListWalker([('weight', 1, top), ('weight', 5, mid), ('weight', 1, bottom)])
        pile = urwid.Pile(simple_walk)

        main_frame = urwid.Frame(pile)
        main_frame.set_footer(footer)
        main_frame.set_header(header)

        return main_frame

class GraphController:
    """
    A class responsible for setting up the model and view and running
    the application.
    """
    def __init__(self):
        self.view = GraphView( self )

    def main(self):
        self.loop = urwid.MainLoop(self.view, self.view.palette, unhandled_input=self.view.exit_on_q)
        self.stdout = self.loop.watch_pipe(self.view.update_text)
        self.stderr = self.loop.watch_pipe(self.view.update_text)
        self.view.stdout = self.stdout
        self.view.stderr = self.stderr
        self.loop.run()


def main():
    GraphController().main()

if '__main__'==__name__:
    main()