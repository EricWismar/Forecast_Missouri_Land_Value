#!/usr/bin/env python
# coding: utf-8

# In[158]:


import warnings
warnings.filterwarnings("ignore")
import matplotlib.ticker as ticker 
import random
import numpy as np
import pandas as pd
import requests
import lxml.html as lh
import re
import matplotlib.pyplot as plt
import seaborn as sns


# In[166]:


url='https://extension2.missouri.edu/G403'
#Create a handle, page, to handle the contents of the website
page = requests.get(url)
#Store the contents of the website under doc
doc = lh.fromstring(page.content)
#Parse data that are stored between <tr>..</tr> of HTML
tr_elements = doc.xpath('//tr')
tr_elements = doc.xpath('//tr')
#Create empty list
col=[]
i=0
#For each row, store each first element (header) and an empty list
for t in tr_elements[0]:
    i+=1
    name=t.text_content()
    col.append((name,[]))

#Since out first row is the header, data is stored on the second row onwards
for j in range(1,len(tr_elements)):
    #T is our j'th row
    T=tr_elements[j]
    
    #If row is not of size 3, the //tr data is not from our table 
    '''if len(T)!=3:
        print("Length of T mismatch")
        break'''
#i is the index of our column
    i=0
    
    #Iterate through each element of the row
    for t in T.iterchildren():
        data=t.text_content()
        #Check if row is empty
        #if i>0:
        #Convert any numerical value to integers
            #try:
             #   data=int(data)
            #except:
             #   None
        #Append the data to the empty list of the i'th column
        col[i][1].append(data)
        #Increment i for the next column
        i+=1

#Convert List of tuples (with lists) into a dict and then into a dataframe
Dict={title:column for (title,column) in col}
df=pd.DataFrame(Dict)


# In[169]:


df.rename(columns={'1997b':'1997'},inplace=True)
variables_list=df.columns[1:]
variables_list


# In[171]:


for v in variables_list:
    df[v].replace(to_replace='[^0-9]+', value='',inplace=True,regex=True)
    df=df.astype({v:'int64'})


# In[172]:


dfWide=df
dfWide=pd.melt(dfWide,id_vars=['County'],value_vars=variables_list, var_name='Year',value_name='AcrePrice')
dfWide=dfWide.sort_values(by=['County','Year'])
dfWide['Pct_Chg']=dfWide.groupby('County')['AcrePrice'].apply(lambda x: (x-x.shift(1))/x)
dfWide.head(10)


# In[190]:


url='https://mcdc.missouri.edu/geography/reference/MO_Region_Codes.html'
#Create a handle, page, to handle the contents of the website
page = requests.get(url)
#Store the contents of the website under doc
doc = lh.fromstring(page.content)
#Parse data that are stored between <tr>..</tr> of HTML
tr_elements = doc.xpath('//tr')[14:]
#Create empty list
col=[]
i=0
#For each row, store each first element (header) and an empty list
for t in tr_elements[0]:
    i+=1
    name=t.text_content()
    col.append((name,[]))

#Since our first row is the header, data is stored on the second row onwards
for j in range(1,len(tr_elements)):
    #T is our j'th row
    T=tr_elements[j]
    
    #If row is not of size 3, the //tr data is not from our table 
    '''if len(T)!=3:
        print("Length of T mismatch")
        break'''
#i is the index of our column
    i=0
    
    #Iterate through each element of the row
    for t in T.iterchildren():
        data=t.text_content()
        #Check if row is empty
        #if i>0:
        #Convert any numerical value to integers
            #try:
             #   data=int(data)
            #except:
             #   None
        #Append the data to the empty list of the i'th column
        col[i][1].append(data)
        #Increment i for the next column
        i+=1

#Convert List of tuples (with lists) into a dict and then into a dataframe
Dict={title:column for (title,column) in col}
df2=pd.DataFrame(Dict)


# In[232]:


dfWide2=pd.merge(dfWide,df2, left_on='County', right_on='county', how='left')
dfWide2.drop(columns='county',inplace=True)


# In[233]:


dfWide2['Region']=np.where(pd.isnull(dfWide2['Region']),'Avg',dfWide2['Region'])
dfWide2


# In[237]:


dfWide2['Region'].unique()


# In[257]:



for v in dfWide2['Region'].unique():
    dfPlot=dfWide2[dfWide2.Region==v]
    sns.set_theme(style="darkgrid")
    g=sns.lineplot(x = "Year", y = "Pct_Chg", hue="County", data = dfPlot)
    g.set_xticklabels(labels=dfPlot.Year.unique(),rotation=30)
    g.set_ylabel('Pct Change')
    g.set(title='Price Change in Farm Acreage for {} Region'.format(v))
    plt.legend(bbox_to_anchor=(1, 1), loc='upper left', borderaxespad=0)
    plt.show()


# In[246]:


help(g.)

