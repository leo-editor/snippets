from docutils.core import publish_string, publish_parts

# make a new node
nd = p.insertAfter()

# include '@rich' in the node headline so it's viewed in the HTML
# editor if richtext plugin is enabled, so we need to say "@norich"
# here to avoid the button's code being shown in HTML mode

nd.h = 'HTML: %s @rich' % (p.h)

# either of these works, the first is complete HTML, the second just
# body parts (ewww)

# nd.b = publish_string(p.b, writer_name='html')

nd.b = publish_parts(p.b, writer_name='html')['html_body']

c.selectPosition(nd)
c.redraw()
