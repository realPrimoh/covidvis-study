import streamlit as st
import pandas as pd
import numpy as np
import csv
import datetime
import collections
import requests
import time

from random import random
import SessionState
from functools import reduce

from scripts.generate_trendlines import *

testing = False
widget_values = collections.defaultdict(list)


# urlparams = st.experimental_get_query_params()
platform = "Prolific"

# if "platform" in urlparams:
#     platform = urlparams["platform"][0]
    
widget_values["platform"] = platform

# widget_values["otherParams"] = urlparams

# Hides first radio obutton option, which we set to "-"
# Allows us to avoid a pre-selected value
st.markdown(
    """ <style>
            div[role="radiogroup"] >  :first-child{
                display: none !important;
            }
            .stSelectbox>label {
                display: none;
            }
            .stTextInput>label {
                display: none;
            }
            .stRadio>label {
                display: none;
            }
            .st-d5 .st-b7 .st-er {
                padding-left: 10;
                padding-right: 10;
            }
            
        </style>
        """,
    unsafe_allow_html=True
)

session_state = SessionState.get(traj_looked_at=0, roll_looked_at=0, _next = False, _rolling = False, start=0, end=0, demo=True)

i = 1
st.title('A User Study of COVID-19 Intervention Measures')

st.info("In this study, we are trying examine the best way to convey information about COVID-19 to the general public. Your data will be kept as confidential as possible.")

st.subheader("Details")
st.markdown("The primary researchers conducting this study are Murtaza Ali and Priyam Mohanty. If you have questions at any point, you may contact Priyam Mohanty at priyam.mohanty@berkeley.edu or Murtaza Ali at murtzali_5253@berkeley.edu.  If you have any questions or concerns regarding your rights as a participant in this study, you may contact the Institutional Review Board (IRB) for Human Participants at https://cphs.berkeley.edu.")

st.subheader("What we will ask you to do")
st.markdown("If you agree to take part, you will be asked to complete a questionnaire. The survey will last approximately 10-20 minutes and will be conducted online.")

st.subheader("Risks and discomforts")
st.markdown("There is little risk to you in taking part in this research. Your study data will be treated as confidentially as possible. The data will be stored on an encrypted database online. None of your personal information is collected.")

st.subheader("Benefits")
st.markdown("It is our hope that the research will benefit the scientific community in better understanding societal implications of COVID-19 interventions. You will be compensated for completion of this study. This study is expected to take 10-20 minutes to complete.")

st.subheader("Statement of Consent")
st.markdown("Please check the box below to continue. By continuing with this survey and submitting your response, you are consenting to the above statements. If you do not consent, please exit the survey now.")

consent = st.checkbox("I consent")
if testing:
    consent = True
demographic_complete = False
if consent:

    def record(f, widgetLabel):
        """Return a function that wraps a streamlit widget and records the
        widget's values to a global dictionary.
        """
        def wrapper(label, *args, **kwargs):
            widget_value = f(label, *args, **kwargs)
            widget_values[widgetLabel].append(widget_value)
            return widget_value

        return wrapper

    if testing:
        demographic_complete = True

    st.subheader("Please enter your Prolific ID")
    prolificID = record(st.text_input, "Prolific ID")
    pid = prolificID("Prolific ID")
        
    demo_survey = st.empty()
    st.header("Demographical Information")

    st.subheader(str(i) + ". What is your age?")
    ageSlider = record(st.selectbox, "Age")
    age = ageSlider("Age", ('Select...', "18-24", "25-34", "35-44", "45-54", "55-64", "65-74", "75+"))
#
    i += 1
    st.subheader(str(i) + ". What state are you residing in right now?")
    stateSelect = record(st.selectbox, "State")
    demo_state = stateSelect("State", ['Select...', "AL", "AK", "AZ", "AR", "CA", "CO", "CT", "DC", "DE", "FL", "GA", 
              "HI", "ID", "IL", "IN", "IA", "KS", "KY", "LA", "ME", "MD", 
              "MA", "MI", "MN", "MS", "MO", "MT", "NE", "NV", "NH", "NJ", 
              "NM", "NY", "NC", "ND", "OH", "OK", "OR", "PA", "RI", "SC", 
              "SD", "TN", "TX", "UT", "VT", "VA", "WA", "WV", "WI", "WY"])

    i += 1
#
    st.subheader(str(i) + ". What is your gender?")
    genderSel = record(st.selectbox, "Gender")
    demo_gender = genderSel("Gender", ('Select...','Male', 'Female', 'Nonbinary', 'Prefer not to say'))

    i += 1
