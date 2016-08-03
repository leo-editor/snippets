# full and minimal examples for adding widgets in panes in Leo
# Note: to add the widget, right click a pane divider, and select
# Insert.  Then click the Action button that appears, and select
# your widget.

# Copy all this text (use Raw view) to a node, and run it (Ctrl-B) once
# After doing that, the pane divider right click context menu open window
# submenu will have "Demo * slider" options.

from leo.core.leoQt import QtCore, QtWidgets
class DemoProvider:
    def ns_provides(self):
        """should return a list of ('Item name', '__item_id') strings, 
        'Item name' is displayed in the Action button menu, and
        '__item_id' is used in ns_provide()."""
        return [
            ("Demo horizontal slider", "__demo_provider_hs"),
            ("Demo vertical slider", "__demo_provider_vs"),
        ]
    def ns_provide(self, id_):
        """should return the widget to replace the Action button based on
        id_, or None if the called thing is not the provider for this id_"""
        if id_ == "__demo_provider_hs":
            w = QtWidgets.QSlider(QtCore.Qt.Horizontal)
            return w
        if id_ == "__demo_provider_vs":
            w = QtWidgets.QSlider()
            return w
        return None
    def ns_context(self):
        """should return a list of ('Item name', '__item_id') strings, 
        'Item name' is displayed in the splitter handle context-menu, and
        '__item_id' is used in ns_do_context().  May also return a dict,
        in which case each key is used as a sub-menu title, whose menu
        items are the corresponding dict value, a list of tuples as above.
        dicts and tuples may be interspersed in lists."""
        return [
            ("Put 'text' in log", "__demo_provider_til"),
            {
                'More texts': [
                    ("Put 'frog' in log", "__demo_provider_txt_frog"),
                    ("Put 'otters' in log", "__demo_provider_txt_otters"),
                ],
                'Numbers': [
                    ("Put 7 in log", "__demo_provider_txt_7"),
                    ("Put 77 in log", "__demo_provider_txt_77"),
                ],
            }
        ]
    def ns_do_context(self,id_, splitter, index):
        """should do something based on id_ and return True, or return False
        if the called thing is not the provider for this id_
        
        splitter and index as per QSplitter"""
        if id_ == '__demo_provider_til':
            g.es("'text'")
            return True
        if id_.startswith('__demo_provider_txt_'):
            # silly example, but storing info in id_ is legitimate
            g.es(id_.replace('__demo_provider_txt_', ''))
            return True
        return False
    def ns_provider_id(self):
        """return a string identifying the provider (at class or instance level),
        any providers with the same id will be removed before a new one is
        added"""
        return "__demo_provider"
        
class MinimalDemoProvider:
    def ns_provides(self):
        return [("Demo minimal slider", "__demo_provider_minimal_slider")]
    def ns_provide(self, id_):
        if id_ == "__demo_provider_minimal_slider":
            w = QtWidgets.QSlider()
            return w
        return None
    def ns_provider_id(self):
        return "__demo_provider_minimal"
        
c.free_layout.get_top_splitter().register_provider(DemoProvider())
c.free_layout.get_top_splitter().register_provider(MinimalDemoProvider())

