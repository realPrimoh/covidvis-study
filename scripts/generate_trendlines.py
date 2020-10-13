import pandas as pd
import numpy as np
import altair as alt
import random
import streamlit as st



def create_state_df(state):
    jhu_df = pd.read_csv('./data/jhu-data.csv') # B/C this gets called from ../../covidvisstudy.py
    # grab us-specific
    jhu_df = jhu_df[(jhu_df.Country_Region == 'United States') & jhu_df.Province_State.notnull()]
    state_cases = jhu_df[jhu_df["Province_State"] == state].sort_values("Date")
    state_cases["Date"] = pd.to_datetime(state_cases["Date"])
    state_cases = state_cases[state_cases["Date"] < pd.to_datetime("05-03-2020")]
    # Convert timedelta to days
    # Source https://stackoverflow.com/questions/18215317/extracting-days-from-a-numpy-timedelta64-value
    earliest_date = state_cases.sort_values('Date')['Date'].values[0]
    days_passed = lambda date : int((date - earliest_date) / np.timedelta64(1, 'D'))
    state_cases['Day'] = state_cases['Date'].apply(days_passed)
    # Add new cases each day
    state_cases["New_Cases"] = state_cases["Confirmed"].diff().fillna(0)
    state_cases = state_cases.drop(["Unnamed: 0", 'Country_Region', 'Recovered',\
        'Active', 'Deaths'], axis=1)
    # Necessary for methods below to work properly; index should match day
    state_cases = state_cases.reset_index().drop("index", axis=1) 
    return state_cases

# The method below takes in a processed state_cases df and adds an image column
# based on the day of the stay_at_home order
# Returns a NEW dataframe; not a destructive method
def add_image_col_to_df(state_cases_df, day):
    state_image = state_cases_df.copy()
    state_image["image_url"] = "" # Will automatically fill up all columns
    state_image.loc[day, "image_url"] = "https://raw.githubusercontent.com/Murtz5253/covid19-vis/master/images/x-shelter.png"
    colors = ['before' if x < (day+1) else 'after' for x in range(state_image.shape[0])]
    state_image["color"] = colors
    return state_image

def add_image_col_to_df_with_date(state_cases_df, date):
    state_image = state_cases_df.copy()
    state_image["image_url"] = "" # Will automatically fill up all columns
    state_image.loc[state_cases_df['Date'] == date, "image_url"] = "https://raw.githubusercontent.com/Murtz5253/covid19-vis/master/images/x-shelter.png"
    bools = state_cases_df['Date'] <= date
    colors = ['before' if x else 'after' for x in bools]
    state_image["color"] = colors
    return state_image



def create_image_layer(df, x_label, y_label, image_col_name):
    img = alt.Chart(df).mark_image(
            width=50,
            height=50
        ).encode(
            x=x_label+':Q',
            y=y_label+':Q',
            url=image_col_name
        ).properties(
            width=500,
            height=300
        )
    return img

