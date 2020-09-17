import streamlit as st
import pandas as pd
import numpy as np
import csv

st.title('CovidVis User Study')

st.info("Welcome to the Covidvis User Study. In this study, we are trying to measure the effects of seeing visualizations of COVID's ascent throughout the world on people's opinions about COVID interventions. Your data will be kept confidential and you will maintain anonymity.")

widget_values = {}


def record(f, widgetLabel):
    """Return a function that wraps a streamlit widget and records the
    widget's values to a global dictionary.
    """
    def wrapper(label, *args, **kwargs):
        widget_value = f(label, *args, **kwargs)
        widget_values[widgetLabel] = widget_value
        return widget_value

    return wrapper

st.header("Demographical Information")

st.subheader("What is your age?")
ageSlider = record(st.slider, "Age")
age = ageSlider("Age", 18, 80)

st.subheader("What state are you from?")
stateSelect = record(st.selectbox, "State")
stateSelect("State", ["AL", "AK", "AZ", "AR", "CA", "CO", "CT", "DC", "DE", "FL", "GA", 
          "HI", "ID", "IL", "IN", "IA", "KS", "KY", "LA", "ME", "MD", 
          "MA", "MI", "MN", "MS", "MO", "MT", "NE", "NV", "NH", "NJ", 
          "NM", "NY", "NC", "ND", "OH", "OK", "OR", "PA", "RI", "SC", 
          "SD", "TN", "TX", "UT", "VT", "VA", "WA", "WV", "WI", "WY"])

st.subheader("What is your gender?")
genderSel = record(st.selectbox, "Gender")
genderSel("Gender", ('Male', 'Female'))

st.subheader("What political party do you affiliate with?")
partySel = record(st.selectbox, "Political Party")
partySel("Party", ('D', 'R', 'Ind'))

st.subheader("What is your race or ethnicity?")
raceSel = record(st.selectbox, "Race")
raceSel("Race", ("Asian", "White", "African-American", "Etc."))

st.subheader("What is your highest level of education?")
eduSel = record(st.selectbox, "Education Level")
eduSel("Education Level", ("High School", "Some College", "Bachelors", "Masters", "Doctorate"))

st.subheader("How many days a week do you view coronavirus related info (articles, data, press releases, etc.)?")
virusInfoSel = record(st.selectbox, "Days a week consuming virus information")
virusInfoSel("Viewing", ("0", "1", "2", "3", "4", "5", "6", "7"))

st.subheader("Do you believe in wearing a mask?")
maskSel = record(st.selectbox, "Mask Belief")
maskSel("Mask Belief", ("Yes", "No"))

st.subheader("For each of the following orders, how effective are they?")
radio1 = record(st.radio, "Stay-at-home Effectiveness")
radio2 = record(st.radio, "Social Distancing Effectiveness")
radio3 = record(st.radio, "Mask On Effectiveness")
radio4 = record(st.radio, "Closing Bars/Restaurants Effectiveness")

radio1("Stay-at-home", ["Strongly Ineffective", "Slightly Ineffective", "Neutral", "Somewhat Effective", "Strongly Effective"])
radio2("Social distancing", ["Strongly Ineffective", "Slightly Ineffective", "Neutral", "Somewhat Effective", "Strongly Effective"])
radio3("Masks on", ["Strongly Ineffective", "Slightly Ineffective", "Neutral", "Somewhat Effective", "Strongly Effective"])
radio4("Closing bars/restaurants", ["Strongly Ineffective", "Slightly Ineffective", "Neutral", "Somewhat Effective", "Strongly Effective"])

#

st.header("Phase 1")

# NORMAL INTERVENTIONS
# ----------------

st.subheader("State A hadn't implemented a stay-at-home order at any point shown on the graph. Here, the graph's x-axis shows the number of days after the first case is recorded. What do you think is the trajectory of virus cases?")
#What do you think... (TODO: language)

slider1 = record(st.select_slider, "Trajectory w/ No Stay-At-Home Order (Before)")
chart_to_show = slider1("Trajectory", [i for i in range(1,7) for _ in range(5)])
chart = "visualization/visualization" + str(int(chart_to_show)) + ".png"
st.image(chart)

# PICK WHERE IT IS 
# --------------------

st.subheader("In this situation, State B implemented a lockdown order. Where on the curve do you think the lockdown order was put in place?")

slider2 = record(st.select_slider, "Lockdown Order (Before)")
chart_to_show_intervention = slider2("Lockdown Order", [i for i in range(1,4) for _ in range(5)])
chart = "intervention/visualization" + str(int(chart_to_show_intervention) - 1) + ".png"
st.image(chart)

