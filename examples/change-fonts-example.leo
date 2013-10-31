<?xml version="1.0" encoding="utf-8"?>
<!-- Created by Leo (http://leoeditor.com/leo_toc.html) -->
<?xml-stylesheet ekr_test?>
<leo_file xmlns:leo="http://www.leo-editor.org/2011/leo" >
<leo_header file_format="2" tnodes="0" max_tnode_index="0" clone_windows="0"/>
<globals body_outline_ratio="0.5" body_secondary_ratio="0.5">
	<global_window_position top="50" left="50" height="500" width="700"/>
	<global_log_window_position top="0" left="0" height="0" width="0"/>
</globals>
<preferences/>
<find_panel_settings/>
<vnodes>
<v t="maphew.20131030221945.3473" a="E"><vh>@settings</vh>
<v t="maphew.20131030221945.3474"><vh>@data qt-gui-plugin-style-sheet</vh></v>
</v>
</vnodes>
<tnodes>
<t tx="maphew.20131030221945.3473">A stripped down example of changing Leo's default fonts. 

For a more extensive treatment see Help &gt; "LeoSettings.leo --&gt; @settings --&gt;
Appearance" and "LeoSettings.leo --&gt; Themes".</t>
<t tx="maphew.20131030221945.3474">/* The body pane */
QTextEdit#richTextEdit {
    font-family: Garamond, Times New Roman;
    /* font-family: Courier New; */
    font-size: 18px;
    font-weight: normal; /* normal,bold,100,..,900 */
    font-style: normal; /* normal,italic,oblique */
}

/* The log panes */
QTextEdit#log-widget {
    font-family: Courier New;
    font-size: 12px;
}

QTreeWidget {
    /* These apply to the selected item, but not to editing items.*/
    font-family: Garamond, Times New Roman;
    font-size: 16px;
}

/* Headline edit widgets */
QTreeWidget QLineEdit View{
    font-family: Garamond, Times New Roman;
    font-size: 16px;
}
</t>
</tnodes>
</leo_file>
