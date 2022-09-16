# -*- coding: utf-8 -*-
"""
Spyder Editor

This is a temporary script file.
"""

key = 'Du6KAnTlafTRjaYemrazK1jMPiTsnM2Z'
HEADER = {"x-dune-api-key" : key}

import queries as dune

from requests import get, post
import pandas as pd
import json
import time

execution_id = dune.execute_query("783816")
#response = dune.get_query_status(execution_id)
#data = dune.get_query_results(execution_id)


#print(t)

while 1:
    if dune.get_query_status(execution_id).json()['state'] == 'QUERY_STATE_COMPLETED':
        data = dune.get_query_results(execution_id).json()
        break


df = pd.DataFrame(data=data['result']['rows'])




import matplotlib.pyplot as plt

plt.bar(df.iloc[:,0],df.iloc[:,1])
plt.scatter(df.iloc[:,0],df.iloc[:,1])
plt.plot(df.iloc[:,0],df.iloc[:,1])

