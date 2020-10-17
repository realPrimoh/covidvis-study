import streamlit as st
import pandas as pd
#import geopandas as gpd
import numpy as np
import csv
import datetime
import collections

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
st.title('CovidVis User Study')

st.info("Welcome to the Covidvis User Study. In this study, we are trying to measure the effects of seeing visualizations of COVID's ascent throughout the world on people's opinions about COVID interventions. Your data will be kept confidential and you will maintain anonymity.")

st.info("Consent to take part in the study: \n\n I am asking you to participate in a research study titled “The Impact of Visualizations on Perception of COVID-19 Intervention Measures”. I will describe this study to you and answer any of your questions. \n\n This study is being led by Aditya Parameswaran, Priyam Mohanty, Murtaza Ali, Doris Lee, and B. Aditya Prakash, a research team from UC Berkeley and Georgia Tech.")

st.info("What the study is about:\n\nThe purpose of this research is to examine the impact of visualizations on COVID-19 intervention perception.")

st.info("What we will ask you to do:\n\nIf you agree to take part, you will be asked to complete a questionnaire and provide your opinions. The survey will last approximately 15 minutes and will be conducted online.")

st.info("Risks and discomforts:\n\nThere is little risk to you in taking part in this research. As with all research there is a chance that confidentiality may be compromised; however, we will take the following precautions to minimize this risk: Your study data will be treated as confidentially as possible. The data will be stored on a password protected laptop. None of your personal information is collected.")

st.info("Benefits:\n\nThere are no direct benefits to you from this research. It is our hope that the research will benefit the scientific community and lead to a greater understanding of visualizations and their effects on people's understanding of things.")

st.info("Privacy/Confidentiality/Data Security:\n\nAll data will be de-identified with identifiers. Consent forms will be kept separate from the rest of the research data. All physical data will be stored in locked cabinets accessible only by the Principal Researcher. All electronic data will be stored on password protected servers accessible only by the Principal Researcher. We anticipate that your participation in this survey presents no greater risk than everyday use of the Internet.")

st.info("Taking part is voluntary\n\nYour involvement in this research is voluntary, and you may refuse to participate before the study begins or discontinue at any time. You will only receive compensation for this study if you complete all tasks and survey questions.")

st.info("If you have questions:\n\nThe main researchers conducting this study Aditya Parameswaran, Priyam Mohanty, and Murtaza Ali. Please ask any questions you have now. If you have questions later, you may contact Aditya Parameswaran at adityagp@berkeley.edu.  If you have any questions or concerns regarding your rights as a subject in this study, you may contact the Institutional Review Board (IRB) for Human Participants at https://cphs.berkeley.edu. ")
st.info("Statement of Consent:\n\nBy continuing with this survey, you are consenting to the above statements.")


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

st.subheader(str(i) + ". On Day 35, how many confirmed cases were there?")
st.image("./ny_trendlines/actual.png", width=800)
vizcheck1 = record(st.radio, "Vizcheck 1")
vizcheck1("How many confirmed cases were on Day 35?", ("1,000", "2,000", "20,000", "100,000", "200,000", "250,000"))

i += 1

#st.subheader(str(i) + ". The house icon represents a stay-at-home order being implemented. On approximately what day was the stay-at-home order implemented in this graph?")
#st.image("ny_intervention_cumulative/actual.png", width=800)
#vizcheck2 = record(st.radio, "Vizcheck 2")
#vizcheck2("On approximately what day was the stay-at-home order implemented in this graph?", ["1", "2", "5", "8", "10", "12", "15", "18"])
#
#i += 1

st.subheader(str(i) + ". The house icon represents a stay-at-home order being implemented. On approximately what day was the stay-at-home order implemented in this graph?")
st.image("ny_log/actual.png", width=800)
vizcheck2 = record(st.radio, "Vizcheck 2")
vizcheck2("On approximately what day was the stay-at-home order implemented in this graph?", ["1", "2", "5", "9", "12", "15", "18"])

i += 1


st.header("Visualization Survey")
st.info("There are three phases to this survey. In Phase 1, you will be answering questions based on visualizations presented to you. In Phase 2, you will get to interact with some visualizations. In Phase 3, you will answer questions again based on visualizations shown to you.")


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

st.info("Why do we use a log scale graph for disease modeling? https://www.weforum.org/agenda/2020/04/covid-19-spread-logarithmic-graph/")

# MIDDLE
# -----------------------

st.header("Here are some examples of where lockdown orders were put in place.")

state_intervention = {"New York": '03-22-2020', "California": '03-10-2020', "Georgia": '04-02-2020', "Illinois": '03-19-2020', "Florida": '04-01-2020'}
phase2state = st.selectbox("State (Normal)", ('New York', 'California', 'Georgia', 'Illinois', 'Florida'))
alt_chart1 = generate_state_chart_normal(phase2state, state_intervention[phase2state])
st.altair_chart(alt_chart1)

phase2stateRolling = st.selectbox("State (Rolling Average)", ('New York', 'California', 'Georgia', 'Illinois', 'Florida'))
alt_chart2 = generate_intervention_images_new_cases_rolling(phase2stateRolling, state_intervention[phase2stateRolling])
st.altair_chart(alt_chart2)


st.image("ny_interventions_new_day/actual.png", width=800)
st.image("ny_log/actual.png", width=800)

