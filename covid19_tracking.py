#!/usr/bin/env python3
from bs4 import BeautifulSoup
import requests
from tkinter import *
from tkinter import ttk
import re
from autocomplete_class import AutocompleteCombobox

webpage = requests.get("https://www.worldometers.info/coronavirus/")
bs = BeautifulSoup(webpage.content, 'html.parser')

app = Tk()
app.title("Covid-19 Tracker by Country")

country_search = bs.select("div tbody tr td a.mt_a")

# extracts all the country names from the table
# puts them in a list
country_names = []
for name in country_search:
    match = r'<a class="mt_a".+>([a-zA-z]+)</a>'
    cleaned = re.findall(match, str(name))
    for i in cleaned:
        country_names.append(i)

country_names.insert(0,"Select a country") #instructional option

variable = StringVar() #dropdown list variable

# creates drop down list in application
w = ttk.Combobox(app, textvariable = variable)
w.pack()
w.config(values = country_names)

# autocompletes drop down list as you type, case insensitive
combo = AutocompleteCombobox(app)
combo.set_completion_list(country_names)
combo.pack()
combo.focus_set()

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
    dirty_data = data_collection(variable.get())
    print(dirty_data)
    data = data_cleanup(dirty_data)
    message = "Country: {}\nTotal infected = {}\nNew Case = {}\nTotal Deaths = {}\nNew Deaths = {}\nRecovered = {}\nActive Case = {}\nSerious Critical = {}".format(variable.get(), *data)
    print(message)

# creates button that will display results
button = ttk.Button(app, text = "Display", command = display)
button.pack()

app.mainloop()

