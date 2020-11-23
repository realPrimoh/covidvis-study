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

# Hides first radio obutton option, which we set to "-"
# Allows us to avoid a pre-selected value
st.markdown(
    """ <style>
            div[role="radiogroup"] >  :first-child{
                display: none !important;
            }
        </style>
        """,
    unsafe_allow_html=True
)

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

#st.subheader("Taking part is voluntary")
#st.markdown("Your involvement in this research is voluntary, and you may refuse to participate before the study begins or discontinue at any time. You will only receive compensation for this study if you complete all tasks and survey questions.")

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
    platform = platformSel("Platform", ("-", "MTurk", "Prolific", "Other"))

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

    st.subheader(str(i) + ". What is your race?")
    raceSel = record(st.selectbox, "Race")
    raceSel("Race", ("Select...", "Asian / Pacific Islander", "White", "Black or African-American", "Native American or American Indian", "Hispanic or Latino", "Other"))

    i += 1


    st.subheader(str(i) + ". What is the highest level of education you have completed or are currently completing?")
    eduSel = record(st.selectbox, "Education Level")
    eduSel("Education Level", ("Select...", "No schooling completed", "High School", "Undergraduate", "Graduate"))

    i += 1

    st.subheader(str(i) + ". What is your occupation, if any?")
    occupationSel = record(st.text_input, "Occupation")
    occupation = occupationSel("Occupation")

    i += 1
