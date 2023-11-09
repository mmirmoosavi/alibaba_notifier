import json
import time
import os
import requests
import random

class TelegramBot:
    def __init__(self):
        self.bot_token = os.environ.get('BOT_TOKEN')
        self.channel_chat_id = os.environ.get('CHANNEL_CHAT_ID')

        if not self.bot_token or not self.channel_chat_id:
            raise Exception('you should specify you bot token and also channel chat id')

    def send_message(self, text):
        url = f'https://api.telegram.org/bot{self.bot_token}/sendMessage?chat_id={self.channel_chat_id}&text={text}'
        response = requests.get(url, timeout=10)
        return response


class AliBabaNotifier:

    def __init__(self, random_number:int):
        # Define the POST request data for details of flight
        self.post_data = {
            "infant": 0,
            "child": 0,
            "adult": 1,
            "departureDate": os.environ.get("DEPARTURE_DATE", "2023-12-10"),
            "origin": "ISTALL",
            "destination": "IKA",
            "flightClass": "economy",
            "userVariant": "pricing-ist-v1-decrease"
        }

        # Define the POST request headers
        self.headers = {
            'User-Agent': 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:109.0) Gecko/20100101 Firefox/119.0',
            'Accept': 'application/json, text/plain, */*',
            'Accept-Language': 'en-US,en;q=0.5',
            'Accept-Encoding': 'gzip, deflate, br',
            'Content-Type': 'application/json',
            'ab-channel': 'WEB-NEW,PRODUCTION,CSR,www.alibaba.ir,N,Firefox,119.0,N,N,Ubuntu',
            'tracing-sessionid': f'1699{random_number}',
            'tracing-device': 'N,Firefox,119.0,N,N,Ubuntu',
            'Origin': 'https://www.alibaba.ir',
            'Connection': 'keep-alive',
            'Referer': 'https://www.alibaba.ir/',
            'Sec-Fetch-Dest': 'empty',
            'Sec-Fetch-Mode': 'cors',
            'Sec-Fetch-Site': 'same-site'
        }

        self.post_url = 'https://ws.alibaba.ir/api/v1/flights/international/proposal-requests'

    def get_cheapest_data(self):
        cheapest_data = {}
        post_response = requests.post(self.post_url, json=self.post_data, headers=self.headers, timeout=10)
        if post_response.status_code == 200:

            post_data = post_response.json()
            request_id = post_data.get('result', {}).get('requestId')
            if request_id:
                # Build the URL for the GET request
                # Send the GET request
                self.get_url = f'https://ws.alibaba.ir/api/v1/flights/international/proposal-requests/{request_id}'

                get_response = requests.get(self.get_url, headers=self.headers, timeout=10)

                if get_response.status_code == 200:
                    get_data = get_response.json()
                    # Extract and print the desired information from the GET response
                    results = get_data.get('result', {})
                    proposals = results.get('proposals', [])
                    if proposals:
                        first_proposal = proposals[0]

                        arrivalDateTime = first_proposal['leavingFlightGroup']["arrivalDateTime"]
                        departureDateTime = first_proposal['leavingFlightGroup']["departureDateTime"]
                        total_price = first_proposal.get('total')
                        if total_price and arrivalDateTime and departureDateTime:
                            cheapest_data["arrivalDateTime"] = arrivalDateTime
                            cheapest_data["departureDateTime"] = departureDateTime
                            cheapest_data["total_price"] = total_price
                            cheapest_data.update(self.post_data)
                            print(f"Total: {total_price}")
                        else:
                            print("The 'total' cannot get data correctly")
                    else:
                        print("No proposals found in the GET response.")
                else:
                    print(f"Failed to retrieve data from the GET request. Status code: {get_response.status_code}")
            else:
                print("Request ID not found in the POST response.")
        else:
            print(f"Failed to retrieve data from the POST request. Status code: {post_response.status_code}")

        return cheapest_data

    def send_total_data_telegram_channel(self, telegram_bot_object: TelegramBot, data: dict, threshold: float):

        total = data.get('total_price')
        if total is not None:

            # Check if the 'total' is less than or equal to 35,000,000
            if float(total) <= threshold:
                # Initialize the Telegram Bot
                telegram_instance = telegram_bot_object
                response = telegram_instance.send_message(json.dumps(data, indent=4))
                print(response.status_code)
        else:
            print("The 'total' field is not present in the first proposal.")


if __name__ == '__main__':

    telegram_bot_object = TelegramBot()
    while True:
        random_number = random.randint(10 ** 8, (10 ** 9) - 1)
        alibaba_notifier = AliBabaNotifier(random_number)

        cheapest_data = alibaba_notifier.get_cheapest_data()
        alibaba_notifier.send_total_data_telegram_channel(telegram_bot_object,
                                                          cheapest_data,
                                                          float(os.environ.get("PRICE_THRESHOLD", 35000000))
                                                          )
        time.sleep(5 * 60)
