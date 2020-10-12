import streamlit as st
import pandas as pd
import numpy as np
import csv
import datetime
import collections
from random import random

from scripts.generate_trendlines import *


my_bar = st.sidebar.progress(0)
i = 1
st.title('CovidVis User Study')

st.info("Welcome to the Covidvis User Study. In this study, we are trying to measure the effects of seeing visualizations of COVID's ascent throughout the world on people's opinions about COVID interventions. Your data will be kept confidential and you will maintain anonymity.")

widget_values = collections.defaultdict(list)

# TODO: Record more data - record selections on the way (in order)
def record(f, widgetLabel):
    """Return a function that wraps a streamlit widget and records the
    widget's values to a global dictionary.
    """
    def wrapper(label, *args, **kwargs):
        widget_value = f(label, *args, **kwargs)
        widget_values[widgetLabel].append(widget_value)
        return widget_value

    return wrapper

st.header("Demographical Information")

st.subheader(str(i) + ". What is your age?")
ageSlider = record(st.selectbox, "Age")
age = ageSlider("Age", ('Select...', "18-24", "25-34", "35-44", "45-54", "55-64", "65-74", "75+"))

i += 1

# TODO: International or reduce target pop. to USA

st.subheader(str(i) + ". What state are you from?")
stateSelect = record(st.selectbox, "State")
stateSelect("State", ['Select...', "AL", "AK", "AZ", "AR", "CA", "CO", "CT", "DC", "DE", "FL", "GA", 
          "HI", "ID", "IL", "IN", "IA", "KS", "KY", "LA", "ME", "MD", 
          "MA", "MI", "MN", "MS", "MO", "MT", "NE", "NV", "NH", "NJ", 
          "NM", "NY", "NC", "ND", "OH", "OK", "OR", "PA", "RI", "SC", 
          "SD", "TN", "TX", "UT", "VT", "VA", "WA", "WV", "WI", "WY"])

i += 1

# TODO: Prefer not to say, nonbinary, etc
st.subheader(str(i) + ". What is your gender?")
genderSel = record(st.selectbox, "Gender")
genderSel("Gender", ('Select...','Male', 'Female'))

i += 1

st.subheader(str(i) + ". What political party do you affiliate with?")
partySel = record(st.selectbox, "Political Party")
partySel("Party", ('Select...', 'Democrat', 'Republican', 'Independent'))

i += 1

st.subheader(str(i) + ". What is your ethnicity?")
raceSel = record(st.selectbox, "Ethnicity")
raceSel("Race", ("Select...", "Asian / Pacific Islander", "White", "Black or African-American", "Native American or American Indian", "Hispanic or Latino", "Other"))

i += 1


st.subheader(str(i) + ". What is the highest level of education you have completed?")
eduSel = record(st.selectbox, "Education Level")
eduSel("Education Level", ("Select...", "No schooling completed", "High School", "Undergraduate", "Graduate"))

i += 1

st.subheader(str(i) + ". Do you agree with this?")
agree1 = record(st.radio, "Botcheck 1")
agree1("Select Slightly Agree.", ["Strongly Disagree", "Slightly Disagree", "Neutral", "Slightly Agree", "Strongly Agree"])

i += 1

st.subheader(str(i) + ". What is your occupation?")
occupationSel = record(st.text_input, "Occupation")
occupation = occupationSel("Occupation")

i += 1

st.subheader(str(i) + ". How many days a week do you view coronavirus related info (articles, data, press releases, etc.)?")
virusInfoSel = record(st.selectbox, "Days a week consuming virus information")
virusInfoSel("Viewing", ("Select...", "0-3", "4-7"))

i += 1

# TODO: Add spam-checker questions (Select 'agree', etc...)

st.subheader(str(i) + ". For each of the following orders, how effective are they?")
radio1 = record(st.selectbox, "Stay-at-home Effectiveness")
radio2 = record(st.selectbox, "Social Distancing Effectiveness")
radio3 = record(st.selectbox, "Mask On Effectiveness")
radio4 = record(st.selectbox, "Closing Bars/Restaurants Effectiveness")

i += 1

radio1("Stay-at-home", ["Select...", "Strongly Ineffective", "Slightly Ineffective", "Neutral", "Somewhat Effective", "Strongly Effective"])
radio2("Social distancing", ["Select...", "Strongly Ineffective", "Slightly Ineffective", "Neutral", "Somewhat Effective", "Strongly Effective"])
radio3("Masks on", ["Select...", "Strongly Ineffective", "Slightly Ineffective", "Neutral", "Somewhat Effective", "Strongly Effective"])
radio4("Closing bars/restaurants", ["Select...", "Strongly Ineffective", "Slightly Ineffective", "Neutral", "Somewhat Effective", "Strongly Effective"])

