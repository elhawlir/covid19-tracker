#!/usr/bin/env python3
from bs4 import BeautifulSoup
import requests
import streamlit as st
import re
import pandas as pd

webpage = requests.get("https://www.worldometers.info/coronavirus/#c-all")
r = webpage.content
bs = BeautifulSoup(r, 'html.parser')

# extract country names
country_search = bs.find_all("tr")
# print(country_search)

# extract the column headers
header = bs.find_all('thead')
# print(header)

for h in header:
    match = r'<th width=".*">(.*?)</th>'
    cleaned = re.findall(match, str(h))
# print(cleaned[:-1])

# extracts all the rows of the table
row_info = []
count = 0
for row in country_search:
    match = r'<td style=".*">(.*?)</td>'
    rows = re.findall(match, str(row))
    row_info.append(rows)
    count += 1
    if count == 229:
        break

# remove first 9 elements of row_info since they are not needed
row_info = row_info[9:]
# print(row_info)

# convert list of lists into df
df = pd.DataFrame(row_info, columns=cleaned[:-1])
print(df.columns)

# remove </a> from the end of each name in names column
def remove_tag(series):
    names_list = series.map(lambda x: re.findall(r'(.*?)</a>',x)).apply(','.join)
    return names_list
# print(df)
# print(df[df['Country,<br/>Other'] == "China"])
df['Country Name'] = remove_tag(df['Country,<br/>Other'])
# print(remove_tag(df['Population']))

#######################################################################################################################
# laying out streamlit app
title = st.title('Covid-19 Tracker by Country')

# creates drop down list in application
drop_down = st.selectbox('Choose the country you want to track', list(df['Country Name']))
if not drop_down:
    print(st.error("Please select a country."))

df['Total Cases'] = df['Total<br/>Cases']
df['New Cases'] = df['New<br/>Cases']
df['Total Deaths'] = df['Total<br/>Deaths']
df['New Deaths'] = df['New<br/>Deaths']
df['Total Recovered'] = df['Total<br/>Recovered']
df['Active Cases'] = df['Active<br/>Cases']
df['Serious/Critical'] = df['Serious,<br/>Critical']


# response to pressing button on application
def display(country_name):
    print(country_name)
    country_df = df[df['Country Name'] == drop_down]
    # important metrics displayed up top
    # death_popn = int(country_df['Total Deaths'])/int(country_df['Population'])
    # death_cases = int(country_df['Total Deaths'])/int(country_df['Total Cases'])

    # summary = f"Rate of death by population = {death_popn}  Rate of death by cases = {death_cases}"
    
    st.write(drop_down) # name of country
    # st.write(summary) # metrics calculated above
    st.write(country_df['Total Cases'])
    st.write(country_df['New Cases'])
    st.write(country_df['Total Deaths'])
    st.write(country_df['New Deaths'])
    st.write(country_df['Total Recovered'])
    st.write(country_df['Active Cases'])
    st.write(country_df['Serious/Critical']) # all of these are self-expanatory :)

# creates button that will display results
if st.button('Display Results'):
    display(drop_down)

country_df = df[df['Country Name'] == 'India'].index
# print(df.loc[country_df]['Total<br/>Deaths'][0])
