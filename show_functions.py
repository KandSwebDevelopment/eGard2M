from dialogs import _Main


def show_main(p):
    w = _Main(p)
    w.ControlBox = False
    w.TopLevel = True
    sub = p.mdiArea.addSubWindow(w)
    w.show()