# TODO: Use a more basic graph

st.subheader(str(i) + ". On Day 35, how many confirmed cases were there?")
st.image("./ny_trendlines/actual.png", width=800)
vizcheck1 = record(st.radio, "Vizcheck 1")
vizcheck1("How many confirmed cases were on Day 35?", ("1,000", "2,000", "20,000", "100,000", "200,000", "250,000"))

i += 1

st.subheader(str(i) + ". The house icon represents a stay-at-home order being implemented. On approximately what day was the stay-at-home order implemented in this graph?")
st.image("ny_intervention_cumulative/actual.png", width=800)
vizcheck2 = record(st.radio, "Vizcheck 2")
vizcheck2("On approximately what day was the stay-at-home order implemented in this graph?", ["1", "2", "5", "8", "10", "12", "15", "18"])

i += 1


st.header("Visualization Survey")


st.header("Phase 1")

# NORMAL INTERVENTIONS
# ----------------

#st.subheader(str(i) + ". State A hadn't implemented a stay-at-home order at any point shown on the graph. Here, the graph's x-axis shows the number of days after the first case is recorded. What do you think is the trajectory of virus cases?")
##What do you think... (TODO: language)
#
#slider1 = record(st.select_slider, "Trajectory w/ No Stay-At-Home Order (Before)")
#chart_to_show = slider1("Trajectory", [i for i in range(1,7) for _ in range(5)])
#chart = "visualization/visualization" + str(int(chart_to_show)) + ".png"
#st.image(chart)
#
#i += 1

# PICK WHERE IT IS 
# --------------------
#
#st.subheader(str(i) + ". In this situation, State B implemented a lockdown order. Where on the curve do you think the lockdown order was put in place?")
#
#slider2 = record(st.select_slider, "Lockdown Order (Before)")
#chart_to_show_intervention = slider2("Lockdown Order", [i for i in range(1,4) for _ in range(5)])
#chart = "intervention/visualization" + str(int(chart_to_show_intervention) - 1) + ".png"
#st.image(chart)
#
#i += 1

#TODO: fix log scale text

# LOG SCALE 
# ----------------------
st.subheader(str(i) + ". In this situation, State C implemented a lockdown order. How do you think the trajectory for the number of cases changed afterwards? The lockdown order is marked by the house icon on the graph.")
slider3 = record(st.selectbox, "Log Scale (Before)")
chart_to_show_log = slider3("Log Scale Chart", [i for i in range(1,11)])
chart = "ny_log/visualization" + str(int(chart_to_show_log) - 1) + ".png"
st.image(chart)

i+=1

# NORMAL TRENDLINES
# --------------------
st.subheader(str(i) + ". This is the same question as above with an expanded y-axis.")
slider4 = record(st.selectbox, "Normal Trendline (Before)")
chart_to_show_normal_trend = slider4("Normal Trendline Chart", [i for i in range(1,11)])
chart = "ny_trendlines/visualization" + str(int(chart_to_show_normal_trend) - 1) + ".png"
st.image(chart)

i += 1

# NEW CASES A DAY 
# --------------------

# TODO: y-axis variable
# TODO: have an easier sub header
# TODO: put all on one chart

st.subheader(str(i) + ". This chart shows the amount of new cases per day. At some point, a lockdown order was put in place. Can you guess where?")
# slider5 = record(st.select_slider, "Pin the Lockdown on Smoothed Average Cases (Before)")
# chart_to_show_casesday_lockdown = slider5("Cases per Day Lockdown Order Guess", [i for i in range(1,4) for _ in range(5)])
# chart = "ny_interventions_new_day/visualization" + str(int(chart_to_show_casesday_lockdown) - 1) + ".png"
pick_img = st.radio("", ["Image 1", "Image 2", "Image 3"])
charts = ["ny_interventions_new_day/visualization0.png", \
"ny_interventions_new_day/visualization1.png", "ny_interventions_new_day/visualization2.png"]
st.image(charts)

i+=1
# Random states - not every user gets the same state

st.subheader(str(i) + ". Which trendline do you think most accurately represents New York's confirmed\
  cases of COVID-19 after the lockdown order indicated by the house?")
ny_cases = create_state_df('New York')
ny_image = add_image_col_to_df(ny_cases, 12) # Day 12 is when NY had a lockdown order
alt_chart = generate_single_graph_exponential(ny_image, 12)
st.altair_chart(alt_chart)

