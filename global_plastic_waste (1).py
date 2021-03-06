# -*- coding: utf-8 -*-
"""Global_Plastic_Waste.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1Mkz94db_EFzxpn6drKA8jiSkW0WLML6n
"""

# Commented out IPython magic to ensure Python compatibility.
import numpy as np 
import pandas as pd 
import seaborn as sns 
import warnings
import matplotlib.pyplot as plt 
# %matplotlib inline 

warnings.filterwarnings('ignore')
sns.set_style('darkgrid')

df = pd.read_csv('per-capita-plastic-waste-vs-gdp-per-capita.csv')

df.head()

df.shape

df.info()

df.rename(columns={'GDP per capita, PPP (constant 2011 international $)': 'GDP per capita in PPP',
                   'Total population (Gapminder, HYDE & UN)': 'Total Population',
                    'Per capita plastic waste (kg/person/day)': 'Waste per person(kg/day)'},inplace = True)
df.head()

incm_df_idx = df[(df['Total Population'].isna() & df['GDP per capita in PPP'].isna())].index
df.drop(incm_df_idx,inplace = True)
df.head()
df.shape

df_2010 = df[df['Year']==2010]
df_2010 = df_2010.drop(columns='Continent')
df_2010

df_2015 = df[df['Year']==2015]

df_2010['Continent'] = df_2015['Continent'].values
df_2015

missing_idx = df_2010[df_2010['Continent'].isna()].index
df_2010.drop(missing_idx,inplace = True)
df_2010

df_2010 = df_2010[df_2010['Waste per person(kg/day)'].notna()]
wa_g = df_2010.reset_index().drop('index',axis=1)
wa_g
# df_2010

df2 = pd.read_csv('per-capita-mismanaged-plastic-waste-vs-gdp-per-capita.csv')
df2.head()

df2.rename(columns={'Per capita mismanaged plastic waste': 'Mismanaged waste per person(kg/day)',
                  'GDP per capita, PPP (constant 2011 international $)': 'GDP per capita in PPP',
                  'Total population (Gapminder, HYDE & UN)': 'Total Population'},inplace=True)
df2.head()

df2.drop('Continent',axis=1,inplace=True)

df2_2010 = df2[df2.Year==2010]
df2_2010

df2_2010 = df2_2010[df2_2010['Mismanaged waste per person(kg/day)'].isna() != True]
# df2_2010
w_m = df2_2010.reset_index().drop('index',axis=1)
w_m

df_plastic_waste = pd.merge(wa_g,w_m,how='inner')
df_plastic_waste
# wa_g

df_plastic_waste.columns.tolist()
col_names = ['Entity','Code','Year','Waste per person(kg/day)','Mismanaged waste per person(kg/day)',
           'GDP per capita in PPP','Total Population','Continent']
df_plastic_waste = df_plastic_waste[col_names]
df_plastic_waste.iloc[:,3:5] = np.around(df_plastic_waste[['Waste per person(kg/day)', 
                                                            'Mismanaged waste per person(kg/day)']],decimals = 2)
df_plastic_waste['Total Population'] = df_plastic_waste['Total Population'].astype(int)
df_plastic_waste.info()

df_plastic_waste['Total waste(kgs/year)'] = ((df_plastic_waste['Waste per person(kg/day)'] * df_plastic_waste['Total Population']) * 365)
df_plastic_waste['Total waste mismanaged(kgs/year)'] = ((df_plastic_waste['Mismanaged waste per person(kg/day)'] * df_plastic_waste['Total Population']) * 365)
df_plastic_waste.head()

plt.figure(1,figsize=(12,8))
plt.scatter(df_plastic_waste['GDP per capita in PPP'],df_plastic_waste['Mismanaged waste per person(kg/day)'])
plt.title('Waste Mismanaged',loc='center', fontsize=15)
plt.ylabel('Mismanaged waste', fontsize=15)
plt.xlabel('GDP per capita', fontsize=15)

sns.regplot(x='GDP per capita in PPP', y='Mismanaged waste per person(kg/day)',data=df_plastic_waste,
            scatter_kws={'color':'#34568B'}, line_kws={'color': '#650021'})
plt.show()

plt.figure(1,figsize=(12,8))
plt.scatter(df_plastic_waste['GDP per capita in PPP'],df_plastic_waste['Waste per person(kg/day)'])
plt.title('Waste Generated by GDP',loc='center', fontsize=15)
plt.ylabel('Waste per person(kg/day)', fontsize=12)
plt.xlabel('GDP per capita', fontsize=12)

sns.regplot(x='GDP per capita in PPP', y='Waste per person(kg/day)',data=df_plastic_waste,
            scatter_kws={'color':'#CD212A'}, line_kws={'color': '#380282'})
plt.show()

