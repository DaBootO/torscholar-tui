import urwid

def exit_on_q(key):
    if key in ('q', 'Q'):
        raise urwid.ExitMainLoop()


def MovingBlock():

    palette = [
        ('header', 'black', 'dark cyan', 'standout'),
        ('key', 'yellow', 'dark blue', 'bold'),
        ('bg', 'light gray', 'black' )
    ]

    header = urwid.Text(u"Block should move...")
    header = urwid.AttrWrap(header,'header')

    solid_bg = urwid.SolidFill(' ')
    solid_block = urwid.SolidFill('X')

    top_ov = urwid.Overlay(solid_block, solid_bg, align='left', width=1, height=1, valign='top', left=1, top=1)
    top = urwid.Frame(top_ov, header)


    def input_filter(keys, raw):
        if 'q' in keys or 'Q' in keys:
            raise urwid.ExitMainLoop
        
        if 'left' in keys:
            if top_ov.left > 0:
                top_ov.left -= 1
                top_ov.set_overlay_parameters(
                    align='left',
                    width=1,
                    height=1,
                    valign='top',
                    left=top_ov.left,
                    top=top_ov.top)
            header.set_text('top: %s left: %s' % (repr(top_ov.top), repr(top_ov.left)))
            

        if 'right' in keys:
            if top_ov.left < 10:
                top_ov.left += 1
                top_ov.set_overlay_parameters(
                    align='left',
                    width=1,
                    height=1,
                    valign='top',
                    left=top_ov.left,
                    top=top_ov.top)
            header.set_text('top: %s left: %s' % (repr(top_ov.top), repr(top_ov.left)))

        if 'up' in keys:
            if top_ov.top > 0:
                top_ov.top -= 1
                top_ov.set_overlay_parameters(
                    align='left',
                    width=1,
                    height=1,
                    valign='top',
                    left=top_ov.left,
                    top=top_ov.top)
            header.set_text('top: %s left: %s' % (repr(top_ov.top), repr(top_ov.left)))
    
        if 'down' in keys:
            if top_ov.top < 10:
                top_ov.top += 1
                top_ov.set_overlay_parameters(
                    align='left',
                    width=1,
                    height=1,
                    valign='top',
                    left=top_ov.left,
                    top=top_ov.top)
            header.set_text('top: %s left: %s' % (repr(top_ov.top), repr(top_ov.left)))
    
    print("We r here")
    loop = urwid.MainLoop(top, palette, input_filter=input_filter)
    loop.run()


# solid = urwid.SolidFill('X')
# print(solid.sizing())

# solid_bg = urwid.SolidFill(' ')

# ovlay = urwid.Overlay(solid, solid_bg, align='left', width=2, valign='top', height=2, left=0)

# print(ovlay.sizing())
# main_frame = urwid.Frame(ovlay)
# loop = urwid.MainLoop(main_frame, unhandled_input=exit_on_q)
# loop.run()

def main():
    MovingBlock()

if '__main__' == __name__:
    print("helo")
    main()