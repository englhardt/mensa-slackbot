import os
import re
import slack
from datetime import datetime
from parsers import build_food_message

@slack.RTMClient.run_on(event='message')
def get_food(**payload):
    data = payload['data']
    web_client = payload['web_client']
    rtm_client = payload['rtm_client']
    if 'text' in data and '!food' in data['text']:
        channel_id = data['channel']
        thread_ts = data['ts']
        user = data['user']

        web_client.chat_postMessage(
            channel=channel_id,
            text=build_food_message()
        )

slack_token = os.environ["SLACK_API_TOKEN"]
rtm_client = slack.RTMClient(token=slack_token)
print("Bot running...")
rtm_client.start()
