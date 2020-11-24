import pandas as pd
import numpy as np
import altair as alt
import random
import streamlit as st
import math



def create_state_df(state):
    jhu_df = pd.read_csv('./final_data/jhu-data.csv') # B/C this gets called from ../../covidvisstudy.py
    # grab us-specific
    jhu_df = jhu_df[(jhu_df.Country_Region == 'United States') & jhu_df.Province_State.notnull()]
    state_cases = jhu_df[jhu_df["Province_State"] == state].sort_values("Date")
    state_cases["Date"] = pd.to_datetime(state_cases["Date"])
    state_cases = state_cases[(state_cases["Date"] > pd.to_datetime("03-9-2020")) & (state_cases["Date"] < pd.to_datetime("10-1-2020"))]
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
def add_image_col_to_df(state_cases_df, start_day, end_day=None):
    if end_day:
        state_image = state_cases_df.copy()
        state_image["image_url"] = "" # Will automatically fill up all columns
        state_image.loc[start_day, "image_url"] = "https://raw.githubusercontent.com/Murtz5253/covid19-vis/master/images/x-shelter.png"
        state_image.loc[end_day, "image_url"] = "https://raw.githubusercontent.com/Murtz5253/covid19-vis/master/images/shelter.png"
        colors = ['lockdown_off' if (x < (start_day + 1) or x > (end_day - 1)) else 'lockdown_on' for x in range(state_image.shape[0])]
        state_image["color"] = colors
        return state_image
    else:
        state_image = state_cases_df.copy()
        state_image["image_url"] = "" # Will automatically fill up all columns
        state_image.loc[start_day, "image_url"] = "https://raw.githubusercontent.com/Murtz5253/covid19-vis/master/images/x-shelter.png"
        colors = ['before' if x < (start_day+1) else 'after' for x in range(state_image.shape[0])]
        state_image["color"] = colors
        return state_image

def add_image_col_to_df_with_date(state_cases_df, start_date, end_date=None):
    if end_date:
        state_image = state_cases_df.copy()
        state_image["image_url"] = "" # Will automatically fill up all columns
        state_image.loc[state_cases_df['Date'] == start_date, "image_url"] = "https://raw.githubusercontent.com/Murtz5253/covid19-vis/master/images/x-shelter.png"
        state_image.loc[state_cases_df['Date'] == end_date, "image_url"] = "https://raw.githubusercontent.com/Murtz5253/covid19-vis/master/images/shelter.png"
        bools1, bools2 = state_cases_df['Date'] <= start_date, state_cases_df['Date'] >= end_date
        bools = [x or y for (x, y) in zip(bools1, bools2)] # Should do a pairwise or of the list elements
        colors = ['off' if x else 'on' for x in bools]
        state_image["color"] = colors
        return state_image
    else:
        state_image = state_cases_df.copy()
        state_image["image_url"] = "" # Will automatically fill up all columns
        state_image.loc[state_cases_df['Date'] == date, "image_url"] = "https://raw.githubusercontent.com/Murtz5253/covid19-vis/master/images/x-shelter.png"
        bools = state_cases_df['Date'] <= date
        colors = ['before' if x else 'after' for x in bools]
        state_image["color"] = colors
        return state_image

def create_base_log_layer(df, x_label, y_label, is_selection=False, selection=None, title=""):
    if is_selection:
        base = alt.Chart(df).mark_line().encode(
            alt.X('Day:Q',
                 scale=alt.Scale(domain=(0, max(df[x_label])))
            ),
            alt.Y('Confirmed:Q',
                 scale=alt.Scale(type='log', base=10, domain=[1, 10000000])
            ),
            color=alt.Color('color:N', legend=None),
            ).properties(
                width=600,
                height=400,
                title=title
            ).add_selection(
                selection
            ).transform_filter(
                selection
            )
    else:
        base = alt.Chart(df).mark_line().encode(
                alt.X('Day:Q',
                     scale=alt.Scale(domain=(0, max(df[x_label])))
                ),
                alt.Y('Confirmed:Q',
                     scale=alt.Scale(type='log', base=10, domain=[1, 10000000])
                ),
                color=alt.Color('color:N', legend=None),
                ).properties(
                    width=600,
                    height=400,
                    title=title
                )
    return base



def create_image_layer(df, x_label, y_label, image_col_name):
    img = alt.Chart(df).mark_image(
            width=28,
            height=28
        ).encode(
            x=x_label+':Q',
            y=y_label+':Q',
            url=image_col_name
        ).properties(
            width=600,
            height=400
        )
    return img

