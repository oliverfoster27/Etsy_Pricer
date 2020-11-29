import streamlit as st
from multiapp import MultiApp
from apps import st_analyze, st_process

app = MultiApp()

# Add all your application here
app.add_app("Analyze", st_analyze.app)
app.add_app("Process", st_process.app)

# The main apps
app.run()