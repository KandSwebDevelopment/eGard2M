from defines import *


def get_css_colours(level, part='css'):
    # part 1 = Background, 2 = Foreground, 3 = CSS string for both
    bg = "black"  # Set these to reverse colours, it the are used then something not caught here
    fg = "white"
    if level == CRITICAL:
        bg = CRITICAL_BG
        fg = CRITICAL_FG
    elif level == ERROR:
        bg = ERROR_BG
        fg = ERROR_FG
    elif level == WARNING:
        bg = WARNING_BG
        fg = WARNING_FG
    elif level == INFO:
        bg = INFO_BG
        fg = INFO_FG
    elif level == OK:
        bg = OK_BG
        fg = OK_FG
    elif level == PENDING:
        bg = PENDING_BG
        fg = PENDING_FG
    elif level == OPERATE:
        bg = OPERATE_BG
        fg = OPERATE_FG
    if part == 1:
        return bg
    elif part == 2:
        return fg
    else:
        return "background-color: {}; color: {};".format(bg, fg)
