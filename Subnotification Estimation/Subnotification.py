import numpy as np
import pands as pd
import Data

## The program focus on estimating the amount of subnotification that is
##not being reported in Brazil. To do that, a statistical analysis was
##developed. The article that explains the math behind can be read at
## [ref].
## However, any model will be only as good as the data that is put into it.
##With that in mind and considering the on going political conflict between
##states and federation in Brazil, a more careful atention is needed when
##when extracting info from files.
## A history of the data collected is avaiable at the repository to eye check
##but also, the code raises errors when there is a time series discrepancy
##between the tmp stored files and the new data file.

file_name = "" ##name of or path to file

with open(file_name, "r") as file:
    if ".xsv" in file_name:
        data = pd.read_excel(file)
    elif ".csv" in file_name:
        data = pd.read_csv(file)

data = Data.control.parse(data)