#
    st.subheader(str(i) + ". What political party do you affiliate with?")
    partySel = record(st.selectbox, "Political Party")
    demo_party = partySel("Party", ('Select...', 'Democrat', 'Republican', 'Independent', 'Libertarian', 'Green Party', 'Other'))

    partyOtherSel = record(st.text_input, "Political Party (Other)")
    demo_partyOther = None

    if demo_party == 'Other':
        demo_partyOther = partyOtherSel("Political Party (Other)")

    # TODO (priyam): add check for other

    i += 1

    st.subheader(str(i) + ". What is your race?")
    raceSel = record(st.selectbox, "Race")
    demo_race = raceSel("Race", ("Select...", "Asian / Pacific Islander", "White", "Black or African-American", "Native American or American Indian", "Hispanic or Latino", "Other"))

    raceOtherSel = record(st.text_input, "Race (Other)")
    demo_raceOther = None

    if demo_race == 'Other':
        demo_raceOther = raceOtherSel("Race (Other)")

    # TODO (priyam): add check for other

    i += 1


    st.subheader(str(i) + ". What is the highest level of education you have completed or are currently completing?")
    eduSel = record(st.selectbox, "Education Level")
    demo_edu = eduSel("Education Level", ("Select...", "No schooling completed", "High School Diploma", "Undergraduate Degree", "Advanced Degree"))

    i += 1
    
    st.subheader(str(i) + ". Are you an US citizen?")
    citizenSel = record(st.selectbox, "Citizenship")
    demo_citizen = citizenSel("US Citizenship", ("Select...", "Yes", "No"))

    i += 1

    st.subheader(str(i) + ". What is your occupation, if any?")
    occupationSel = record(st.text_input, "Occupation")
    demo_occu = occupation = occupationSel("Occupation")

    i += 1

    st.info("Note: You must complete the above questions before you can move on.")
