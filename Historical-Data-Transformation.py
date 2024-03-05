#!/usr/bin/env python
# coding: utf-8

# In[4]:


import pandas as pd


# # Load input csv file

# In[3]:


input_file_path = 'input.csv'
df = pd.read_csv(input_file_path)


# # Sort dataframe by employee ID and date

# In[ ]:


df = df.sort_values(by=['EmployeeID', 'Date'])


# # Initialize Effective Date and End Date columns

# In[ ]:


df['Effective Date'] = df['Date']
df['End Date'] = df['Date'].shift(-1) - pd.Timedelta(days=1)
df['End Date'].iloc[-1] = '2100-01-01


# # Iterate through each employee's records

# In[ ]:


for employee_id, employee_group in df.groupby('EmployeeID'):
    for i in range(1, len(employee_group)):
        # Calculate Effective Date and End Date
        df.loc[employee_group.index[i], 'Effective Date'] = employee_group['End Date'].iloc[i - 1] + pd.Timedelta(days=1)
        df.loc[employee_group.index[i], 'End Date'] = min(employee_group['Effective Date'].iloc[i + 1], '2100-01-01')


# # Handle missing data by inheriting values from the most recent past record

# In[ ]:


df = df.ffill()


# # Copy unchanged values for fields without associated dates across different records

# In[ ]:


for column in df.columns:
    if 'Date' not in column:
        df[column] = df.groupby('EmployeeID')[column].transform('first')


# # Save the transformed dataframe to a new CSV file

# In[ ]:


output_file_path = 'output.csv'
df.to_csv(output_file_path, index=False)

