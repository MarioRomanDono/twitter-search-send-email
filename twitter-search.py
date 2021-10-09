import requests
import os
import json
import datetime

# To set your environment variables in your terminal run the following line:
# export 'BEARER_TOKEN'='<your_bearer_token>'
bearer_token = os.environ.get("BEARER_TOKEN")
search_url = "https://api.twitter.com/2/tweets/search/recent"
date = (datetime.datetime.today() - datetime.timedelta(days=1)).strftime('%Y-%m-%dT%H:%M:%SZ')
# Optional params: start_time,end_time,since_id,until_id,max_results,next_token,
# expansions,tweet.fields,media.fields,poll.fields,place.fields,user.fields
query_params = {'query': '(preestreno OR proyeccion) from:ucmccinf','tweet.fields': 'author_id', 'start_time': date}

def bearer_oauth(r):
    """
    Method required by bearer token authentication.
    """

    r.headers["Authorization"] = f"Bearer {bearer_token}"
    r.headers["User-Agent"] = "v2RecentSearchPython"
    return r

def connect_to_endpoint(url, params):
    response = requests.get(url, auth=bearer_oauth, params=params)
    if response.status_code != 200:
        raise Exception(response.status_code, response.text)
    return response.json()


def twitter_search():
    json_response = connect_to_endpoint(search_url, query_params)
    return json.dumps(json_response)

if __name__ == "__main__":
    twitter_search()