# LOG SCALE 
# ----------------------
st.subheader("In this situation, State C implemented a lockdown order. How do you think the trajectory for the number of cases changed afterwards? The lockdown order is marked by the house icon on the graph.")
slider3 = record(st.select_slider, "Log Scale (Before)")
chart_to_show_log = slider3("Log Scale Chart", [i for i in range(1,11) for _ in range(5)])
chart = "ny_log/visualization" + str(int(chart_to_show_log) - 2) + ".png"
st.image(chart)

# NORMAL TRENDLINES
# --------------------
st.subheader("This is the same question as above with an expanded y-axis.")
slider4 = record(st.select_slider, "Normal Trendline (Before)")
chart_to_show_normal_trend = slider4("Normal Trendline Chart", [i for i in range(1,11) for _ in range(5)])
chart = "ny_trendlines/visualization" + str(int(chart_to_show_normal_trend) - 1) + ".png"
st.image(chart)

# NEW CASES A DAY 
# --------------------

st.subheader("This chart shows the amount of new cases per day. At some point, a lockdown order was put in place. Can you guess where?")
slider5 = record(st.select_slider, "Pin the Lockdown on Smoothed Average Cases (Before)")
chart_to_show_casesday_lockdown = slider5("Cases per Day Lockdown Order Guess", [i for i in range(1,4) for _ in range(5)])
chart = "ny_interventions_new_day/visualization" + str(int(chart_to_show_casesday_lockdown) - 1) + ".png"
st.image(chart)

# Random states - not every user gets the same state

st.header("Phase 2")

# MIDDLE
# -----------------------

st.header("Here are some examples of where lockdown orders were put in place.")
st.image("ny_intervention_cumulative/actual.png", width=800)
st.image("ny_interventions_new_day/actual.png", width=800)
st.image("ny_log/actual.png", width=800)
st.image("ny_trendlines/actual.png", width=800)


st.header("Phase 3")

st.subheader("State A hadn't implemented a stay-at-home order at any point shown on the graph. Here, the graph's x-axis shows the number of days after the first case is recorded. What do you think is the trajectory of virus cases?")
#What do you think... (TODO: language)

slider0 = record(st.select_slider, "Trajectory w/ No Stay-At-Home Order (After)")
chart_to_show_traj_after = slider0("Trajectory (After)", [i for i in range(1,7) for _ in range(5)])
chart = "visualization/visualization" + str(int(chart_to_show_traj_after)) + ".png"
st.image(chart)


# PICK WHERE IT IS 
# --------------------

st.subheader("In this situation, State B implemented a lockdown order. Where on the curve do you think the lockdown order was put in place?")

slider6 = record(st.select_slider, "Lockdown Order (After)")
chart_to_show_after = slider6("Lockdown Order (After)", [i for i in range(1,5) for _ in range(5)])
chart = "intervention/visualization" + str(int(chart_to_show_after) - 1) + ".png"
st.image(chart)

# LOG SCALE 
# ----------------------
st.subheader("Log scale description")
slider7 = record(st.select_slider, "Log Scale (After)")
chart_to_show_log_after = slider7("Log Scale Chart (after)", [i for i in range(1,11) for _ in range(5)])
chart = "ny_log/visualization" + str(int(chart_to_show_log_after) - 2) + ".png"
st.image(chart)

# NORMAL TRENDLINES
# --------------------
st.subheader("Normal trendline description")
slider8 = record(st.select_slider, "Normal Trendline (After)")
chart_to_show_normal_trend_after = slider8("Normal Trendline Chart (After)", [i for i in range(1,11) for _ in range(5)])
chart = "ny_trendlines/visualization" + str(int(chart_to_show_normal_trend_after) - 1) + ".png"
st.image(chart)

# NEW CASES A DAY 
# --------------------

st.subheader("This chart shows the amount of new cases per day. At some point, a lockdown order was put in place. Can you guess where?")
slider9 = record(st.select_slider, "Pin the Lockdown on Smoothed Average Cases (After)")
chart_to_show_casesday_lockdown_after = slider9("Cases per Day Lockdown Order Guess (After)", [i for i in range(1,4) for _ in range(5)])
chart = "ny_interventions_new_day/visualization" + str(int(chart_to_show_casesday_lockdown_after) - 1) + ".png"
st.image(chart)

st.header("Conclusion")

st.info("Thank you so much for participating!")



# Overlays of lines to provide context to the user when picking (highlight line when picked)

# Generate random trends to reduce bias
# Generate lines independent of the true line, which of these random lines do you think are closest to the true line
# Random sample of trends (reduce bias of the true line, ex. no median picking should be the answer)

# Plot the rate of change versus cumulative (log scale)
st.write("Recorded values: ", widget_values)

if st.button("Submit"):
    field_names = widget_values.keys()
    with open('data.csv', 'w') as csvfile:
        writer = csv.DictWriter(csvfile, fieldnames=field_names)
        writer.writeheader()
        writer.writerows([widget_values])
