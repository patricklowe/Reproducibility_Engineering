#!/usr/bin/env python
# coding: utf-8

# In[1]:


### Excel-Solver Implementation in Python
# This short script looks at implementing a type of excel-solver for the Head First Chapter 3 "Duckies" problem

import pandas as pd # To open excel file (XLS)
import pulp as p # the core package, to replace Excels Solver
import matplotlib.pyplot as plt # PLotting graphs
import datetime # adding our predicted values for graphing
import math # for a minor calculation, converting to integer could also work


# In[2]:


# Read the xls file sheet 1, with our needed data
input_df = pd.read_excel(open('bathing_friends_unlimited.xls', 'rb'),sheet_name='Sheet1') 
# rename columns
input_df.columns = ["name","value1","value2"]


# In[3]:


# Get rubber cost per item
duck_rubber = input_df[8:9]['value1'][8]
fish_rubber = input_df[9:10]['value1'][9]
rubber_available = input_df[12:13]['value1'][12]

# Get profits per item
duck_profit = input_df[15:16]['value1'][15]
fish_profit = input_df[16:17]['value1'][16]


# In[27]:


def Solver(fish_limit, ducks_limit):
    # Identify optimization problem
    Lp_prob = p.LpProblem('Duckies_Analysis', p.LpMaximize)

    # Generate Problem Variables for ducks (d) and fish (f)
    d = p.LpVariable("d", lowBound = 0)
    f = p.LpVariable("f", lowBound = 0)

    # Create Objective Function:
    Lp_prob += (duck_profit*d) + (fish_profit*f)

    # Set Up the Constraints: 
    Lp_prob += (duck_rubber*d) + (fish_rubber*f) <= rubber_available
    Lp_prob += d <= duck_limit
    Lp_prob += f <= fish_limit

    # Solve the problem, print the results
    status = Lp_prob.solve(PULP_CBC_CMD(msg=0))
    p.PULP_CBC_CMD(msg=0).solve(Lp_prob)
    print("Fish Created: " + str(int(p.value(f))))
    print("Ducks Created: " + str(int(p.value(d))))
    print("Profit Expected: $" + str(int(p.value(Lp_prob.objective))))


# # Create 1st Analysis

# In[28]:


print("--- 1st Analysis ---")
# Values provided in Head First Data Analysis Chapter 3
duck_limit = 400
fish_limit = 300
Solver(fish_limit,duck_limit)


# # Create 2nd Analysis

# In[6]:


print("--- 2nd Analysis ---")
# Values provided in Head First Data Analysis Chapter 3
duck_limit = 150
fish_limit = 50
Solver(fish_limit,duck_limit)


# # Exploring historical data to predict next months sales

# In[7]:


# Open historical data
sales_df = pd.read_excel(open('historical_sales_data.xls', 'rb'),sheet_name='Sheet1')

# Create new frame for date, not ideal if 1st month is not january
sales_df['temp_month'] = (sales_df.index % 12) + 1
sales_df['temp_date'] = sales_df['Year'].astype(str) + '-' + sales_df['temp_month'].astype(str)
sales_df['date'] =  pd.to_datetime(sales_df['temp_date'], format='%Y-%m')

# Drop temporary/old columns
sales_df.drop(['Month','Year','temp_month','temp_date'], axis= 1, inplace=True)


# In[8]:


# Get the average change in sales between the 2 products; Dec-Jan
products = ['Fish','Ducks']
dates = {
    "dec_06": '2006-12-01',
    "jan_07": '2007-01-01',
    "dec_07": '2007-12-01',
    "jan_08": '2008-01-01',
}


# In[9]:


next_limit_f = 0
next_limit_d = 0

for prod in products:
    print("% Change in sales of " + prod)
    predict_values = []
    change = []
    for date in dates.values():
        predict_values.append(sales_df[sales_df['date'] == date][prod].values[0])
    c1 = 1 - (predict_values[1] / predict_values[0])
    c2 = 1 - (predict_values[3] / predict_values[2])
    change.append(c1)
    change.append(c2)
    c3 = (change[0] + change[1])/2
    print("Year 1:  " + str(round(c1*100, 2)) + "%")
    print("Year 2:  " + str(round(c2*100, 2)) + "%")
    print("Average: " + str(round(c3*100, 2)) + "%")
    if prod == 'Fish':
        next_limit_f = round(c3, 2) # Round to 2 decimal places
    elif prod == 'Ducks':
        next_limit_d = round(c3, 2)


# In[10]:


# Sales of Dec-08
fish_last_sale = sales_df[-1:]['Fish'].values[0]
ducks_last_sale = sales_df[-1:]['Ducks'].values[0]

# Predicted values for Jan-09
predicted_fish_sales = math.ceil(fish_last_sale + (fish_last_sale * -next_limit_f))
predicted_ducks_sales = math.ceil(ducks_last_sale + (ducks_last_sale * -next_limit_d))

# Our Results
print("--- Estimated production based on Avg Sales ---")
print("Produce " + str(predicted_fish_sales) + " Fish, and " + str(predicted_ducks_sales) + " Ducks for next month")
#Produce 98 Fish, and 133 Ducks for next month


# In[11]:


print("--- 3rd Analysis ---")
# Values provided in Head First Data Analysis Chapter 3
duck_limit = predicted_ducks_sales
fish_limit = predicted_fish_sales
Solver(fish_limit,duck_limit)


# # Graphs

# In[12]:


plt.figure(figsize=(9, 4.5), layout='constrained')
markers_on = [35]
plt.plot(sales_df['date'], sales_df['Ducks'], '-D', markevery=markers_on, label='Ducks', color="orange")
plt.plot(sales_df['date'], sales_df['Fish'], '-D', markevery=markers_on, label='Fish', color="skyblue")
plt.plot(sales_df['date'], sales_df['Total '], '-D', markevery=markers_on, label='Total', color="brown")
plt.xlabel('Date')
plt.ylabel('Sales')
plt.title("Historical Sales")
plt.grid(True)
plt.xticks(rotation=45)
plt.legend()
plt.annotate('Markers indicate Current sales for Dec-08', 
             xy = (1.0, -0.25),
             xycoords='axes fraction',
             ha='right',
             va="center",
             fontsize=10)
plt.savefig('historic_sales.png', bbox_inches='tight', dpi=150)


# In[ ]:




