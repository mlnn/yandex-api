from pprint import pprint
from urllib.parse import urljoin
import requests

TOKEN = ''


class YMManagment:
    management_url = 'https://api-metrika.yandex.ru/'

    def __init__(self, token):
        self.token = token

    def get_headers(self):
        headers = {
            'Authorization': 'OAuth {}'.format(self.token)
        }
        return headers

    def get_counters(self):
        url = urljoin(self.management_url, 'management/v1/counters')
        headers = self.get_headers()
        response = requests.get(url, headers=headers)
        return [c['id'] for c in response.json()['counters']]

    def get_counter_info(self, counter_id):
        url = urljoin(self.management_url, 'management/v1/counter/{}'.format(counter_id))
        headers = self.get_headers()
        response = requests.get(url, headers=headers)
        return response.json()


class Counter(YMManagment):
    def get_url(self, counter_id):
        url = urljoin(super().management_url, 'stat/v1/data'.format(counter_id))
        return url

    def get_visits(self, counter_id, token):
        url = self.get_url(counter_id)
        params = {
            'id': counter_id,
            'metrics': 'ym:s:visits',
            'oauth_token': token
        }
        response = requests.get(url, params)
        return [c['metrics'] for c in response.json()['data']]

    def get_pageviews(self, counter_id, token):
        url = self.get_url(counter_id)
        params = {
            'id': counter_id,
            'metrics': 'ym:s:pageviews',
            'oauth_token': token
        }
        response = requests.get(url, params)
        return [c['metrics'] for c in response.json()['data']]

    def get_users(self, counter_id, token):
        url = self.get_url(counter_id)
        params = {
            'id': counter_id,
            'metrics': 'ym:s:users',
            'oauth_token': token
        }
        response = requests.get(url, params)
        return [c['metrics'] for c in response.json()['data']]

account = Counter(TOKEN)
counters = account.get_counters()
pprint(counters)
for counter in counters:
    counter_visits = account.get_visits(counter, TOKEN)
    counter_pageviews = account.get_pageviews(counter, TOKEN)
    counter_users = account.get_users(counter, TOKEN)
    pprint(counter_visits)
    pprint(counter_pageviews)
    pprint(counter_users)
