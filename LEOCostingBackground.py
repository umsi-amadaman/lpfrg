from datetime import datetime
import math
import ipywidgets as widgets
from IPython.display import display
import pandas as pd

class Lec2:
    def __init__(self, df_row):
        self.name = f"{df_row['Employee First Name']} {df_row['Employee Last Name']}"
        self.id = df_row['UM ID']
        self.appointment = df_row['Appointment Period']
        self.start_date = df_row['Hire Begin Date']
        self.campus = self.get_campus(df_row['School/College/Division'])
        self.title = df_row['Job Title']
        self.effort = df_row['FTE']
        self.dept = df_row['Department Name']
        if df_row['Deduction'] == 'LEODUE':
           self.memberstatus = 'Union Dues'
        else:
           self.memberstatus = 'Non-Payer'
        self.calculate_service_year()
        
        self.calculate_rates(df_row)
        
        self.MRcount24 = 0
        self.MRcount25 = 0
        self.MRcount26 = 0
        self.MRraiseIn24 = None
        self.MRraiseIn25 = None
        self.MRraiseIn26 = None
        self.salary24 = None
        self.salary25 = None
        self.salary26 = None
        self.cost24 = None
        self.cost25 = None
        self.cost26 = None
        self.Rate24 = None
        self.Rate25 = None
        self.Rate26 = None

        self.count_MRs()
    
    def calculate_rates(self, df_row):
        comp_rate = float(df_row['Comp Rate'].replace('$', '').replace(',',''))
        fte = self.effort
        comp_frequency = df_row['Comp Frequency']
        
        if self.appointment == "7":  # 12 month
            self.Rate23 = comp_rate * (1 / fte)
            self.cost23 = comp_rate
            self.salary23 = comp_rate
        elif self.appointment == "9":  # 8 month paid over 8
            self.Rate23 = comp_rate * 8.348 * (1 / fte)
            self.cost23 = comp_rate * 8.348
            self.salary23 = comp_rate * 8.348
        elif self.appointment == "6":  # worked a 7 week course paid twice
            self.Rate23 = comp_rate * 8 * (1 / fte)
            self.cost23 = comp_rate * 2
            self.salary23 = comp_rate * 2
        elif self.appointment == "5":  # 8 month Dbn paid over 12
            if comp_frequency == "Annual":
                self.Rate23 = comp_rate * (1 / fte)
                self.cost23 = comp_rate
                self.salary23 = comp_rate
            elif comp_frequency == "Monthly":
                self.Rate23 = comp_rate * 12 * (1 / fte)
                self.cost23 = comp_rate * 12
                self.salary23 = comp_rate * 12
        elif self.appointment == "4":  # 9 month AA paid over 12
            if comp_frequency == "Annual":
                self.Rate23 = comp_rate * (1 / fte)
                self.cost23 = comp_rate
                self.salary23 = comp_rate
            elif comp_frequency == "Monthly":
                self.Rate23 = comp_rate * 12 * (1 / fte)
                self.cost23 = comp_rate * 12
                self.salary23 = comp_rate * 12
        elif self.appointment == "3":  # Term worker paid monthly. Costed out as both terms
            self.Rate23 = comp_rate * 8.348 * (1 / fte)
            self.cost23 = comp_rate * 8.348
            self.salary23 = comp_rate * 4.174
        
    def get_campus(self, division):
        if division.startswith('FLINT'):
            return "Flint"
        elif division.startswith('DBN'):
            return "Dearborn"
        else:
            return "Ann Arbor"
    
    def calculate_service_year(self):
        ContractStart = datetime(2024, 9, 21)
        date_format = "%m/%d/%Y" 
        hire_begin_date = datetime.strptime(self.start_date, date_format)
        self.ServiceYear = math.floor((ContractStart - hire_begin_date).days / 365)#math.floor(((ContractStart - hire_begin_date).days / 365)*2)/2
    
    def info(self):
        return f"Employee Information:\nName: {self.name}\nID: {self.id}\nAppointment: {self.appointment}\nStart Date: {self.start_date}\nTitle: {self.title}\nEffort: {self.effort}\nFull Time Rate: {self.Rate}\nCosted in Budget as: {self.cost}\nSalary: {self.salary}\nCampus: {self.campus}"
    
    def count_MRs(self):
        if self.title in ["LEO Lecturer I", "LEO Lecturer II", "LEO Lecturer III", "LEO Lecturer IV"]:
            for x in [24,25,26]:
                MRcount = "MRcount"+str(x)
                MRraise = "MRraiseIn"+str(x)
                z = x -23
                if (self.ServiceYear + z) > 8:
                    setattr(self, MRcount, 2)
                    setattr(self, MRraise, "NO")
                elif (self.ServiceYear + z) == 8:
                    setattr(self, MRcount, 2)
                    setattr(self, MRraise, "YES")
                elif (self.ServiceYear + z) >= 6:
                    setattr(self, MRcount, 1)
                    setattr(self, MRraise, "NO")
                elif (self.ServiceYear + z) == 5:
                    setattr(self, MRcount, 1)
                    setattr(self, MRraise, "YES")
                else:
                    setattr(self, MRcount, 0)
                    setattr(self, MRraise, "NO")
        return self

