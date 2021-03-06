<?xml version="1.0" encoding="utf-8"?>
<!-- Created by Leo (http://leoeditor.com/leo_toc.html) -->
<?xml-stylesheet ekr_test?>
<leo_file xmlns:leo="http://www.leo-editor.org/2011/leo" >
<leo_header file_format="2"/>
<vnodes>
<v t="ekr.20131114191618.17401" a="E"><vh>@settings</vh>
<v t="maphew.20131115063329.1572" a="E"><vh>@menuat /help before</vh>
<v t="maphew.20131115063329.9475"><vh>@item open-leo12pt-leo</vh></v>
</v>
<v t="ekr.20131114191618.17400"><vh>@data qt-gui-plugin-style-sheet</vh></v>
</v>
</vnodes>
<tnodes>
<t tx="ekr.20131114191618.17400">/* Disable this to continually test leoSettings.leo */

/* Documentation of Qt stylesheets at http://doc.trolltech.com/4.2/stylesheet.html */

/* constants - *parsed from this comment*

   needed for zoom in / out
   
   @font-size-body = 10pt
   
   *color names*
   @MistyRose1 = #FFE4E1
   @LightSteelBlue1 = #CAE1FF
   @LightBlue = #ADD8E6

   Buttons may be styled by name:
      QPushButton#&lt;button text&gt;-button { &lt;style&gt; }
   or by kind:
      QPushButton[button_kind="&lt;button kind&gt;"] { &lt;style&gt; }
   Button kinds are:
   'run-script' (the singleton run-script button),
   'debug-script',
   'script-button-button' (the singleton script-button button), 
   'script-button' (buttons created by the script-button button),
   'generic-button' (default), 
   'quick-move' from the quickMove plugin,
   'interact' from the interact plugin,
   'at-button' (created from @button nodes)
   Search 'button_kind' below for button styling examples.
   
   *button background colors*
   @run-script-btn-bg = @MistyRose1
   @debug-script-btn-bg = @MistyRose1
   @script-button-button-btn-bg = #ffffcc
   @script-button-btn-bg = @MistyRose1
   @generic-button-btn-bg = @LightSteelBlue1
   @quick-move-btn-bg = @LightSteelBlue1
   @interact-btn-bg = @LightBlue
   @at-button-btn-bg = @LightSteelBlue1
       
*/

/* Valid color names: http://www.w3.org/TR/SVG/types.html#ColorKeywords */

/*
    Important: this stylesheets is responsible for most, but *not* all, of Leos appearance.
    See also settings in "Colorizer and colors" 
*/

QScrollArea {
    background-color: white;
}

/* Components of the Find Tab */

QWidget#findTab {
    background-color: white;
}

QLabel#findHeading {
    font-family: DejaVu Sans Mono;
    font-size: 10pt;
    font-weight: normal; /* normal,bold,100,..,900 */
    font-style: normal; /* normal,italic,oblique */
}

QLabel#findLabel {
    font-family: DejaVu Sans Mono;
    font-size: 10pt;
    font-weight: normal; /* normal,bold,100,..,900 */
    font-style: normal; /* normal,italic,oblique */
}

QLabel#changeLabel {
    font-family: DejaVu Sans Mono;
    font-size: 10pt;
    font-weight: normal; /* normal,bold,100,..,900 */
    font-style: normal; /* normal,italic,oblique */
}

QLabel#findHelp {
    font-family: DejaVu Sans Mono;
    font-size: 10pt;
    font-weight: normal; /* normal,bold,100,..,900 */
    font-style: normal; /* normal,italic,oblique */
}

QLineEdit#findPattern {
    font-family: DejaVu Sans Mono;
    font-size: 10pt;
    font-weight: normal; /* normal,bold,100,..,900 */
    font-style: normal; /* normal,italic,oblique */
}

QLineEdit#findChange {
    font-family: DejaVu Sans Mono;
    font-size: 10pt;
    font-weight: normal; /* normal,bold,100,..,900 */
    font-style: normal; /* normal,italic,oblique */
}

/* A QWidget: supports only background attributes.*/

QSplitter::handle {
    background-color: #CAE1FF; /* lightSteelBlue1 */
}

QStackedWidget {
    /* background-color:lightpink; */
    border-color: red;
    padding: 0px;
    /* border-width: 0px; */
    /* background-color: yellow; */
}

QSplitter {
    border-color: white;
    background-color: white;
    border-style: solid;
}

QTreeWidget {
    /* These apply to the selected item, but not to editing items.*/
    background-color: #ffffec; /* Leo's traditional tree color */
    selection-color: black; /* was white */
    selection-background-color: lightgrey;
    /* font-family: SansSerif; */
    font-family: DejaVu Sans Mono;
    font-size: 10pt;
    font-weight: normal; /* normal,bold,100,..,900 */
    font-style: normal; /* normal, italic,oblique */
    show-decoration-selected: 1 /* 1: select entire row */
 }

