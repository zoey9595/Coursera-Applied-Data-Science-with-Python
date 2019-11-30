
# coding: utf-8

# ---
# 
# _You are currently looking at **version 1.1** of this notebook. To download notebooks and datafiles, as well as get help on Jupyter notebooks in the Coursera platform, visit the [Jupyter Notebook FAQ](https://www.coursera.org/learn/python-data-analysis/resources/0dhYG) course resource._
# 
# ---

# In[5]:


import pandas as pd
import numpy as np
from scipy.stats import ttest_ind


# # Assignment 4 - Hypothesis Testing
# This assignment requires more individual learning than previous assignments - you are encouraged to check out the [pandas documentation](http://pandas.pydata.org/pandas-docs/stable/) to find functions or methods you might not have used yet, or ask questions on [Stack Overflow](http://stackoverflow.com/) and tag them as pandas and python related. And of course, the discussion forums are open for interaction with your peers and the course staff.
# 
# Definitions:
# * A _quarter_ is a specific three month period, Q1 is January through March, Q2 is April through June, Q3 is July through September, Q4 is October through December.
# * A _recession_ is defined as starting with two consecutive quarters of GDP decline, and ending with two consecutive quarters of GDP growth.
# * A _recession bottom_ is the quarter within a recession which had the lowest GDP.
# * A _university town_ is a city which has a high percentage of university students compared to the total population of the city.
# 
# **Hypothesis**: University towns have their mean housing prices less effected by recessions. Run a t-test to compare the ratio of the mean price of houses in university towns the quarter before the recession starts compared to the recession bottom. (`price_ratio=quarter_before_recession/recession_bottom`)
# 
# The following data files are available for this assignment:
# * From the [Zillow research data site](http://www.zillow.com/research/data/) there is housing data for the United States. In particular the datafile for [all homes at a city level](http://files.zillowstatic.com/research/public/City/City_Zhvi_AllHomes.csv), ```City_Zhvi_AllHomes.csv```, has median home sale prices at a fine grained level.
# * From the Wikipedia page on college towns is a list of [university towns in the United States](https://en.wikipedia.org/wiki/List_of_college_towns#College_towns_in_the_United_States) which has been copy and pasted into the file ```university_towns.txt```.
# * From Bureau of Economic Analysis, US Department of Commerce, the [GDP over time](http://www.bea.gov/national/index.htm#gdp) of the United States in current dollars (use the chained value in 2009 dollars), in quarterly intervals, in the file ```gdplev.xls```. For this assignment, only look at GDP data from the first quarter of 2000 onward.
# 
# Each function in this assignment below is worth 10%, with the exception of ```run_ttest()```, which is worth 50%.

# In[6]:


# Use this dictionary to map state names to two letter acronyms
states = {'OH': 'Ohio', 'KY': 'Kentucky', 'AS': 'American Samoa', 'NV': 'Nevada', 'WY': 'Wyoming', 'NA': 'National', 'AL': 'Alabama', 'MD': 'Maryland', 'AK': 'Alaska', 'UT': 'Utah', 'OR': 'Oregon', 'MT': 'Montana', 'IL': 'Illinois', 'TN': 'Tennessee', 'DC': 'District of Columbia', 'VT': 'Vermont', 'ID': 'Idaho', 'AR': 'Arkansas', 'ME': 'Maine', 'WA': 'Washington', 'HI': 'Hawaii', 'WI': 'Wisconsin', 'MI': 'Michigan', 'IN': 'Indiana', 'NJ': 'New Jersey', 'AZ': 'Arizona', 'GU': 'Guam', 'MS': 'Mississippi', 'PR': 'Puerto Rico', 'NC': 'North Carolina', 'TX': 'Texas', 'SD': 'South Dakota', 'MP': 'Northern Mariana Islands', 'IA': 'Iowa', 'MO': 'Missouri', 'CT': 'Connecticut', 'WV': 'West Virginia', 'SC': 'South Carolina', 'LA': 'Louisiana', 'KS': 'Kansas', 'NY': 'New York', 'NE': 'Nebraska', 'OK': 'Oklahoma', 'FL': 'Florida', 'CA': 'California', 'CO': 'Colorado', 'PA': 'Pennsylvania', 'DE': 'Delaware', 'NM': 'New Mexico', 'RI': 'Rhode Island', 'MN': 'Minnesota', 'VI': 'Virgin Islands', 'NH': 'New Hampshire', 'MA': 'Massachusetts', 'GA': 'Georgia', 'ND': 'North Dakota', 'VA': 'Virginia'}


