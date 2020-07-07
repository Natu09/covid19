#!/usr/bin/env python
__author__ = "Nathaniel Habtegergesa"

"""
Dataset:
    https://systems.jhu.edu/ 
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
import dash_bootstrap_components as dbc
from dash.dependencies import Input, Output, State
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
    'active_text': '#ffa500',
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
recovered_df = recovered_df.rename(columns={'Country/Region': 'country'})

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
total_active = total_confirmed - (total_deaths + total_recovered)
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
world_rate_df['mortality rate'] = world_rate_df['deaths'] / \
    world_rate_df['confirmed'] * 100
world_rate_df['date'] = world_rate_df.index
# print(world_rate_df)
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
#                          title="COVID-19 Worldwide Confirmed Cases Over Time")
# fig_map.update_layout(
#     margin={'t': 30, 'l': 0, 'r': 0, 'b': 0},
#     plot_bgcolor=colors['background'],
#     paper_bgcolor=colors['background'],
#     font_color=colors['text']
# )

print("Here 15")
# print(full_latest)
# Tree map
full_latest["world"] = "world"
fig_tree = px.treemap(full_latest, path=[
    "world", "Country/Region", "Province/State"], title="Total Number of Confirmed Cases", values="Confirmed", color_discrete_sequence=px.colors.qualitative.Prism, template="seaborn")
fig_tree.data[0].textinfo = 'label+text+value'
fig_tree.update_layout(
    margin={'t': 50, 'l': 0, 'r': 0, 'b': 0},
    plot_bgcolor=colors['background'], paper_bgcolor=colors['background'], font_color=colors['text'])

print(temp)
# Area chart
fig_area = px.area(temp, x="Date", y="Count", color='Case',
                   title='Evolution of Cases Status', color_discrete_sequence=["green", "red", "blue"])
fig_area.update_layout(
    margin={'l': 0, 'r': 0, 'b': 0},
    plot_bgcolor=colors['background'], paper_bgcolor=colors['background'], font_color=colors['text'])

# Bar Chart
# fig_bar = px.bar(temp, x="Date", y="Count", color='Case',
#                  title='Cases over time', color_discrete_sequence=["green", "red", "blue"])
# fig_bar.update_layout(
#     plot_bgcolor=colors['background'], paper_bgcolor=colors['background'], font_color=colors['text'])

# print(covid_confirmed_agg_long)
fig_line = px.line(covid_confirmed_agg_long, x="date", y="date_confirmed_cases", title="Evolution of Cases Over Time", color="country",
                   line_group="country", hover_name="country")
fig_line.update_layout(
    margin={'l': 0, 'r': 0, 'b': 0},
    plot_bgcolor=colors['background'], paper_bgcolor=colors['background'], font_color=colors['text'])


# ---------------------------------------------------------------------------------------------

external_stylesheets = ['https://codepen.io/anon/pen/mardKv.css',
                        'https://codepen.io/amyoshino/pen/jzXypZ.css']

app = dash.Dash(__name__, external_stylesheets=external_stylesheets)


print("Here 16")

# App layout (contains all the html components: the graphs, drop down, etc)
app.layout = html.Div(children=[
    html.Div([
        html.H1("COVID19 Web Application",
                style={
                    'textAlign': 'left',
                    'color': colors['text'],
                    'backgroundColor': colors['background'],
                },
                className='ten columns',
                ),
        html.Div([
            dbc.Button("MORE INFO", id="open", className="fa fa-info-circle",
                       style={
                           'color': colors['text'],
                           'backgroundColor': colors['background'],
                       }),
            dbc.Modal(
                [
                    html.Div([
                        dbc.ModalHeader(
                            "Dataset provided by Johns Hopkins University Center for Systems Science and Engineering (JHU CSSE):"),
                        html.A("https://systems.jhu.edu/"),
                    ], style={'textAlign': 'center'}),
                    html.Hr(),
                    dbc.ModalBody(
                        "SARS-CoV-2, better known as COVID-19 (coronavirus disease 2019) is a viral \
                            infectious disease and is currently a World Health Organization (WHO) declared pandemic. \
                                Having now killed over half a million people, this novel coronavirus that was first detected in Wuhan China, has now spread to over \
                                    200 locations internationally. "
                    ),
                    html.Br(),
                    dbc.ModalBody(
                        "This web application intends to serve as an informative guide around the novel \
                            coronavirus. This"
                    ),
                    html.Hr(),
                    dbc.ModalFooter(
                        dbc.Button("Close", id="close", className="ml-auto", style={
                            'color': colors['text'],
                            'backgroundColor': colors['background'],
                        })
                    ),
                ],
                id="modal", className="six columns offset-by-three",
            ),
        ], style={
            'color': colors['text'],
            'backgroundColor': colors['background'],
        }),
    ], className="row"),

    # # Top column display of confirmed, death and recovered total numbers
    html.Div([
        html.Div([
            html.H4(children='Total Confirmed: ',
                    style={
                        'textAlign': 'center',
                        'color': colors['confirmed_text'],
                    }
                    ),
            html.P(f"{total_confirmed:,d}",
                   style={
                       'textAlign': 'center',
                       'color': colors['confirmed_text'],
                       'fontSize': 30,
                   }
                   ),
            html.P('Past 24hrs increase: +' + f"{total_confirmed - worldwide_confirmed[-2]:,d}" + ' (' + str(round(((total_confirmed - worldwide_confirmed[-2])/total_confirmed)*100, 2)) + '%)',
                   style={
                       'textAlign': 'center',
                       'color': colors['confirmed_text'],
            }
            ),
        ],
            style=divBorderStyle,
            className='three columns',
        ),
        html.Div([
            html.H4(children='Total Deceased: ',
                    style={
                        'textAlign': 'center',
                        'color': colors['deaths_text'],
                    }
                    ),
            html.P(f"{total_deaths:,d}",
                   style={
                       'textAlign': 'center',
                       'color': colors['deaths_text'],
                       'fontSize': 30,
                   }
                   ),
            html.P('Mortality Rate: ' + str(round(total_deaths/total_confirmed * 100, 3)) + '%',
                   style={
                       'textAlign': 'center',
                       'color': colors['deaths_text'],
            }
            ),
        ],
            style=divBorderStyle,
            className='three columns'),
        html.Div([
            html.H4(children='Total Active: ',
                    style={
                        'textAlign': 'center',
                        'color': colors['active_text'],
                    }
                    ),
            html.P(f"{total_active:,d}",
                   style={
                       'textAlign': 'center',
                       'color': colors['active_text'],
                       'fontSize': 30,
                   }
                   ),
            html.P('Past 24hrs increase: +' + f"{total_active - worldwide_active[-2]:,d}" + ' (' + str(round(((total_active - worldwide_active[-2])/total_active)*100, 2)) + '%)',
                   style={
                'textAlign': 'center',
                       'color': colors['active_text'],
            }
            ),
        ],
            style=divBorderStyle,
            className='three columns',
        ),
        html.Div([
            html.H4(children='Total Recovered: ',
                    style={
                        'textAlign': 'center',
                        'color': colors['recovered_text'],
                    }
                    ),
            html.P(f"{total_recovered:,d}",
                   style={
                       'textAlign': 'center',
                       'color': colors['recovered_text'],
                       'fontSize': 30,
                   }
                   ),
            html.P('Recovery Rate: ' + str(round(worldwide_recovered[-1]/worldwide_confirmed[-1] * 100, 3)) + '%',
                   style={
                'textAlign': 'center',
                'color': colors['recovered_text'],
            }
            ),
        ],
            style=divBorderStyle,
            className='three columns'),
    ], className='row'),


    html.Div([
        html.Div([
            # dcc.Graph(figure=fig_map, style={
            #     'display': 'flex',
            #     'flex-direction': 'column',
            #     'box-sizing': 'border-box',
            #     # 'margin-left': 'auto',
            #     # 'margin-right': 'auto',
            #     'height': '70vh',
            #     'padding': '0.75rem',
            #     'textAlign': 'center',
            #     'color': colors['text'],
            #     'backgroundColor': colors['background'],
            #     'border-color': colors['background'],
            # },
            #     className="twelve columns"),
        ], style={
            'textAlign': 'center',
            'color': colors['text'],
            'backgroundColor': colors['background'],
        }),

    ], className="row"),


    html.Div([
        html.Div([
            dcc.Tabs([
                dcc.Tab(label='Cases by Status', children=[
                    html.Div([
                        html.Div([
                            html.Label(['X-axis categories to compare:'],
                                       style={'font-weight': 'bold'}),
                            dcc.RadioItems(
                                id='xaxis_raditem',
                                options=[
                                    {'label': 'Cumulative',
                                     'value': 'Cumulative'},
                                    {'label': 'Instantaneous',
                                     'value': 'Instantaneous'},
                                ],
                                value='Cumulative',
                                style={"width": "50%"}
                            ),
                        ], className="six columns"),

                        html.Div([
                            html.Div([
                                html.Label(['Y-axis values to compare:'],
                                           style={'font-weight': 'bold'}),
                                dcc.RadioItems(
                                    id='yaxis_raditem',
                                    options=[
                                        {'label': 'Linear',
                                         'value': 'Linear'},
                                        {'label': 'Semi-log',
                                         'value': 'Semi-log'},
                                    ],
                                    value='Linear',
                                    style={"width": "50%"}
                                ),
                            ], style={'float': 'right'}),
                        ], className="six columns"),
                    ], className="row"),

                    dcc.Graph(figure=fig_area),
                ], style={
                    'color': colors['text'],
                    'backgroundColor': colors['background'], }),
                dcc.Tab(label='Cases by Time', children=[
                    dcc.Graph(figure=fig_line),
                ], style={
                    'color': colors['text'],
                    'backgroundColor':colors['background'], }),
                dcc.Tab(label='Cases by Country', children=[
                    dcc.Graph(figure=fig_tree),
                ], style={
                    'color': colors['text'],
                    'backgroundColor': colors['background'], }, ),
            ], style={'padding-top': '2rem'},)
        ], className="six columns"),

        html.Iframe(
            style={
                'display': 'flex',
                'flex-direction': 'column',
                'box-sizing': 'border-box',
                'margin-left': 'auto',
                'margin-right': 'auto',
                'margin-top': 'auto',
                'margin-bottom': 'auto',
                'height': '60vh',
                'padding-top': '10rem',
                'padding': '0.75rem',
                'color': colors['text'],
                'backgroundColor': colors['background'],
                'border-style': 'none',

            },
            className="six columns",
            srcDoc='''
                <div class="flourish-embed flourish-bar-chart-race" data-src="visualisation/1571387">
                    <script src="https://public.flourish.studio/resources/embed.js"></script>
                </div>
                '''
        ),
    ], className="row"),

], style={
    'textAlign': 'left',
    'color': colors['text'],
    'backgroundColor': colors['background'],
    'margin-top': '0',
    'width': '100%'
},)

print("Here 17")
# ------------------------------------------------------------------------------
# Connect the Plotly graphs with Dash Components
# @app.callback()


@app.callback(
    Output("modal", "is_open"),
    [Input("open", "n_clicks"), Input("close", "n_clicks")],
    [State("modal", "is_open")],
)
def toggle_modal(n1, n2, is_open):
    if n1 or n2:
        return not is_open
    return is_open

# @app.callback(
#     Output(component_id='the_graph', component_property='figure'),
#     [Input(component_id='xaxis_raditem', component_property='value'),
#      Input(component_id='yaxis_raditem', component_property='value')]
# )

# def update_graph(x_axis, y_axis):

#     dff = mydataset for the graph im using
#     # print(dff[[x_axis,y_axis]][:1])

#     barchart=px.bar(
#             data_frame=dff,
#             x=x_axis,
#             y=y_axis,
#             title=y_axis+': by '+x_axis,
#             # facet_col='Borough',
#             # color='Borough',
#             # barmode='group',
#             )

#     barchart.update_layout(xaxis={'categoryorder':'total ascending'},
#                            title={'xanchor':'center', 'yanchor': 'top', 'y':0.9,'x':0.5,})

#     return (barchart)


# ---------------------------------------------------------------------------------------------
if __name__ == '__main__':
    app.run_server(debug=True)
