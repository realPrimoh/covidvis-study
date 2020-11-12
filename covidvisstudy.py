import streamlit as st
import pandas as pd
#import geopandas as gpd
import numpy as np
import csv
import datetime
import collections
import requests

from random import random
#from vega_datasets import data
from functools import reduce

from scripts.generate_trendlines import *

# TODO: we don't need to show too much after lockdown.
# TODO: local neighborhood, show difference before/after lockdown order begins, ends
# TODO: Check re-opening data (collected manually) 

# B. Aditya: Track epidemic until reopening starts (too many factors after re-opening, reopening happens in phases, more nuanced, more confounding factors)

# Randomization of state (in phase 1, phase 3). It is only needed if there is a learning effect. User would like to see own state possibly.

i = 1
st.title('CovidVis: The Impact of Visualizations on Perception of COVID-19 Intervention Measures')

st.info("Welcome to the Covidvis User Study. In this study, we are trying to measure the effects of seeing visualizations of COVID's ascent throughout the world on people's opinions about COVID interventions. Your data will be kept as confidential as possible.")

st.subheader("Consent to take part in the study")
st.markdown("We are asking you to participate in a research study titled “The Impact of Visualizations on Perception of COVID-19 Intervention Measures”. We will describe this study to you and answer any of your questions. \n\n This study is being led by Aditya Parameswaran, Priyam Mohanty, Murtaza Ali, Doris Lee, and B. Aditya Prakash, a research team from UC Berkeley and Georgia Tech.")

st.subheader("What the study is about")
st.markdown("The purpose of this research is to examine the impact of visualizations on COVID-19 intervention perception.")

st.subheader("What we will ask you to do")
st.markdown("If you agree to take part, you will be asked to complete a questionnaire and provide your opinions. The survey will last approximately 15 minutes and will be conducted online.")

st.subheader("Risks and discomforts")
st.markdown("There is little risk to you in taking part in this research. As with all research there is a chance that confidentiality may be compromised; however, we will take the following precautions to minimize this risk: Your study data will be treated as confidentially as possible. The data will be stored on a password protected laptop. None of your personal information is collected.")

st.subheader("Benefits")
st.markdown("There are no direct benefits to you from this research. It is our hope that the research will benefit the scientific community and lead to a greater understanding of visualizations and their effects on people's understanding of COVID interventions.")

st.subheader("Taking part is voluntary")
st.markdown("Your involvement in this research is voluntary, and you may refuse to participate before the study begins or discontinue at any time. You will only receive compensation for this study if you complete all tasks and survey questions.")

st.subheader("If you have questions")
st.markdown("The main researchers conducting this study Aditya Parameswaran, Priyam Mohanty, and Murtaza Ali. Please ask any questions you have now. If you have questions later, you may contact Priyam Mohanty at priyam.mohanty@berkeley.edu.  If you have any questions or concerns regarding your rights as a subject in this study, you may contact the Institutional Review Board (IRB) for Human Participants at https://cphs.berkeley.edu.")

st.subheader("Statement of Consent")
st.markdown("By continuing with this survey and submitting your response, you are consenting to the above statements. If you do not consent, please exit the survey now.")


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

st.subheader("Enter your MTurk ID here.")
mturkSel = record(st.text_input, "MTurk ID")
mturk = mturkSel("MTurk ID")

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
genderSel("Gender", ('Select...','Male', 'Female', 'Nonbinary', 'Prefer not to say'))

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
st.subheader("Below, we present the trajectory for confirmed cases in Georgia on a logarithmic scale. Once you have\
              studied it, please answer the questions below.")
georgia_generated_trendlines = pd.read_csv("data/georgia_generated_trendlines.csv")
georgia_generated_trendlines.loc[:, ["image_url"]] = georgia_generated_trendlines["image_url"].fillna("")
base = create_base_log_layer(georgia_generated_trendlines[georgia_generated_trendlines["Type"] == "actual"], "Day", "Confirmed")
img = create_image_layer(georgia_generated_trendlines[georgia_generated_trendlines["Type"] == "actual"], "Day", "Confirmed", "image_url")
st.altair_chart(base + img)

st.subheader(str(i) + ". The house icon represents a stay-at-home order being implemented. On approximately what day was the stay-at-home order implemented in this graph?")
vizcheck1 = record(st.radio, "Vizcheck 1")
vizcheck1("Please make a selection", ["1", "7", "23", "40", "55", "70", "18"])

i += 1