import ipywidgets as widgets
from IPython.display import display
def AnnualRaises(campus):

    # Define the number of rows and columns for your grid
    rows = 3
    columns = 3

    # Create a list to store the Text widgets
    text_entries = []
    years = [2024, 2025, 2026]

    for year in years:
        year_str = str(year)
        prompts = [
            f"% Annual Raise in {year_str} (for example 6.3)",
            f"Flat Raise in {year_str} (for example $8000)",
            f"Threshold to switch from % to Flats in {year_str} (if only want flats enter 0)"
        ]
        text_entries.extend([widgets.Text(placeholder=prompt) for prompt in prompts])

    # Create a VBox to organize the Text widgets
    grid = widgets.VBox([widgets.HBox(text_entries[i:i+columns]) for i in range(0, len(text_entries), columns)])

    # Function to get the entered values when the "Submit" button is clicked
    entered_values = []

    def on_submit_button_click(b):
        values = [entry.value for entry in text_entries]
        entered_values.append(values)

    # Create a "Submit" button
    submit_button = widgets.Button(description="Submit")
    submit_button.on_click(on_submit_button_click)

    print(f"Enter the Annual Raise Proposal for {campus} for the following years: {', '.join(map(str, years))}")
    print(" ")
    print("You have to enter numbers for both flats & percentages.")
    print("If you only want flats, just enter 0 for % and 0 for threshold")
    print("If you only want %, just enter 0 for flats & 999999 for threshold")
    print(" ")
    print("Currently we can only give individual lecs one or the other.")
    print("You have to choose a threshold in the 3rd column to go from % to Flat")
    print("This basically acts like a Cap on Annuals for those over that number.")
    print(" ")
    print("A good threshold is 100K, make sure the flat they get = %s * 100000 so they don't get a penalty")

    # Display the grid and the "Submit" button
    display(grid, submit_button)

    # Return the entered values
    return entered_values

# Example usage:
#column_name = "Ann Arbor"
#entered_data = AnnualRaises(column_name, 2024)
def MajorReviewRaises():

    prompts = ["Major Review Raise (%)",]
    # Define the number of rows for your grid
    rows = 1

    # Create a list to store the widgets
    widgets_list = []

    for i, prompt in enumerate(prompts):
        label = widgets.Label(value=prompt)
        text_entry = widgets.Text(placeholder=prompt)
        widgets_list.extend([label, text_entry])

    # Create a VBox to organize the prompt-text bar pairs
    prompt_text_pairs = [widgets.VBox(widgets_list[i:i+2]) for i in range(0, len(widgets_list), 2)]

    # Create a VBox to organize the prompt-text bar pairs
    grid = widgets.VBox(prompt_text_pairs)

    # Function to get the entered values when the "Submit" button is clicked
    entered_values = []

    def on_submit_button_click(b):
        values = [text_entry.value]
        entered_values.append(values)

    # Create a "Submit" button
    submit_button = widgets.Button(description="Submit")
    submit_button.on_click(on_submit_button_click)

    print("What will the major review raise be for those hired after Sept 1, 2024")
    print("Those hired after 9/1/2001 currently get 5% with MR1 & MR2")

    # Display the grid and the "Submit" button
    display(grid, submit_button)

    # Return the entered values
    return entered_values

