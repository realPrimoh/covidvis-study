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
if testing:
    consent = True
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

    if platform != "Other" and platform != "-":
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
    demo_state = stateSelect("State", ['Select...', "AL", "AK", "AZ", "AR", "CA", "CO", "CT", "DC", "DE", "FL", "GA", 
              "HI", "ID", "IL", "IN", "IA", "KS", "KY", "LA", "ME", "MD", 
              "MA", "MI", "MN", "MS", "MO", "MT", "NE", "NV", "NH", "NJ", 
              "NM", "NY", "NC", "ND", "OH", "OK", "OR", "PA", "RI", "SC", 
              "SD", "TN", "TX", "UT", "VT", "VA", "WA", "WV", "WI", "WY"])

    i += 1

    # TODO: Prefer not to say, nonbinary, etc
    st.subheader(str(i) + ". What is your gender?")
    genderSel = record(st.selectbox, "Gender")
    demo_gender = genderSel("Gender", ('Select...','Male', 'Female', 'Nonbinary', 'Prefer not to say'))

    i += 1

    st.subheader(str(i) + ". What political party do you affiliate with?")
    partySel = record(st.selectbox, "Political Party")
    demo_party = partySel("Party", ('Select...', 'Democrat', 'Republican', 'Independent'))

    i += 1

    st.subheader(str(i) + ". What is your race?")
    raceSel = record(st.selectbox, "Race")
    demo_race = raceSel("Race", ("Select...", "Asian / Pacific Islander", "White", "Black or African-American", "Native American or American Indian", "Hispanic or Latino", "Other"))

    i += 1


    st.subheader(str(i) + ". What is the highest level of education you have completed or are currently completing?")
    eduSel = record(st.selectbox, "Education Level")
    demo_edu = eduSel("Education Level", ("Select...", "No schooling completed", "High School Diploma", "Undergraduate Degree", "Advanced Degree"))

    i += 1

    st.subheader(str(i) + ". What is your occupation, if any?")
    occupationSel = record(st.text_input, "Occupation")
    demo_occu = occupation = occupationSel("Occupation")

    i += 1
#
#    st.subheader(str(i) + ". How many times a week do you view coronavirus related info (articles, data, press releases, etc.)?")
#    virusInfoSel = record(st.selectbox, "Times a week consuming virus information")
#    virusInfoSel("Viewing", ("Select...", "0-5", "5-10", "10+"))
#
#    i += 1

    demographic_complete = False
    if testing:
        demographic_complete = True
    if demo_gender != 'Select...' and demo_party != "Select..." and demo_race != "Select..." and demo_edu != "Select..." and demo_occu != "Select...":
        demographic_complete = st.checkbox("I have completed the demographics survey above.")

    if demographic_complete:
        st.info("There are three phases to this survey. In Phase 1, you will be answering questions based on visualizations presented to you. In Phase 2, you will get to interact with some visualizations. In Phase 3, you will answer questions again based on visualizations shown to you.")


        st.header("Phase 1")

        st.subheader(str(i) + ". For each of the following orders, how effective are they to you if implemented properly and everyone follows them?")
        radio1 = record(st.selectbox, "Stay-at-home Effectiveness (Phase 1-effective)")
        radio2 = record(st.selectbox, "Social Distancing Effectiveness (Phase 1-effective)")
        radio3 = record(st.selectbox, "Mask On Effectiveness (Phase 1-effective)")
        radio4 = record(st.selectbox, "Closing Bars/Restaurants Effectiveness (Phase 1-effective)")

        i += 1

        radio1("Lockdown order (mandatory stay-at-home) if everyone obeys the directive", ["Select...", "Strongly Ineffective", "Slightly Ineffective", "Neutral", "Somewhat Effective", "Strongly Effective"])
        radio2("Social distancing if everyone obeys the directive", ["Select...", "Strongly Ineffective", "Slightly Ineffective", "Neutral", "Somewhat Effective", "Strongly Effective"])
        radio3("Mandatory masks in public if everyone obeys the directive", ["Select...", "Strongly Ineffective", "Slightly Ineffective", "Neutral", "Somewhat Effective", "Strongly Effective"])
        radio4("Closing bars/restaurants if everyone obeys the directive", ["Select...", "Strongly Ineffective", "Slightly Ineffective", "Neutral", "Somewhat Effective", "Strongly Effective"])

        st.subheader(str(i) + ". For each of the following orders, how effective are they to you in reality (if you feel there is a difference)?")
        radio1_1 = record(st.selectbox, "Stay-at-home Effectiveness")
        radio2_1 = record(st.selectbox, "Social Distancing Effectiveness")
        radio3_1 = record(st.selectbox, "Mask On Effectiveness")
        radio4_1 = record(st.selectbox, "Closing Bars/Restaurants Effectiveness")

        i += 1

        radio1_1("Lockdown order (mandatory stay-at-home) in reality", ["Select...", "Strongly Ineffective", "Slightly Ineffective", "Neutral", "Somewhat Effective", "Strongly Effective"])
        radio2_1("Social distancing in reality", ["Select...", "Strongly Ineffective", "Slightly Ineffective", "Neutral", "Somewhat Effective", "Strongly Effective"])
        radio3_1("Mandatory masks in public in reality", ["Select...", "Strongly Ineffective", "Slightly Ineffective", "Neutral", "Somewhat Effective", "Strongly Effective"])
        radio4_1("Closing bars/restaurants in reality", ["Select...", "Strongly Ineffective", "Slightly Ineffective", "Neutral", "Somewhat Effective", "Strongly Effective"])

        show_phase2 = False


        st.subheader(str(i) + ". Below, you'll be presented with a graph of the AVERAGE number of COVID-19 cases recorded per day in a certain US state. Based on your current knowledge and opinion of the pandemic, select an area of where RESTAURANTS/BARS were potentially CLOSED. Leave blank if you do not think restaurants/bars were closed at any point in the graph.")
        start_phase1 = record(st.slider, "Start - phase1")
        end_phase1 = record(st.slider, "End - phase1")
        start = start_phase1("Choose when you think restaurants/bars closed, if at all", 0, 160, 1)
        end = end_phase1("Choose when you think restaurants/bars opened, if at all", 0, 175, 170)
        phase1_base, phase1_img, warning = generate_rolling_cases_interactive('Arizona', datetime.datetime.strptime('03-10-2020', '%m-%d-%Y') + datetime.timedelta(days=start), datetime.datetime.strptime('03-10-2020', '%m-%d-%Y') + datetime.timedelta(days=end), False, False)