st.subheader(str(i) + ". On Day 20, approximately how many confirmed cases were there?")
vizcheck2 = record(st.radio, "Vizcheck 2")
vizcheck2("Please make a selection.", ("100", "30,000", "8,000", "3,000", "100,000", "250,000"))

i += 1




st.header("Visualization Survey")
st.info("There are three phases to this survey. In Phase 1, you will be answering questions based on visualizations presented to you. In Phase 2, you will get to interact with some visualizations. In Phase 3, you will answer questions again based on visualizations shown to you.")


st.header("Phase 1")
st.subheader("Below, you will be presented with a choice of potential trendlines for three states. The house image\
              signifies when that state put a lockdown order in place (Day 0 indicates the first set of meaningful\
              available data regarding COVID-19 cases). Your job is to identify which trendlines most accurately\
              captures the state's trajectory of confirmed cases after the lockdown order. Use the slider to view\
              the range of different options, and make your selection using the drop-down menu.")
# slot1 = st.empty()
# slot2 = st.empty()
# slot3 = st.empty()
# states = ["ny", "flor", "tex"]
# random.shuffle(states)

# # We want to display them in a random order for each user
# i = 1
# options = ["actual", "less_steep_1", "less_steep_2", "less_steep_3", 
#                       "less_steep_4", "less_steep_5", "steeper_1", "steeper_2", 
#                       "steeper_3", "steeper_4", "steeper_5"]
# full_names = {"ny" : "New York", "flor" : "Florida", "tex" : "Texas"}


# def display_chart(state_trendlines_df, type, slot):
#   test = state_trendlines_df[state_trendlines_df["Type"] == type]
#   test["image_url"] = test["image_url"].fillna("") #necessary because dataframe gets messed up when exporting
#   base = create_base_log_layer(test, 'Day', 'Confirmed')
#   img = create_image_layer(test, 'Day', 'Confirmed', 'image_url')
#   slot.altair_chart(base + img)

# for state in states:
#   generated_trendlines = pd.read_csv("data/{state_name}_generated_trendlines.csv".format(state_name=state))
#   if i == 1:
#     selectbox1 = record(st.selectbox, "Log Scale (Before)")
#     type = selectbox1('Select an option for {full_state_name}.'.format(full_state_name=full_names[state]), options=options)
#     display_chart(generated_trendlines, type, slot1)
#     i += 1
#   elif i == 2:
#     selectbox2 = record(st.selectbox, "Log Scale (Before)")
#     type = selectbox2('Select an option for {full_state_name}.'.format(full_state_name=full_names[state]), options=options)
#     display_chart(generated_trendlines, type, slot2)
#     i += 1
#   elif i == 3:
#     selectbox3 = record(st.selectbox, "Log Scale (Before)")
#     type = selectbox3('Select an option for {full_state_name}.'.format(full_state_name=full_names[state]), options=options)
#     display_chart(generated_trendlines, type, slot3)
#     i += 1





# def display_chart(state_trendlines_df, type):
#   test = state_trendlines_df[state_trendlines_df["Type"] == type]
#   test.loc[:, ["image_url"]] = test["image_url"].fillna("") #necessary because dataframe gets messed up when exporting
#   base = create_base_log_layer(test, 'Day', 'Confirmed')
#   img = create_image_layer(test, 'Day', 'Confirmed', 'image_url')
#   st.altair_chart(base + img)

selectbox1 = record(st.selectbox, "Log Scale (Before)")
type = selectbox1('Select an option for State A.', # Users should not know what the state is
                  options=range(1, 11))
ny_generated_trendlines = pd.read_csv("data/ny_generated_trendlines.csv")
ny_chart = generate_altair_slider_log_chart(ny_generated_trendlines)
st.altair_chart(ny_chart)

selectbox2 = record(st.selectbox, "Log Scale (Before)")
type = selectbox2('Select an option for State B.',
                  options=range(1, 11))
flor_generated_trendlines = pd.read_csv("data/flor_generated_trendlines.csv")
flor_chart = generate_altair_slider_log_chart(flor_generated_trendlines)
st.altair_chart(flor_chart)

selectbox3 = record(st.selectbox, "Log Scale (Before)")
type = selectbox3('Select an option for State C.',
                  options=range(1, 11))
