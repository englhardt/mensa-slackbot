import os
import re
import slack
from datetime import datetime
from parsers import parse_mri_food, parse_kit_food

MRI_URL = "https://www.casinocatering.de/speiseplan/max-rubner-institut"
KIT_URL = "https://www.sw-ka.de/en/essen/"

def build_answer():
    food_mri = '\n'.join(parse_mri_food(MRI_URL))
    food_kit = '\n'.join(parse_kit_food())

    food = f"\nFood for <!date^{int(datetime.now().timestamp())}" + "^{date_long}|today>\n"
    food += f"*MRI* <{MRI_URL}|(Link)>\n{food_mri if len(food_mri) > 0 else '_closed today_'}\n"
    food += f"*KIT* <{KIT_URL}|(Link)>\n{food_kit if len(food_kit) > 0 else '_closed today_'}\n"
    return food

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
            text=build_answer()
        )

slack_token = os.environ["SLACK_API_TOKEN"]
rtm_client = slack.RTMClient(token=slack_token)
print("Bot running...")
rtm_client.start()
