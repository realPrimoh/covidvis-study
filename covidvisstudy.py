import streamlit as st
import pandas as pd
import numpy as np
import csv
import datetime
import collections
import requests

from random import random
import SessionState
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
st.markdown("Please check the box below to continue. By continuing with this survey and submitting your response, you are consenting to the above statements. If you do not consent, please exit the survey now.")

consent = st.checkbox("I consent")
if consent:
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

    st.subheader("What platform are you using?")
    platformSel = record(st.radio, "Platform")
    platform = st.radio("Platform", ("MTurk", "Prolific", "Other"))

    if platform != "Other":
        st.subheader("Enter your " + platform + " ID here.")
        mturkSel = record(st.text_input, platform + " ID")
        mturk = mturkSel(platform + " ID")

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

    st.subheader(str(i) + ". Attention check: Do you agree with this?")
    agree1 = record(st.radio, "Botcheck 1")
    agree1("Select Slightly Agree.", ["Strongly Disagree", "Slightly Disagree", "Neutral", "Slightly Agree", "Strongly Agree"])

    i += 1

    st.subheader(str(i) + ". What is your occupation?")
    occupationSel = record(st.text_input, "Occupation")
    occupation = occupationSel("Occupation")

    i += 1

    st.subheader(str(i) + ". How many times a week do you view coronavirus related info (articles, data, press releases, etc.)?")
    virusInfoSel = record(st.selectbox, "Times a week consuming virus information")
    virusInfoSel("Viewing", ("Select...", "0-5", "5-10", "10+"))

    i += 1

    # TODO: Add spam-checker questions (Select 'agree', etc...)

    st.subheader(str(i) + ". For each of the following orders, how effective are they to you?")
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


    show_phase2 = False
    
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


    ny_generated_trendlines = pd.read_csv("final_data/ny_generated_trendlines.csv")
    ny_chart = generate_altair_slider_log_chart(ny_generated_trendlines, "State A")
    st.altair_chart(ny_chart)
    selectbox1 = record(st.selectbox, "Log Scale (Before)")
    type = selectbox1('Please confirm your selection for State A.', # Users should not know what the state is
                      options=range(1, 11))

    st.text("")
    st.text("")
    st.text("")
    st.text("")
    st.text("")
    st.text("")
    st.text("")
    st.text("")

    flor_generated_trendlines = pd.read_csv("final_data/flor_generated_trendlines.csv")
    flor_chart = generate_altair_slider_log_chart(flor_generated_trendlines, "State B")
    st.altair_chart(flor_chart)
    selectbox2 = record(st.selectbox, "Log Scale (Before)")
    type = selectbox2('Please confirm your selection for State B.',
                      options=range(1, 11))

    st.text("")
    st.text("")
    st.text("")
    st.text("")
    st.text("")
    st.text("")
    st.text("")
    st.text("")

    tex_generated_trendlines = pd.read_csv("final_data/tex_generated_trendlines.csv")
    tex_chart = generate_altair_slider_log_chart(tex_generated_trendlines, "State C")
    st.altair_chart(tex_chart)
    selectbox3 = record(st.selectbox, "Log Scale (Before)")
    type = selectbox3('Please confirm your selection for State C.',
                      options=range(1, 11))

    st.text("")
    st.text("")
    st.text("")
    st.text("")
    st.text("")
    st.text("")
    st.text("")
    st.text("")


    st.subheader(str(i) + ". The charts below shows the average number of new cases per day in State A. At some point, a lockdown order was put in place.\
                           Choose which day you think it occurred.")
    pick_ny_img = st.radio("", ["Day 12", "Day 31", "Day 50"])

    col1, col2, col3 = st.beta_columns(3)
    ny_new_cases_actual = generate_new_cases_rolling("New York", 12, width=400, height=300, title="Day 12")
    col1.altair_chart(ny_new_cases_actual)
    col2.text("")
    ny_new_cases_fake1 = generate_new_cases_rolling("New York", 31, width=400, height=300, title="Day 31")
    col3.altair_chart(ny_new_cases_fake1)
    ny_new_cases_fake2 = generate_new_cases_rolling("New York", 50, width=400, height=300, title="Day 50")
    st.altair_chart(ny_new_cases_fake2)

    i+=1

    st.subheader(str(i) + ". This is the same question as above, but for State B.")
    pick_flor_img = st.radio("", ["Day 22", "Day 34", "Day 50"])

    col1, col2, col3 = st.beta_columns(3)
    flor_new_cases_actual = generate_new_cases_rolling("Florida", 22, width=400, height=300, title="Day 22")
    col1.altair_chart(flor_new_cases_actual)
    col2.text("")
    flor_new_cases_fake1 = generate_new_cases_rolling("Florida", 34, width=400, height=300, title="Day 34")
    col3.altair_chart(flor_new_cases_fake1)
    flor_new_cases_fake2 = generate_new_cases_rolling("Florida", 50, width=400, height=300, title="Day 50")
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

    show_phase3 = False

    st.header("Phase 2")

    st.info("Why do we use a log scale graph for disease modeling? Log scales allow us to assess the trend of a disease, which is whether the spread is getting faster, slower, or staying the same. For more information, see here: https://www.weforum.org/agenda/2020/04/covid-19-spread-logarithmic-graph/")

    # MIDDLE
    # -----------------------
    session_state = SessionState.get(looked_at=0, _next = False)


    state_intervention = {"New York": '03-22-2020', "California": '03-19-2020', "Georgia": '04-02-2020', "Illinois": '03-21-2020', "Florida": '04-01-2020', "New Jersey": '03-21-2020', "Arizona": '03-31-2020', "Colorado": '03-26-2020', 'Indiana': '03-25-2020', 'Louisiana': '03-23-2020'}
    states = ['California', 'Georgia', 'Illinois', 'New Jersey', 'Arizona', 'Colorado', 'Indiana', 'Louisiana']
    st.write("Look through at least 3 states' graphs and try to see if you can find a pattern with the effects of lockdowns on the COVID-19 case trendline.")
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
                st.subheader("Below, we present a choice of possible trajectories for Georgia, identical to what you saw in Phase 1.\
                              Please choose the trajectory you think is correct.")
                # TODO (Murtaza): These lines below signify where to put in your code for the "Phase 2 Questions" trendlines
                georgia_generated_trendlines = pd.read_csv("data/georgia_generated_trendlines.csv")
                georgia_chart = generate_altair_slider_log_chart_KEEP_ACTUAL(georgia_generated_trendlines)
                # georgia_generated_trendlines.loc[:, ["image_url"]] = georgia_generated_trendlines["image_url"].fillna("")
                # base = create_base_log_layer(georgia_generated_trendlines[georgia_generated_trendlines["Type"] == "actual"], "Day", "Confirmed")
                # img = create_image_layer(georgia_generated_trendlines[georgia_generated_trendlines["Type"] == "actual"], "Day", "Confirmed", "image_url")
                st.altair_chart(georgia_chart)
                # TODO (Murtaza): Change the wording of "Is this correct?"
                x = st.selectbox("Which number is the correct trendline for Georgia?", ["Select...", ] + [str(i) for i in range(1, 12)])
                if x == "6":
                    st.info("Correct! Try one more.")
                     # TODO (Murtaza): These lines below signify where to put in your code for the "Phase 2 Questions" trendlines. This is question #2 which is after the person answers Question 1
                    georgia_generated_trendlines = pd.read_csv("data/georgia_generated_trendlines.csv")
                    georgia_chart = generate_altair_slider_log_chart_KEEP_ACTUAL(georgia_generated_trendlines)
                    # georgia_generated_trendlines.loc[:, ["image_url"]] = georgia_generated_trendlines["image_url"].fillna("")
                    # base = create_base_log_layer(georgia_generated_trendlines[georgia_generated_trendlines["Type"] == "actual"], "Day", "Confirmed")
                    # img = create_image_layer(georgia_generated_trendlines[georgia_generated_trendlines["Type"] == "actual"], "Day", "Confirmed", "image_url")
                    st.altair_chart(georgia_chart)
                    # TODO (Murtaza): Change the wording of "Is this correct?"
                    y = st.selectbox("Which number is the correct trendline for [insert]?", ["Select...", ] + [str(i) for i in range(1, 12)])
                    if y == '6': # May need to change for different state
                        st.info("Correct! Now, you can move on to Phase 3.")
                        show_phase3 = True
                    elif y in [str(i) for i in range(1, 12) if i != 6]:
                        st.info("Try again!")
                    else:
                        pass
                elif x in [str(i) for i in range(1, 12) if i != 6]:
                    st.info("Try again!")
                else:
                    pass



    # FLOW: 1. Pick a state:
    # 2. Here's the trajectory of the state. Once you're done looking, click next.
    # 3. What is the trajectory closest to you

    #st.subheader("Below, we present you with some actual trajectories of confirmed cases for various states. Please study them\
    #              carefully, and take note of whether seeing these trajectories causes you to change your answers from Phase 1.\
    #              In Phase 3, we will be asking you to reconsider your answers from Phase 1.")
    #
    #phase2state = st.selectbox("State (Normal)", ('California', 'Georgia', 'Illinois', 'New Jersey', 'Arizona', 'Colorado', 'Indiana', 'Louisiana'))
    #alt_chart1 = generate_actual_state_log_chart(phase2state, state_intervention[phase2state])
    #st.altair_chart(alt_chart1)
    #
    #st.subheader("Below, we present you with some actual trajectories of average daily cases for various states. Please study them\
    #              carefully, and take note of whether seeing these trajectories causes you to change your answers from Phase 1.\
    #              In Phase 3, we will be asking you to reconsider your answers from Phase 1.")
    #state_intervention_day = {"New York": 12, "California": 9, "Georgia": 23, "Illinois": 11, "Florida": 22, "New Jersey": 11, "Arizona": 21, "Colorado": 16, 'Indiana': 15, 'Louisiana': 13}
    #phase2stateRolling = st.selectbox("State (Rolling)", ('California', 'Georgia', 'Illinois', 'New Jersey', 'Arizona', 'Colorado', 'Indiana', 'Louisiana'))
    #alt_chart2 = generate_new_cases_rolling(phase2stateRolling, state_intervention_day[phase2stateRolling], width=600, height=400)
    #st.altair_chart(alt_chart2)

    if show_phase3:
        st.header("Phase 3")
        st.subheader("Below, you will be presented with the same questions you answered from Phase 1. You should revise your choices based\
                      on the actual trajectories you studied in Phase 2. If your answers have not changed, please make \
                      the same selections again. Use the slider to view the range of different options, and make your selection\
                      using the drop-down menu.")




        ny_generated_trendlines = pd.read_csv("final_data/ny_generated_trendlines.csv")
        ny_chart = generate_altair_slider_log_chart(ny_generated_trendlines, title="State A")
        st.altair_chart(ny_chart)
        selectbox1_phase3 = record(st.selectbox, "Log Scale (Before)")
        type = selectbox1('Please confirm your revised option for State A.', # Users should not know what the state is
                          options=range(1, 11))

        st.text("")
        st.text("")
        st.text("")
        st.text("")
        st.text("")
        st.text("")
        st.text("")
        st.text("")


        flor_generated_trendlines = pd.read_csv("final_data/flor_generated_trendlines.csv")
        flor_chart = generate_altair_slider_log_chart(flor_generated_trendlines, title="State B")
        st.altair_chart(flor_chart)
        selectbox2_phase3 = record(st.selectbox, "Log Scale (Before)")
        type = selectbox2('Please confirm your revised option for State B.',
                          options=range(1, 11))

        st.text("")
        st.text("")
        st.text("")
        st.text("")
        st.text("")
        st.text("")
        st.text("")
        st.text("")


        tex_generated_trendlines = pd.read_csv("final_data/tex_generated_trendlines.csv")
        tex_chart = generate_altair_slider_log_chart(tex_generated_trendlines, title="State C")
        st.altair_chart(tex_chart)
        selectbox3_phase3 = record(st.selectbox, "Log Scale (Before)")
        type = selectbox3('Please confirm your revised option for State C.',
                          options=range(1, 11))

        st.text("")
        st.text("")
        st.text("")
        st.text("")
        st.text("")
        st.text("")
        st.text("")
        st.text("")

        st.subheader(str(i) + ". The charts below shows the average number of new cases per day in State A. At some point, a lockdown order was put in place.\
                               Choose which day you think it occurred.")
        pick_ny_img_phase3 = st.radio("Pick a revised option.", ["Day 12", "Day 31", "Day 50"])
        col1, col2, col3 = st.beta_columns(3)
        ny_new_cases_actual = generate_new_cases_rolling("New York", 12, width=400, height=300, title="Day 12")
        col1.altair_chart(ny_new_cases_actual)
        col2.text("")
        ny_new_cases_fake1 = generate_new_cases_rolling("New York", 31, width=400, height=300, title="Day 31")
        col3.altair_chart(ny_new_cases_fake1)
        ny_new_cases_fake2 = generate_new_cases_rolling("New York", 50, width=400, height=300, title="Day 50")
        st.altair_chart(ny_new_cases_fake2)

        i+=1

        st.subheader(str(i) + ". This is the same question as above, but for State B.")
        pick_flor_img_phase3 = st.radio("Pick a revised option", ["Day 22", "Day 34", "Day 55"])
        col1, col2, col3 = st.beta_columns(3)
        flor_new_cases_actual = generate_new_cases_rolling("Florida", 22, width=400, height=300, title="Day 22")
        col1.altair_chart(flor_new_cases_actual)
        col2.text("")
        flor_new_cases_fake1 = generate_new_cases_rolling("Florida", 34, width=400, height=300, title="Day 34")
        col3.altair_chart(flor_new_cases_fake1)
        flor_new_cases_fake2 = generate_new_cases_rolling("Florida", 55, width=400, height=300, title="Day 55")
        st.altair_chart(flor_new_cases_fake2)


        i+=1
        
        st.subheader(str(i) + ". For each of the following orders, how effective are they to you?")
        radio1phase3 = record(st.selectbox, "Stay-at-home Effectiveness (Phase 3)")
        radio2phase3 = record(st.selectbox, "Social Distancing Effectiveness (Phase 3)")
        radio3phase3 = record(st.selectbox, "Mask On Effectiveness (Phase 3)")
        radio4phase3 = record(st.selectbox, "Closing Bars/Restaurants Effectiveness (Phase 3)")
        i += 1
        
        radio1phase3("Stay-at-home (Phase 3)", ["Select...", "Strongly Ineffective", "Slightly Ineffective", "Neutral", "Somewhat Effective", "Strongly Effective"])
        radio2phase3("Social distancing (Phase 3)", ["Select...", "Strongly Ineffective", "Slightly Ineffective", "Neutral", "Somewhat Effective", "Strongly Effective"])
        radio3phase3("Masks on (Phase 3)", ["Select...", "Strongly Ineffective", "Slightly Ineffective", "Neutral", "Somewhat Effective", "Strongly Effective"])
        radio4phase3("Closing bars/restaurants (Phase 3)", ["Select...", "Strongly Ineffective", "Slightly Ineffective", "Neutral", "Somewhat Effective", "Strongly Effective"])


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
            if platform == "MTurk":
                st.info("Please record this ID down and enter it in the appropriate place in MTurk to signify your completion.")

                st.info(str(response.content.decode('UTF-8')))
            elif platform == "Prolific":
                st.info("If you're using Prolific, please click this link. https://app.prolific.co/submissions/complete?cc=7AC56F74")



    # TODO: Collect more feedback from the study
    # TODO: Number the questions
    # TODO: Add progress bar



    # Overlays of lines to provide context to the user when picking (highlight line when picked)

    # Generate random trends to reduce bias
    # Generate lines independent of the true line, which of these random lines do you think are closest to the true line
    # Random sample of trends (reduce bias of the true line, ex. no median picking should be the answer)

    # Plot the rate of change versus cumulative (log scale)
    #st.write("Recorded values: ", widget_values)
