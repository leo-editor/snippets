from PyQt4 import QtGui, QtWebKit, QtCore, Qt
from PyQt4.QtCore import Qt as QtConst
from collections import OrderedDict
import sys

if sys.version_info.major == 3:
    toUtf8 = lambda x: x
else:
    toUtf8 = lambda x: x.toUtf8()
    

# create Rich Text layout if it doesn't exist
if 'ns_layouts' not in g.app.db:
    g.app.db['ns_layouts'] = {}
if 'Rich Text' not in g.app.db['ns_layouts']:
    g.app.db['ns_layouts']['Rich Text'] = {
        'content': [
            {'content': ['_leo_pane:outlineFrame', '_leo_pane:logFrame'],
             'orientation': 2,
             'sizes': [538, 221]
            },
            '_add_rte_pane'],
        'orientation': 1,
        'sizes': [339, 1033]
    }

# create Default layout if it doesn't exist
if 'Default' not in g.app.db['ns_layouts']:
    g.app.db['ns_layouts']['Default'] = {
        'content': [
            {'content': ['_leo_pane:outlineFrame', '_leo_pane:logFrame'],
             'orientation': 2,
             'sizes': [573, 186]
            },
            '_leo_pane:bodyFrame'],
        'orientation': 1,
        'sizes': [390, 982]
    }

@g.command('rich-text-open')
def rich_text_open(kwargs):
    c.free_layout.get_top_splitter().load_layout(
        g.app.db['ns_layouts']['Rich Text'])
        
@g.command('rich-text-close')
def rich_text_close(kwargs):
    c.free_layout.get_top_splitter().load_layout(
        g.app.db['ns_layouts']['Default'])


