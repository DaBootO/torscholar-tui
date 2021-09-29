# internal imports
from src.torchecking import torchecker


# external imports
import urwid


def exit_on_q(key):
    if key in ('q', 'Q'):
        raise urwid.ExitMainLoop()

def button(self, t, fn):
        w = urwid.Button(t, fn)
        w = urwid.AttrWrap(w, 'button normal', 'button select')
        return w

def addText2TextWidget(widget, updateText):
    widget.set_text(widget.text + "\n" + updateText)

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
        urwid.WidgetWrap.__init__(self, self.main_window())

    def on_animate_button(self, button):
        """Toggle started state and button text."""
        if self.started: # stop animation
            button.set_label("Start")
            self.offset = self.get_offset_now()
            self.started = False
            self.controller.stop_animation()
        else:
            button.set_label("Stop")
            self.started = True
            self.start_time = time.time()
            self.controller.animate_graph()

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

    def graph_controls(self):
        l = [urwid.Text("Mode",align="center"),
            ] + self.mode_buttons + [
            urwid.Divider(),
            urwid.Text("Animation",align="center"),
            animate_controls,
            self.animate_progress_wrap,
            urwid.Divider(),
            urwid.LineBox( unicode_checkbox ),
            urwid.Divider(),
            self.button("Quit", self.exit_program ),
            ]
        w = urwid.ListBox(urwid.SimpleListWalker(l))
        return w

    def main_window(self):
        
        return w

footer = urwid.AttrMap(urwid.Text(u'Press [q] / [Q] to exit...', align='center'), 'footer')
if connected_to_tor:
    header = urwid.AttrMap(urwid.Text(u'You are connected to the tor network', align='center'), 'tor_correct')
else:
    header = urwid.AttrMap(urwid.Text(u'You are !NOT! connected to the tor network! Pls fix!', align='center'), 'tor_false')

txt_box_upper = urwid.Text(('banner', u'Benutzung: blab bla'), align='center')
filler_top = urwid.Filler(txt_box_upper)

top = urwid.LineBox(urwid.Columns([filler_top]))


mid_txt1 = urwid.Text(('banner', u'Zeitfenster eingeben'), align='center')
mid_fill1 = urwid.BoxAdapter(urwid.Filler(mid_txt1, valign='top'), height=1)
div1 = urwid.Divider()

checkboxlist = []
for year in years:
    text = str(year[0])+'-'+str(year[1])
    checkboxlist.append(urwid.CheckBox(text))

checkbox_walker = urwid.SimpleFocusListWalker([mid_fill1, div1] + checkboxlist)
left_side = urwid.LineBox(urwid.ListBox(checkbox_walker))


mid_txt2 = urwid.Text(('banner', u'Queries eingeben'), align='center')
mid_fill2 = urwid.BoxAdapter(urwid.Filler(mid_txt2, valign='top'), height=1)
div2 = urwid.Divider()

query_box = urwid.Edit(multiline=True)

middle_walker = urwid.SimpleFocusListWalker([mid_fill2, div2, query_box])
middle_box = urwid.LineBox(urwid.ListBox(middle_walker))

start_stop_button
mid_txt3 = urwid.Text(('banner', u'Outputfeld Subprozesse'), align='center')
right_side = urwid.LineBox(urwid.Filler(mid_txt3, valign='top'))


mid = urwid.Columns([('weight', 1, left_side), ('weight', 2, middle_box), ('weight', 3, right_side)])



pg_bar = urwid.ProgressBar('progress_start', 'progress_end')
bottom = urwid.LineBox(urwid.Filler(pg_bar))


simple_walk = urwid.SimpleFocusListWalker([('weight', 1, top), ('weight', 5, mid), ('weight', 1, bottom)])
pile = urwid.Pile(simple_walk)

main_frame = urwid.Frame(pile)
main_frame.set_footer(footer)
main_frame.set_header(header)
loop = urwid.MainLoop(main_frame, palette, unhandled_input=exit_on_q)
loop.run()