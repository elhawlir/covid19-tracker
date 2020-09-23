#!/usr/bin/env python3
from bs4 import BeautifulSoup
import requests
import streamlit as st
import re

webpage = requests.get("https://www.worldometers.info/coronavirus/")
bs = BeautifulSoup(webpage.content, 'html.parser')

country_search = bs.select("div tbody tr td a.mt_a")

# extracts all the country names from the table
# puts them in a list
country_names = []
for name in country_search:
    match = r'<a class="mt_a".+>([a-zA-z]+)</a>'
    cleaned = re.findall(match, str(name))
    for i in cleaned:
        country_names.append(i)

title = st.title('Covid-19 Tracker by Country')

# creates drop down list in application
drop_down = st.selectbox('Choose the country you want to track', country_names)
if not drop_down:
    print(st.error("Please select a country."))


#cleanses data extracted
def data_cleanup(array):
    L = []
    for i in array:
        i = i.replace("+","")
        i = i.replace("-","")
        # i = i.replace(",",".")
        if i == "":
            i = "0"
        L.append(i.strip())
    return L

#extracts covid-19 country info from https://www.worldometers.info/coronavirus/
def data_collection(country):
    print(country)
    webpage = requests.get("https://www.worldometers.info/coronavirus/")
    bs = BeautifulSoup(webpage.content, 'html.parser')

    search = bs.select("div tbody tr td")

    start = -1
    for i in range(len(search)):
        if search[i].get_text().find(str(country)) != -1:
            start = i
            break

    data = []
    for i in range(1, 8):
        try:
            data += [search[start + i].get_text()]
        except:
            data += [0]
        country_names.append([0])
    return data

# response to pressing button on application
def display():
    dirty_data = data_collection(drop_down)
    print(dirty_data)
    data = data_cleanup(dirty_data)
    message = """
    {}
    
    Total infected = {}\n
    New Cases = {}\n
    Total Deaths = {}\n
    New Deaths = {}\n
    Recovered = {}\n
    Active Cases = {}\n
    Seriously Critical = {}
    """.format(drop_down, *data)
    disp = st.write(message)
    return disp

# creates button that will display results
if st.button('Display Results'):
    display()

