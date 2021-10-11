# Copyright 2021 Mario Román Dono
# Copyright 2020 @TwitterDev

# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at

#     http://www.apache.org/licenses/LICENSE-2.0

# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

import requests
import os
import json
import datetime

# To set your environment variables in your terminal run the following line:
# export 'BEARER_TOKEN'='<your_bearer_token>'
bearer_token = os.getenv("BEARER_TOKEN")
n_days = int(os.getenv("DAYS"))
query = os.getenv("QUERY")

search_url = "https://api.twitter.com/2/tweets/search/recent"
date = (datetime.datetime.today() - datetime.timedelta(days=n_days)).strftime('%Y-%m-%dT%H:%M:%SZ')

# Optional params: start_time,end_time,since_id,until_id,max_results,next_token,
# expansions,tweet.fields,media.fields,poll.fields,place.fields,user.fields
query_params = {'query': query, 'start_time': date}

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