def MajorReviewRaisesbyCampuses():

    prompts = ["Major Review Raise for Dearborn (%)",
               "Major Review Raise for Flint (%)",
               "Major Review Raise for Ann Arbor (%)"]
    # Define the number of rows for your grid
    rows = 3

    # Create a list to store the Text widgets
    text_entries = [widgets.Text(placeholder=prompt) for prompt in prompts]

    # Create a VBox to organize the Text widgets
    grid = widgets.VBox(text_entries)

    # Function to get the entered values when the "Submit" button is clicked
    entered_values = []

    def on_submit_button_click(b):
        values = [entry.value for entry in text_entries]
        entered_values.append(values)

    # Create a "Submit" button
    submit_button = widgets.Button(description="Submit")
    submit_button.on_click(on_submit_button_click)

    print("Enter the Major Review Raise Proposal for each campus")

    # Display the grid and the "Submit" button
    display(grid, submit_button)

    # Return the entered values
    return entered_values

def AnnualRaiseSliders(campus):

    # Define the number of rows and columns for your grid
    rows = 3
    columns = 3
    years = [2024, 2025, 2026]

    # Create a list to store the widgets
    widgets_list = []

    for year in years:
        year_str = str(year)
        prompts = [
            f"{year_str} % Annual Raise (ex: 6.3)",
            f"{year_str} Flat Raise in (ex: $3500)",
            f"{year_str} Threshold to switch % to Flats (ex: $100000)"
        ]

        # Create an HBox to hold the widgets for this year
        year_widgets = []
        for i, prompt in enumerate(prompts):
            label = widgets.Label(value=prompt)
            if i == 1:  # Second column
                slider = widgets.FloatSlider(value=0, min=0, max=10000, step=100, description="")
            elif i == 2:
                slider = widgets.FloatSlider(value=0, min=0, max=500000, step=1000, description="")
            else:
                slider = widgets.FloatSlider(value=0, min=0, max=100, step=0.1, description="")
            year_widgets.extend([label, slider])
        widgets_list.extend([widgets.VBox(year_widgets)])

    # Create a VBox to organize the rows
    grid = widgets.VBox([widgets.HBox(widgets_list[i:i+columns]) for i in range(0, len(widgets_list), columns)])

    def on_submit_button_click(b):
        values = [slider.value for widget in widgets_list for slider in widget.children if isinstance(slider, widgets.FloatSlider)]


    # Function to get the entered values when the "Submit" button is clicked
    entered_values = {}

    #def on_submit_button_click(b):
    #    values = [slider.value for slider in [widget.children[1] for widget in widgets_list]]
    #    entered_values.append(values)
    promptLabels = []
    for year in years:
        year_str = str(year)
        prompts2 = [
            f"{year_str} % Annual Raise (ex: 6.3)",
            f"{year_str} Flat Raise in (ex: $3500)",
            f"{year_str} Threshold to switch % to Flats (ex: $100000)"
        ]
        promptLabels += prompts2

  


    def on_submit_button_click(b):
        values = [slider.value for widget in widgets_list for slider in widget.children if isinstance(slider, widgets.FloatSlider)]

        for x in range(len(promptLabels)):
            entered_values[promptLabels[x]] = values[x]

    # Create a "Submit" button
    submit_button = widgets.Button(description="Submit")
    submit_button.on_click(on_submit_button_click)


    print(f"Enter the Annual Raise Proposal for {campus} for the following years: {', '.join(map(str, years))}")
    print(" ")

    print("You have to adjust the sliders for both flats & percentages.")
    print("If you only want flats, set the % slider to 0.")
    print("If you only want %, set the flat slider to 0 and the threshold slider to 500000.")
    print(" ")
    print("Currently we can only give individual lecs one or the other.")
    print("You have to choose a threshold in the threshold slider to go from % to Flats.")
    print("This threshold acts as a cap on Annuals for those over that number.")
    print(" ")
    print("A good threshold is 100K, make sure the flat they get = %s * 100000 so they don't get a penalty")

    # Display the grid and the "Submit" button
    display(grid, submit_button)

    # Return the entered values
    return entered_values


