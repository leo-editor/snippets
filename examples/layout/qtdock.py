"""
Testing Qt Dock widgets as a replacement for NestedSplitter

Things learned

 - "close" control just hides the widget
 - don't use visibilityChanged to manage close / vs. hide, it's
   called during dragging etc.
 - instead override .closeEvent() to manage close / vs. hide
 - the central widget is a nuisance, easiest just to not have one,
   rather than manage moving dock widgets in and out of that role
 - allowing nested widgets comes at the price of more complicated
   behavior, in return for more freedom in layouts
 - my regular workbook.leo layout requires nested widgets
 - floating windows cannot contain docks, which is a major loss
   vs. NestedSplitter, might be able to address that by adding
   another main window, but (a) doesn't work out of the box, would
   need widget transfer code, and (b) would require more
   save/restore code

The no docks in floating windows issue and the pointless central widget
issue may have resulted in NestedSplitter being developed, but at this
point it seems it would be better to use Qt docking.

Thoughts

 - save / restore state needs to be handled
 - the Leo "log pane" can be simulated by using the pane
   containing the actual log widget
 - rather than (safer than?) maintaining our own dock_widgets
   list, could just search main window for QDockWidget children
   track_widgets controls this choice

"""

import sys
from PyQt4 import QtGui, QtCore, Qt
from PyQt4.QtCore import Qt as QtConst

app = Qt.QApplication(sys.argv)
main = QtGui.QMainWindow()
main.resize(800,800)
main.move(40,40)
qtextedit = QtGui.QPushButton("Click to close central widget")
main.setCentralWidget(qtextedit)
def close(clicked, qtextedit=qtextedit):
    qtextedit.hide()
qtextedit.clicked.connect(close)

main.setDockOptions(QtGui.QMainWindow.AllowNestedDocks |
                    QtGui.QMainWindow.AllowTabbedDocks)

# start - extra dock window
main2 = QtGui.QMainWindow()
main2.resize(200,200)
main2.move(20,140)
qtextedit = QtGui.QPushButton("Click to close central widget")
main2.setCentralWidget(qtextedit)
def close(clicked, qtextedit=qtextedit):
    qtextedit.hide()
qtextedit.clicked.connect(close)
main2.setDockOptions(QtGui.QMainWindow.AllowNestedDocks |
                    QtGui.QMainWindow.AllowTabbedDocks)
main2.show()
# end - extra dock window

areas = {
    'Left': QtConst.LeftDockWidgetArea,
    'Right': QtConst.RightDockWidgetArea,
    'Top': QtConst.TopDockWidgetArea,
    'Bottom': QtConst.BottomDockWidgetArea,
}

track_widgets = False

dock_widgets = []

def get_dock_widgets():
    if track_widgets:
        return dock_widgets
    else:
        return main.findChildren(QtGui.QDockWidget)

def add_widget(name, deleteable=False, moveable=True,
               area=QtConst.RightDockWidgetArea):
    widget = QtGui.QDockWidget(name)
    widget._is_deleteable = deleteable
    if track_widgets:
        dock_widgets.append(widget)
    qtextedit = QtGui.QTextEdit()
    qtextedit.setPlainText(name)
    qtextedit.setReadOnly(True)
    widget.setWidget(qtextedit)
    main.addDockWidget(area, widget)

    if not moveable:
        widget.setFeatures(QtGui.QDockWidget.DockWidgetClosable)
    if deleteable:
        # fixme should make LeoQDockWidget subclass, maybe
        def closeEvent(event, widget=widget):
            if track_widgets:
                dock_widgets.remove(widget)
            widget.deleteLater()
        widget.closeEvent = closeEvent

    return widget

add_widget("Tree", area=QtConst.LeftDockWidgetArea)
add_widget("Log", area=QtConst.LeftDockWidgetArea)
add_widget("Body")

def show_dock_placeholders():
    clear_placeholders()
    docks_used = set()
    for widget in get_dock_widgets():
        if widget.isVisible() and not widget.isFloating():
            docks_used.add(main.dockWidgetArea(widget))
    for name, area in areas.items():
        if area not in docks_used:
            text = "%s Dock Placeholder" % name
            widget = add_widget(
                text, deleteable=True, moveable=False, area=area)

            widget._is_placeholder = True
            widget.setStyleSheet("background: #fdd;")

def clear_placeholders():
    cull = [i for i in get_dock_widgets()
            if getattr(i, '_is_placeholder', False)]
    for widget in cull:
        widget.close()

def hide_titles():
    for widget in get_dock_widgets():
        widget.setTitleBarWidget(QtGui.QWidget())

def show_titles():
    for widget in get_dock_widgets():
        widget.setTitleBarWidget(None)

menu = main.menuBar().addMenu("Windows")
menu = menu.addMenu("Docks")
menu.addAction("Show placeholders", show_dock_placeholders)
menu.addAction("Hide placeholders", clear_placeholders)
menu.addAction("Show titles / handles", show_titles)
menu.addAction("Hide titles / handles", hide_titles)

# demo specific code, no place in real app.
widget_count = [0]

def add_new_widget(**kwargs):
    widget_count[0] += 1
    n = widget_count[0]
    add_widget("Widget %d" % n, deleteable=True, **kwargs)

for n in range(3):
    add_new_widget(area=QtConst.BottomDockWidgetArea)

menu.addAction("Add new widget", add_new_widget)
# end demo specific code

main.show()
sys.exit(app.exec_())

