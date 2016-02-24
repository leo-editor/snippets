# monkey patch to give Leo body widget X11 like select->copy and
# middle-button->paste behaviors in Windows, run it from a @script
# node with @bool scripting-at-script-nodes = True

from leo.core.leoQt import isQt5, QtCore, QtGui, Qsci, QtWidgets
from leo.plugins.qt_text import QTextEditWrapper

old = QTextEditWrapper.set_signals

def set_signals(self, old=old):

    old(self)

    def new_selection(w=self.widget):
        sel = w.textCursor().selectedText()
        but = QtGui.QApplication.mouseButtons() & QtCore.Qt.LeftButton
        if sel and but:
            QtGui.QApplication.clipboard().setText(sel)

    def middle_click(event, w=self.widget, old=self.widget.mouseReleaseEvent):
        if not event.button() == QtCore.Qt.MiddleButton:
            return old(event)
        cursor = w.cursorForPosition(event.pos())
        w.copy()  # copy selection to clipboard if not there already
        text = QtGui.QApplication.clipboard().text()
        cursor.insertText(text)
        w.setTextCursor(cursor)

    self.widget.selectionChanged.connect(new_selection)
    self.widget.mouseReleaseEvent = middle_click

QTextEditWrapper.set_signals = set_signals
c.frame.body.wrapper.set_signals()