tex_generated_trendlines = pd.read_csv("data/tex_generated_trendlines.csv")
tex_chart = generate_altair_slider_log_chart(tex_generated_trendlines)
st.altair_chart(tex_chart)



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
# st.subheader(str(i) + ". In this situation, State C implemented a lockdown order. How do you think the trajectory for the number of cases changed afterwards? The lockdown order is marked by the house icon on the graph.")
# selectbox3 = record(st.selectbox, "Log Scale (Before)")
# chart_to_show_log = selectbox3("Please predict the trajectory of cases after the lockdown order. You can see and choose the different options by using the dropdown menu.", [i for i in range(1,11)])
# chart = "ny_log/visualization" + str(int(chart_to_show_log) - 1) + ".png"
# st.image(chart, width=800)

# i+=1

# NORMAL TRENDLINES
# --------------------
# st.subheader(str(i) + ". This is the same question as above with an expanded y-axis.")
# slider4 = record(st.selectbox, "Normal Trendline (Before)")
# chart_to_show_normal_trend = slider4("Normal Trendline Chart", [i for i in range(1,11)])
# chart = "ny_trendlines/visualization" + str(int(chart_to_show_normal_trend) - 1) + ".png"
# st.image(chart)

# i += 1

# NEW CASES A DAY 
# --------------------

# TODO: y-axis variable
# TODO: have an easier sub header
# TODO: put all on one chart

st.subheader(str(i) + ". The charts below shows the average number of new cases per day in State A. At some point, a lockdown order was put in place.\
                       Choose which day you think it occurred.")
pick_ny_img = st.radio("", ["Day 12", "Day 31", "Day 50"])
ny_new_cases_actual = generate_new_cases_rolling("New York", 12)
st.altair_chart(ny_new_cases_actual)
ny_new_cases_fake1 = generate_new_cases_rolling("New York", 31)
st.altair_chart(ny_new_cases_fake1)
ny_new_cases_fake2 = generate_new_cases_rolling("New York", 50)
st.altair_chart(ny_new_cases_fake2)

i+=1

st.subheader(str(i) + ". This is the same question as above, but for State B.")
pick_flor_img = st.radio("", ["Day 22", "Day 34", "Day 55"])
flor_new_cases_actual = generate_new_cases_rolling("Florida", 22)
st.altair_chart(flor_new_cases_actual)
flor_new_cases_fake1 = generate_new_cases_rolling("Florida", 34)
st.altair_chart(flor_new_cases_fake1)
flor_new_cases_fake2 = generate_new_cases_rolling("Florida", 55)
st.altair_chart(flor_new_cases_fake2)


i+=1
# Random states - not every user gets the same state

# st.subheader(str(i) + ". Which trendline do you think most accurately represents New York's confirmed\
#   cases of COVID-19 after the lockdown order indicated by the house?")
# ny_cases = create_state_df('New York')
# ny_image = add_image_col_to_df(ny_cases, 12) # Day 12 is when NY had a lockdown order
# alt_chart = generate_single_graph_exponential(ny_image, 12)
# st.altair_chart(alt_chart)
# pick_img = st.radio("", ["1", "2", "3", "4", "5"])

# i+=1

st.header("Phase 2")

st.info("Why do we use a log scale graph for disease modeling? https://www.weforum.org/agenda/2020/04/covid-19-spread-logarithmic-graph/")

# MIDDLE
# -----------------------

st.subheader("Below, we present you with some actual trajectories of confirmed cases for various states. Please study them\
              carefully, and take note of whether seeing these trajectories causes you to change your answers from Phase 1.\
              In Phase 3, we will be asking you to reconsider your answers from Phase 1.")

state_intervention = {"New York": '03-22-2020', "California": '03-19-2020', "Georgia": '04-02-2020', "Illinois": '03-21-2020', "Florida": '04-01-2020', "New Jersey": '03-21-2020', "Arizona": '03-31-2020', "Colorado": '03-26-2020', 'Indiana': '03-25-2020', 'Louisiana': '03-23-2020'}
phase2state = st.selectbox("State (Normal)", ('California', 'Georgia', 'Illinois', 'New Jersey', 'Arizona', 'Colorado', 'Indiana', 'Louisiana'))
alt_chart1 = generate_actual_state_log_chart(phase2state, state_intervention[phase2state])
st.altair_chart(alt_chart1)

st.subheader("Below, we present you with some actual trajectories of average daily cases for various states. Please study them\
              carefully, and take note of whether seeing these trajectories causes you to change your answers from Phase 1.\
              In Phase 3, we will be asking you to reconsider your answers from Phase 1.")
