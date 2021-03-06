#!/usr/bin/env python
# coding: utf-8

# In[3]:


#import pandas
import pandas as pd

#import numpy
import numpy as np

#import matplotlib
import matplotlib.pyplot as plt

#import csv
file_path = 'https://raw.githubusercontent.com/bigdatacup/Big-Data-Cup-2021/main/hackathon_scouting.csv'

otters = pd.read_csv(file_path)


# In[11]:


otters["X1 Adjusted"] = 189 - otters["X Coordinate"]
otters["Y1 Adjusted"] = abs(otters["Y Coordinate"] - 42.5)
otters["Angle On Net"] = (np.arctan(otters["Y1 Adjusted"]/otters["X1 Adjusted"]))*180/np.pi
otters["Distance From Net"] = np.sqrt((otters["X1 Adjusted"])*(otters["X1 Adjusted"]) + (otters["Y1 Adjusted"])*(otters["Y1 Adjusted"]))
otters["Previous Event"] = otters["Event"].shift(+1)
otters["Next Event"] = otters["Event"].shift(-1)

def stconditions(otters):
    if (otters["Home Team"] == "Erie Otters") & (otters["Home Team Skaters"] > otters["Away Team Skaters"]) | (otters["Away Team"] == "Erie Otters") & (otters["Away Team Skaters"] > otters["Home Team Skaters"]):
        return "Power Play"
    else:
        return 0
    
otters["Power Play"] = otters.apply(stconditions, axis=1)

def evconditions(otters):
    if otters["Home Team Skaters"] == otters["Away Team Skaters"]:
        return "EV"
    else:
        return 0
    
otters["EV"] = otters.apply(evconditions, axis=1)
    
def conditions(otters):
    if (otters["Next Event"] == "Shot") | (otters["Next Event"] == "Goal") & (otters["Event"] == "Play"):
        return 1/(1+np.exp(-(otters["Distance From Net"]*-0.0437 + otters["Angle On Net"]*-0.0162)))
    else:
        return 0
    
otters["ProxG Pass"] = otters.apply(conditions, axis=1)    

def conditions2(otters):
    if (otters["Previous Event"] == "Play") & ((otters["Event"] == "Shot")|(otters["Event"] == "Goal")):
        return 1/(1+np.exp(-(otters["Distance From Net"]*-0.0437 + otters["Angle On Net"]*-0.0162)))
    else:
        return 0
    

otters["ProxG Shot"] = otters.apply(conditions2, axis=1)   
otters["ProxG Shot Up"] = otters["ProxG Shot"].shift(-1)
otters["Cumulative PlusProxG"] = otters["ProxG Shot Up"] - otters["ProxG Pass"]
otters.loc[otters["X1 Adjusted"] < 0, "Cumulative PlusProxG"] = 0

otters["Pos CPPxG"] = np.where(otters["Cumulative PlusProxG"] > 0, 1, 0)
otters["Neg CPPxG"] = np.where(otters["Cumulative PlusProxG"] < 0, 1, 0)
otters["Total CPPxG"] = otters["Pos CPPxG"] + otters["Neg CPPxG"]

otters


# In[24]:


#Player Filters

jd = otters[otters["Player"]=="Jamie Drysdale"]
jdev = jd[jd["EV"]=="EV"]
jdpp = jd[jd["Power Play"]=="Power Play"]

mg = otters[otters["Player"]=="Maxim Golod"]
mgev = mg[mg["EV"]=="EV"]
mgpp = mg[mg["Power Play"]=="Power Play"]

cy = otters[otters["Player"]=="Chad Yetman"]
cyev = cy[cy["EV"]=="EV"]
cypp = cy[cy["Power Play"]=="Power Play"]


# In[22]:


jdevpercentage = jdev["Pos CPPxG"].sum()/jdev["Total CPPxG"].sum()
jdevpp = jdev["Cumulative PlusProxG"].sum()/jdev["Total CPPxG"].sum()
jdpopercentage = jdpp["Pos CPPxG"].sum()/jdpp["Total CPPxG"].sum()
jdpopp = jdpp["Cumulative PlusProxG"].sum()/jdpp["Total CPPxG"].sum()

