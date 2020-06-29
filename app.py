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
# ---------------------------------------------------------------------------------------------

# ---------------------------------------------------------------------------------------------
# Collecting and cleaning data (importing csv into pandas)
death_df = pd.read_csv(
    "https://raw.githubusercontent.com/CSSEGISandData/COVID-19/master/csse_covid_19_data/csse_covid_19_time_series/time_series_covid19_deaths_global.csv")
confirmed_df = pd.read_csv(
    "https://raw.githubusercontent.com/CSSEGISandData/COVID-19/master/csse_covid_19_data/csse_covid_19_time_series/time_series_covid19_confirmed_global.csv")
recovered_df = pd.read_csv(
    "https://raw.githubusercontent.com/CSSEGISandData/COVID-19/master/csse_covid_19_data/csse_covid_19_time_series/time_series_covid19_recovered_global.csv")
country_df = pd.read_csv(
    "https://raw.githubusercontent.com/CSSEGISandData/COVID-19/web-data/data/cases_country.csv")

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
# print(world_df)

print("Here 6")

# unpivot the dataframe from wide to long format
word_long_df = world_df.melt(
    value_vars=['active', 'deaths', 'recovered'], var_name="status", value_name="count")
word_long_df['upper'] = 'confirmed'
# print(word_long_df)

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

# Sort the mortality rates
# sorted_mortality_rates_df = country_df.sort_values(
#     'Mortality_Rate', ascending=False)
# ---------------------------------------------------------------------------------------------

colors = {
    'dark': True,
    'background': 'black',
    'text': 'white',
}

# ---------------------------------------------------------------------------------------------
# Visualizations
print("Here 14")
# World map
fig_map = px.scatter_geo(covid_confirmed_agg_long,
                         lat="Lat", lon="Long", color="country",
                         hover_name="country", size="date_confirmed_cases",
                         size_max=50, animation_frame="date", width=800, height=400,
                         projection="natural earth",
                         title="COVID-19 worldwide confirmed cases over time")
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
    "status"], title="hello world!", values="count", color_discrete_sequence=["blue", "red", "green"], template="seaborn")

# line chart
fig_line_data = [go.Scatter(
    x=world_rate_df.index,
    y=worldwide_confirmed,
    mode="lines",
    name="add name here"
)]
layout = go.Layout(title='Add title here')
fig_line = go.Figure(data=fig_line_data, layout=layout)

# fig_line.add_trace(go.scatter(world_rate_df.index,
#                              y=worldwide_confirmed, mode='lines', name='lines'))

# ---------------------------------------------------------------------------------------------

external_stylesheets = ['https://codepen.io/anon/pen/mardKv.css',
                        'https://codepen.io/amyoshino/pen/jzXypZ.css']

app = dash.Dash(__name__, external_stylesheets=external_stylesheets)

print("Here 16")

# App layout (contains all the html components: the graphs, drop down, etc)
app.layout = html.Div(id='dark-theme-container', children=[

    html.Div([

        html.Div([
            html.H1("COVID19 Web Application Dashboards",
                    style={
                        'text-align': 'center'
                    }),
        ], className="row"),

        html.Div([
            dcc.Graph(figure=fig_tree, className='four columns'),

            html.Div([
                html.H2("Covid-19",
                        #className='four columns'
                        ),
                html.H5(
                    "What began with a handful of mysterious illnesses in a central China city has traveled the world. First detected on the last day of 2019, the novel coronavirus has killed more than 470,000 people with infections surpassing nine million worldwide"
                ),
            ], className='four columns'),

            html.Img(
                src='https://images.newscientist.com/wp-content/uploads/2020/02/11165812/c0481846-wuhan_novel_coronavirus_illustration-spl.jpg?width=1200',
                className='four columns',
                style={
                    'height': '25%',
                    'width': '25%',
                    # 'float': 'left',
                    # 'position': 'relative',
                    'margin-top': 70
                },
            ),
        ], className="row"),

        html.Div([
            dcc.Graph(figure=fig_map),
            dcc.Graph(figure=fig_line),
        ]),

    ], className="row")
])

print("Here 17")
# ------------------------------------------------------------------------------
# Connect the Plotly graphs with Dash Components
# @app.callback()


# ---------------------------------------------------------------------------------------------
if __name__ == '__main__':
    app.run_server(debug=True)