def LongevityRaises():

    prompts = ["How much should the longevity raise be",  
               "After what year is the first longevity raise", 
               "After how many years are the subsequent raises?"]
    # Define the number of rows for your grid
    rows = 3

    # Create a list to store the widgets
    widgets_list = []

    for i, prompt in enumerate(prompts):
        label = widgets.Label(value=prompt)
        text_entry = widgets.Text(placeholder=prompt)
        widgets_list.extend([label, text_entry])

    # Create a VBox to organize the prompt-text bar pairs
    prompt_text_pairs = [widgets.VBox(widgets_list[i:i+2]) for i in range(0, len(widgets_list), 2)]

    # Create a VBox to organize the prompt-text bar pairs
    grid = widgets.VBox(prompt_text_pairs)

    # Function to get the entered values when the "Submit" button is clicked
    entered_values = []

    def on_submit_button_click(b):
        values = [text_entry.value for text_entry in [pair.children[1] for pair in prompt_text_pairs]]
        entered_values.append(values)

    # Create a "Submit" button
    submit_button = widgets.Button(description="Submit")
    submit_button.on_click(on_submit_button_click)

    print("Enter the Rules for Our Longevity proposal")

    # Display the grid and the "Submit" button
    display(grid, submit_button)

    # Return the entered values
    return entered_values


def MinimumSalaries():

    prompts = ["Min for Lec I/II",
               "Min for Lec II with 1 MR",
               "Min for Lec II with 2 MR",
               "Min for Lec III/IV",
               "Min for Lec IV with 1 MR",
               "Min for Lec IV with 2 MR",
               "How much to raise Mins from 24 -> 25",
               "How much to raise Mins from 25 -> 26"]
    # Define the number of rows for your grid
    rows = len(prompts)

    # Create a list to store the widgets
    widgets_list = []

    for i, prompt in enumerate(prompts):
        label = widgets.Label(value=prompt)
        text_entry = widgets.Text(placeholder=prompt)
        widgets_list.extend([label, text_entry])

    # Create a VBox to organize the prompt-text bar pairs
    prompt_text_pairs = [widgets.VBox(widgets_list[i:i+2]) for i in range(0, len(widgets_list), 2)]

    # Create a VBox to organize the prompt-text bar pairs
    grid = widgets.VBox(prompt_text_pairs)

    # Function to get the entered values when the "Submit" button is clicked
    entered_values = {}

    def on_submit_button_click(b):
        values = [text_entry.value for text_entry in [pair.children[1] for pair in prompt_text_pairs]]
        print(values, "are the values")
        for x in range(len(prompts)):
            entered_values[prompts[x]] = values[x]


    # Create a "Submit" button
    submit_button = widgets.Button(description="Submit")
    submit_button.on_click(on_submit_button_click)

    print("Follow the prompts to enter the minimum salary proposal")

    # Display the grid and the "Submit" button
    display(grid, submit_button)

    # Return the entered values
    return entered_values


file_path = 'LEOMonthlyOctober.xlsx'
df = pd.read_excel(file_path)
df = df[df['Appointment Period'] != 'H'] # Removing the Rest of the H
df = df[df['Appointment Period'] != ' '] # Removing Catherine Owsik because she doesn't have an Appointment Period

TotLecs = [Lec2(row) for index, row in df.iterrows()]


def BuildAProposal():
  AR = AnnualRaiseSliders("All Campuses")
  print("  ")
  print("=="*60)
  print("  ")

  LR = LongevityRaises()
  print("  ")
  print("=="*60)
  print("  ")

  Mins = MinimumSalaries()
  print("  ")
  print("=="*60)
  print("  ")

  MR = MajorReviewRaises()

  ProposalDict = {
  "Annuals": AR,
  "Longevity": LR,
  "Minimums": Mins,
  "Promotions": MR
  }
  
  return ProposalDict

###########################
name_count = {}

name_count = {}
unique_TotLecs = []

for obj in TotLecs:
    if obj.name in name_count:
        name_count[obj.name] += 1
    else:
        name_count[obj.name] = 1
        unique_TotLecs.append(obj)

# Use a list comprehension to isolate objects with names that appear multiple times
duplicates = [obj for obj in TotLecs if name_count[obj.name] > 1]

