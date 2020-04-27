<?xml version="1.0" encoding="utf-8"?>
<!-- Created by Leo: http://leoeditor.com/leo_toc.html -->
<leo_file xmlns:leo="http://leoeditor.com/namespaces/leo-python-editor/1.1" >
<leo_header file_format="2"/>
<globals/>
<preferences/>
<find_panel_settings/>
<vnodes>
<v t="maphew.20200427084906.1"><vh>Readme</vh></v>
<v t="TomP.20200420171628.1"><vh>@buttons</vh>
<v t="TomP.20200420171628.2"><vh>@button Show Current Dir</vh></v>
<v t="TomP.20200420171628.4"><vh>@button Cmd Window Here</vh></v>
</v>
<v t="TomP.20200420171732.1"><vh>Menus</vh>
<v t="TomP.20200420171732.2"><vh>@menuat /file/openwith before</vh>
<v t="TomP.20200420171732.3"><vh>@openwith Editplus = Alt+Shift+E </vh></v>
<v t="TomP.20200420171732.4"><vh>@openwith Pyzo = Alt+Shift+P</vh></v>
</v>
</v>
<v t="TomP.20200420171840.1"><vh>Line Numbers</vh>
<v t="TomP.20200420171840.2"><vh>@bool use_gutter = True</vh></v>
<v t="TomP.20200420171840.3"><vh>@int gutter-y-adjust = 5</vh></v>
</v>
<v t="TomP.20200420172358.1"><vh>@shortcuts</vh></v>
<v t="TomP.20200420172132.1"><vh>@bool create_nonexistent_directories = True</vh></v>
</vnodes>
<tnodes>
<t tx="TomP.20200420171628.1"></t>
<t tx="TomP.20200420171628.2">from subprocess import Popen
cmd = 'explorer.exe .'
Popen(cmd)</t>
<t tx="TomP.20200420171628.4">from subprocess import Popen
cmd = 'cmd.exe cd .'
Popen(cmd)</t>
<t tx="TomP.20200420171732.1">Note that these paths are specific to my system.  Change them for another system.</t>
<t tx="TomP.20200420171732.2"></t>
<t tx="TomP.20200420171732.3">ext:
kind:   subprocess.Popen
arg:    "C:\Program Files\EditPlus\editplus.exe"

</t>
<t tx="TomP.20200420171732.4">ext:    .exe
kind:   subprocess.Popen
arg:    "c:\Program Files\pyzo\pyzo.exe"

</t>
<t tx="TomP.20200420171840.1">Change the gutter-y-adjust value to make the line numbers line up right.</t>
<t tx="TomP.20200420171840.2"></t>
<t tx="TomP.20200420171840.3"></t>
<t tx="TomP.20200420172132.1"></t>
<t tx="TomP.20200420172358.1">goto-next-marked = F4
mark = F9
unmark-all = F10

match-brackets = Ctrl+]
add-comments = Ctrl+'
delete-comments = Ctrl+;

vr3-toggle = Alt+0
</t>
<t tx="maphew.20200427084906.1">Contributed by Thomas Passin
https://groups.google.com/d/msg/leo-editor/kgwfUHJdM1s/QU_1HA3vDQAJ

To use this example, all of the nodes in this file go under the @settings node in MyLeoSettings.Leo.

QQQ
One of the more useful little things I did was to create two buttons that appear above every outline:

1. Show Current Directory
2. Cmd Window Here

They both open in the currently effective directory, which is usually the directory of the outline itself.  That can be changed using @path directives. So, for example, if you changed an HTML file and wanted to load it into the browser, you could open e.g., Windows Explorer on its directory and then double click it.

Another thing that is easy to do is to add a menu item that opens the selected file in your favorite editor (or it could be any program, such as a browser).

Another very useful thing I have done is to show line numbers for files.  It takes a bit of tinkering to get them aligned right, but I think it's worth it.

[...]

Note that the two @button commands are specific to Windows.  They could be done in Linux, of course, but the exact commands would be specific to each linux distro.  Maybe someone would like to suggest example Linux commands.  For example, launching a GUI program like the file manager can be a little tricky, so help us get it set up right.

The actual paths to the programs in the @menuat items would have to be adjusted for some else's system.

I have included some keyboard shortcuts that I find very useful.  They don't conflict with any existing shortcuts so far as I know.  There is a group to make it easy to set, jump to, and remove node markers.  There is a pair that make it easy to comment out or uncomment a selection of lines.  And there is my favored ALT-0 for opening viewrendered3.

Actually, I would find it hard to operate for any period of time without these settings.  I use them all the time.
QQQ</t>
</tnodes>
</leo_file>
