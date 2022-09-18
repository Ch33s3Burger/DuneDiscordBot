import os
import time
import asyncio
import functools
import typing

import pandas as pd
from requests import get, post

DUNE_TOKEN = os.getenv('DUNE_TOKEN')
if DUNE_TOKEN is None:
    raise EnvironmentError('Set Environment variable: DUNE_TOKEN')
HEADER = {"x-dune-api-key": DUNE_TOKEN}

BASE_URL = "https://api.dune.com/api/v1/"


def to_thread(func: typing.Callable) -> typing.Coroutine:
    @functools.wraps(func)
    async def wrapper(*args, **kwargs):
        return await asyncio.to_thread(func, *args, **kwargs)

    return wrapper


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

@to_thread
def get_query_content(query_id):
    execution_id = execute_query(query_id)
    while True:
        response = get_query_status(execution_id)
        response_status = response.json()['state']
        print(f'Status: {response_status}')
        if response_status == 'QUERY_STATE_COMPLETED':
            data = get_query_results(execution_id).json()
            break
        elif response_status == 'QUERY_STATE_EXECUTING':
            time.sleep(1)
        else:
            return None

    return pd.DataFrame(data=data['result']['rows'])
