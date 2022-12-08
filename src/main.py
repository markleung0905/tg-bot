import requests
import feedparser
import time
from dotenv import load_dotenv
import os

load_dotenv()

COUNTRY = os.getenv('COUNTRY_CODE')
# Feed URL
feedURL = f'https://rpilocator.com/feed/?country={COUNTRY}'

# After creating your pushbullet account, create an 
# Access Token and enter it here
BOT_TOKEN = os.getenv('BOT_TOKEN')

# Customize the message title
CHANNEL_ID = os.getenv('CHANNEL_ID')

apiURL = f'https://api.telegram.org/bot{BOT_TOKEN}/sendMessage'

REST_INTERVAL = os.getenv('REST__INTERVAL')

# Send the push/message to all devices connected to Pushbullet
def send_message(message):
    try:
        response = requests.post(apiURL, json=message)
    except Exception as e:
        print(e)


# Create the message body
def formatMessage(entry):
    title = f"{entry.title}\n"
    url = f"{entry.link}\n"
    message = title + url
    res = {'chat_id':CHANNEL_ID, 'disable_web_page_preview':'true', 'text':message}
    return res


# Set control to blank list
control = []

# Fetch the feed
f = feedparser.parse(feedURL)

# If there are entries in the feed, add entry guid to the control variable
if f.entries:
    for entries in f.entries:
        control.append(entries.id)
#Only wait 30 seconds after initial run.
time.sleep(int(REST_INTERVAL))


while True:
    # Fetch the feed again, and again, and again...
    f = feedparser.parse(feedURL)

    # Compare feed entries to control list.
    # If there are new entries, send a message/push
    # and add the new entry to control variable
    for entries in f.entries:
        if entries.id not in control:

            message = formatMessage(entries)

            send_message(message)

            # Add entry guid to the control variable
            control.append(entries.id)

    time.sleep(int(REST_INTERVAL))