state_intervention_day = {"New York": 12, "California": 9, "Georgia": 23, "Illinois": 11, "Florida": 22, "New Jersey": 11, "Arizona": 21, "Colorado": 16, 'Indiana': 15, 'Louisiana': 13}
phase2stateRolling = st.selectbox("State (Rolling)", ('California', 'Georgia', 'Illinois', 'New Jersey', 'Arizona', 'Colorado', 'Indiana', 'Louisiana'))
alt_chart2 = generate_new_cases_rolling(phase2stateRolling, state_intervention_day[phase2stateRolling])
st.altair_chart(alt_chart2)


st.header("Phase 3")
st.subheader("Below, you will be presented with a choice of potential trendlines for three states. The house image\
              signifies when that state put a lockdown order in place (Day 0 indicates the first set of meaningful\
              available data regarding COVID-19 cases). Your job is to identify which trendlines most accurately\
              captures the state's trajectory of confirmed cases after the lockdown order. Use the slider to view\
              the range of different options, and make your selection using the drop-down menu.")



selectbox1_phase3 = record(st.selectbox, "Log Scale (Before)")
type = selectbox1('Select your revised option for State A.', # Users should not know what the state is
                  options=range(1, 11))
ny_generated_trendlines = pd.read_csv("data/ny_generated_trendlines.csv")
ny_chart = generate_altair_slider_log_chart(ny_generated_trendlines)
st.altair_chart(ny_chart)

selectbox2_phase3 = record(st.selectbox, "Log Scale (Before)")
type = selectbox2('Select your revised option for State B.',
                  options=range(1, 11))
flor_generated_trendlines = pd.read_csv("data/flor_generated_trendlines.csv")
flor_chart = generate_altair_slider_log_chart(flor_generated_trendlines)
st.altair_chart(flor_chart)

selectbox3_phase3 = record(st.selectbox, "Log Scale (Before)")
type = selectbox3('Select your revised option for State C.',
                  options=range(1, 11))
tex_generated_trendlines = pd.read_csv("data/tex_generated_trendlines.csv")
tex_chart = generate_altair_slider_log_chart(tex_generated_trendlines)
st.altair_chart(tex_chart)

st.subheader(str(i) + ". The charts below shows the average number of new cases per day in State A. At some point, a lockdown order was put in place.\
                       Choose which day you think it occurred.")
pick_ny_img_phase3 = st.radio("Pick a revised option.", ["Day 12", "Day 31", "Day 50"])
ny_new_cases_actual = generate_new_cases_rolling("New York", 12)
st.altair_chart(ny_new_cases_actual)
ny_new_cases_fake1 = generate_new_cases_rolling("New York", 31)
st.altair_chart(ny_new_cases_fake1)
ny_new_cases_fake2 = generate_new_cases_rolling("New York", 50)
st.altair_chart(ny_new_cases_fake2)

i+=1

st.subheader(str(i) + ". This is the same question as above, but for State B.")
pick_flor_img_phase3 = st.radio("Pick a revised option", ["Day 22", "Day 34", "Day 55"])
flor_new_cases_actual = generate_new_cases_rolling("Florida", 22)
st.altair_chart(flor_new_cases_actual)
flor_new_cases_fake1 = generate_new_cases_rolling("Florida", 34)
st.altair_chart(flor_new_cases_fake1)
flor_new_cases_fake2 = generate_new_cases_rolling("Florida", 55)
st.altair_chart(flor_new_cases_fake2)


i+=1


st.header("Conclusion")


st.info("Thank you so much for participating! Click submit below. \n\n After submitting your responses, you can protect your privacy by clearing your browser’s history, cache, cookies, and other browsing data. (Warning: This will log you out of online services.)")
widget_values["id"] = 10
import json 
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
        
    response = requests.post('http://covidvis-api.herokuapp.com/send/', data=widget_values)
    st.info("Please record this ID down and enter it in the appropriate place in MTurk to signify your completion.")
    
    st.info(response.body)
    st.info(hash(str(response)))


        
# TODO: Collect more feedback from the study
# TODO: Number the questions
# TODO: Add progress bar
        


# Overlays of lines to provide context to the user when picking (highlight line when picked)

# Generate random trends to reduce bias
# Generate lines independent of the true line, which of these random lines do you think are closest to the true line
# Random sample of trends (reduce bias of the true line, ex. no median picking should be the answer)

# Plot the rate of change versus cumulative (log scale)
#st.write("Recorded values: ", widget_values)
