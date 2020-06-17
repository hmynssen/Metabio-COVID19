import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from scipy.stats import gamma

## Since every State provides its own data
##there was no pattern across files. Futher
##analysis may reexamination on DataFrame.columns
##and other parameters setted at the beginning
##of the code.

rj = False
ce = False
pe = True

if rj:
    name1 = "dt_sintoma"    ##symptoms
    name2 = "dt_obito"      ##death
    file_name = "rj.csv"
    stateName = "RJ"
    data1 = pd.read_csv(file_name, sep = ";", dtype = "str")
elif ce:
    name1 = "DATAINICIOSINTOMAS"    ##symptoms
    name2 = "DATAOBITO"             ##death
    file_name = "casos_coronavirus.xls"
    stateName = "CE"
    data1 = pd.read_excel(file_name)
elif pe:
    name1 = "dt_primeiros_sintomas" ##symptoms
    name2 = "dt_obito"              ##death
    file_name = "PE.csv"
    stateName = "PE"
    data1 = pd.read_csv(file_name, sep = ";")

print(data1.columns)
tdata = data1[[name1,name2]].dropna().reset_index()
print(tdata)

if rj:
    time = pd.to_datetime(tdata[name2],format='%d/%m/%Y').dt.dayofyear - pd.to_datetime(tdata[name1],format='%d/%m/%Y').dt.dayofyear
elif ce:
    time = pd.to_datetime(tdata[name2],format='%Y/%m/%d').dt.dayofyear - pd.to_datetime(tdata[name1],format='%Y/%m/%d').dt.dayofyear
elif pe:
    time = pd.to_datetime(tdata[name2],format='%Y/%m/%d').dt.dayofyear - pd.to_datetime(tdata[name1],format='%Y/%m/%d').dt.dayofyear


num_bins = 100
fig, ax = plt.subplots()
n, bins, patches = ax.hist(time[time >= 0], num_bins, (0,100),density=1, label = stateName + ' data', color = "#003f5c")

# fit gamma distribution
shape, loc, scale = gamma.fit(time[time > 0], floc=0)
x = np.arange(101)
y = gamma.pdf(x, shape, loc, scale)

##Stats info for the state
mean, var, skew, kurt = gamma.stats(shape, loc, scale, moments='mvsk')
print("{}\nmean={}\nstd={}\ncof={}\n".format(stateName, mean, np.sqrt(var), np.sqrt(var)/mean))


gamma_label = "Fitted Gamma Distribution\n(Alpha={:.2f} Beta={:.2f})".format(shape, 1/scale)
ax.plot(bins, y, '--', lw=2, c='#ffa600', label = gamma_label)



# http://www.imperial.ac.uk/mrc-global-infectious-disease-analysis/covid-19/report-13-europe-npi-impact/
##      "infection-to-onset distribution is Gamma distributed with mean
##      5.1 days and coefficient of variation 0.86. The onset-to-death
##      distribution is also Gamma distributed with a mean of 18.8 days
##      and a coefficient of variation 0.45."
meanIC = 18.8
stdIC = (18.8*0.45)

##      The coefficient of variation (CV) of a population is defined as
##      the ratio of the population standard deviation to the population mean.
##
##https://math.stackexchange.com/questions/1810257/gamma-functions-mean-and-standard-deviation-through-shape-and-rate#:~:text=1%20Answer&text=A%20gamma%20distribution%20has%20a,%5D%3D√a%2Fb.

shape2 = (meanIC/stdIC)**2
beta = meanIC/(stdIC**2)
scale2 = 1/beta
yIC = gamma.pdf(x, shape2, scale2)

## Stats info from IC (reference)
mean, var, skew, kurt = gamma.stats(shape2, loc, scale2, moments='mvsk')
print("IC\nmean={}\nstd={}\ncof={}".format(mean, np.sqrt(var), np.sqrt(var)/mean))
ax.plot(bins, yIC, '--', lw=1, c='black', label = 'IC onset-to-death distribution')

ax.set_xlabel('Time (days)')
ax.set_ylabel('Probability Density')
ax.grid("on")
plt.xlim([-0.0001, 80])
legend = ax.legend()
legend.get_frame().set_alpha(1)
fig.tight_layout()
plt.show()