#        shading = create_shading_layer(180, 4000, start, end)
        if warning:
            st.warning(warning)
        x = st.altair_chart(phase1_base + phase1_img)
        i += 1
    #    y = st.altair_chart(shading)
    #    st.write(dir(x))
    #    st.write(dir(phase1_rolling))
    #    st.write(x.vega_lite_chart)
        # TODO: ADD INTERACTIVE TRENDLINE HERE


        # TODO: SELECT AN AREA WHERE YOU THINK MASKS WERE MANDATED

        show_phase3 = False
        
        if not warning:

            st.header("Phase 2")

            # MIDDLE
            # -----------------------
            session_state = SessionState.get(traj_looked_at=0, roll_looked_at=0, _next = False, _rolling = False)


            state_restaurant_close_dates = {"New York": '03-20-2020', "California": '03-19-2020', "Georgia": '04-02-2020', "Illinois": '03-21-2020', "Florida": '04-01-2020', "New Jersey": '03-21-2020', "Arizona": '06-29-2020', "Colorado": '03-19-2020', 'Indiana': '03-25-2020', 'Louisiana': '03-23-2020', "Texas": '03-31-2020', "Washington": '03-23-2020', "Pennsylvania": '04-01-2020'} # Bars/nightclubs in Florida = March 17
            state_restaurant_open_dates = {"New York": '05-15-2020', "California": '05-26-2020', "Georgia": '06-13-2020', "Illinois": '05-29-2020', "Florida": '06-03-2020', "New Jersey": '06-03-2020', "Arizona": '08-10-2020', "Colorado": '03-26-2020', 'Indiana': '07-04-2020', 'Louisiana': '05-15-2020', "Texas": '06-3-2020', "Washington": '06-01-2020', "Pennsylvania": '06-05-2020'} # NY: July 10 for malls too, NJ: May 18 for beginning, September 1 for end (https://en.wikipedia.org/wiki/COVID-19_pandemic_in_New_Jersey#Government_response)

            # Georgia: https://www.acluga.org/en/timeline-georgia-government-actions-regarding-covid-19
            # Texas: https://www.texastribune.org/2020/07/31/coronavirus-timeline-texas/
            # Florida: https://en.wikipedia.org/wiki/COVID-19_pandemic_in_Florida#Response
            # New York: https://en.wikipedia.org/wiki/COVID-19_pandemic_in_New_York_(state)#Government_response
            # Washington: https://www.seattlemet.com/health-and-wellness/2020/08/seattle-s-coronavirus-timeline-from-toilet-paper-to-mask-laws
            # Pennsylvania: https://en.wikipedia.org/wiki/COVID-19_pandemic_in_Pennsylvania#Government_response (REMOVE b/c of too many "phases")
            state_intervention = {"New York": '03-22-2020', "California": '03-19-2020', "Georgia": '04-02-2020', "Illinois": '03-21-2020', "Florida": '04-01-2020', "New Jersey": '03-21-2020', "Arizona": '05-11-2020', "Colorado": '04-30-2020', 'Indiana': '03-25-2020', 'Louisiana': '03-23-2020'}
            states = ['New York', 'Florida', 'Texas']
            # Florida: April 1st was statewide stay-at-home-order> Bars/nightclubs had already closed by this day. Phase 2 reopening June 3rd
            # Texas: March 19th (restaurants, bars, schools, closed). March 31st Texans told to stay home but not called "stay-at-home order",
            # and on June 3rd almost all businesses at 50% capacity. On June 12th, restaurants at 75% capacity.
            # New York: March 20th stay at home order, it officially ends May 15th but no real "reopening of whole state" occurred

            st.subheader("Choose a state from the drop-down menu to see the number of new cases each day.\
                      Once you choose a state, you can click and drag on the graph to see the total number of cases that fall in a\
                      certain region. You can move your selected square as well as change its size by scrolling up or down. A video\
                      demonstrating how to interact with the graph is also presented below. \n\nYou must study at least three states\
                      before you can move on.")
            st.video('./media/demo.mp4', format='video/mp4', start_time=7)
            phase2_look1 = st.selectbox("Pick a state to view its trajectory and play around with it.",  ["Select..."] + states)
            #but = False
            if not session_state._next:
                if testing:
                        session_state.traj_looked_at = 5
                        show_phase3 = True
                if phase2_look1 in states:
                    if phase2_look1 == 'New York':
                      st.info("New York implemented a state-wide stay-at-home order on Day 12, which closed all non-essential businesses and\
                              canceled/postponed all non-essential gatherings. New York did not ever reopen the entire state, but we mark Day 66\
                              as the end date, as that was when the first counties were allowed to enter some phase of reopening.")
                    if phase2_look1 == 'Florida':
                      st.info("We mark Day 22 as the start day, as that is when a state-wide stay-at-home order was issue. It is worth noting\
                              that bars and restaurants had already closed previously. We mark Day 85 as the end day, as that is when Florida\
                              entered Phase 2 of reopening (except Broward, Miami-Dade, and Palm Beach counties), which allowed most businesses\
                              to resume operations at 50 percent capacity. For details about Florida's Phase 2, see this link: https://www.flgov\
                              .com/wp-content/uploads/covid19/Exec%20Order%20Phase%202%20FAQs.pdf")
                    if phase2_look1 == 'Texas':
                      st.info("Texas closed restaurants, bars, and schools on Day 9. However, we mark Day 21 as the start date, as that is when\
                              Texans were told to stay home for all non-essential reasons. It is worth noting that the governor declined to call\
                              this an official stay-at-home order. We mark Day 85 as the end day, as Texas allowed almost all businesses to resume\
                              operations at 50 percent capacity. On Day 94, restaurants were allowed to open at 75 percent capacity.")
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


            if show_phase3:
                st.header("Phase 3")
                st.subheader("Below, you will be presented with the same questions you answered from Phase 1. If your answers to these questions are the same as in Phase 1, please select them again. Use the slider to view the range of different options, and make your selection\
                              using the drop-down menu.")


                st.subheader(str(i) + ". For each of the following orders, how effective are they to you if implemented properly and everyone follows them?")
                radio1phase3 = record(st.selectbox, "Lockdown (Mandatory stay-at-home) Effectiveness (Phase 3-effective)")
                radio2phase3 = record(st.selectbox, "Social Distancing Effectiveness (Phase 3-effective)")
                radio3phase3 = record(st.selectbox, "Mask On Effectiveness (Phase 3-effective)")
                radio4phase3 = record(st.selectbox, "Closing Bars/Restaurants Effectiveness (Phase 3-effective)")
                i += 1

                radio1phase3("Lockdown order (mandatory stay-at-home) if everyone obeys the directive (Phase 3)", ["Select...", "Strongly Ineffective", "Slightly Ineffective", "Neutral", "Somewhat Effective", "Strongly Effective"])
                radio2phase3("Social distancing if everyone obeys the directive (Phase 3)", ["Select...", "Strongly Ineffective", "Slightly Ineffective", "Neutral", "Somewhat Effective", "Strongly Effective"])
                radio3phase3("Mandatory masks in public in if everyone obeys the directive (Phase 3)", ["Select...", "Strongly Ineffective", "Slightly Ineffective", "Neutral", "Somewhat Effective", "Strongly Effective"])
                radio4phase3("Closing bars/restaurants if everyone obeys the directive (Phase 3)", ["Select...", "Strongly Ineffective", "Slightly Ineffective", "Neutral", "Somewhat Effective", "Strongly Effective"])

                st.subheader(str(i) + ". For each of the following orders, how effective are they to you if they were implemented in the US today?")
                radio1phase3_1 = record(st.selectbox, "Stay-at-home Effectiveness (Phase 3)")
                radio2phase3_1 = record(st.selectbox, "Social Distancing Effectiveness (Phase 3)")
                radio3phase3_1 = record(st.selectbox, "Mask On Effectiveness (Phase 3)")
                radio4phase3_1 = record(st.selectbox, "Closing Bars/Restaurants Effectiveness (Phase 3)")
                i += 1

                radio1phase3_1("Lockdown order (mandatory stay-at-home) in reality (Phase 3)", ["Select...", "Strongly Ineffective", "Slightly Ineffective", "Neutral", "Somewhat Effective", "Strongly Effective"])
                radio2phase3_1("Social distancing in reality (Phase 3)", ["Select...", "Strongly Ineffective", "Slightly Ineffective", "Neutral", "Somewhat Effective", "Strongly Effective"])
                radio3phase3_1("Mandatory masks in public in reality (Phase 3)", ["Select...", "Strongly Ineffective", "Slightly Ineffective", "Neutral", "Somewhat Effective", "Strongly Effective"])
                radio4phase3_1("Closing bars/restaurants in reality (Phase 3)", ["Select...", "Strongly Ineffective", "Slightly Ineffective", "Neutral", "Somewhat Effective", "Strongly Effective"])

                st.subheader(str(i) + ". Below, you'll be presented with a graph of the AVERAGE number of COVID-19 cases recorded per day in a certain US state. Based on your current knowledge and opinion of the pandemic, select an area of where RESTAURANTS/BARS were potentially CLOSED. Leave blank if you do not think restaurants/bars were closed at any point in the graph.")

                record_start_phase3 = record(st.slider, "start-phase3")
                record_end_phase3 = record(st.slider, "end-phase3")
                start_phase3 = record_start_phase3("Choose when you think restaurants/bars closed, if at all ", 0, 160, 1)
                end_phase3 = record_end_phase3("Choose when you think restaurants/bars opened, if at all ", 0, 175, 170)
                phase3_base, phase3_img, warning_phase3 = generate_rolling_cases_interactive('Arizona', datetime.datetime.strptime('03-10-2020', '%m-%d-%Y') + datetime.timedelta(days=start_phase3), datetime.datetime.strptime('03-10-2020', '%m-%d-%Y') + datetime.timedelta(days=end_phase3), False, False)
    #            shading = create_shading_layer(180, 4000, start, end)
    
                if warning_phase3:
                    st.warning(warning_phase3)
                x = st.altair_chart(phase3_base + phase3_img)

                
                if not warning_phase3:

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
                        bar = st.progress(0)
                        for percent_complete in range(100):
                            time.sleep(0.05)
                            bar.progress(percent_complete + 1)
                        if platform == "MTurk":
                            st.info("Please record this ID down and enter it in the appropriate place in MTurk to signify your completion.")
                            st.balloons()

                            st.info(str(response.content.decode('UTF-8')))
                        elif platform == "Prolific":
                            st.info("If you're using Prolific, please click this link. https://app.prolific.co/submissions/complete?cc=7AC56F74")
                            st.balloons()
                        else:
                            st.info("Thanks for taking our survey!")
                            st.balloons()



                # Overlays of lines to provide context to the user when picking (highlight line when picked)

                # Generate random trends to reduce bias
                # Generate lines independent of the true line, which of these random lines do you think are closest to the true line
                # Random sample of trends (reduce bias of the true line, ex. no median picking should be the answer)

                # Plot the rate of change versus cumulative (log scale)
                #st.write("Recorded values: ", widget_values)
