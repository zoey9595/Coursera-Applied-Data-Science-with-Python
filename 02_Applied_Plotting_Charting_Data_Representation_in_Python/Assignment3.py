
# coding: utf-8

# # Assignment 3 - Building a Custom Visualization
# 
# ---
# 
# In this assignment you must choose one of the options presented below and submit a visual as well as your source code for peer grading. The details of how you solve the assignment are up to you, although your assignment must use matplotlib so that your peers can evaluate your work. The options differ in challenge level, but there are no grades associated with the challenge level you chose. However, your peers will be asked to ensure you at least met a minimum quality for a given technique in order to pass. Implement the technique fully (or exceed it!) and you should be able to earn full grades for the assignment.
# 
# 
# &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;Ferreira, N., Fisher, D., & Konig, A. C. (2014, April). [Sample-oriented task-driven visualizations: allowing users to make better, more confident decisions.](https://www.microsoft.com/en-us/research/wp-content/uploads/2016/02/Ferreira_Fisher_Sample_Oriented_Tasks.pdf) 
# &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;In Proceedings of the SIGCHI Conference on Human Factors in Computing Systems (pp. 571-580). ACM. ([video](https://www.youtube.com/watch?v=BI7GAs-va-Q))
# 
# 
# In this [paper](https://www.microsoft.com/en-us/research/wp-content/uploads/2016/02/Ferreira_Fisher_Sample_Oriented_Tasks.pdf) the authors describe the challenges users face when trying to make judgements about probabilistic data generated through samples. As an example, they look at a bar chart of four years of data (replicated below in Figure 1). Each year has a y-axis value, which is derived from a sample of a larger dataset. For instance, the first value might be the number votes in a given district or riding for 1992, with the average being around 33,000. On top of this is plotted the 95% confidence interval for the mean (see the boxplot lectures for more information, and the yerr parameter of barcharts).
# 
# <br>
# <img src="readonly/Assignment3Fig1.png" alt="Figure 1" style="width: 400px;"/>
# <h4 style="text-align: center;" markdown="1">  &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;Figure 1 from (Ferreira et al, 2014).</h4>
# 
# <br>
# 
# A challenge that users face is that, for a given y-axis value (e.g. 42,000), it is difficult to know which x-axis values are most likely to be representative, because the confidence levels overlap and their distributions are different (the lengths of the confidence interval bars are unequal). One of the solutions the authors propose for this problem (Figure 2c) is to allow users to indicate the y-axis value of interest (e.g. 42,000) and then draw a horizontal line and color bars based on this value. So bars might be colored red if they are definitely above this value (given the confidence interval), blue if they are definitely below this value, or white if they contain this value.
# 
# 
# <br>
# <img src="readonly/Assignment3Fig2c.png" alt="Figure 1" style="width: 400px;"/>
# <h4 style="text-align: center;" markdown="1">  Figure 2c from (Ferreira et al. 2014). Note that the colorbar legend at the bottom as well as the arrows are not required in the assignment descriptions below.</h4>
# 
# <br>
# <br>
# 
# **Easiest option:** Implement the bar coloring as described above - a color scale with only three colors, (e.g. blue, white, and red). Assume the user provides the y axis value of interest as a parameter or variable.
# 
# 
# **Harder option:** Implement the bar coloring as described in the paper, where the color of the bar is actually based on the amount of data covered (e.g. a gradient ranging from dark blue for the distribution being certainly below this y-axis, to white if the value is certainly contained, to dark red if the value is certainly not contained as the distribution is above the axis).
# 
# **Even Harder option:** Add interactivity to the above, which allows the user to click on the y axis to set the value of interest. The bar colors should change with respect to what value the user has selected.
# 
# **Hardest option:** Allow the user to interactively set a range of y values they are interested in, and recolor based on this (e.g. a y-axis band, see the paper for more details).
# 
# ---
# 
# *Note: The data given for this assignment is not the same as the data used in the article and as a result the visualizations may look a little different.*

# In[4]:

# Use the following data for this assignment:
import pandas as pd
import numpy as np

np.random.seed(12345)

df = pd.DataFrame([np.random.normal(32000,200000,3650), 
                   np.random.normal(43000,100000,3650), 
                   np.random.normal(43500,140000,3650), 
                   np.random.normal(48000,70000,3650)], 
                  index=[1992,1993,1994,1995])
df = df.T
dfd = df.describe()
dfdt = dfd.T
# 添加95%的标准误差值为yerr
dfdt['yerr'] = 1.96 * dfdt['std'] / np.sqrt(dfdt['count'])
dfd = dfdt.T
dfd


# In[2]:

get_ipython().magic('matplotlib notebook')

import matplotlib.pyplot as plt

plt.figure()
bx = plt.boxplot([df[1992], df[1993], df[1994], df[1995]], whis='range')


# In[5]:

import numpy as np
import pandas as pd 
import matplotlib.pyplot as plt
import mpl_toolkits.axes_grid1.inset_locator as mpl_il

get_ipython().magic('matplotlib notebook')

# 1.绘制中值和error bar的柱状图
meanvalue = dfd.loc['mean']
xvalue = list(dfd)
yvalue = list(meanvalue)
yerrvalue = list(dfd.loc['yerr'])

newxvalue = np.arange(len(xvalue))/2

plt.figure()
basic = plt.bar(newxvalue, yvalue, yerr=yerrvalue, color=['blue','white','white','red'], width=0.5, edgecolor='black')
_ = plt.xticks(newxvalue,xvalue)

# 2.把图的右侧空出一个柱的距离
x1, x2 = plt.xlim()
plt.xlim(x1, x2 + .8)
bars = basic.get_children()
for b in bars:
    b.set_color((0.1, 0.2, 0.5, 0.3))
    

# 3.手动设置一条线
y1=41000
x1, x2 = plt.xlim()
line, = plt.plot([x1,x2],[y1,y1],'k-', color=(0,0,1,.5), lw=1,label="_not in legend")

# 4.定义一个判断颜色变化的函数
def change_color(event):
    plt.gca().set_title('You select Y={} to Compare Different Distributions'.format(event.ydata))
    line.set_ydata([event.ydata,event.ydata])
    y = event.ydata
    for b,meanv,yerror in zip(bars,yvalue,yerrvalue):
        bluev = 0
        redv = 0
        alpha = 1
        if y > meanv:
            bluev = 1
            alpha = min(1, (y-meanv)/yerror)
        if y < meanv:
            redv = 1
            alpha = min(1, (meanv-y)/yerror)
        b.set_color((redv,0,bluev,alpha))
        b.set_edgecolor('black')
        
plt.gcf().canvas.mpl_connect('button_press_event', change_color)    


# In[ ]:

from matplotlib import pyplot as plt

class LineBuilder:
    def __init__(self, line):
        self.line = line
        self.xs = list(line.get_xdata())
        self.ys = list(line.get_ydata())
        self.cid = line.figure.canvas.mpl_connect('button_press_event', self)

    def __call__(self, event):
        print('click', event)
        if event.inaxes!=self.line.axes: return
        self.xs.append(event.xdata)
        self.ys.append(event.ydata)
        self.line.set_data(self.xs, self.ys)
        self.line.figure.canvas.draw()

fig = plt.figure()
ax = fig.add_subplot(111)
ax.set_title('click to build line segments')
line, = ax.plot([0], [0])  # empty line
linebuilder = LineBuilder(line)

plt.show()

