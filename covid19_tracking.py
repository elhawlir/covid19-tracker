#!/usr/bin/env python3
from bs4 import BeautifulSoup
import requests
from tkinter import *
from tkinter import ttk
import re

webpage = requests.get("https://www.worldometers.info/coronavirus/")
bs = BeautifulSoup(webpage.content, 'html.parser')

app = Tk()
app.title("Covid-19 Tracker by Country")


class AutocompleteCombobox(ttk.Combobox):

    def set_completion_list(self, completion_list):
        """Use our completion list as our drop down selection menu, arrows move through menu."""
        self._completion_list = sorted(completion_list, key=str.lower)  # Work with a sorted list
        self._hits = []
        self._hit_index = 0
        self.position = 0
        self.bind('<KeyRelease>', self.handle_keyrelease)
        self['values'] = self._completion_list  # Setup our popup menu

    def autocomplete(self, delta=0):
        """autocomplete the Combobox, delta may be 0/1/-1 to cycle through possible hits"""
        if delta:  # need to delete selection otherwise we would fix the current position
            self.delete(self.position, END)
        else:  # set position to end so selection starts where textentry ended
            self.position = len(self.get())
        # collect hits
        _hits = []
        for element in self._completion_list:
            if element.lower().startswith(self.get().lower()):  # Match case insensitively
                _hits.append(element)
        # if we have a new hit list, keep this in mind
        if _hits != self._hits:
            self._hit_index = 0
            self._hits = _hits
        # only allow cycling if we are in a known hit list
        if _hits == self._hits and self._hits:
            self._hit_index = (self._hit_index + delta) % len(self._hits)
        # now finally perform the auto completion
        if self._hits:
            self.delete(0, END)
            self.insert(0, self._hits[self._hit_index])
            self.select_range(self.position, END)

    def handle_keyrelease(self, event):
        """event handler for the keyrelease event on this widget"""
        if event.keysym == "BackSpace":
            self.delete(self.index(INSERT), END)
            self.position = self.index(END)
        if event.keysym == "Left":
            if self.position < self.index(END):  # delete the selection
                self.delete(self.position, END)
            else:
                self.position = self.position - 1  # delete one character
                self.delete(self.position, END)
        if event.keysym == "Right":
            self.position = self.index(END)  # go to end (no selection)
        if len(event.keysym) == 1:
            self.autocomplete()
        # No need for up/down, we'll jump to the popup
        # list at the position of the autocompletion


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