# In[7]:


# Use this dictionary to map state names to two letter acronyms
states = {'OH': 'Ohio', 'KY': 'Kentucky', 'AS': 'American Samoa', 'NV': 'Nevada', 'WY': 'Wyoming', 'NA': 'National', 'AL': 'Alabama', 'MD': 'Maryland', 'AK': 'Alaska', 'UT': 'Utah', 'OR': 'Oregon', 'MT': 'Montana', 'IL': 'Illinois', 'TN': 'Tennessee', 'DC': 'District of Columbia', 'VT': 'Vermont', 'ID': 'Idaho', 'AR': 'Arkansas', 'ME': 'Maine', 'WA': 'Washington', 'HI': 'Hawaii', 'WI': 'Wisconsin', 'MI': 'Michigan', 'IN': 'Indiana', 'NJ': 'New Jersey', 'AZ': 'Arizona', 'GU': 'Guam', 'MS': 'Mississippi', 'PR': 'Puerto Rico', 'NC': 'North Carolina', 'TX': 'Texas', 'SD': 'South Dakota', 'MP': 'Northern Mariana Islands', 'IA': 'Iowa', 'MO': 'Missouri', 'CT': 'Connecticut', 'WV': 'West Virginia', 'SC': 'South Carolina', 'LA': 'Louisiana', 'KS': 'Kansas', 'NY': 'New York', 'NE': 'Nebraska', 'OK': 'Oklahoma', 'FL': 'Florida', 'CA': 'California', 'CO': 'Colorado', 'PA': 'Pennsylvania', 'DE': 'Delaware', 'NM': 'New Mexico', 'RI': 'Rhode Island', 'MN': 'Minnesota', 'VI': 'Virgin Islands', 'NH': 'New Hampshire', 'MA': 'Massachusetts', 'GA': 'Georgia', 'ND': 'North Dakota', 'VA': 'Virginia'}

def get_list_of_university_towns():
    '''Returns a DataFrame of towns and the states they are in from the 
    university_towns.txt list. The format of the DataFrame should be:
    DataFrame( [ ["Michigan", "Ann Arbor"], ["Michigan", "Yipsilanti"] ], 
    columns=["State", "RegionName"]  )

    The following cleaning needs to be done:

    1. For "State", removing characters from "[" to the end.
    2. For "RegionName", when applicable, removing every character from " (" to the end.
    3. Depending on how you read the data, you may need to remove newline character '\n'. '''
    towns = pd.read_table("university_towns.txt",header=None,names=["RegionName"])

    current_state = ""
    def get_state(cell):
        if cell.endswith("[edit]"):
            global current_state
            current_state = cell[:-6]
            return cell[:-6]
        else:
            return current_state

    towns["State"] = towns["RegionName"].map(get_state)

    towns = towns[~towns["RegionName"].str.endswith("[edit]")]
    towns["RegionName"] = towns["RegionName"].map(lambda x:x.split("(")[0].strip())
    towns = towns.reindex(columns=["State","RegionName"]).reset_index(drop=True)
    towns.State = towns.State.map(dict(zip(states.values(),states.keys())))

    return towns
get_list_of_university_towns().head()


# In[10]:


gdp = (pd.read_excel("gdplev.xls",header=1) #读写文件
                 .drop(["Annual","Unnamed: 1","Unnamed: 2","Unnamed: 3","Unnamed: 5","Unnamed: 7"],axis=1) #修剪数据-去除行
                 .iloc[217:] #修剪数据-2000年以后数据
                 .rename(columns={"Unnamed: 6":"GDP"}) #整理column索引
                 .reset_index(drop=True) #整理index索引
        )
gdp.GDP = gdp.GDP.astype(np.float64)

old = None
def do_math(cell):
    global old
    if old == None: old = cell
    delta = cell - old
    old = cell
    return delta

before = None
def again_math(cell):
    global before
    if before == None: before = 0
    before_cell = before
    before = cell
    if cell < 0 and before_cell < 0:
        return "DES"
    elif cell > 0 and before_cell > 0:
        return "INS"
    else:
        return np.nan


gdp["Delta"] = gdp["GDP"].map(do_math)
gdp["Type"] = gdp["Delta"].map(again_math)