/* Headline edit widgets */
QTreeWidget QLineEdit {
    background-color: cornsilk;
    selection-color: white;
    selection-background-color: blue;
    font-family: DejaVu Sans Mono;
    font-size: 10pt;
    font-weight: normal; /* normal,bold,100,..,900 */
    font-style: normal; /* normal, italic,oblique */
}

/* The log panes */
QTextEdit {
    background-color: white; /* #f2fdff; */
    selection-color: white;
    selection-background-color: blue;
    /* font-family: Courier New; */
    font-family: DejaVu Sans Mono;
    font-size: 10pt;
    font-weight: normal; /* normal,bold,100,..,900 */
    font-style: normal; /* normal, italic,oblique */
}

/* The body pane */
QTextEdit#richTextEdit {
    background-color: white; /* #fdf5f5; A kind of pink. */
    selection-color: white;
    selection-background-color: lightgrey;
    font-family: DejaVu Sans Mono;
    /* font-family: Courier New; */
    font-size: @font-size-body;
    font-weight: normal; /* normal,bold,100,..,900 */
    font-style: normal; /* normal,italic,oblique */
}

/* Editor labels */
QLineEdit#editorLabel {
    background-color: #ffffec;
    font-family: DejaVu Sans Mono;
    font-size: 10pt;
    font-weight: normal; /* normal,bold,100,..,900 */
    font-style: normal; /* normal,italic,oblique */
    border: 2px;
    margin: 2px;
}

/* The text "Minibuffer" in the minibuffer aread.

Do not overide QLabel directly.  It is used for dialog text.
*/

QLabel#minibufferLabel {
    font-family: DejaVu Sans Mono;
    font-size: 10pt;
    font-weight: normal;
    font-style: normal;
}

/* 
QLabel {
    font-family: DejaVu Sans Mono;
    font-size: 10pt;
    font-weight: normal;
    font-style: normal;
    border: 2px;
    margin: 2px;
}
*/


/* The mini-buffer

**Important**: Because Leo changes the color of the minibuffer dynamically,
stylesheets can not be used. Instead, set the desired colors using one of the
following settings, with defaults as shown::

    @color minibuffer-background-color = lightblue
    @color minibuffer-error-color = red
    @color minibuffer-foreground-color = black
    @color minibuffer-warning-color = lightgrey
*/
QLineEdit#lineEdit {
    selection-color: white;
    selection-background-color: lightgrey;
    font-family: DejaVu Sans Mono;
    font-size: 10pt;
    font-weight: normal; /* normal,bold,100,..,900 */
    font-style: normal; /* normal,italic,oblique */
}

QLineEdit#status1 {
    background-color: lightgrey;
    border-width: 1px;
    border-style: solid;
    border-color: darkgrey;
    font-size: 10pt;
}

QLineEdit#status2 {
    background-color: lightgrey;
    border-width: 1px;
    border-style: solid;
    border-color: darkgrey;
    font-size: 10pt;
}

/* button_kind based button coloring */
QPushButton[button_kind="run-script"] { 
    background-color: @run-script-btn-bg; }
QPushButton[button_kind="debug-script"] { 
    background-color: @debug-script-btn-bg; }
QPushButton[button_kind="generic-button"] { 
    background-color: @generic-button-btn-bg; }
QPushButton[button_kind="quick-move"] { 
    background-color: @quick-move-btn-bg; }
QPushButton[button_kind="interact"] { 
    background-color: @interact-btn-bg; }
QPushButton[button_kind="at-button"] { 
    background-color: @at-button-btn-bg; }
QPushButton[button_kind="script-button"] { 
    background-color: @script-button-btn-bg; }
/* example of name based button coloring.  Coincidentally, the
   name and button_kind of this button are the same */
QPushButton#script-button-button { 
    background-color: @script-button-button-btn-bg; }

QPlainTextEdit#screencastcaption {
    background-color: yellow;
    font-family: DejaVu Sans Mono; /* Times New Roman; */
    font-size: 18pt;
    font-weight: normal; /* normal,bold,100,..,900 */
    font-style: normal; /* normal,italic,oblique */
}

/* focused pane border highlight */
QTextEdit#log-widget, LeoQTreeWidget#treeWidget, QTextEdit#richTextEdit { 
  border-style: @focused-border-style;
  border-width: @focused-border-width; 
  border-color: @focused-border-unfocus-color; 
}
QTextEdit:focus#log-widget, LeoQTreeWidget:focus#treeWidget, QTextEdit:focus#richTextEdit { 
  border-style: @focused-border-style;
  border-width: @focused-border-width; 
  border-color: @focused-border-focus-color; 
}
</t>
<t tx="ekr.20131114191618.17401"></t>
<t tx="maphew.20131115063329.1572"></t>
<t tx="maphew.20131115063329.9475">Open &amp;leo12pt.leo</t>
</tnodes>
</leo_file>
