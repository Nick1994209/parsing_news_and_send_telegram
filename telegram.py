import requests
import json


class Bot(object):

    def __init__(self, token):
        self.token = token
        self.url = 'https://api.telegram.org/bot' + token

    def get_me(self):
        url_get_me = self.url + '/getMe'
        response = requests.get(url_get_me)
        return response.json()

    def get_updates(self):
        url_updates = self.url + '/getUpdates'
        response = requests.get(url_updates)
        return response.json()

    def get_new_messages(self, last_message_id=None):
        if last_message_id:
            self.last_message_id = last_message_id
        elif not hasattr(self, 'last_message_id'):
            self.last_message_id = 0

        updates = self.get_updates()
        messages = updates['result']
        new_messages = [message['message'] for message in messages
                        if message['message']['message_id'] > self.last_message_id]
        if new_messages:
            self.last_message_id = new_messages[-1]['message_id']
        return new_messages

    def send_message(self, chat_id, text):
        send_url = self.url + '/sendMessage'
        data = {'chat_id': chat_id, 'text': text}
        requests.post(send_url, data=data)