i+=1

st.header("Phase 2")

# MIDDLE
# -----------------------

st.header("Here are some examples of where lockdown orders were put in place.")
st.image("ny_intervention_cumulative/actual.png", width=800)
st.image("ny_interventions_new_day/actual.png", width=800)
st.image("ny_log/actual.png", width=800)
st.image("ny_trendlines/actual.png", width=800)


st.header("Phase 3")

#st.subheader(str(i) + ". State A hadn't implemented a stay-at-home order at any point shown on the graph. Here, the graph's x-axis shows the number of days after the first case is recorded. What do you think is the trajectory of virus cases?")
##What do you think... (TODO: language)
#i+=1
#
#slider0 = record(st.select_slider, "Trajectory w/ No Stay-At-Home Order (After)")
#chart_to_show_traj_after = slider0("Trajectory (After)", [i for i in range(1,7) for _ in range(5)])
#chart = "visualization/visualization" + str(int(chart_to_show_traj_after)) + ".png"
#st.image(chart)


# PICK WHERE IT IS 
# --------------------

#st.subheader(str(i) + ". In this situation, State B implemented a lockdown order. Where on the curve do you think the lockdown order was put in place?")
#
#slider6 = record(st.select_slider, "Lockdown Order (After)")
#chart_to_show_after = slider6("Lockdown Order (After)", [i for i in range(1,5) for _ in range(5)])
#chart = "intervention/visualization" + str(int(chart_to_show_after) - 1) + ".png"
#st.image(chart)
#i+=1

# LOG SCALE 
# ----------------------
st.subheader(str(i) + ". In this situation, State C implemented a lockdown order. How do you think the trajectory for the number of cases changed afterwards? The lockdown order is marked by the house icon on the graph.")
slider7 = record(st.select_slider, "Log Scale (After)")
chart_to_show_log_after = slider7("Pick the chart that seems the most correct to you. The x-axis represents the number of days, while the y-axis represents the number of COVID-19 cases.", [i for i in range(1,11) for _ in range(5)])
chart = "ny_log/visualization" + str(int(chart_to_show_log_after) - 1) + ".png"
st.image(chart)
i+=1

# NORMAL TRENDLINES
# --------------------
st.subheader(str(i) + ". This is the same question as above with an expanded y-axis.")
slider8 = record(st.select_slider, "Normal Trendline (After)")
chart_to_show_normal_trend_after = slider8("Pick the chart that seems the most correct to you. The x-axis represents the number of days, while the y-axis represents the number of COVID-19 cases. The difference here from the above question is an expanded y-axis.", [i for i in range(1,11) for _ in range(5)])
chart = "ny_trendlines/visualization" + str(int(chart_to_show_normal_trend_after) - 1) + ".png"
st.image(chart)
i+=1

# NEW CASES A DAY 
# --------------------

st.subheader(str(i) + ". This chart shows the amount of new cases per day. At some point, a lockdown order was put in place. Can you guess where?")
slider9 = record(st.select_slider, "Pin the Lockdown on Smoothed Average Cases (After)")
chart_to_show_casesday_lockdown_after = slider9("Pick the chart that seems the most correct to you. The x-axis represents the number of days, while the y-axis represents the average number of COVID-19 cases confirmed on each day., [i for i in range(1,4) for _ in range(5)])
chart = "ny_interventions_new_day/visualization" + str(int(chart_to_show_casesday_lockdown_after) - 1) + ".png"
st.image(chart)
i+=1

st.header("Conclusion")

st.info("Thank you so much for participating! Click submit below.")

if st.button("Submit"):
    field_names = list(widget_values.keys())
#    field_names.append("timestamp")
#    field_names.append("id")
#    now = datetime.datetime.now()
#    widget_values["timestamp"] = now.strftime("%Y-%b-%d, %A %I:%M:%S$p")
#    widget_values["id"] = random()
    with open('data.csv', 'w') as csvfile:
        writer = csv.DictWriter(csvfile, fieldnames=field_names)
        writer.writeheader()
        writer.writerows([widget_values])

        
# TODO: Collect more feedback from the study
# TODO: Number the questions
# TODO: Add progress bar
        


# Overlays of lines to provide context to the user when picking (highlight line when picked)

# Generate random trends to reduce bias
# Generate lines independent of the true line, which of these random lines do you think are closest to the true line
# Random sample of trends (reduce bias of the true line, ex. no median picking should be the answer)

# Plot the rate of change versus cumulative (log scale)
st.write("Recorded values: ", widget_values)
