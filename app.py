import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go

# -*- coding: utf-8 -*-
import dash
import dash_core_components as dcc
import dash_html_components as html


# ---------------------------------------------------------------------------------------------
# Import and cleaning data (importing csv into pandas)
death_df = pd.read_csv("https://raw.githubusercontent.com/CSSEGISandData/COVID-19/master/csse_covid_19_data/csse_covid_19_time_series/time_series_covid19_deaths_global.csv")
confirmed_df = pd.read_csv("https://raw.githubusercontent.com/CSSEGISandData/COVID-19/master/csse_covid_19_data/csse_covid_19_time_series/time_series_covid19_confirmed_global.csv")
recorved_df =  pd.read_csv("https://raw.githubusercontent.com/CSSEGISandData/COVID-19/master/csse_covid_19_data/csse_covid_19_time_series/time_series_covid19_recovered_global.csv")
country_df =  pd.read_csv("https://raw.githubusercontent.com/CSSEGISandData/COVID-19/web-data/data/cases_country.csv")

confirmed_df = confirmed_df.rename(columns = {'Country/Region': 'country'})
death_df = death_df.rename(columns = {'Country/Region': 'country'})

sorted_mortality_rates_df = country_df.sort_values('Mortality_Rate', ascending = False)
# ---------------------------------------------------------------------------------------------

# App layout
# app.layout = html.Div([
#
# ])