dupNames = [obj.name for obj in duplicates]
'''
print(len(set(dupNames)))
print(len(dupNames))
print(" ")
'''
UnproblematicDups = []
UnproblematicDupNames = []
FixedDups = []
FixedDupNames = []
easyCount = 0
for dupName in set(dupNames):
  if dupName not in UnproblematicDupNames:
    dupTests = [L for L in duplicates if L.name==dupName]
    #print(dupName, sum([L.effort for L in dupTests]))
    if sum([L.effort for L in dupTests])<=1:
      easyCount +=1
      '''
      dupTests[0].Rate23 += dupTests[1].Rate23
      dupTests[0].cost23 += dupTests[1].cost23
      dupTests[0].salary23 += dupTests[1].salary23
      dupTests[0].effort += dupTests[1].effort
      '''
      UnproblematicDups += dupTests
      UnproblematicDupNames.append(dupTests[0].name)
print(" ")
ComplicatedDupes = [L for L in duplicates if L.name not in UnproblematicDupNames]
OverloadLecs = []
OverloadLecNames = []
dupNames = [obj.name for obj in ComplicatedDupes]
for dupName in set(dupNames):
  if dupName not in UnproblematicDupNames:
    dupTests = [L for L in ComplicatedDupes if L.name==dupName]
    #print(dupName, [L.title for L in dupTests], [L.effort for L in dupTests])
    for dup in dupTests:
      if dup.effort ==1:
        OverloadLecs.append(dup)
        OverloadLecNames.append(dup.name)

    
WeirdDupes = [L for L in duplicates if L.name not in UnproblematicDupNames and L.name not in OverloadLecNames]

#print(len(UnproblematicDups))
#print(len(UnproblematicDupNames))
#print(len(OverloadLecNames))
#print(WeirdDupes)
print("Fuck it, we'll leave shannon brines in")

AllLecs = unique_TotLecs + UnproblematicDups + OverloadLecs + WeirdDupes
currentProposal = {'Annuals': [{'2024 % Annual Raise (ex: 6.3)': 0.0,
   '2024 Flat Raise in (ex: $3500)': 8000.0,
   '2024 Threshold to switch % to Flats (ex: $100000)': 0.0,
   '2025 % Annual Raise (ex: 6.3)': 0.0,
   '2025 Flat Raise in (ex: $3500)': 7000.0,
   '2025 Threshold to switch % to Flats (ex: $100000)': 0.0,
   '2026 % Annual Raise (ex: 6.3)': 0.0,
   '2026 Flat Raise in (ex: $3500)': 6000.0,
   '2026 Threshold to switch % to Flats (ex: $100000)': 0.0}],
 'Longevity': [['2000', '11', '5']],
 'Minimums': [{'Min for Lec I/II': '60000',
  'Min for Lec II with 1 MR': '66000',
  'Min for Lec II with 2 MR': '72000',
  'Min for Lec III/IV': '62000',
  'Min for Lec IV with 1 MR': '70000',
  'Min for Lec IV with 2 MR': '76000',
  'How much to raise Mins from 24 -> 25': '1000',
  'How much to raise Mins from 25 -> 26': '1000'}],
 'Promotions': [['5']]}
currentProposal['Longevity'][-1]

