"""Frameworks for running multiple Streamlit applications as a single apps.
"""
import streamlit as st

class MultiApp:
    """Framework for combining multiple streamlit applications.
    Usage:
        def foo():
            st.title("Hello Foo")
        def bar():
            st.title("Hello Bar")
        apps = MultiApp()
        apps.add_app("Foo", foo)
        apps.add_app("Bar", bar)
        apps.run()
    It is also possible keep each application in a separate file.
        import foo
        import bar
        apps = MultiApp()
        apps.add_app("Foo", foo.apps)
        apps.add_app("Bar", bar.apps)
        apps.run()
    """
    def __init__(self):
        self.apps = []

    def add_app(self, title, func):
        """Adds a new application.
        Parameters
        ----------
        func:
            the python function to render this apps.
        title:
            title of the apps. Appears in the dropdown in the sidebar.
        """
        self.apps.append({
            "title": title,
            "function": func
        })

    def run(self):
        app = st.sidebar.radio(
            'Go To',
            self.apps,
            format_func=lambda app: app['title'])

        app['function']()