#
#    st.subheader(str(i) + ". How many times a week do you view coronavirus related info (articles, data, press releases, etc.)?")
#    virusInfoSel = record(st.selectbox, "Times a week consuming virus information")
#    virusInfoSel("Viewing", ("Select...", "0-5", "5-10", "10+"))
#
#    i += 1

    st.subheader(str(i) + ". For each of the following orders, how effective are they to you if implemented properly and everyone follows them?")
    radio1 = record(st.selectbox, "Stay-at-home Effectiveness (Phase 1-effective)")
    radio2 = record(st.selectbox, "Social Distancing Effectiveness (Phase 1-effective)")
    radio3 = record(st.selectbox, "Mask On Effectiveness (Phase 1-effective)")
    radio4 = record(st.selectbox, "Closing Bars/Restaurants Effectiveness (Phase 1-effective)")

    i += 1
    
    radio1("Stay-at-home if everyone follows", ["Select...", "Strongly Ineffective", "Slightly Ineffective", "Neutral", "Somewhat Effective", "Strongly Effective"])
    radio2("Social distancing if everyone follows", ["Select...", "Strongly Ineffective", "Slightly Ineffective", "Neutral", "Somewhat Effective", "Strongly Effective"])
    radio3("Masks on if everyone follows", ["Select...", "Strongly Ineffective", "Slightly Ineffective", "Neutral", "Somewhat Effective", "Strongly Effective"])
    radio4("Closing bars/restaurants if everyone follows", ["Select...", "Strongly Ineffective", "Slightly Ineffective", "Neutral", "Somewhat Effective", "Strongly Effective"])
    
    st.subheader(str(i) + ". For each of the following orders, how effective are they to you if they were implemented today (if you feel there is a difference)?")
    radio1_1 = record(st.selectbox, "Stay-at-home Effectiveness")
    radio2_1 = record(st.selectbox, "Social Distancing Effectiveness")
    radio3_1 = record(st.selectbox, "Mask On Effectiveness")
    radio4_1 = record(st.selectbox, "Closing Bars/Restaurants Effectiveness")

    i += 1

    radio1_1("Stay-at-home if implemented today", ["Select...", "Strongly Ineffective", "Slightly Ineffective", "Neutral", "Somewhat Effective", "Strongly Effective"])
    radio2_1("Social distancing if implemented today", ["Select...", "Strongly Ineffective", "Slightly Ineffective", "Neutral", "Somewhat Effective", "Strongly Effective"])
    radio3_1("Masks on if implemented today", ["Select...", "Strongly Ineffective", "Slightly Ineffective", "Neutral", "Somewhat Effective", "Strongly Effective"])
    radio4_1("Closing bars/restaurants if implemented today", ["Select...", "Strongly Ineffective", "Slightly Ineffective", "Neutral", "Somewhat Effective", "Strongly Effective"])

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
    vizcheck1("Please make a selection", ["-", "1", "7", "23", "40", "55", "70", "18"])

    i += 1

    st.subheader(str(i) + ". On Day 20, approximately how many confirmed cases were there?")
    vizcheck2 = record(st.radio, "Vizcheck 2")
    vizcheck2("Please make a selection.", ("-", "100", "3,000", "30,000", "8,000", "100,000", "250,000"))

    i += 1




    st.header("Visualization Survey")
    st.info("There are three phases to this survey. In Phase 1, you will be answering questions based on visualizations presented to you. In Phase 2, you will get to interact with some visualizations. In Phase 3, you will answer questions again based on visualizations shown to you.")


    show_phase2 = False
    
    st.header("Phase 1")
    
    
    st.subheader("NEW: Below, you'll be presented with a graph of the AVERAGE number of COVID-19 cases recorded per day in a certain US state. Based on your current knowledge and opinion of the pandemic, select an area of where RESTAURANTS/BARS were potentially CLOSED. Leave blank if you do not think restaurants/bars were closed at any point in the graph.")
    
    # TODO: ADD INTERACTIVE TRENDLINE HERE
    
    
    # TODO: SELECT AN AREA WHERE YOU THINK MASKS WERE MANDATED
    
    st.subheader("Below, you will be presented with a choice of potential trendlines for three states. The house image\
                  signifies when that state put a lockdown order in place (Day 0 indicates the first set of meaningful\
                  available data regarding COVID-19 cases). Your job is to identify which trendlines most accurately\
                  captures the state's trajectory of confirmed cases after the lockdown order. Use the slider to view\
                  the range of different options, and make your selection using the drop-down menu.")
    


    ny_generated_trendlines = pd.read_csv("final_data/ny_generated_trendlines.csv")
    ny_chart = generate_altair_slider_log_chart(ny_generated_trendlines, "State A")
    st.altair_chart(ny_chart)
    selectbox1 = record(st.selectbox, "Log Scale, State A (Before)")
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
    selectbox2 = record(st.selectbox, "Log Scale, State B (Before)")
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
    selectbox3 = record(st.selectbox, "Log Scale, State C (Before)")
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
    record_avg_day_before_stateA = record(st.radio, "Daily Avg, State A (Before)")
    pick_ny_img = record_avg_day_before_stateA("", ["-", "Day 12", "Day 31", "Day 50"])

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
    record_avg_day_before_stateB = record(st.radio, "Daily Avg, State B (Before)")
    pick_flor_img = record_avg_day_before_stateB("", ["-", "Day 22", "Day 34", "Day 50"])

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

    # MIDDLE
    # -----------------------
    session_state = SessionState.get(traj_looked_at=0, roll_looked_at=0, _next = False, _rolling = False)


    state_restaurant_close_dates = {"New York": '03-17-2020', "California": '03-19-2020', "Georgia": '04-02-2020', "Illinois": '03-21-2020', "Florida": '04-01-2020', "New Jersey": '03-21-2020', "Arizona": '03-31-2020', "Colorado": '03-19-2020', 'Indiana': '03-25-2020', 'Louisiana': '03-23-2020'} # Bars/nightclubs in Florida = March 17
    state_restaurant_open_dates = {"New York": '06-22-2020', "California": '05-26-2020', "Georgia": '04-24-2020', "Illinois": '05-29-2020', "Florida": '06-03-2020', "New Jersey": '06-03-2020', "Arizona": '03-31-2020', "Colorado": '03-26-2020', 'Indiana': '07-04-2020', 'Louisiana': '05-15-2020'} # NY: July 10 for malls too, NJ: May 18 for beginning, September 1 for end (https://en.wikipedia.org/wiki/COVID-19_pandemic_in_New_Jersey#Government_response)
    state_intervention = {"New York": '03-22-2020', "California": '03-19-2020', "Georgia": '04-02-2020', "Illinois": '03-21-2020', "Florida": '04-01-2020', "New Jersey": '03-21-2020', "Arizona": '05-11-2020', "Colorado": '04-30-2020', 'Indiana': '03-25-2020', 'Louisiana': '03-23-2020'}
    states = ['California', 'Georgia', 'Florida', 'New York']
    st.subheader("Choose a state from the drop-down menu to see the number of new cases each day (we provide a 7-day average\
              Once you choose a state, you can click and drag on the graph to see the total number of cases that fall in a\
              certain region. You can move your selected square as well as change its size by scrolling up or down. A video\
              demonstrating how to interact with the graph is also presented below. You must study at least three states\
              before you can move on.")
    st.video('./media/demo.mp4', format='video/mp4', start_time=7)
    phase2_look1 = st.selectbox("Pick a state to view its trajectory and play around with it.",  ["Select..."] + states)
    #but = False
    if not session_state._next:
        if phase2_look1 in states:
            st.info("Observe the trajectory for the COVID-19 cases.")
            alt_chart1_ = generate_rolling_cases_interactive(phase2_look1, state_restaurant_close_dates[phase2_look1], state_restaurant_open_dates[phase2_look1])
            st.altair_chart(alt_chart1_)
            session_state.traj_looked_at += 1
            if session_state.traj_looked_at >= 3:
                st.info("Now, we will ask you some questions about the charts.")
                st.subheader("Approximately how many new cases occurred in California while restaurants were closed?")
                x = st.radio("Make your selection for California below.", 
                    ["-", 10000, 38000, 100000, 120000, 200000])
                if x == 100000:
                    st.info("Correct! Nice work. Let's try a couple more.")
                    st.subheader("Approximately how many new cases occurred in Florida between Day 90 and Day 130?")
                    y = st.radio("Make your selection for Florida below.", 
                    ["-", 53000, 122000, 190000, 240000, 300000])
                    if y == 240000: # May need to change for different state
                        st.info("Correct! Just one more.")
                        st.subheader("About how many days after restaurants closed was the growth rate of the number of cases\
                                      in Georgia the highest? Hint: Look for where the line is steepest.")
                        z = st.radio("Make your selection for Georgia below.", 
                        ["-", 20, 45, 70, 100, 200])
                        if z == 70: # May need to change for different state
                            st.info("Correct! You can now move on to Phase 3.")
                            show_phase3 = True
                        elif z in [20, 45, 100, 200]:
                            st.info("Try again!")
                        else:
                            pass
                    elif y in [53000, 122000, 190000, 300000]:
                        st.info("Try again!")
                    else:
                        pass
                elif x in [10000, 38000, 120000, 200000]:
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
        st.subheader("Below, you will be presented with the same questions you answered from Phase 1. If your answers to these questions are the same as in Phase 1, please select them again. Use the slider to view the range of different options, and make your selection\
                      using the drop-down menu.")




        ny_generated_trendlines = pd.read_csv("final_data/ny_generated_trendlines.csv")
        ny_chart = generate_altair_slider_log_chart(ny_generated_trendlines, title="State A")
        st.altair_chart(ny_chart)
        selectbox1_phase3 = record(st.selectbox, "Log Scale, State A (After)")
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
        selectbox2_phase3 = record(st.selectbox, "Log Scale, State B (After)")
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
        selectbox3_phase3 = record(st.selectbox, "Log Scale, State C (After)")
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
        radio_dailyAvg_phase3 = record(st.radio, "Daily Avg, State A  (After)")
        pick_ny_img_phase3 = radio_dailyAvg_phase3("Pick a revised option.", ["-", "Day 12", "Day 31", "Day 50"])
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
        radio_dailyAvg_b_phase3 = record(st.radio, "Daily Avg, State B  (After)")
        pick_flor_img_phase3 = radio_dailyAvg_b_phase3("Pick a revised option", ["-", "Day 22", "Day 34", "Day 55"])
        col1, col2, col3 = st.beta_columns(3)
        flor_new_cases_actual = generate_new_cases_rolling("Florida", 22, width=400, height=300, title="Day 22")
        col1.altair_chart(flor_new_cases_actual)
        col2.text("")
        flor_new_cases_fake1 = generate_new_cases_rolling("Florida", 34, width=400, height=300, title="Day 34")
        col3.altair_chart(flor_new_cases_fake1)
        flor_new_cases_fake2 = generate_new_cases_rolling("Florida", 55, width=400, height=300, title="Day 55")
        st.altair_chart(flor_new_cases_fake2)


        i+=1
        
        st.subheader(str(i) + ". For each of the following orders, how effective are they to you if implemented properly and everyone follows them?")
        radio1phase3 = record(st.selectbox, "Stay-at-home Effectiveness (Phase 3-effective)")
        radio2phase3 = record(st.selectbox, "Social Distancing Effectiveness (Phase 3-effective)")
        radio3phase3 = record(st.selectbox, "Mask On Effectiveness (Phase 3-effective)")
        radio4phase3 = record(st.selectbox, "Closing Bars/Restaurants Effectiveness (Phase 3-effective)")
        i += 1
        
        radio1phase3("Stay-at-home (Phase 3)", ["Select...", "Strongly Ineffective", "Slightly Ineffective", "Neutral", "Somewhat Effective", "Strongly Effective"])
        radio2phase3("Social distancing (Phase 3)", ["Select...", "Strongly Ineffective", "Slightly Ineffective", "Neutral", "Somewhat Effective", "Strongly Effective"])
        radio3phase3("Masks on (Phase 3)", ["Select...", "Strongly Ineffective", "Slightly Ineffective", "Neutral", "Somewhat Effective", "Strongly Effective"])
        radio4phase3("Closing bars/restaurants (Phase 3)", ["Select...", "Strongly Ineffective", "Slightly Ineffective", "Neutral", "Somewhat Effective", "Strongly Effective"])
        
        st.subheader(str(i) + ". For each of the following orders, how effective are they to you if they were implemented in the US today?")
        radio1phase3_1 = record(st.selectbox, "Stay-at-home Effectiveness (Phase 3)")
        radio2phase3_1 = record(st.selectbox, "Social Distancing Effectiveness (Phase 3)")
        radio3phase3_1 = record(st.selectbox, "Mask On Effectiveness (Phase 3)")
        radio4phase3_1 = record(st.selectbox, "Closing Bars/Restaurants Effectiveness (Phase 3)")
        i += 1
        
        radio1phase3_1("Stay-at-home (Phase 3)", ["Select...", "Strongly Ineffective", "Slightly Ineffective", "Neutral", "Somewhat Effective", "Strongly Effective"])
        radio2phase3_1("Social distancing (Phase 3)", ["Select...", "Strongly Ineffective", "Slightly Ineffective", "Neutral", "Somewhat Effective", "Strongly Effective"])
        radio3phase3_1("Masks on (Phase 3)", ["Select...", "Strongly Ineffective", "Slightly Ineffective", "Neutral", "Somewhat Effective", "Strongly Effective"])
        radio4phase3_1("Closing bars/restaurants (Phase 3)", ["Select...", "Strongly Ineffective", "Slightly Ineffective", "Neutral", "Somewhat Effective", "Strongly Effective"])


        st.header("Conclusion")

        st.text_input("Is there anything else you would like to share with us regarding this study?")


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



    # Overlays of lines to provide context to the user when picking (highlight line when picked)

    # Generate random trends to reduce bias
    # Generate lines independent of the true line, which of these random lines do you think are closest to the true line
    # Random sample of trends (reduce bias of the true line, ex. no median picking should be the answer)

    # Plot the rate of change versus cumulative (log scale)
    #st.write("Recorded values: ", widget_values)