#
    if age != 'Select...' and demo_state != 'Select...' and demo_gender != 'Select...' and demo_party != "Select..." and demo_race != "Select..." and demo_edu != "Select..." and demo_occu != "Select..." and demo_citizen != 'Select...':
        demographic_complete = st.checkbox("I have completed the demographics survey above.")
    
            
    if demographic_complete:
        demo_survey.empty()
        st.header("Phase 1")
        
        st.warning("In Phase 1, you will be answering a few questions about your opinion on various aspects of the COVID-19 pandemic.")

        st.subheader(str(i) + ". For each of the following orders, how effective are they to you if implemented properly and everyone follows them?")
        radio1 = record(st.selectbox, "Stay-at-home Effectiveness (Phase 1-effective)")
        radio2 = record(st.selectbox, "Social Distancing Effectiveness (Phase 1-effective)")
        radio3 = record(st.selectbox, "Mask On Effectiveness (Phase 1-effective)")
        radio4 = record(st.selectbox, "Closing Bars/Restaurants Effectiveness (Phase 1-effective)")
        radio5 = record(st.selectbox, "Closing Schools Effectiveness (Phase 1-effective)")
        radio6 = record(st.selectbox, "Restricting Indoor Gatherings Effectiveness (Phase 1-effective)")

        i += 1

        st.write("a. Lockdown order (mandatory stay-at-home) if everyone obeys the directive")
        r1 = radio1("Lockdown order (mandatory stay-at-home) if everyone obeys the directive", ["Select...", "Strongly Ineffective", "Slightly Ineffective", "Neutral", "Somewhat Effective", "Strongly Effective"])
        st.write("b. Social distancing if everyone obeys the directive")
        r2 = radio2("Social distancing if everyone obeys the directive", ["Select...", "Strongly Ineffective", "Slightly Ineffective", "Neutral", "Somewhat Effective", "Strongly Effective"])
        st.write("c. Mandatory masks in public if everyone obeys the directive")
        r3 = radio3("Mandatory masks in public if everyone obeys the directive", ["Select...", "Strongly Ineffective", "Slightly Ineffective", "Neutral", "Somewhat Effective", "Strongly Effective"])
        st.write("d. Closing bars/restaurants if everyone obeys the directive")
        r4 = radio4("Closing bars/restaurants if everyone obeys the directive", ["Select...", "Strongly Ineffective", "Slightly Ineffective", "Neutral", "Somewhat Effective", "Strongly Effective"])
        st.write("e. Closing schools if everyone obeys the directive")
        r5 = radio5("Closing schools if everyone obeys the directive", ["Select...", "Strongly Ineffective", "Slightly Ineffective", "Neutral", "Somewhat Effective", "Strongly Effective"])
        st.write("f. Restricting Indoor Gatherings if everyone obeys the directive")
        r6 = radio6("Restricting Indoor Gatherings if everyone obeys the directive", ["Select...", "Strongly Ineffective", "Slightly Ineffective", "Neutral", "Somewhat Effective", "Strongly Effective"])

        st.subheader(str(i) + ". For each of the following orders, how effective have they been in practice as implemented in the US?")
        radio1_1 = record(st.selectbox, "Stay-at-home Effectiveness")
        radio2_1 = record(st.selectbox, "Social Distancing Effectiveness")
        radio3_1 = record(st.selectbox, "Mask On Effectiveness")
        radio4_1 = record(st.selectbox, "Closing Bars/Restaurants Effectiveness")
        radio5_1 = record(st.selectbox, "Closing Schools Effectiveness")
        radio6_1 = record(st.selectbox, "Restricting Indoor Gatherings Effectiveness")

        i += 1

        st.write("a. Lockdown order (mandatory stay-at-home) in practice")
        r11 = radio1_1("Lockdown order (mandatory stay-at-home) in practice", ["Select...", "Strongly Ineffective", "Slightly Ineffective", "Neutral", "Somewhat Effective", "Strongly Effective"])
        st.write("b. Social distancing in practice")
        r21 = radio2_1("Social distancing in practice", ["Select...", "Strongly Ineffective", "Slightly Ineffective", "Neutral", "Somewhat Effective", "Strongly Effective"])
        st.write("c. Mandatory masks in public in practice")
        r31 = radio3_1("Mandatory masks in public in practice", ["Select...", "Strongly Ineffective", "Slightly Ineffective", "Neutral", "Somewhat Effective", "Strongly Effective"])
        st.write("d. Closing bars/restaurants in practice")
        r41 = radio4_1("Closing bars/restaurants in practice", ["Select...", "Strongly Ineffective", "Slightly Ineffective", "Neutral", "Somewhat Effective", "Strongly Effective"])
        st.write("e. Closing schools in practice")
        r51 = radio5_1("Closing schools in practice", ["Select...", "Strongly Ineffective", "Slightly Ineffective", "Neutral", "Somewhat Effective", "Strongly Effective"])
        st.write("f. Restricting Indoor Gatherings in practice")
        r61 = radio6_1("Restricting Indoor Gatherings in practice", ["Select...", "Strongly Ineffective", "Slightly Ineffective", "Neutral", "Somewhat Effective", "Strongly Effective"])

        show_phase2 = False


        st.subheader(str(i) + ". Below is a graph of new COVID-19 cases per day in a certain US state.")
        
        start_phase1 = record(st.slider, "Start - phase1")
        end_phase1 = record(st.slider, "End - phase1")
        test_chart = st.empty()
        expand = st.beta_expander("Chart Legend (click to expand)")
        expand.markdown(
    """ <h4><img src="https://raw.githubusercontent.com/realPrimoh/covidvis-study/master/close-image.png" width=90 height=72 />: This marks where restaurants, bars, and other establishments were closed.<br/>
    <img src="https://raw.githubusercontent.com/realPrimoh/covidvis-study/master/open-image.png" width=90 height=72 />: This marks where restaurants, bars, and other establishments were opened.
        """,
    unsafe_allow_html=True
)
        expand = st.beta_expander("Confused? Click here for a quick video explanation.")
        # https://www.veed.io/download/7229df92-9b0a-4a92-98d2-d91814abebfa
        expand.markdown(
    """ <video width="640" height="349" controls><source src="https://github.com/realPrimoh/covidvis-study/raw/master/explainer1.mp4" type="video/mp4"> Your browser doesn't support the video tag. Please visit <a src="https://github.com/realPrimoh/covidvis-study/raw/master/explainer1.mp4">this link</a> to view the video.</video>
        """,
    unsafe_allow_html=True
)
        st.subheader("Use the sliders below to pick a point on the graph where restaurants, bars, and other establishments were CLOSED and a point where they OPENED.")
#        st.write("Leave blank (slider at -1) if you do not think restaurants/bars/other establishments were closed at any point in the graph. ")
        
        start = start_phase1("Choose when you think restaurants/bars/other establishments closed, if at all (-1 = never closed).", -1, 170, -1)
        end = end_phase1("Choose when you think restaurants/bars/other establishments opened, if at all (-1 = never opened).", -1, 170, -1)
        phase1_base, phase1_img, warning = generate_rolling_cases_interactive('Arizona', datetime.datetime.strptime('03-10-2020', '%m-%d-%Y') + datetime.timedelta(days=start), datetime.datetime.strptime('03-10-2020', '%m-%d-%Y') + datetime.timedelta(days=end), False, False)
        #https://www.veed.io/download/52899626-ee76-4569-82c6-ab7cee173c06
        #https://www.veed.io/download/52899626-ee76-4569-82c6-ab7cee173c06
        test_chart.altair_chart(phase1_base + phase1_img)
        st.info("Note: Day 0 is March 10, 2020. \n\nNote: There may be a small delay between the slider movement and the icon on the chart.")
        g = st.empty()
        if start < 0 or end < 0 or start > 170 or end > 170:
            g.warning("You have chosen to leave part or all of the graph blank. This means you do not think restaurants/bars/other establishments were closed at any point in the graph. Please confirm this is your choice before moving on.")
        if warning:
            st.warning(warning)

