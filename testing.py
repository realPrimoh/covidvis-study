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
st.write("Look through the states and try to see if you can find a pattern with the effects of lockdowns on the COVID-19 case trendline.")
phase2_look1 = st.selectbox("Pick a state",  ["Select..."] + states)
but = False
if not session_state._next:
    if phase2_look1 in states:
        st.info("Observe the trajectory for the COVID-19 cases.")
        alt_chart1_ = generate_actual_state_log_chart(phase2_look1, state_intervention[phase2_look1])
        st.altair_chart(alt_chart1_)
        session_state.looked_at += 1
        if session_state.looked_at >= 3:
            st.info("Nice job!")
            st.subheader("Below, we present the trajectory for confirmed cases in Georgia on a logarithmic scale. Once you have\
              studied it, please answer the questions below.")
            georgia_generated_trendlines = pd.read_csv("data/georgia_generated_trendlines.csv")
            georgia_generated_trendlines.loc[:, ["image_url"]] = georgia_generated_trendlines["image_url"].fillna("")
            base = create_base_log_layer(georgia_generated_trendlines[georgia_generated_trendlines["Type"] == "actual"], "Day", "Confirmed")
            img = create_image_layer(georgia_generated_trendlines[georgia_generated_trendlines["Type"] == "actual"], "Day", "Confirmed", "image_url")
            st.altair_chart(base + img)
            x = st.selectbox("Is this correct?", ["Select...", "Yes", "No"])
            if x == "Yes":
                st.info("Correct! Try one more.")
                eorgia_generated_trendlines = pd.read_csv("data/georgia_generated_trendlines.csv")
                georgia_generated_trendlines.loc[:, ["image_url"]] = georgia_generated_trendlines["image_url"].fillna("")
                base = create_base_log_layer(georgia_generated_trendlines[georgia_generated_trendlines["Type"] == "actual"], "Day", "Confirmed")
                img = create_image_layer(georgia_generated_trendlines[georgia_generated_trendlines["Type"] == "actual"], "Day", "Confirmed", "image_url")
                st.altair_chart(base + img)
                y = st.selectbox("Is this correct? ", ["Select...", "Yes", "No"])
                if y == "Yes":
                    st.info("Correct! Now, you can move on to Phase 3.")
                elif y == "No":
                    st.info("Try again!")
                else:
                    pass
            elif x == "No":
                st.info("Try again!")
            else:
                pass