# Function below takes in dataframe with at least two numerical columns: x & y
def generate_single_graph_exponential(df, inflection_day):
    # Source: https://stackoverflow.com/questions/33186740/fitting-exponential-function-through-two-data-points-with-scipy-curve-fit
    # Used for second half of function
    def func(x, adj1,adj2):
        return ((x+adj1) ** pw) * adj2
    
    counter = 1
    trends = []
    seq = np.arange(.3, 1.0, .1)
    weights = [random.choice(seq) for i in range(5)] # First the smaller slopes
    weights.sort() # Ensures that charts are generates in correct order

    for val in weights:
        test = df.copy()
        original = df["Confirmed"].values[inflection_day:]
        step = original[1] - original[0]
        new_step = step * val
        # y = m(x - x1) + y1
        f = lambda x : new_step * (x - inflection_day) + original[0]
        updated = [f(x) for x in range(inflection_day, test.shape[0])]
        test.loc[inflection_day:, "Confirmed"] = np.random.normal(updated, scale=500)
        test['Option'] = np.array([counter] * test.shape[0])
        trends.append(test)
        counter += 1
    seq = np.arange(1, 2, .1) # Range of exponents
    weights = [random.choice(seq) for i in range(5)] # Now the larger, exponential slopes
    weights.sort()

    for val in weights:
        test = df.copy()
        original = df["Confirmed"].values[inflection_day:]
        #print(original)
        x = [inflection_day, inflection_day + 1]
        y = [original[0], original[1]]
        
        pw = val # the weight is the exponent this time
        A = np.exp(np.log(y[0]/y[1])/pw)
        a = (x[0] - x[1]*A)/(A-1)
        b = y[0]/(x[0]+a)**pw
        
        xf = np.arange(inflection_day, df.shape[0])
        updated = func(xf, a, b)
        #print(updated)
        test.loc[inflection_day:, "Confirmed"] = np.random.normal(updated, scale=500)
        test['Option'] = np.array([counter] * test.shape[0])
        trends.append(test)
        counter += 1
        
    # Now we put them all together into a single graph
    trends = trends[::2] # Keep every other element
    final = pd.concat(trends)
    final = final.reset_index()
    final = final.drop(["index"], axis=1)
    selector = alt.selection_single(empty='all', fields=['Option'])
    color = alt.condition(selector,
                          alt.Color('Option:N'),
                          alt.value('lightgray'))
    final["size"] = 1
    opacity = alt.condition(selector, alt.value(1.0), alt.value(0.3))

    result = alt.Chart(final).mark_line().encode(
        x='Day:Q',
        y='Confirmed:Q',
        color=alt.Color('Option:N', legend=None),
        opacity=opacity,
        size=alt.Size('size:Q', legend=None)
    ).add_selection(selector
    ).properties(
            width=600,
            height=400
    )
    
    img = create_image_layer(df, 'Day', 'Confirmed', 'image_url')
    result = result + img
    return result

def generate_state_chart_normal(state, inflection_day):
    jhu_df = pd.read_csv('./data/jhu-data.csv') # B/C this gets called from ../../covidvisstudy.py
    # grab us-specificjhu_df = jhu_df[(jhu_df.Country_Region == 'United States') & jhu_df.Province_State.notnull()]
    state_cases = jhu_df[jhu_df["Province_State"] == state].sort_values("Date")
    state_cases["Date"] = pd.to_datetime(state_cases["Date"])
    state_cases = state_cases[(state_cases["Date"] < pd.to_datetime("10-20-2020"))]
    earliest_date = state_cases.sort_values('Date')['Date'].values[0]
    days_passed = lambda date : int((date - earliest_date) / np.timedelta64(1, 'D'))
    state_cases['Day'] = state_cases['Date'].apply(days_passed)
    state_cases["image_url"] = "" # Will automatically fill up all comments
    state_cases.loc[state_cases['Date'] == inflection_day, "image_url"] = "https://raw.githubusercontent.com/Murtz5253/covid19-vis/master/images/x-shelter.png"
    result = alt.Chart(state_cases).mark_line().encode(
            x='Day:Q',
            y='Confirmed:Q',
            color=alt.Color('Province_State', legend=alt.Legend(title="State", titleFontSize=20, labelFontSize=20, symbolStrokeWidth=10, symbolSize=1000))
        ).properties(
                width=750,
                height=500,
                
        )
    
    
    img = alt.Chart(state_cases).mark_image(
            width=30,
            height=30
        ).encode(
            x='Day'+':Q',
            y='Confirmed'+':Q',
            url='image_url'
        ).properties(
            width=600,
            height=400
        )
    
    return result + img


# ASSUMES THE INDEX HAS BEEN RESET SO BE CAREFUL
def generate_intervention_images_new_cases_rolling(state, inflection_date):
    df = create_state_df(state)
    df = add_image_col_to_df_with_date(df, inflection_date)
    df["new_cases_rolling"] = df["New_Cases"].rolling(window=7).mean().fillna(50) # KEPT FIRST 7 DAYS AS ESTIMATE OF 50
    base = alt.Chart(df).mark_line().encode(
        x='Day:Q',
        y='new_cases_rolling:Q',
        color='color',
    ).properties(
        width=500,
        height=300
    )

    img = create_image_layer(df, 'Day', 'new_cases_rolling', 'image_url')
    
    final = base + img
    return final
    #print(val)
    #display(final)