# Copyright 2022 Mario Román Dono

# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at

#     http://www.apache.org/licenses/LICENSE-2.0

# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

import json as js
import requests
import os
import sys

def send_telegram_message(json):
    json_dict = js.loads(json)

    if "data" in json_dict:
        chat_id = os.getenv("CHAT_ID")
        bot_token = os.getenv("BOT_TOKEN")
        username = os.getenv("TWITTER_USERNAME")

        if not chat_id or not bot_token or not username:
            raise SystemExit("You must provide CHAT_ID, BOT_TOKEN and TWITTER_USERNAME env vars")

        for tweet in json_dict["data"]:
            text = ""
            text += tweet["text"] + "\n"
            text += f'Enlace: https://twitter.com/{username}/status/{tweet["id"]}'

            try:
                response = requests.post(f'https://api.telegram.org/bot{bot_token}/sendMessage', json={'chat_id': chat_id, 'text': text, 'parse_mode': 'HTML'})
                response.raise_for_status()
            except requests.exceptions.HTTPError as errh:
                raise SystemExit("HTTP Error: " + str(errh))
            except requests.exceptions.ConnectionError as errc:
                raise SystemExit("Error Connecting: " + str(errc))
            except requests.exceptions.Timeout as errt:
                raise SystemExit("Timeout Error: " + str(errt))
            except requests.exceptions.RequestException as err:
                raise SystemExit("Oops: Something else:" + str(err))
    else:
        print("No hay tweets que enviar")

if __name__ == "__main__":
    if len(sys.argv) != 2:
        raise SystemExit(f'Usage: {sys.argv[0]} <JSON_Object>')

    send_telegram_message(sys.argv[1])