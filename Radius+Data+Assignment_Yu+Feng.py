
# coding: utf-8

# In[58]:

import pandas as pd
import numpy as np
import json
#import matplotlib.pyplot as plt
#import seaborn as sns
import collections


# ## Load Json file

# In[2]:

with open('data_analysis.json') as radius_data:
   data = json.load(radius_data)
   df = pd.DataFrame(data)
#df=pd.read_json("/Users/Yu/Downloads/data_analysis.json")
#pd.DataFrame(df)


# In[3]:

df.shape


# In[4]:

df.head()


# In[5]:

df.dtypes


# In[6]:

# check number of unique values of each field
# None value not included
df.apply(pd.Series.nunique)


# In[17]:

# check what categories each field has
a = df.zip.unique()
a.sort()
a
#df.address.unique()
#df.category_code.unique()
#df.state.unique()
#df.city.unique()
#df.headcount.unique()
#df.name.unique()
#df.phone.unique()
#df.revenue.unique()
#df.state.unique()
#df.zip.unique()


# ## Calcualting fill rate and create summary table

# In[18]:

# use filter(None,..) to detect all false values for all string objects
cols = df.columns.tolist()
list1 = []
list2 = []
for i in cols:
    feat = i
    filtered = filter(None, df[i]).__len__()
    list1.append(feat)
    list2.append(filtered)
df1 = pd.DataFrame({'features': list1, 'filled_num': list2})
del list1, list2


# In[19]:

df1
#number of rows filled for each column (exclude false values: None, 0, '')


# In[20]:

# show numbers of rows for each column excluding None values only
df2= df.count().to_frame().reset_index()
df2 = df2.rename(columns= {'index': 'features',0: 'not_None_value'})


# In[21]:

df2


# In[22]:

df.isnull().sum()
# so isnull only detect cells filled with None value


# In[23]:

df[df['category_code'].isnull()]


# In[24]:

# create a dataframe for summary
df1['total_row_num'] = df.shape[0]
df3 = pd.merge(df1, df2, on='features')
df_Q1 = df3[['features', 'total_row_num','filled_num']]
df_Q1.dtypes


# In[25]:

# Q1: calculate fill rate (define records with [None, '', 0] as not having a value )
df_Q1['total_row_num'] = df_Q1['total_row_num'].astype(float)
df_Q1['filled_num'] = df_Q1['filled_num'].astype(float)
df_Q1['not_filled_num'] =  df_Q1['total_row_num'] - df_Q1['filled_num']
df_Q1['fill_rate'] = df_Q1['filled_num']/df_Q1['total_row_num']


# In[26]:

df_Q1


# ## Calculating true-valued fill rate

# In[27]:

list_a = df.values.T.tolist()
non_valued_fills = ['null', 'none', '0', ' ','', 0, None]
for list in list_a:
    for idx, x in enumerate(list):
        if x in non_valued_fills:
            list[idx] = None
dfx= pd.DataFrame(list_a)
df4= dfx.transpose() 
my_columns = ["address", "category_code", "city", "headcount", "name", "phone", "revenue", "state", "time_in_business", "zip"]
df4.columns = my_columns
# df4 is a dataframe with only None as missing or not true-valued data, 
# all the other types of problematic data were replaced by None


# In[29]:

df4[df4['address'].isnull()] #only None values


# In[30]:

null_count = pd.DataFrame(df4.isnull().sum())
null_count['features'] = null_count.index
null_count = null_count.reset_index(drop=True)
null_count.columns = ['not_true_sum','features']


# In[31]:

# merge the true-valued data with the summary filled data 
df_Q2 = pd.merge(df_Q1, null_count, on='features')
df_Q2['not_true_sum'] = df_Q2['not_true_sum'].astype(float)
df_Q2['true_valued_sum'] = df_Q2['total_row_num'] - df_Q2['not_true_sum']
df_Q2['true_valued_fill_rate'] = df_Q2['true_valued_sum']/ df_Q2['total_row_num']
df_Q2


# ## Calculating cardinality

# In[32]:

unique = pd.DataFrame(df4.apply(pd.Series.nunique))
unique.columns = ['Cardinality']


# In[33]:

unique['total_row_num'] = df.shape[0]
unique


# ## Exploring data for more info

# ### Analysis of location related fields (address, city, state, zip)

# In[34]:

df_Q2
# noticed that these 4 fields have similar amount of missing values (102, 105, 104, 110)
# questions: are these missing from almost the same businesses?
# which means we lost the location info of the businesses?


# In[35]:

df4.isnull().sum()


# In[36]:

# get index of None values of the 4 fields to see if they came from the same obs
index1 = df4['address'].index[df4['address'].isnull()]
index1


# In[37]:

index2 = df4['city'].index[df4['city'].isnull()]
index2


# In[38]:

index3 = df4['state'].index[df4['state'].isnull()]
index4 = df4['zip'].index[df4['zip'].isnull()]


# In[40]:

index3


# In[44]:

# index back to the data recordings
#df.index[df['address'] == 0].tolist()
#index= df.index[df['address'] == ' '].tolist()
#df4.loc[index1] #address 102x10
#df4.loc[index2] #city 105x10
#df4.loc[index3] #state 104x10
df4.loc[index4] #zip 110x10


# ### Analysis of headcount and time_in_business relationship

# In[45]:

df_Q4_1 = df4[['time_in_business','headcount','name']].groupby(['time_in_business', 'headcount']).count()


# In[46]:

# to see the if the headcount will increase as time in business increase
df_Q4_1


# In[47]:

df_Q4_2 = df4['name']
dups_name = [item for item, count in collections.Counter(df_Q4_2).items() if count > 1]
print dups_name


# In[55]:

df4[df4['name'] == 'ARIZONA CHEMICAL COMPANY LLC']


# In[56]:

unique.to_csv('unique.csv')


# In[57]:

df_Q4_1.to_csv('df_Q4_1.csv')


# In[64]:

df4.to_csv('data.csv', header=True, index=False, encoding='utf-8')


# In[ ]:



