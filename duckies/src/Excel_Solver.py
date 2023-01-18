#!/usr/bin/env python
# coding: utf-8

# # Excel-Solver Implementation in Python
# This short script looks at implementing a type of excel-solver for the Head First Chapter 3 "Duckies" problem

# In[1]:


import pandas as pd
#!pip install pulp
import pulp as p
import matplotlib.pyplot as plt
import math


# ### Step 1
# Load the data from the excel sheet and store variables

# In[2]:


input_df = pd.read_excel(open('bathing_friends_unlimited.xls', 'rb'),sheet_name='Sheet1') 
input_df.columns = ["name","value1","value2"]


# In[3]:


# Original Constraints to be applied
duck_limit = 400
fish_limit = 300
# Rubber cost per item
duck_rubber = input_df[8:9]['value1'][8]
fish_rubber = input_df[9:10]['value1'][9]
rubber_available = input_df[12:13]['value1'][12]
# Profits per item
duck_profit = input_df[15:16]['value1'][15]
fish_profit = input_df[16:17]['value1'][16]


# # Create 1st Analysis

# In[4]:


Lp_prob = p.LpProblem('Duckies_Analysis_1', p.LpMaximize)
# Generate Problem Variables (>= 0):
d = p.LpVariable("d", lowBound = 0)
f = p.LpVariable("f", lowBound = 0)

# Create Objective Function:
Lp_prob += duck_profit*d + fish_profit*f

# Set Up the Constraints: 
Lp_prob += duck_rubber*d + fish_rubber*f <= rubber_available
Lp_prob += d <= duck_limit
Lp_prob += f <= fish_limit

status = Lp_prob.solve()
print("Ducks: " + str(int(p.value(d))))
print("Fish: " + str(int(p.value(f))))
print("Profit: $" + str(int(p.value(Lp_prob.objective))))


# # Explore limits for 2nd Analysis

# In[5]:


sales_df = pd.read_excel(open('historical_sales_data.xls', 'rb'),sheet_name='Sheet1')
sales_df['temp_month'] = (sales_df.index % 12) + 1
sales_df['temp_date'] = sales_df['Year'].astype(str) + '-' + sales_df['temp_month'].astype(str)
sales_df['date'] =  pd.to_datetime(sales_df['temp_date'], format='%Y-%m')
sales_df.drop(['Month','Year','temp_month','temp_date'], axis= 1, inplace=True)
sales_df.head(3)


# # Create 2nd Analysis

# In[6]:


duck_limit = 150
fish_limit = 50

Lp_prob2 = p.LpProblem('Duckies_Analysis_2', p.LpMaximize)
# Generate Problem Variables (>= 0):
d = p.LpVariable("d", lowBound = 0)
f = p.LpVariable("f", lowBound = 0)

# Create Objective Function:
Lp_prob2 += duck_profit*d + fish_profit*f

# Set Up the Constraints: 
Lp_prob2 += duck_rubber*d + fish_rubber*f <= rubber_available
Lp_prob2 += d <= duck_limit
Lp_prob2 += f <= fish_limit

status = Lp_prob2.solve()
print("Ducks: " + str(int(p.value(d))))
print("Fish: " + str(int(p.value(f))))
print("Profit: $" + str(int(p.value(Lp_prob2.objective))))


# # Creating 3rd analysis of my Estimate on historic sales

# In[7]:


#06_dec: 125 , 49 
#07_jan:  90 , 34
#07_dec: 148 , 60
#08_jan: 103 , 37
# % drop 06-07: -28% , -30%
# % drop 07-08: -30% , -38%
# average drop: -29% , -34%
#08_dec: 137 , 201
# Predicted values:
fish_last_sale = sales_df[-1:]['Fish'].values[0]
ducks_last_sale = sales_df[-1:]['Ducks'].values[0]
predicted_fish_sales = math.ceil(fish_last_sale + (fish_last_sale * -0.29))
predicted_ducks_sales = math.ceil(ducks_last_sale + (ducks_last_sale * -0.34))
print("Produce " + str(predicted_fish_sales) + " Fish, and " + str(predicted_ducks_sales) + " Ducks for next month")


# In[8]:


duck_limit = predicted_ducks_sales
fish_limit = predicted_fish_sales

Lp_prob3 = p.LpProblem('Duckies_Analysis_3', p.LpMaximize)
# Generate Problem Variables (>= 0):
d = p.LpVariable("d", lowBound = 0)
f = p.LpVariable("f", lowBound = 0)

# Create Objective Function:
Lp_prob3 += duck_profit*d + fish_profit*f

# Set Up the Constraints: 
Lp_prob3 += duck_rubber*d + fish_rubber*f <= rubber_available
Lp_prob3 += d <= duck_limit
Lp_prob3 += f <= fish_limit

status = Lp_prob3.solve()
print("Ducks: " + str(int(p.value(d))))
print("Fish: " + str(int(p.value(f))))
print("Profit: $" + str(int(p.value(Lp_prob3.objective))))


# # Graphs

# In[14]:


plt.figure(figsize=(9, 4.5), layout='constrained')
plt.plot(sales_df['date'], sales_df['Ducks'], label='Ducks', color="orange")
plt.plot(sales_df['date'], sales_df['Fish'], label='Fish', color="skyblue")
plt.plot(sales_df['date'], sales_df['Total '], label='Total', color="brown")
plt.xlabel('Date')
plt.ylabel('Sales')
plt.title("Historical Sales")
plt.grid(True)
plt.xticks(rotation=45)
plt.legend()

plt.savefig('historic_sales.png', bbox_inches='tight', dpi=150)


# In[ ]:




