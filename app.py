#!/usr/bin/env python
__author__ = "Nathaniel Habtegergesa"

"""
Dataset location:
    https://github.com/CSSEGISandData/COVID-19/tree/master/csse_covid_19_data/csse_covid_19_time_series
"""

# ---------------------------------------------------------------------------------------------
# imports
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go

# -*- coding: utf-8 -*-
import dash
import dash_core_components as dcc
import dash_html_components as html

# html embedding
from IPython.display import Javascript
from IPython.core.display import display, HTML
# ---------------------------------------------------------------------------------------------

# Overwrite your CSS setting by including style locally
colors = {
    'background': '#2D2D2D',
    'text': '#E1E2E5',
    'figure_text': '#ffffff',
    'confirmed_text': '#3CA4FF',
    'deaths_text': '#f44336',
    'recovered_text': '#5A9E6F',
    'highest_case_bg': '#393939',

}

# Creating custom style for local use
divBorderStyle = {
    'backgroundColor': '#393939',
    'borderRadius': '12px',
    'lineHeight': 0.9,
}

# Creating custom style for local use
boxBorderStyle = {
    'borderColor': '#393939',
    'borderStyle': 'solid',
    'borderRadius': '10px',
    'borderWidth': 2,
}


# ---------------------------------------------------------------------------------------------
# Collecting and cleaning data (importing csv into pandas)
# importing datasets
death_df = pd.read_csv(
    "https://raw.githubusercontent.com/CSSEGISandData/COVID-19/master/csse_covid_19_data/csse_covid_19_time_series/time_series_covid19_deaths_global.csv")
confirmed_df = pd.read_csv(
    "https://raw.githubusercontent.com/CSSEGISandData/COVID-19/master/csse_covid_19_data/csse_covid_19_time_series/time_series_covid19_confirmed_global.csv")
recovered_df = pd.read_csv(
    "https://raw.githubusercontent.com/CSSEGISandData/COVID-19/master/csse_covid_19_data/csse_covid_19_time_series/time_series_covid19_recovered_global.csv")
url = 'https://raw.githubusercontent.com/imdevskp/covid_19_jhu_data_web_scrap_and_cleaning/master/covid_19_clean_complete.csv'
full_table = pd.read_csv(url,
                         parse_dates=['Date'])

# cases
cases = ['Confirmed', 'Deaths', 'Recovered', 'Active']

# Active Case = confirmed - deaths - recovered
full_table['Active'] = full_table['Confirmed'] - \
    full_table['Deaths'] - full_table['Recovered']

# replacing Mainland china with just China
full_table['Country/Region'] = full_table['Country/Region'].replace(
    'Mainland China', 'China')

# filling missing values
full_table[['Province/State']] = full_table[['Province/State']].fillna('')
full_table[cases] = full_table[cases].fillna(0)

# latest
full_latest = full_table[full_table['Date']
                         == max(full_table['Date'])].reset_index()

# latest condensed
full_latest_grouped = full_latest.groupby(
    'Country/Region')['Confirmed', 'Deaths', 'Recovered', 'Active'].sum().reset_index()

temp = full_table.groupby(['Country/Region', 'Province/State']
                          )['Confirmed', 'Deaths', 'Recovered', 'Active'].max()

# hide_input
temp = full_table.groupby(
    'Date')['Confirmed', 'Deaths', 'Recovered', 'Active'].sum().reset_index()
temp = temp[temp['Date'] == max(temp['Date'])].reset_index(drop=True)

temp = full_table.groupby(
    'Date')['Recovered', 'Deaths', 'Active'].sum().reset_index()
temp = temp.melt(id_vars="Date", value_vars=['Recovered', 'Deaths', 'Active'],
                 var_name='Case', value_name='Count')

print("Here 1")

# Rename to consistent values
confirmed_df['Country/Region'].replace('Mainland China', 'China', inplace=True)
death_df['Country/Region'].replace('Mainland China', 'China', inplace=True)
recovered_df['Country/Region'].replace('Mainland China', 'China', inplace=True)

print("Here 2")

# rename
confirmed_df = confirmed_df.rename(columns={'Country/Region': 'country'})
death_df = death_df.rename(columns={'Country/Region': 'country'})
recovered_df = death_df.rename(columns={'Country/Region': 'country'})

print("Here 3")

# Handle empty data
confirmed_df[['Province/State']] = confirmed_df[['Province/State']].fillna('')
confirmed_df.fillna(0, inplace=True)
death_df[['Province/State']] = death_df[['Province/State']].fillna('')
death_df.fillna(0, inplace=True)
recovered_df[['Province/State']] = recovered_df[['Province/State']].fillna('')
recovered_df.fillna(0, inplace=True)

print("Here 4")

# Aggregating all the data to see a snapshot of the total number of cases
# the columns up to four are non-integer columns
total_confirmed = confirmed_df.iloc[:, 4:].sum().max()
total_deaths = death_df.iloc[:, 4:].sum().max()
total_recovered = recovered_df.iloc[:, 4:].sum().max()
# print(total_confirmed, total_deaths, total_recovered)

print("Here 5")

# the total number of active cases is: Active = confimred - deaths - recovered
world_df = pd.DataFrame({
    'confirmed': [total_confirmed],
    'deaths': [total_deaths],
    'recovered': [total_recovered],
    'active': [total_confirmed - total_deaths - total_recovered]
})
print(world_df)

print("Here 6")

# unpivot the dataframe from wide to long format
word_long_df = world_df.melt(
    value_vars=['active', 'deaths', 'recovered'], var_name="status", value_name="count")
word_long_df['upper'] = 'confirmed'
print(word_long_df)

print("Here 7")

# time series
worldwide_confirmed = confirmed_df.iloc[:, 4:].sum(axis=0)
worldwide_deaths = death_df.iloc[:, 4:].sum().max(axis=0)
worldwide_recovered = recovered_df.iloc[:, 4:].sum(axis=0)
worldwide_active = worldwide_confirmed - worldwide_deaths - worldwide_recovered

print("Here 8")

# calculate recovery and mortality rates as a fraction of confirmed
world_rate_df = pd.DataFrame({
    'confirmed': worldwide_confirmed,
    'deaths': worldwide_deaths,
    'recovered': worldwide_recovered,
    'active': worldwide_active
}, index=worldwide_confirmed.index)

print("Here 9")

world_rate_df['recovery rate'] = world_rate_df['recovered'] / \
    world_rate_df['confirmed'] * 100
world_rate_df['mortality rate'] = world_rate_df['recovered'] / \
    world_rate_df['confirmed'] * 100
world_rate_df['date'] = world_rate_df.index

print("Here 10")

# unpivot the dataframe from wide to long format
word_rate_long_df = world_rate_df.melt(id_vars='date',
                                       value_vars=['recovery rate', 'mortality rate'], var_name="status", value_name="ratio")
# print(word_rate_long_df)

print("Here 11")

# group by rows that contain the country/region values and then sum all the values
covid_confirmed_agg = confirmed_df.groupby(
    'country').sum().reset_index()

covid_confirmed_agg.loc[:, ['Lat', 'Long']
                        ] = confirmed_df.groupby('country').mean().reset_index().loc[:, ['Lat', 'Long']]

# covid_confirmed_agg = covid_confirmed_agg[covid_confirmed_agg.iloc[:, 3:].max(
#     axis=1)]

print("Here 12")

# Since there are a lot of countries, for easy visualization let us only look at countries with high numbers
MIN_CASES = 1000
covid_confirmed_agg = covid_confirmed_agg[covid_confirmed_agg.iloc[:, 3:].max(
    axis=1) > MIN_CASES]

covid_confirmed_agg_long = pd.melt(covid_confirmed_agg,
                                   id_vars=covid_confirmed_agg.iloc[:, :3],
                                   var_name='date',
                                   value_vars=covid_confirmed_agg.iloc[:, 3:],
                                   value_name='date_confirmed_cases')


print("Here 13")

# ---------------------------------------------------------------------------------------------


# ---------------------------------------------------------------------------------------------
# Visualizations
print("Here 14")
# World map
# fig_map = px.scatter_geo(covid_confirmed_agg_long,
#                          lat="Lat", lon="Long", color="country",
#                          hover_name="country", size="date_confirmed_cases",
#                          size_max=50, animation_frame="date",
#                          projection="natural earth",
#                          title="COVID-19 worldwide confirmed cases over time")
# fig_map.update_layout(
#     plot_bgcolor=colors['background'],
#     paper_bgcolor=colors['background'],
#     font={
#         'color': colors['text']
#     }
# )

print("Here 15")
# Tree map
fig_tree = px.treemap(word_long_df, path=[
    "status"], title="Title", values="count", color_discrete_sequence=["blue", "red", "green"], template="seaborn")

# area chart
fig_area = px.area(temp, x="Date", y="Count", color='Case',
                   title='Cases over time', color_discrete_sequence=["green", "red", "blue"])

# ---------------------------------------------------------------------------------------------

external_stylesheets = ['https://codepen.io/anon/pen/mardKv.css',
                        'https://codepen.io/amyoshino/pen/jzXypZ.css']

app = dash.Dash(__name__, external_stylesheets=external_stylesheets)

print("Here 16")

# App layout (contains all the html components: the graphs, drop down, etc)
app.layout = html.Div(
    html.Div([
        html.H1("COVID19 Web Application Dashboards",
                style={
                    'textAlign': 'left',
                    'color': colors['text'],
                    'backgroundColor': colors['background'],
                },
                className='ten columns',
                ),
    ], className="row"),

    html.Div([
        html.Div([
            dcc.Graph(figure=fig_tree)
            # dcc.Graph(figure=fig_map, className="eight columns"),
        ]),

    ], className="row"),

    html.Div([
        html.Iframe(
            className="six columns",
            style={'border': 'thin lightgrey solid', 'height': '100%'},
            srcDoc='''
                <div class="flourish-embed flourish-bar-chart-race" data-src="visualisation/1571387">
                    <script src="https://public.flourish.studio/resources/embed.js"></script>
                </div>
                ''',
        ),
        dcc.Graph(figure=fig_area, className='six columns')
    ], className="row"),
)

print("Here 17")
# ------------------------------------------------------------------------------
# Connect the Plotly graphs with Dash Components
# @app.callback()


# ---------------------------------------------------------------------------------------------
if __name__ == '__main__':
    app.run_server(debug=True)