def apply_mins(proposal, LecList, year):
    NewMinsApplied = [z for z in LecList]
    min_rates = {
        "LEO Lecturer IV": {
            0: 'Min for Lec III/IV',
            1: 'Min for Lec IV with 1 MR',
            2: 'Min for Lec IV with 2 MR'
        },
        "LEO Lecturer III": {
            0: 'Min for Lec III/IV'
        },
        "LEO Lecturer II": {
            0: 'Min for Lec I/II',
            1: 'Min for Lec II with 1 MR',
            2: 'Min for Lec II with 2 MR'
        }
    }

    def calc_minRate(MRcount, rate, proposal, min_rates, title, year):
        min_rate_key = min_rates.get(title, {}).get(MRcount, 'Min for Lec I/II')
        if year == 2024:
          return max(float(rate), float(proposal['Minimums'][min_rate_key]))
        if year == 2025:
          return max(float(rate), float(proposal['Minimums'][min_rate_key]) + float(proposal['Minimums']['How much to raise Mins from 24 -> 25']))
        if year == 2026:
          return max(float(rate), float(proposal['Minimums'][min_rate_key])+ float(proposal['Minimums']['How much to raise Mins from 25 -> 26']))

    for x in NewMinsApplied:
      title = x.title
      fte = float(x.effort)
      if year == 2024:
        x.Rate24 = calc_minRate(x.MRcount24, x.Rate24, proposal, min_rates, title, year)
        x.cost24 = x.Rate24*fte
      if year == 2025:
        x.Rate25 = calc_minRate(x.MRcount25, x.Rate25, proposal, min_rates, title, year)
        x.cost25 = x.Rate25*fte
      if year == 2026:
        x.Rate26 = calc_minRate(x.MRcount26, x.Rate26, proposal, min_rates, title, year)
        x.cost26 = x.Rate26*fte

    '''

    for x in NewMinsApplied:
      title = x.title
      MRcount24 = x.MRcount24
      rate = float(x.Rate24)
      min_rate_key = min_rates.get(title, {}).get(MRcount24, 'Min for Lec I/II')
      x.Rate24 = max(rate, float(proposal['Minimums'][min_rate_key]))

      MRcount25 = x.MRcount25
      rate = float(x.Rate25)
      min_rate_key = min_rates.get(title, {}).get(MRcount24, 'Min for Lec I/II')
      Min25 =  float(proposal['Minimums'][min_rate_key]) + float(proposal['Minimums']['How much to raise Mins from 24 -> 25'])
      x.Rate25 = max(rate, Min25)

      MRcount26 = x.MRcount26
      rate = float(x.Rate26)
      min_rate_key = min_rates.get(title, {}).get(MRcount24, 'Min for Lec I/II')
      Min25 =  float(proposal['Minimums'][min_rate_key]) + float(proposal['Minimums']['How much to raise Mins from 24 -> 25'])
      x.Rate24 = max(rate, Min25)
      '''
    return NewMinsApplied

def apply_Annuals(proposal, LecList, year):
  AnnualApplied = [z for z in LecList]
  promptTail = [' % Annual Raise (ex: 6.3)',' Flat Raise in (ex: $3500)', ' Threshold to switch % to Flats (ex: $100000)']
  for x in AnnualApplied:
    fte = float(x.effort)
    AnnualKey  = [str(year)+p for p in promptTail]
    y = str(year)[-2:]

    if x.__dict__.get(f"Rate{y}", None) is not None:
        rate_key = f'Rate{y}'
        cost_key = f'cost{y}'
        ##if salary greater than threshold then use Flats otherwise use percentages!
        if x.__dict__[rate_key] > proposal['Annuals'][AnnualKey[2]]:
            x.__dict__[rate_key] += proposal['Annuals'][AnnualKey[1]]
            x.__dict__[cost_key] = fte*x.__dict__[rate_key]
        else:
            x.__dict__[rate_key] *= (1 + .01*proposal['Annuals'][AnnualKey[0]])
            x.__dict__[cost_key] = fte*x.__dict__[rate_key]

    '''
    if year == 2024:
      if x.Rate24 > proposal['Annuals'][AnnualKey[2]]:
        x.Rate24 = x.Rate24 + proposal['Annuals'][AnnualKey[1]]
      else:
        x.Rate24 = x.Rate24 + proposal['Annuals'][AnnualKey[0]]
    if year == 2025:
      if x.Rate25 > proposal['Annuals'][AnnualKey[2]]:
        x.Rate25 = x.Rate25 + proposal['Annuals'][AnnualKey[1]]
      else:
        x.Rate25 = x.Rate25 + proposal['Annuals'][AnnualKey[0]]
    if year == 2026:
      if x.Rate26 > proposal['Annuals'][AnnualKey[2]]:
        x.Rate26 = x.Rate26 + proposal['Annuals'][AnnualKey[1]]
      else:
        x.Rate26 = x.Rate26 + proposal['Annuals'][AnnualKey[0]]
    '''
  return AnnualApplied


def apply_MajorReviews(proposal, LecList, year):
    MRapplied = [z for z in LecList]
    for x in MRapplied:
      fte = x.effort
      if year == 2024:
        if x.MRraiseIn24=='YES':
          x.Rate24 = x.Rate24*1.07
          x.cost24 = x.Rate24*fte
      if year == 2025:
        if x.MRraiseIn25=='YES':
          x.Rate25 = x.Rate25*1.07
          x.cost25 = x.Rate25*fte
      if year == 2026:
        if x.MRraiseIn26=='YES':
          x.Rate26 = x.Rate26*1.07
          x.cost26 = x.Rate26*fte
    return MRapplied

