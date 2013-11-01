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
<v t="mhw-test.20131028232230.1550"><vh>@settings</vh></v>
<v t="mhw-test.20131026223538.1538" a="E"><vh>@rst ~/myDocument.html</vh>
<v t="mhw-test.20131028232230.1551" a="E"><vh>Chapter I</vh>
<v t="mhw-test.20131028232230.1549"><vh>@rst-ignore</vh></v>
</v>
<v t="mhw-test.20131029183239.1559" a="E"><vh>@rst-ignore-tree Chapter 2+</vh>
<v t="mhw-test.20131029183239.1560" a="E"><vh>Chapter II</vh>
<v t="mhw-test.20131029183239.1561"><vh>translation</vh></v>
</v>
</v>
<v t="mhw-test.20131029183239.1552"><vh>Chapter XII</vh></v>
<v t="mhw-test.20131028232230.1552"><vh>@rst-no-head The End</vh></v>
</v>
</vnodes>
<tnodes>
<t tx="mhw-test.20131026223538.1538">#############
War and Peace
#############

        by Leo Tolstoy/Tolstoi
        
        BOOK ONE: 1805
        </t>
<t tx="mhw-test.20131028232230.1549">You can make whatever notes 
to yourself you like here, 
as these lines won't appear 
in the output files. :)

</t>
<t tx="mhw-test.20131028232230.1550"># these rst settings will apply to all @rst nodes in this .leo file, unless overwritten locally.

@bool rst3_call_docutils = True
    # Use False when using Sphinx
@bool rst3_write_intermediate_file = True
@string rst3_write_intermediate_extension = .txt
</t>
<t tx="mhw-test.20131028232230.1551">"Well, Prince, so Genoa and Lucca are now just family estates of the
Buonapartes. But I warn you, if you don't tell me that this means war,
if you still try to defend the infamies and horrors perpetrated by
that Antichrist--I really believe he is Antichrist--I will have
nothing more to do with you and you are no longer my friend, no longer
my 'faithful slave,' as you call yourself! But how do you do? I see
I have frightened you--sit down and tell me all the news."

...stuff happens...</t>
<t tx="mhw-test.20131028232230.1552">.. and now we skip to the end of last chapter, while demonstrating use of an
    organizer node (a node whose name does not appear in the output document),
    and that rst comments appear as html comments (try 'View Source' on
    output.html)

In the first case it was necessary to renounce the consciousness
of an unreal immobility in space and to recognize a motion we did
not feel; in the present case it is similarly necessary to renounce
a freedom that does not exist, and to recognize a dependence of
which we are not conscious.
   
--- The End ---

</t>
<t tx="mhw-test.20131029183239.1552">From the time the law of Copernicus was discovered and proved, the
mere recognition of the fact that it was not the sun but the earth
that moves sufficed to destroy the whole cosmography of the
ancients.

...</t>
<t tx="mhw-test.20131029183239.1559">this node and all child nodes will not appear in the output files.</t>
<t tx="mhw-test.20131029183239.1560">TL;DR

...la femme la plus seduisante de Petersbourg,* ...</t>
<t tx="mhw-test.20131029183239.1561">*The most fascinating woman in Petersburg.</t>
</tnodes>
</leo_file>