class RTEEditor(QtGui.QWidget):
    
    def __init__(self, *args, **kwargs):
        self.c = kwargs['c']
        del kwargs['c']
        QtGui.QWidget.__init__(self, *args, **kwargs)
        self.setLayout(QtGui.QVBoxLayout())
        self.layout().setSpacing(0)
        self.layout().setContentsMargins(0,0,0,0)
        buttons = QtGui.QWidget()
        buttons.setLayout(QtGui.QHBoxLayout())
        buttons.layout().setSpacing(0)
        buttons.layout().setContentsMargins(0,0,0,0)
        self.layout().addWidget(buttons)
        
        actions = [
            # text, name, Ctrl-<key>
            ['Clr', 'clear', QtConst.Key_Space],
            ['B', 'bold', QtConst.Key_B],
            ['I', 'italic', QtConst.Key_I],
            ['U', 'underline', QtConst.Key_U],
            ['---', 'strikeout', QtConst.Key_Underscore],
            ['FG', 'foreground', None],
            ['BG', 'background', None],
            ['Font', 'font', None],
            ['+', 'larger', QtConst.Key_Plus],
            ['-', 'smaller', QtConst.Key_Minus],
        ]
        self.key_to_style = {}
        
        for action in actions:
            
            # record these for use in key stroke event
            key = action[2]
            if key:
                self.key_to_style[key] = action[1]
            
            btn = QtGui.QPushButton(action[0])
            buttons.layout().addWidget(btn)
            btn.clicked.connect(
                lambda checked, style=action[1]: self.set_style(style))
                
        self.styles = OrderedDict([
            ("Paragraph", ['clear']),
            ("Heading 1", ['bold', ('larger', 20)]),
            ("Heading 2", ['bold', 'italic', ('larger', 16)]),
            ("Heading 3", ['bold', 'italic', ('larger', 12), ('foreground', '#444')]),
            ("Warning", ['bold', ('foreground', '#f00')]),
            ("Latin", ['italic']),
            ("Literal", [('background', '#ccc')]),
        ])
        
        # style picker
        style_menu = QtGui.QComboBox()
        buttons.layout().addWidget(style_menu)
        style_menu.addItems([i for i in self.styles.keys()])
        style_menu.currentIndexChanged.connect(self.apply_style)
        
        # auto save checkbox
        self.auto = QtGui.QCheckBox("Auto")
        buttons.layout().addWidget(self.auto)
                
        # close button
        btn = QtGui.QPushButton('X')
        btn.clicked.connect(self.close)
        buttons.layout().addWidget(btn)
        
        buttons.layout().addStretch(1)
            
        self.te = QtGui.QTextEdit()
        self.layout().addWidget(self.te)
        
        g.registerHandler('select3', self.select_node)
        g.registerHandler('unselect1', self.unselect_node)
        self.init_format = self.te.currentCharFormat()
        
        def handle_keys(event, te=self.te, rte=self):
            
            if (event.key() == QtConst.Key_Return and 
                event.modifiers() & QtConst.ControlModifier):
                # Ctrl-Return - save edits
                self.c.p.b = toUtf8(self.te.toHtml())
                self.init_html = self.c.p.b
            elif (event.key() == QtConst.Key_Down and 
                event.modifiers() & QtConst.AltModifier):
                # Alt-Down - select next node
                self.c.selectVisNext()
            elif (event.key() == QtConst.Key_Up and 
                event.modifiers() & QtConst.AltModifier):
                # Alt-Down - select prev node
                self.c.selectVisBack()
            elif (event.key() in rte.key_to_style and
                event.modifiers() & QtConst.ControlModifier):
                self.set_style(rte.key_to_style[event.key()])
            else:
                return QtGui.QTextEdit.keyReleaseEvent(te, event)
                
            event.accept()
        
        self.te.keyReleaseEvent = handle_keys
        
        self.te.setFocus(QtConst.OtherFocusReason)
        
        # Call select_node hook to record initial content so we know
        # if it's edited and needs saving when another node's selected.
        # Why the QTimer?  When the event loop unfolds the HTML content
        # changes very slightly ('16px' -> '10px'), perhaps due to
        # style being applied, so it appears as if we edited the content.
        # QTimer lets us capture the final HTML and only detect real edits.
        QtCore.QTimer.singleShot(0, 
            lambda: self.select_node('', {'c': self.c, 'new_p': self.c.p}))
        
    def close(self):
        if self.c:
            # save changes?
            self.unselect_node('', {'c': self.c, 'old_p': self.c.p})
            # restore Default layout with regular body pane
            QtCore.QTimer.singleShot(0, lambda c=self.c:
                c.free_layout.get_top_splitter().load_layout(
                g.app.db['ns_layouts']['Default']))
        self.c = None
        g.unregisterHandler('select3', self.select_node)
        g.unregisterHandler('unselect1', self.unselect_node)
        return QtGui.QWidget.close(self)
        
    def select_node(self, tag, kwargs):
        c = kwargs['c']
        if c != self.c:
            return
        p = kwargs['new_p']
        
        if p.b.startswith('<!DOCTYPE HTML'):
            self.te.setHtml(p.b)
        else:
            self.te.setHtml("<pre>%s</pre>"%p.b)
        self.init_html = toUtf8(self.te.toHtml())
            
    def unselect_node(self, tag, kwargs):
        c = kwargs['c']
        if c != self.c:
            return
        if toUtf8(self.te.toHtml()) != self.init_html:

            if self.auto.isChecked():
                ans = 'yes'
            else:
                ans = g.app.gui.runAskYesNoCancelDialog(
                    self.c,
                    "Save edits?",
                    "Save edits?"
                )
            if ans == 'yes':
                kwargs['old_p'].b = toUtf8(self.te.toHtml())
            elif ans == 'cancel':
                return 'STOP'
            else:
                pass  # discard edits
            
    def set_style(self, style, value=None):
        format = QtGui.QTextCharFormat()
        
        if style == 'bold':
            format.setFontWeight(QtGui.QFont.Bold)
        elif style == 'italic':
            format.setFontItalic(True)
        elif style == 'underline':
            format.setFontUnderline(True)
        elif style == 'strikeout':
            format.setFontStrikeOut(True)
        elif style in ('foreground', 'background'):
            if not value:
                cp = QtGui.QColorDialog()
                if cp.exec_() != QtGui.QDialog.Rejected:
                    color = cp.selectedColor()
                else:
                    color = None
            else:
                color = QtGui.QColor(value)
            if color and style == 'foreground':
                format.setForeground(color)
            elif color:
                format.setBackground(color)
        elif style == 'font':
            fd = QtGui.QFontDialog()
            if fd.exec_() != QtGui.QDialog.Rejected:
                font = fd.selectedFont()
            else:
                font = None
            if font:
                format.setFont(font)
        elif style in ('larger', 'smaller'):
            
            if not value:
                size = self.te.textCursor().charFormat().fontPointSize()
                if style == 'larger':
                    size += 1
                else:
                    size -= 1
            else:
                size = value
            size = max(2, min(100, size))
            format.setFontPointSize(size)
            
        if style == 'clear':
            self.te.textCursor().setCharFormat(self.init_format)
            self.te.setCurrentCharFormat(self.init_format)
        else:
            self.te.textCursor().mergeCharFormat(format)
            self.te.mergeCurrentCharFormat(format)
            
    def apply_style(self, n):
        style = self.styles[[i for i in self.styles.keys()][n]]
        for attr in style:
            if isinstance(attr, tuple):
                self.set_style(attr[0], attr[1])
            else:
                self.set_style(attr)
            
        
class RTEPaneProvider:
    ns_id = '_add_rte_pane'
    def __init__(self, c):
        self.c = c
        # Careful: we may be unit testing.
        if hasattr(c, 'free_layout'):
            splitter = c.free_layout.get_top_splitter()
            if splitter:
                splitter.register_provider(self)
    def ns_provides(self):
        return[('Rich text editor', self.ns_id)]
    def ns_provide(self, id_):
        if id_ == self.ns_id:
            w = RTEEditor(c=self.c)
            return w
    def ns_provider_id(self):
        # used by register_provider() to unregister previously registered
        # providers of the same service
        return self.ns_id

RTEPaneProvider(c)

# if hasattr(c, 'free_layout'):
#     splitter = c.free_layout.get_top_splitter()
#     if splitter:
#         splitter.open_window(action=RTEPaneProvider.ns_id)
