import json
import requests
import configparser as cfg

class telegram_chatbot():

    #Constructor method
    def __init__(self, config):
        self.token = self.read_token_from_config_file(config)
        self.base = "https://api.telegram.org/bot{}/".format(self.token)

    #Get updates
    def get_updates(self, offset = None):
        url = self.base + 'getUpdates?timeout=100'
        if offset:
            url = url + '&offset={}'.format(offset + 1)
        r = requests.get(url)
        return json.loads(r.content)

    #Send message
    def send_message(self, msg, chat_id):
        url = self.base + 'sendMessage?chat_id={}&text={}&parsemode=markdown'.format(chat_id, msg)
        if msg is not None:
            requests.get(url)


    def read_token_from_config_file(self, config):
        parser = cfg.ConfigParser()
        parser.read(config)
        return parser.get('creds', 'token')