def applyLongevity(proposal, LecList, year):
    LongevityApplied = [z for z in LecList]
    threshold1 = float(proposal["Longevity"][1])
    threshold2 = float(proposal["Longevity"][1]) + float(proposal["Longevity"][2])
    for x in LongevityApplied:
      fte = x.effort

      if year == 2024:
        if x.ServiceYear >= threshold1:
          x.Rate24 += float(proposal["Longevity"][0])
          x.cost24 = x.Rate24*fte
      if year == 2025:
        if (x.ServiceYear +1) == threshold1 or (x.ServiceYear +1) == threshold2:
          x.Rate25 += float(proposal["Longevity"][0])
          x.cost25 = x.Rate25*fte
      if year==2026:
        if (x.ServiceYear +2) == threshold1 or (x.ServiceYear +2) == threshold2:
          x.Rate26 += float(proposal["Longevity"][0])
          x.cost26 = x.Rate26*fte
    return LongevityApplied

def CalcMinsAnnualsMRsLongevity2(proposal, LecList):
  for x in LecList:
      x.Rate24 = x.Rate23
  Min24Applied = apply_mins(proposal, LecList, 2024)
  OldCost = sum([x.cost23 for x in Min24Applied])
  Min24Cost = sum([x.cost24 for x in Min24Applied])

  Ann24Applied = apply_Annuals(proposal, Min24Applied, 2024)
  Ann24Cost = sum([x.cost24 for x in Ann24Applied])

  MR24Applied = apply_MajorReviews(proposal, Ann24Applied, 2024)
  MR24Cost = sum([x.cost24 for x in MR24Applied])

  Long24Applied = applyLongevity(proposal, MR24Applied, 2024)
  Long24Cost = sum([x.cost24 for x in Long24Applied])

  for x in Long24Applied:
    x.Rate25 = x.Rate24

  Min25Applied = apply_mins(proposal, Long24Applied, 2025)
  Min25Cost = sum([x.cost25 for x in Min25Applied])

  Ann25Applied = apply_Annuals(proposal, Min25Applied, 2025)
  Ann25Cost = sum([x.cost25 for x in Ann25Applied])

  MR25Applied = apply_MajorReviews(proposal, Ann25Applied, 2025)
  MR25Cost = sum([x.cost25 for x in MR25Applied])

  Long25Applied = applyLongevity(proposal, MR25Applied, 2025)
  Long25Cost = sum([x.cost25 for x in Long25Applied])


  for x in Long25Applied:
    x.Rate26 = x.Rate25

  Min26Applied = apply_mins(proposal, Long25Applied, 2026)
  Min26Cost = sum([x.cost26 for x in Min26Applied])

  Ann26Applied = apply_Annuals(proposal, Min26Applied, 2026)
  Ann26Cost = sum([x.cost26 for x in Ann26Applied])

  MR26Applied = apply_MajorReviews(proposal, Ann26Applied, 2026)
  MR26Cost = sum([x.cost26 for x in MR26Applied])

  Long26Applied = applyLongevity(proposal, MR26Applied, 2026)
  Long26Cost = sum([x.cost26 for x in Long26Applied])


  for x in Long26Applied:
    if x.appointment == 3:
      x.salary24 = 0.5*x.cost24
      x.salary25 = 0.5*x.cost25
      x.salary26 = 0.5*x.cost26
    else:
      x.salary24 = x.cost24
      x.salary25 = x.cost25
      x.salary26 = x.cost26

  NewMoney = {'Mins24Cost': Min24Cost-OldCost,
              'Annuals24Cost': Ann24Cost-Min24Cost,
              'MR24Cost': MR24Cost-Ann24Cost,
              'Long24Cost': Long24Cost-MR24Cost,
              'Mins25Cost': Min25Cost-Long24Cost,
              'Annuals25Cost': Ann25Cost-Min25Cost,
              'MR25Cost': MR25Cost-Ann25Cost,
              'Long25Cost': Long25Cost- MR25Cost,
              'Mins26Cost': Min26Cost-Long25Cost,
              'Annuals26Cost': Ann26Cost - Min26Cost,
              'MR26Cost': MR26Cost-Ann26Cost,
              'Long26Cost': Long26Cost-MR26Cost}

  return NewMoney, Min24Applied, Long26Applied