from st_analyze import app as app1
from st_process import app as app2

import streamlit as st


class MultiApp:

    def __init__(self):
        self.apps = []

    def add_app(self, title, func):
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


app = MultiApp()

# Add all your application here
app.add_app("Analyze", app1)
app.add_app("Process", app2)

# The main apps
app.run()