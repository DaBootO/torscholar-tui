import urwid


def exit_on_q(key):
    if key in ('q', 'Q'):
        raise urwid.ExitMainLoop()

def button(self, t, fn):
        w = urwid.Button(t, fn)
        w = urwid.AttrWrap(w, 'button normal', 'button select')
        return w

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
    ('progress_end', 'white', 'dark gray')
]

footer = urwid.AttrMap(urwid.Text(u'Press [q] / [Q] to exit...', align='center'), 'footer')

txt_box_upper = urwid.Text(('banner', u'Benutzung: blab bla'), align='center')
filler_top = urwid.Filler(txt_box_upper)

top = urwid.LineBox(urwid.Columns([filler_top]))


mid_txt1 = urwid.Text(('banner', u'Zeitfenster eingeben'), align='center')
mid_fill1 = urwid.BoxAdapter(urwid.Filler(mid_txt1, valign='top'), height=1)

div1 = urwid.Divider()

b1 = urwid.RadioButton([], u'1946-1950')
b2 = urwid.RadioButton([], u'1951-1955')
b3 = urwid.RadioButton([], u'etc')

button_walker = urwid.SimpleFocusListWalker([mid_fill1, div1, b1, b2, b3])
buttonpile = urwid.LineBox(urwid.ListBox(button_walker))
mid_txt2 = urwid.Text(('banner', u'Queries eingeben'), align='center')
mid_fill2 = urwid.LineBox(urwid.Filler(mid_txt2, valign='top'))
mid_txt3 = urwid.Text(('banner', u'Outputfeld Subprozesse'), align='center')
mid_fill3 = urwid.LineBox(urwid.Filler(mid_txt3, valign='top'))

middle = urwid.Columns([('weight', 1, buttonpile), ('weight', 1, mid_fill2), ('weight', 2, mid_fill3)])


pg_bar = urwid.ProgressBar('progress_start', 'progress_end')
bottom = urwid.LineBox(urwid.Filler(pg_bar))


simple_walk = urwid.SimpleFocusListWalker([('weight', 1, top), ('weight', 5, middle), ('weight', 1, bottom)])
pile = urwid.Pile(simple_walk)

main_frame = urwid.Frame(pile)
main_frame.set_footer(footer)
loop = urwid.MainLoop(pile, palette, unhandled_input=exit_on_q)
loop.run()