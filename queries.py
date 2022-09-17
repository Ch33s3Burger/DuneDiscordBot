import time
import pandas as pd
from requests import get, post

key = 'Du6KAnTlafTRjaYemrazK1jMPiTsnM2Z'
HEADER = {"x-dune-api-key": key}

BASE_URL = "https://api.dune.com/api/v1/"


def make_api_url(module, action, ID):
    """
    We shall use this function to generate a URL to call the API.
    """

    url = BASE_URL + module + "/" + ID + "/" + action

    return url


def execute_query(query_id):
    """
    Takes in the query ID.
    Calls the API to execute the query.
    Returns the execution ID of the instance which is executing the query.
    """

    url = make_api_url("query", "execute", query_id)
    response = post(url, headers=HEADER)
    execution_id = response.json()['execution_id']

    return execution_id


def get_query_status(execution_id):
    """
    Takes in an execution ID.
    Fetches the status of query execution using the API
    Returns the status response object
    """

    url = make_api_url("execution", "status", execution_id)
    response = get(url, headers=HEADER)

    return response


def get_query_results(execution_id):
    """
    Takes in an execution ID.
    Fetches the results returned from the query using the API
    Returns the results response object
    """

    url = make_api_url("execution", "results", execution_id)
    response = get(url, headers=HEADER)

    return response


def cancel_query_execution(execution_id):
    """
    Takes in an execution ID.
    Cancels the ongoing execution of the query.
    Returns the response object.
    """

    url = make_api_url("execution", "cancel", execution_id)
    response = get(url, headers=HEADER)

    return response


def get_query_content(query_id):
    execution_id = execute_query(query_id)
    # response = dune.get_query_status(execution_id)
    # data = dune.get_query_results(execution_id)

    # print(t)

    while True:
        response = get_query_status(execution_id)
        response_status = response.json()['state']
        print(f'Status: {response_status}')
        if response_status == 'QUERY_STATE_COMPLETED':
            data = get_query_results(execution_id).json()
            break
        elif response_status == 'QUERY_STATE_FAILED':
            return None
        time.sleep(1)

    return pd.DataFrame(data=data['result']['rows'])