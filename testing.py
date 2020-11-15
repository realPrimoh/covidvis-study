import streamlit as st
import pandas as pd
import numpy as np
import csv
import datetime
import collections
import requests
import SessionState

from random import random
#from vega_datasets import data
from functools import reduce
from scripts.generate_trendlines import *

session_state = SessionState.get(looked_at=0, _next = False)


state_intervention = {"New York": '03-22-2020', "California": '03-19-2020', "Georgia": '04-02-2020', "Illinois": '03-21-2020', "Florida": '04-01-2020', "New Jersey": '03-21-2020', "Arizona": '03-31-2020', "Colorado": '03-26-2020', 'Indiana': '03-25-2020', 'Louisiana': '03-23-2020'}
states = ['California', 'Georgia', 'Illinois', 'New Jersey', 'Arizona', 'Colorado', 'Indiana', 'Louisiana']
phase2_look1 = st.selectbox("Pick a state",  ["Select..."] + states)
if not session_state._next:
    if phase2_look1 in states:
        st.info("Observe the trajectory for the COVID-19 cases.")
        alt_chart1_ = generate_actual_state_log_chart(phase2_look1, state_intervention[phase2_look1])
        st.altair_chart(alt_chart1_)
        session_state.looked_at += 1
        if session_state.looked_at == 3:
            if st.button("Next"):
                st.info("These are the questions...")
                flor_generated_trendlines = pd.read_csv("final_data/flor_generated_trendlines.csv")
                flor_chart = generate_altair_slider_log_chart(flor_generated_trendlines)
    
            

flor_generated_trendlines = pd.read_csv("final_data/flor_generated_trendlines.csv")
flor_chart = generate_altair_slider_log_chart(flor_generated_trendlines)
    
    
x = st.selectbox("Which one is right?", ["Select..."] + [str(i) for i in range(1, 11)])
if x == "1":
    st.info("Correct!")
elif x != "Select...":
    st.info("Loser!")
else:
    pass