Stat = ['EV PVA %','EV PVA/Pass', 'PP PVA %','PP PVA/Pass']
Name = [jdevpercentage - 0.5, jdevpp, jdpopercentage - 0.5, jdpopp]

plt.bar(Stat, Name)
plt.title('Jamie Drysdale PVA')
plt.xlabel('PVA')
plt.ylabel('Value')
plt.show()

jdpopercentage
jdpopp
jdevpercentage


# In[34]:


mgevpercentage = mgev["Pos CPPxG"].sum()/mgev["Total CPPxG"].sum()
mgevpp = mgev["Cumulative PlusProxG"].sum()/mgev["Total CPPxG"].sum()
mgpopercentage = mgpp["Pos CPPxG"].sum()/mgpp["Total CPPxG"].sum()
mgpopp = mgpp["Cumulative PlusProxG"].sum()/mgpp["Total CPPxG"].sum()

cyevpercentage = cyev["Pos CPPxG"].sum()/cyev["Total CPPxG"].sum()
cyevpp = cyev["Cumulative PlusProxG"].sum()/cyev["Total CPPxG"].sum()
cypopercentage = cypp["Pos CPPxG"].sum()/cypp["Total CPPxG"].sum()
cypopp = cypp["Cumulative PlusProxG"].sum()/cypp["Total CPPxG"].sum()

Stat = ['EV PVA %', 'EV PVA/Pass', 'PP PVA %','PP PVA/Pass']
Name = [mgevpercentage - 0.5, mgevpp, mgpopercentage - 0.5, mgpopp]

plt.bar(Stat, Name)
plt.title('Maxim Golod')
plt.xlabel('PVA')
plt.ylabel('Value')
plt.show()


# In[37]:


cyevpercentage = cyev["Pos CPPxG"].sum()/cyev["Total CPPxG"].sum()
cyevpp = cyev["Cumulative PlusProxG"].sum()/cyev["Total CPPxG"].sum()
cypopercentage = cypp["Pos CPPxG"].sum()/cypp["Total CPPxG"].sum()
cypopp = cypp["Cumulative PlusProxG"].sum()/cypp["Total CPPxG"].sum()

Stat = ['EV PVA %', 'EV PVA/Pass', 'PP PVA %','PP PVA/Pass']
Name = [cyevpercentage - 0.5, cyevpp, cypopercentage - 0.5, cypopp]

plt.bar(Stat, Name)
plt.title('Chad Yetman')
plt.xlabel('PVA')
plt.ylabel('Value')
plt.show()

cyevpercentage


# In[11]:


import plotly.graph_objects as go

fig = go.Figure(data=[go.Table(header=dict(values=['<b>PLAYER</b>','<b>MAXIM GOLOD</b>', '<b>CHAD YETMAN</b>']),
                 cells=dict(values=[['GP', 'G', 'A', 'P', 'Central Scouting', 'NHL Status'], [63, 25, 53, 78, 213, 'ANA - FA, 2020'], [61, 43, 31, 74, 'NR', 'CHI - 172nd, 2020']]))
                     ])
fig.show()


# In[31]:





# In[32]:





# In[37]:





# In[39]:





# In[7]:





# In[1]:


# PLAYER TABLE
import plotly.graph_objects as go

fig = go.Figure(data=[go.Table(header=dict(values=['<b>PLAYER</b>','<b>MAXIM GOLOD</b>', '<b>CHAD YETMAN</b>']),
                 cells=dict(values=[['GP', 'G', 'A', 'P', 'Central Scouting', 'NHL Status'], [63, 25, 53, 78, 213, 'ANA - FA, 2020'], [61, 43, 31, 74, 'NR', 'CHI - 172nd, 2020']]))
                     ])
fig.show()


# In[6]:


print(otters.loc[[345]])


# In[ ]:




