import pandas as pd
import math
from Variables import *
df = pd.read_excel(ListPath)
TotalTypes= []
RecordTypesStr=list(df)
for idx in RecordTypesStr:
    DetailedTypes=df[idx].astype(str).values.tolist()
    temp = [x for x in DetailedTypes if x != 'nan'] #Removes nans
    if idx == "Unknown":
        temp.append("nan")
    TotalTypes.append(temp)
print (TotalTypes)