#        session_state.start = start_phase1("Choose when you think restaurants/bars closed, if at all", 0, 170, 1)
#        session_state.end = end_phase1("Choose when you think restaurants/bars opened, if at all", 0, 170, 170)
        i += 1
        show_phase3 = False
        phase1_done = False
        if not warning and r1 != "Select..." and r2 != "Select..." and r3 != "Select..." and r4 != "Select..." and r5 != "Select..." and r6 != "Select..." and r11 != "Select..." and r21 != "Select..." and r31 != "Select..." and r41 != "Select..." and r51 != "Select..." and r61 != "Select...":
            phase1_done = st.checkbox("I am finished with Phase 1.")
            if testing:
                phase1_done = True
        else:
            st.warning("Please complete Phase 1 to continue.")
        if not warning and phase1_done:
            # requests.post("https://formspree.io/f/xnqooqge", data=widget_values)
            st.header("Phase 2")
            st.warning("In Phase 2, you will get a chance to experience a few data visualizations presenting the effect of restaurant/bar closures on the COVID-19 daily case rate. Your answers aren't recorded here. We would like you to explore the visualizations depicting COVID-19 spread below.")

            # MIDDLE
            # -----------------------


            state_restaurant_close_dates = {"New York": '03-20-2020', "California": '03-19-2020', "Georgia": '04-02-2020', "Illinois": '03-21-2020', "Florida": '04-01-2020', "New Jersey": '03-21-2020', "Arizona": '06-29-2020', "Colorado": '03-19-2020', 'Indiana': '03-25-2020', 'Louisiana': '03-23-2020', "Texas": '03-31-2020', "Washington": '03-23-2020', "Pennsylvania": '04-01-2020', "South Dakota": '03-01-2020'} # Bars/nightclubs in Florida = March 17
            
            state_restaurant_open_dates = {"New York": '05-15-2020', "California": '05-18-2020', "Georgia": '06-13-2020', "Illinois": '05-29-2020', "Florida": '06-03-2020', "New Jersey": '06-03-2020', "Arizona": '08-10-2020', "Colorado": '03-26-2020', 'Indiana': '07-04-2020', 'Louisiana': '05-15-2020', "Texas": '06-3-2020', "Washington": '06-01-2020', "Pennsylvania": '06-05-2020', "South Dakota": '12-12-2020'} # NY: July 10 for malls too, NJ: May 18 for beginning, September 1 for end (https://en.wikipedia.org/wiki/COVID-19_pandemic_in_New_Jersey#Government_response)

            # Georgia: https://www.acluga.org/en/timeline-georgia-government-actions-regarding-covid-19
            # Texas: https://www.texastribune.org/2020/07/31/coronavirus-timeline-texas/
            # Florida: https://en.wikipedia.org/wiki/COVID-19_pandemic_in_Florida#Response
            # New York: https://en.wikipedia.org/wiki/COVID-19_pandemic_in_New_York_(state)#Government_response
            # Washington: https://www.seattlemet.com/health-and-wellness/2020/08/seattle-s-coronavirus-timeline-from-toilet-paper-to-mask-laws
            # Pennsylvania: https://en.wikipedia.org/wiki/COVID-19_pandemic_in_Pennsylvania#Government_response (REMOVE b/c of too many "phases")
            # California: https://www.usnews.com/news/best-states/california/articles/2020-07-01/timeline-of-events-during-californias-coronavirus-outbreak
            state_intervention = {"New York": '03-22-2020', "California": '03-19-2020', "Georgia": '04-02-2020', "Illinois": '03-21-2020', "Florida": '04-01-2020', "New Jersey": '03-21-2020', "Arizona": '05-11-2020', "Colorado": '04-30-2020', 'Indiana': '03-25-2020', 'Louisiana': '03-23-2020'}

            states = ['Florida', 'Texas', 'Georgia', 'Washington', 'South Dakota', 'New York', 'California']
            # Green: New York, Red: South Dakota, Orange: Texas, Blue: Florida

            st.subheader("Choose a state from the drop-down menu to see the number of new cases each day.\
                      Once you choose a state, you can click and drag on the graph to see the total number of cases that fall in a\
                      certain region. A video demonstrating how to interact with the graph is also presented below.")
            st.write("Pick a state to view its trajectory and play around with it.")
            phase2_look1 = st.selectbox("Pick a state to view its trajectory and play around with it. You must study at least three states before you can move on.",  ["Select..."] + states)
            expand2 = st.beta_expander("Confused? Click to view a quick video explanation.")
            expand2.markdown(
    """ <video width="640" height="349" controls><source src="https://github.com/realPrimoh/covidvis-study/raw/master/explainer2.mp4" type="video/mp4"> Your browser doesn't support the video tag. Please visit <a src="https://github.com/realPrimoh/covidvis-study/raw/master/explainer2.mp4">this link</a> to view the video.</video>
        """,
    unsafe_allow_html=True
)
            #but = False
            if not session_state._next:
                if testing:
                        session_state.traj_looked_at = 0
                        show_phase3 = True
                if phase2_look1 in states:
                    
                    alt_chart1_ = generate_rolling_cases_interactive(phase2_look1, state_restaurant_close_dates[phase2_look1], state_restaurant_open_dates[phase2_look1])
                    expand1 = st.beta_expander("Chart Legend (Click to expand)")
                    expand1.markdown(
                """ <h4><img src="https://raw.githubusercontent.com/realPrimoh/covidvis-study/master/close-image.png" width=90 height=72 />: This marks where restaurants, bars, and other establishments were closed.<br/>
                <img src="https://raw.githubusercontent.com/realPrimoh/covidvis-study/master/open-image.png" width=90 height=72 />: This marks where restaurants, bars, and other establishments were opened.
                    """,
                unsafe_allow_html=True
                    )
                    expand_info = st.beta_expander("More Info (Click to expand)")
                    if phase2_look1 == 'New York':
                      expand_info.info("Closed: New York implemented a state-wide stay-at-home order on Day 12, which closed all non-essential businesses and\
                              canceled/postponed all non-essential gatherings. \n\n Opened: New York did not ever reopen the entire state formally, but we mark Day 66\
                              as the open day, as that was when the first counties were allowed to enter some phase of reopening.")
                    if phase2_look1 == 'Florida':
                      expand_info.info("Closed: We mark Day 22 as the start day, as that is when a state-wide stay-at-home order was issued. It is worth noting\
                              that some bars and restaurants had already closed previously. \n\n Opened: We mark Day 85 as the open day, as that is when Florida\
                              entered Phase 2 of reopening (except Broward, Miami-Dade, and Palm Beach counties), which allowed most businesses\
                              to resume operations at 50 percent capacity. For details about Florida's Phase 2, see this link: https://www.flgov.com/wp-content/uploads/covid19/Exec%20Order%20Phase%202%20FAQs.pdf")
                    if phase2_look1 == 'Texas':
                      expand_info.info("Closed: Texas closed restaurants, bars, and schools on Day 9. However, we mark Day 21 as the start date, as that is when\
                              Texans were told to stay home for all non-essential reasons. It is worth noting that the governor declined to call\
                              this an official stay-at-home order. \n\n Opened: We mark Day 85 as the open day, as Texas allowed almost all businesses to resume operations at 50 percent capacity. On Day 94, restaurants were allowed to open at 75 percent capacity.")
                    if phase2_look1 == 'Georgia':
                      expand_info.info("Closed: Georgia closed restaurants, bars, and schools on Day 11, as part of a statewide shelter-in-place order.\n\n Opened: We mark Day 94 as the open day, as that is when Gov. Brian Kemp of Georgia started allowing bars to host up to 35% capacity and restaurants no longer had a limit.")
                    if phase2_look1 == 'Washington':
                      expand_info.info("Closed: Washington closed restaurants, bars, and schools on Day 15. \n\n Opened: We mark Day 83 as the open day, as that is when the statewide stay-at-home order expired, allowing restaurants and bars across the state to open up. Select counties, like King County, stayed closed until Day 101. It is worth noting that statewide protests occurred on Days 80-82 where thousands crowded the streets for social justice causes.")
                    if phase2_look1 == 'South Dakota':
                      expand_info.info("South Dakota has not put any COVID-19 intervention measures in place.")
                    if phase2_look1 == 'California':
                      expand_info.info("Closed: California closed restaurants, bars, and schools on Day 9, as part of a state-wide stay-at-home order. \n\n Opened: We mark Day 68 as the open day, as that is when restaurants, bars, and other establishments were able to open up, though not fully.")
                    st.warning("- The bar graphs to the right of the graph contain additional information about the average number of daily\
                                cases. \n\n - The dynamic maroon bar shows the average number for your selected time period (click and drag on the graph). \n\n - The static blue\
                                bar shows the average number of daily cases for the total time period. \n\n - Until you actively make a selection, the\
                                default selection is the entire graph, which is why both bars start out identical.")
                    st.altair_chart(alt_chart1_)
                    
                    st.info("Day 0 is March 10, 2020.")
                    st.info("Now, we will ask you some questions about the charts.")
                    st.subheader("On average, how many new cases each day occurred in Texas while restaurants were closed? Your answer does not have to\
                                    be exact.")
                    x, y, z = -1, -1, -1
                    hint1 = st.beta_expander("Hint: (click to expand)")
                    hint1.error("Click and drag the area from the 'Closed' icon to the 'Opened' icon on the Texas chart. The number is shown on the red bar on the right.")
                    # hint1 = st.radio("Hint: Click and drag the area from the 'closing' icon to the 'opening' icon on the Texas chart.", 
                    #     ["-", 400, 1000, 3300, 5000, 6200])
                    x = st.text_input("Enter your answer for Texas here.")
                    try:
                        x = int(x)
                    except ValueError:
                        st.info("Your answer must be a whole number (no decimals).")
                    if type(x) == int and 900 <= x <= 1100:
                        st.info("Correct! Nice work. Let's try a couple more.")
                        st.subheader("On average, how many new cases each day occurred in Florida between Day 90 and Day 130?")
                        hint2 = st.beta_expander("Hint: (click to expand) ")
                        hint2.error("Click and drag the area from the Day 90 to Day 130 on the Florida chart. The number is shown on the red bar on the right.")
                        # y = st.radio("Hint: Click and drag the area from the Day 90 to Day 130 on the Florida chart.", 
                        # ["-", 1000, 2200, 6000, 7500, 10000])
                        y = st.text_input("Enter your answer for Florida here.")
                        try:
                            y = int(y)
                        except ValueError:
                            st.info("Your answer must be a whole number (no decimals).")
                        if type(y) == int and 5600 <= y <= 6300: #y == 6000: # May need to change for different state
                            st.info("Correct! Just one more.")
                            st.subheader("What was the average number of COVID-19 cases per day in the period after Washington re-opened bars and restaurants?")
                            hint3 = st.beta_expander("Hint: (click to expand)  ")
                            hint3.error("Click and drag the area from the 'Opened' icon to the complete right side on the Washington chart. The number is shown on the red bar on the right.")
                            # z = st.radio("Hint: Click and drag the area from the 'opening' icon to the complete right side on the Georgia chart.", 
                            # ["-", 200, 1000, 2600, 3200, 6300])
                            z = st.text_input("Enter your answer for Washington here.")
                            try:
                                z = int(z)
                            except ValueError:
                                st.info("Your answer must be a whole number (no decimals).")
                            if type(z) == int and 500 <= z <= 625: #z == 2600: # May need to change for different state
                                st.info("Correct! You can now move on to Phase 3.")
                                show_phase3 = True
                            elif type(z) == int and z > 0: #z in [200, 1000, 6300, 3200]:
                                st.info("Try again!")
                            else:
                                pass
                        elif type(y) == int and y > 0: #y in [1000, 2200, 7500, 10000]:
                            st.info("Try again!")
                        else:
                            pass
                    elif type(x) == int and x > 0: #in [400, 3300, 5000, 6200]:
                        st.info("Try again!")
                    else:
                        pass


            if show_phase3:
                st.header("Phase 3")
                st.warning("In Phase 3, you will be presented with the same questions you answered from Phase 1. Based on the information you have received in Phase 2, please answer the questions again, regardless of whether your answers have changed or not.")


                st.subheader(str(i) + ". For each of the following orders, how effective are they to you if implemented properly and everyone follows them?")
                radio1phase3 = record(st.selectbox, "Lockdown (Mandatory stay-at-home) Effectiveness (Phase 3-effective)")
                radio2phase3 = record(st.selectbox, "Social Distancing Effectiveness (Phase 3-effective)")
                radio3phase3 = record(st.selectbox, "Mask On Effectiveness (Phase 3-effective)")
                radio4phase3 = record(st.selectbox, "Closing Bars/Restaurants Effectiveness (Phase 3-effective)")
                radio5phase3 = record(st.selectbox, "Closing Schools Effectiveness (Phase 3-effective)")
                radio6phase3 = record(st.selectbox, "Restricting Indoor Gatherings Effectiveness (Phase 3-effective)")
                i += 1

                st.write("a. Lockdown order (mandatory stay-at-home) if everyone obeys the directive")
                radio1phase3("Lockdown order (mandatory stay-at-home) if everyone obeys the directive (Phase 3)", ["Select...", "Strongly Ineffective", "Slightly Ineffective", "Neutral", "Somewhat Effective", "Strongly Effective"])
                st.write("b. Social distancing if everyone obeys the directive")
                radio2phase3("Social distancing if everyone obeys the directive (Phase 3)", ["Select...", "Strongly Ineffective", "Slightly Ineffective", "Neutral", "Somewhat Effective", "Strongly Effective"])
                st.write("c. Mandatory masks in public in if everyone obeys the directive")
                radio3phase3("Mandatory masks in public in if everyone obeys the directive (Phase 3)", ["Select...", "Strongly Ineffective", "Slightly Ineffective", "Neutral", "Somewhat Effective", "Strongly Effective"])
                st.write("d. Closing bars/restaurants if everyone obeys the directive")
                radio4phase3("Closing bars/restaurants if everyone obeys the directive (Phase 3)", ["Select...", "Strongly Ineffective", "Slightly Ineffective", "Neutral", "Somewhat Effective", "Strongly Effective"])
                st.write("e. Closing schools if everyone obeys the directive")
                radio5phase3("Closing schools if everyone obeys the directive (Phase 3)", ["Select...", "Strongly Ineffective", "Slightly Ineffective", "Neutral", "Somewhat Effective", "Strongly Effective"])
                st.write("f. Restricting Indoor Gatherings if everyone obeys the directive")
                radio6phase3("Restricting Indoor Gatherings if everyone obeys the directive (Phase 3)", ["Select...", "Strongly Ineffective", "Slightly Ineffective", "Neutral", "Somewhat Effective", "Strongly Effective"])
                

                st.subheader(str(i) + ". For each of the following orders, how effective are they to you if they were implemented in the US today?")
                radio1phase3_1 = record(st.selectbox, "Stay-at-home Effectiveness (Phase 3)")
                radio2phase3_1 = record(st.selectbox, "Social Distancing Effectiveness (Phase 3)")
                radio3phase3_1 = record(st.selectbox, "Mask On Effectiveness (Phase 3)")
                radio4phase3_1 = record(st.selectbox, "Closing Bars/Restaurants Effectiveness (Phase 3)")
                radio5phase3_1 = record(st.selectbox, "Closing Schools Effectiveness (Phase 3)")
                radio6phase3_1 = record(st.selectbox, "Restricting Indoor Gatherings Effectiveness (Phase 3)")
                i += 1

                st.write("a. Lockdown order (mandatory stay-at-home) in practice")
                radio1phase3_1("Lockdown order (mandatory stay-at-home) in practice (Phase 3)", ["Select...", "Strongly Ineffective", "Slightly Ineffective", "Neutral", "Somewhat Effective", "Strongly Effective"])
                st.write("b. Social distancing in practice")
                radio2phase3_1("Social distancing in practice (Phase 3)", ["Select...", "Strongly Ineffective", "Slightly Ineffective", "Neutral", "Somewhat Effective", "Strongly Effective"])
                st.write("c. Mandatory masks in public in practice")
                radio3phase3_1("Mandatory masks in public in practice (Phase 3)", ["Select...", "Strongly Ineffective", "Slightly Ineffective", "Neutral", "Somewhat Effective", "Strongly Effective"])
                st.write("d. Closing bars/restaurants in practice")
                radio4phase3_1("Closing bars/restaurants in practice (Phase 3)", ["Select...", "Strongly Ineffective", "Slightly Ineffective", "Neutral", "Somewhat Effective", "Strongly Effective"])
                st.write("e. Closing schools in practice")
                radio5phase3_1("Closing schools in practice (Phase 3)", ["Select...", "Strongly Ineffective", "Slightly Ineffective", "Neutral", "Somewhat Effective", "Strongly Effective"])
                st.write("f. Restricting Indoor Gatherings in practice")
                radio6phase3_1("Restricting Indoor Gatherings in practice (Phase 3)", ["Select...", "Strongly Ineffective", "Slightly Ineffective", "Neutral", "Somewhat Effective", "Strongly Effective"])

                st.subheader(str(i) + ". Below, you'll be presented with a graph of the AVERAGE number of COVID-19 cases recorded per day in a certain US state. Based on your current knowledge and opinion of the pandemic, select an area of where RESTAURANTS/BARS were potentially CLOSED. Leave blank if you do not think restaurants/bars were closed at any point in the graph.")

                st.subheader("Below is a graph of new COVID-19 cases per day in a certain US state.")
                start_phase3 = record(st.slider, "Start - phase3")
                end_phase3 = record(st.slider, "End - phase3")
                test_chart3 = st.empty()
                expand_phase3 = st.beta_expander("Confused? Click here for a quick video explanation.")
        # https://www.veed.io/download/7229df92-9b0a-4a92-98d2-d91814abebfa
                expand_phase3.markdown(
                    """ <video width="640" height="349" controls><source src="https://github.com/realPrimoh/covidvis-study/raw/master/explainer1.mp4" type="video/mp4"> Your browser doesn't support the video tag. Please visit <a src="https://github.com/realPrimoh/covidvis-study/raw/master/explainer1.mp4">this link</a> to view the video.</video>
                        """,
                    unsafe_allow_html=True
                )
                st.subheader("Based on your current knowledge and opinion of the pandemic, use the sliders below to pick a point on the chart where restaurants, bars, and other establishments were potentially CLOSED and a point where they OPENED. Leave blank if you do not think restaurants/bars were closed at any point in the graph.")

                start3 = start_phase3("Choose when you think restaurants/bars closed, if at all", -1, 170, -1)
                end3 = end_phase3("Choose when you think restaurants/bars opened, if at all", -1, 170, -1)
                phase3_base, phase3_img, warning_phase3 = generate_rolling_cases_interactive('Arizona', datetime.datetime.strptime('03-10-2020', '%m-%d-%Y') + datetime.timedelta(days=start3), datetime.datetime.strptime('03-10-2020', '%m-%d-%Y') + datetime.timedelta(days=end3), False, False)
                if warning_phase3:
                    st.warning(warning_phase3)
                test_chart3.altair_chart(phase3_base + phase3_img)
                st.info("Note: Day 0 is a March 10, 2020. \n\nNote: There may be a small delay between the slider movement and the icon on the chart.")

                
                if not warning_phase3:
                    
                    record_phase3_vizchange = record(st.radio, "Effect of Phase 2")
                    st.subheader(str(i) + ". How did Phase 2 affect your opinion about COVID-19 interventions?")
                    rpv = record_phase3_vizchange("Phase 2 Effect", ('-', 'Reinforced my views', 'Changed my views', 'Convinced me to seek more information', 'Didn\'t change my views'))
                    
                    why_phase3 = record(st.text_input, "why_phase3")
                    st.write("Why did you pick the answer you chose above?")
                    why_phase3_r = why_phase3("Why did you pick the answer you chose above?")

                    why_phase2 = record(st.text_input, "why_phase2")
                    st.write("In Phase 2, were there any specific aspects of the visualizations you found particularly helpful\
                              in understanding the data?")
                    why_phase2_r = why_phase2("What did you think of the interactive visualizations in Phase 2?")
                    

                    st.header("Conclusion")
                    
                    if why_phase2_r and why_phase3_r and rpv != '-':
                        
                        text_record = record(st.text_input, "Conclusion_Share")

                        st.write("Is there anything else you would like to share with us regarding this study?")
                        text_r = text_record("Is there anything else you would like to share with us regarding this study?")

                        text_record2 = record(st.text_input, "Conclusion_Share Email")

                        st.write("If you would like to volunteer for a paid post-study interview, please enter your email address below.")
                        text_r2 = text_record2("If you would like to volunteer for a paid post-study interview, please enter your email address below.")


                        st.info("Thank you so much for participating! Click Submit below.")
                        import time

                        import json 
                        if st.button("Submit"):
                            widget_values["time"] = str(time.localtime(time.time()))
                            bar = st.progress(0)
                            # response = requests.post("https://formspree.io/f/xvovvowl", data=widget_values)
                            response = requests.post('http://covidvis-api.herokuapp.com/send/', data=widget_values)
                            for percent_complete in range(100):
                                time.sleep(0.005)
                                bar.progress(percent_complete + 1)
                            if platform == "MTurk":
                                st.info("Please record this ID down and enter it in the appropriate place in MTurk to signify your completion.")
    
                                st.info(str(response.content.decode('UTF-8')))
                            elif platform == "Prolific":
                                if pid == "":
                                    st.info("Please enter your Prolific ID at the top of the survey to prove you've completed this study.")
                                else:
                                    st.info("Thanks for taking our survey!")
                                    st.info("If you're using Prolific, please click this link to confirm your completion. https://app.prolific.co/submissions/complete?cc=7AC56F74")
                            else:
                                st.info("Thanks for taking our survey!")


                        if testing:
                            st.write(widget_values)
                
                    else:
                        st.warning("To complete the survey, please finish Phase 3.")