# The below function creates an area chart that simulates "shading" for our charts
# Note that "max_y_axis" may be larger than the actual max for y--it is basically the max the chart shows
def create_shading_layer(max_x, max_y, lockdown_start_day, lockdown_end_day):
    x_axis = list(range(max_x + 1))
    y_axis = [max_y] * len(x_axis)
    colors = ([0] * lockdown_start_day) + ([1] * (lockdown_end_day - lockdown_start_day)) + ([0] * (len(x_axis) - lockdown_end_day))
    data = {"x" : x_axis[:], "y" : y_axis[:], "colors" : colors[:]}
    shade_df = pd.DataFrame(data)
    shading_chart = alt.Chart(shade_df).mark_area(
                        opacity=0.3
                    ).encode(
                        x="x:Q",
                        y="y:Q",
                        color=alt.Color(
                            scale=alt.Scale(
                                domain=[0, 1],
                                range=['white', 'pink']
                            ),
                            type="quantitative"
                        )
                    ).properties(
                        width=600,
                        height=400
                    )
    return shading_chart


# Function below generates interactive brush selection chart for rolling cases
@st.cache(allow_output_mutation=True, persist=True, suppress_st_warning=True)
def generate_rolling_cases_interactive(state, start_date, end_date, show_bar=True, interactive=True):
    warning = None
    if start_date > end_date:
        warning = "WARNING: Start of restaurant closures cannot be after the end of restaurant closures. You will not be able to move forward until this is fixed."
    df = create_state_df(state)
    df = add_image_col_to_df_with_date(df, start_date, end_date)
    df["New_Cases_Rolling"] = df["New_Cases"].rolling(window=7, min_periods=1).mean()
    brush = alt.selection_interval(encodings=['x'], empty='all', mark=alt.BrushConfig(fill='red'))
    base = alt.Chart(df).mark_line().encode(
                x='Day:Q',
                y=alt.Y('New_Cases_Rolling:Q', axis=alt.Axis(title="New COVID-19 Cases per Day")),
            ).properties(
                width=600,
                height=400
            ).add_selection(
                brush
            )
    
    if not interactive:
        base = alt.Chart(df).mark_line().encode(
                x='Day:Q',
                y=alt.Y('New_Cases_Rolling:Q', axis=alt.Axis(title="New COVID-19 Cases per Day")),
            ).properties(
                width=600,
                height=400
            )

    img = create_image_layer(df, 'Day', 'New_Cases_Rolling', 'image_url')

    bars = alt.Chart(df).mark_bar().encode(
        alt.Y('Province_State:N', axis=alt.Axis(title="State")),
        alt.X('sum(New_Cases_Rolling):Q', axis=alt.Axis(title='Total COVID-19 Cases in Selected Period')),
        opacity=alt.value(0.9)
    ).transform_filter(
        brush
    ).properties(
        width=600,
        height=40
    )

    if not show_bar:
        return (base, img, warning)
    return (base + img) & bars

# Function below creates log_trendline SLIDER charts using the data we loaded in from CSV files
def generate_altair_slider_log_chart(df, title=""):
    df_trimmed = df[df["Type"] != "actual"] # We do not want to display the actual trendline
    for i in range(1, 6):
        df_trimmed.loc[:, ["Type"]] = df_trimmed["Type"].str.replace(
          "steeper_" + str(i), "steeper_" + str(i + 5))
    df_trimmed.loc[:, ["Type"]] = df_trimmed["Type"].str.replace("[^0-9]", "").apply(lambda x : int(x)) # We need numbers for altair slider
    df_trimmed.loc[:, ["image_url"]] = df_trimmed["image_url"].fillna("") # Empty string signifies no image for those rows

    # We want 7 options instead of 10, so we trim down
    #df_trimmed.loc[:, ["Type"]] = df_trimmed["Type"].isin(trendlines_to_keep)

    slider = alt.binding_range(min=1, max=10, step=1)
    select_trend = alt.selection_single(name="Trendline", fields=['Type'],
                                       bind=slider, init={'Type': 1})
    base = create_base_log_layer(df_trimmed, "Day", "Confirmed", is_selection=True, selection=select_trend, title=title)
    # We only use the head for the image layer because the images are in the same position for each trendlines
    # and we do not need a bunch of them overlaid
    img = create_image_layer(df_trimmed.head(60), "Day", "Confirmed","image_url")
    final = base + img
    return final