""" TEMPORARY CODE BELOW TO TEST SOMETHING 
footprints = pd.read_csv("./data/interventionFootprintByState.csv")
footprints['dateBefore'] = pd.to_datetime(footprints['dateBefore']) # Makes date easier to work with
state_geodata = alt.topo_feature(data.us_10m.url, 'states')
hurricanes = pd.read_csv(data.population_engineers_hurricanes.url)[['state', 'id']]
# Convert timedelta to days
# Source https://stackoverflow.com/questions/18215317/extracting-days-from-a-numpy-timedelta64-value

earliest_date = footprints.sort_values('dateBefore')['dateBefore'].values[0]
def days_passed(date):
    return int((date - earliest_date) / np.timedelta64(1, 'D'))
footprints['days_since_Feb_28th'] = footprints['dateBefore'].apply(days_passed)
# Below, we add the ID values for states which will enable us to map to the geodata.
footprints_with_ids = footprints.merge(hurricanes, how='left', left_on='State', right_on='state').drop(['Unnamed: 0', 'state'], axis=1)
footprints_with_ids = footprints_with_ids.loc[: , ['interventionFootprint', 'State', 'days_since_Feb_28th', 'id']] # Isolate the values we need
footprints_with_ids = footprints_with_ids.rename(columns={'State' : 'state'})
def extend_state_dict(state_dict):
    result_dict = state_dict.copy()
    empty_list = [0 for x in range(61)]
    interventions, states, days, ids = empty_list[:], empty_list[:], empty_list[:], empty_list[:]
    
    # We start by setting the existing ones
    for key, val in state_dict['days_since_Feb_28th'].items():
        days[val] = val
        interventions[val] = state_dict['interventionFootprint'][key]
        states[val] = state_dict['state'][key]
        ids[val] = state_dict['id'][key]
        
    # Populate state, days and id, the easy ones as they are constant/known
    for i in range(len(states)):
        states[i] = list(state_dict['state'].values())[0]
        ids[i] = list(state_dict['id'].values())[0]
        days[i] = i
    
    # Now for interventions, the whole reason we are doing this
    # We need to populate the empty days with the most recent one
    # For days before the first intervention footprint, we use a value of 0 for now
    
    curr_footprint = 0
    for i in range(len(interventions)):
        if interventions[i] != 0:
            curr_footprint = interventions[i]
        else:
            interventions[i] = curr_footprint
    
    result_dict['interventionFootprint'] = interventions
    result_dict['state'] = states
    result_dict['days_since_Feb_28th'] = days
    result_dict['id'] = ids
    
    return result_dict


def combine_state_dicts(first, second):
    combined_dict = first.copy()
    for key in combined_dict:
        combined_dict[key].extend(second[key])
    return combined_dict
state_set = set(footprints_with_ids['state'].values) # Get all the states
state_dicts = []
for state in state_set:
    state_dict = footprints_with_ids[footprints_with_ids['state'] == state].to_dict()
    state_dicts.append(extend_state_dict(state_dict)) # Fill in the missing values
    
# We imported the reduce function from the functools module at the top of this notebook
# It takes in a function and an iterable, and combines all values of the iterable together into one value using the function

extended_footprint_df = pd.DataFrame.from_dict(reduce(combine_state_dicts, state_dicts))
# I had to alter this file on my Desktop to get rid of the county data; otherwise, it would just overlook state data for some reason.
state_geomap_data_edited = gpd.read_file('./data/us-10m.json', driver='TopoJSON')
# Ensures consistency of types when we merge
state_geomap_data_edited.id = state_geomap_data_edited.id.astype(int)
extended_footprint_df.id = extended_footprint_df.id.astype(int)
footprints_with_geodata_df = state_geomap_data_edited.merge(extended_footprint_df, on='id', how='inner') # Keep on the left to maintain geodataframe
slider = alt.binding_range(min=0, max=60, step=1) # We set the range of our time slider (60 days in this case)

select_day = alt.selection_single(name="days_since_Feb_28th", fields=['days_since_Feb_28th'],
                                   bind=slider, init={'days_since_Feb_28th': 0})

cpleth = alt.Chart(footprints_with_geodata_df).mark_geoshape().encode(
    alt.Color('interventionFootprint:Q', scale=alt.Scale(domain=(0.0, 1.02))) # We set the possible range for intervention footprint values
).properties(
    width=700,
    height=500
).add_selection(
    select_day
).project(
    type='albersUsa'
).transform_filter(
    select_day
).resolve_scale(
    color='independent'
)
st.altair_chart(cpleth)
"""
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
@st.cache
def generate_log(chart_to_show):
  chart = "ny_log/visualization" + str(int(chart_to_show_log_after) - 1) + ".png"
  return chart
st.subheader(str(i) + ". In this situation, State C implemented a lockdown order. How do you think the trajectory for the number of cases changed afterwards? The lockdown order is marked by the house icon on the graph.")
slider7 = record(st.select_slider, "Log Scale (After)")
chart_to_show_log_after = slider7("Pick the chart that seems the most correct to you. The x-axis represents the number of days, while the y-axis represents the number of COVID-19 cases.", [i for i in range(1,11) for _ in range(5)])
chart = generate_log(chart_to_show_log_after)
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
chart_to_show_casesday_lockdown_after = slider9("Pick the chart that seems the most correct to you. The x-axis represents the number of days, while the y-axis represents the average number of COVID-19 cases confirmed on each day.", [i for i in range(1,4) for _ in range(5)])
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
