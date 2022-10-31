import requests
import feedparser
import time


# Feed URL
FEED_URL = 'https://rpilocator.com/feed/'
# FEED_URL = 'https://hwlocator.com/feed/'

# After creating your pushbullet account, create an 
# Access Token and enter it here
BOT_TOKEN = '5719038324:AAECKDgUduFUyd-fww1nxHNi6rS7TyN2aFo'

# Customize the message title
CHANNEL_ID = '5057299340'

apiURL = f'https://api.telegram.org/bot{BOT_TOKEN}/sendMessage'

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

    res = {'chat_id':CHANNEL_ID, 'text':message}

    return res


# Set control to blank list
control = []

# Fetch the feed
f = feedparser.parse(FEED_URL)

# If there are entries in the feed, add entry guid to the control variable
if f.entries:
    for entries in f.entries:
        control.append(entries.id)
#Only wait 30 seconds after initial run.
time.sleep(30)

while True:
    # Fetch the feed again, and again, and again...
    f = feedparser.parse(FEED_URL)

    # Compare feed entries to control list.
    # If there are new entries, send a message/push
    # and add the new entry to control variable
    for entries in f.entries:
        if entries.id not in control:

            message = formatMessage(entries)

            send_message(message)

            # Add entry guid to the control variable
            control.append(entries.id)

    time.sleep(59)
    