# Same as above, but retains the actual trendline as well
def generate_altair_slider_log_chart_KEEP_ACTUAL(df):
    df_trimmed = df.copy()
    df_trimmed.loc[:, ["Type"]] = df_trimmed["Type"].str.replace("actual", "6") # We want the actual one as trendline 0
    for i in range(1, 6):
        df_trimmed.loc[:, ["Type"]] = df_trimmed["Type"].str.replace(
          "steeper_" + str(i), "steeper_" + str(i + 6)) # Because we want number 6 to be the actual one
    df_trimmed.loc[:, ["Type"]] = df_trimmed["Type"].str.replace("[^0-9]", "").apply(lambda x : int(x)) # We need numbers for altair slider
    df_trimmed.loc[:, ["image_url"]] = df_trimmed["image_url"].fillna("") # Empty string signifies no image for those rows
    slider = alt.binding_range(min=1, max=11, step=1)
    select_trend = alt.selection_single(name="Trendline", fields=['Type'],
                                       bind=slider, init={'Type': 1})
    base = create_base_log_layer(df_trimmed, "Day", "Confirmed", is_selection=True, selection=select_trend)
    # We only use the head for the image layer because the images are in the same position for each trendlines
    # and we do not need a bunch of them overlaid
    img = create_image_layer(df_trimmed.head(60), "Day", "Confirmed","image_url")
    final = base + img
    return final

def generate_new_cases_rolling(state, intervention_day, width, height, title=""):
    df = create_state_df(state)
    df = add_image_col_to_df(df, intervention_day)
    # df["image_url"] = ""
    # df.loc[val, "image_url"] = "https://raw.githubusercontent.com/Murtz5253/covid19-vis/master/images/x-shelter.png"
    colors = ['before' if x < intervention_day else 'after' for x in range(df.shape[0])]
    df["color"] = colors
    df["New_Cases_Rolling"] = df["New_Cases"].rolling(window=7, min_periods=1).mean()

    # We do not use the methods above because these charts are slightly different
    base = alt.Chart(df).mark_line().encode(
        x='Day:Q',
        y='New_Cases_Rolling:Q',
        color=alt.Color('color:N', legend=None),
    ).properties(
        width=width,
        height=height,
        title=title
    )

    img = alt.Chart(df).mark_image(
        width=45,
        height=45
    ).encode(
        x='Day:Q',
        y='New_Cases_Rolling:Q',
        url='image_url'
    ).properties(
        width=width,
        height=height
    )
    final = base + img
    return final

def generate_actual_state_log_chart(state, inflection_date):
    state_cases = create_state_df(state)
    state_cases = add_image_col_to_df_with_date(state_cases, inflection_date)
    base = create_base_log_layer(state_cases, "Day", "Confirmed")
    img = create_image_layer(state_cases, "Day", "Confirmed", "image_url")
    
    return base + img


# ASSUMES THE INDEX HAS BEEN RESET SO BE CAREFUL
def generate_intervention_images_new_cases_rolling(state, inflection_date):
    df = create_state_df(state)
    df = add_image_col_to_df_with_date(df, inflection_date)
    df["new_cases_rolling"] = df["New_Cases"].rolling(window=7).mean().fillna(50) # KEPT FIRST 7 DAYS AS ESTIMATE OF 50
    base = alt.Chart(df).mark_line().encode(
        x='Day:Q',
        y=alt.Y('new_cases_rolling:Q', scale=alt.Scale(domain=[0, 10000])),
        color='color',
    ).properties(
        width=500,
        height=300
    )

    img = create_image_layer(df, 'Day', 'new_cases_rolling', 'image_url')
    
    final = base + img
    final.properties
    return final
    #print(val)
    #display(final)



"""
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
    recalibrate = lambda x : math.ceil(x/2) # So we do not have every other number anymore
    final['Option'] = final['Option'].apply(recalibrate)
    st.write(final)
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
    # Source: https://stackoverflow.com/questions/61194028/adding-labels-at-end-of-line-chart-in-altairs
    labels = alt.Chart(final).mark_text(align='left', dx=3).encode(
        alt.X('Day:Q', aggregate='max'),
        alt.Y('Confirmed:Q', aggregate={'argmax': 'Day'}),
        alt.Text('Option'),
        alt.Color('Option:N', legend=None)
    )
    st.altair_chart(labels)
    
    img = create_image_layer(df, 'Day', 'Confirmed', 'image_url')
    result = result + img + labels
    return result
"""