def get_recession_start():
    '''Returns the year and quarter of the recession start time as a 
    string value in a format such as 2005q3'''
    start = []
    for i in gdp[gdp.Type == "DES"].index:
        if gdp.iloc[i-1].Type != "DES" and gdp.iloc[i-1].Type != "INS":
            start.append(i-1)
    res = gdp.iloc[start][["Quarterly"]].values[0,0]
    return res

get_recession_start()


# In[11]:


def get_recession_end():
    '''Returns the year and quarter of the recession end time as a 
    string value in a format such as 2005q3'''
    quart = get_recession_start()
    index = gdp[gdp.Quarterly == quart].index[0]
    while True:
        if gdp.iloc[index].Delta > 0 and  gdp.iloc[index+1].Delta > 0:
            ends = index + 1
            break
        else:
            index += 1
            if index > 10000000: return None
    res = gdp.iloc[ends]["Quarterly"]
    return res

get_recession_end()


# In[12]:


def get_recession_bottom():
    '''Returns the year and quarter of the recession bottom time as a 
    string value in a format such as 2005q3'''
    start = get_recession_start()
    s_index = gdp[gdp.Quarterly == start].index[0]
    ends = get_recession_end()
    e_index = gdp[gdp.Quarterly == ends].index[0]

    index = s_index
    mins = ""
    while True:
        #print(index,gdp.iloc[index+1].GDP)
        if gdp.iloc[index+1].GDP < gdp.iloc[index].GDP:
            mins = gdp.iloc[index+1].Quarterly
            mins2 = index + 1
        else:
            pass
        index += 1
        if index >= e_index: break

    return mins
get_recession_bottom()


# In[13]:


def convert_housing_data_to_quarters():
    '''Converts the housing data to quarters and returns it as mean 
    values in a dataframe. This dataframe should be a dataframe with
    columns for 2000q1 through 2016q3, and should have a multi-index
    in the shape of ["State","RegionName"].

    Note: Quarters are defined in the assignment description, they are
    not arbitrary three month periods.

    The resulting dataframe should have 67 columns, and 10,730 rows.
    '''
    house = pd.read_csv("City_Zhvi_AllHomes.csv")
    ihouse = house.loc[:,"2000-01":"2016-08"]#提取2000年后纯时间序列进行分析
    ihouse.columns = pd.to_datetime(ihouse.columns).to_period(freq="M")#调整为Period-Month模式显示
    ghouse = ihouse.groupby(ihouse.columns.asfreq("Q"),axis=1).sum()#按照column的Period-Q季度模式进行分组，合并值
    house = (pd.merge(house.loc[:,"RegionID":"SizeRank"],ghouse,left_index=True,right_index=True,how="inner")#合并数据
    .set_index(["State","RegionName"]).iloc[:,4:71])#整理索引排序
    return house
convert_housing_data_to_quarters().size


# In[14]:


from scipy import stats
def run_ttest():
    '''First creates new data showing the decline or growth of housing prices
    between the recession start and the recession bottom. Then runs a ttest
    comparing the university town values to the non-university towns values, 
    return whether the alternative hypothesis (that the two groups are the same)
    is true or not as well as the p-value of the confidence. 

    Return the tuple (different, p, better) where different=True if the t-test is
    True at a p<0.01 (we reject the null hypothesis), or different=False if 
    otherwise (we cannot reject the null hypothesis). The variable p should
    be equal to the exact p value returned from scipy.stats.ttest_ind(). The
    value for better should be either "university town" or "non-university town"
    depending on which has a lower mean price ratio (which is equivilent to a
    reduced market loss).'''
    start = pd.Period(get_recession_start())
    bottom = pd.Period(get_recession_bottom())
    house = convert_housing_data_to_quarters().loc[:,[start,bottom]]
    house.columns = ["Start","Bottom"]
    house["Ratio"] = house.Start / house.Bottom #NAN不用处理，反正数据不使用
    house = house.dropna(axis=0,how="any")
    collage = get_list_of_university_towns().set_index(["State","RegionName"])
    collage["isUnv"] = "Yes"
    res = pd.merge(house,collage,how="left",left_index=True,right_index=True)
    res.isUnv = res.isUnv.fillna("No")

    res_u = res[res.isUnv == "Yes"].Ratio
    res_n = res[res.isUnv == "No"].Ratio
    #print(res_n)
    _,p = stats.ttest_ind(res_u,res_n)
    different = (True if p < 0.01 else False)
    better = ("university town" if np.nanmean(res_u) < np.nanmean(res_n) else "non-university town")
    return different, p, better
run_ttest()


# In[ ]:





# In[ ]:





# In[ ]:




