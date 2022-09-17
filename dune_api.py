import time

import pandas as pd
import matplotlib.pyplot as plt
import queries as dune




execution_id = dune.execute_query("783816")
# response = dune.get_query_status(execution_id)
# data = dune.get_query_results(execution_id)


# print(t)

while True:
    response = dune.get_query_status(execution_id)
    response_status = response.json()['state']
    print(f'Status: {response_status}')
    if response_status == 'QUERY_STATE_COMPLETED':
        data = dune.get_query_results(execution_id).json()
        break
    time.sleep(1)

df = pd.DataFrame(data=data['result']['rows'])


plt.bar(df.iloc[:, 0], df.iloc[:, 1])
plt.show()
plt.scatter(df.iloc[:, 0], df.iloc[:, 1])
plt.show()
plt.plot(df.iloc[:, 0], df.iloc[:, 1])
plt.show()


