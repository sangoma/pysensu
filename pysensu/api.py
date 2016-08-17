import json
import logging

import requests
from requests.auth import HTTPBasicAuth
from pysensu import USER_AGENT

logger = logging.getLogger(__name__)


class SensuAPIException(Exception):
    pass


class SensuAPI(object):
    def __init__(self, url_base, username=None, password=None):
        self._url_base = url_base
        self._header = {
            'User-Agent': USER_AGENT
        }
        self.good_status = (200, 201, 202, 204)

        if username and password:
            self.auth = HTTPBasicAuth(username, password)
        else:
            self.auth = None

    def _request(self, method, path, **kwargs):
        url = '{}{}'.format(self._url_base, path)
        logger.debug('{} -> {} with {}'.format(method, url, kwargs))

        if method == 'GET':
            resp = requests.get(url, auth=self.auth, headers=self._header,
                                **kwargs)

        elif method == 'POST':
            resp = requests.post(url, auth=self.auth, headers=self._header,
                                 **kwargs)

        elif method == 'PUT':
            resp = requests.put(url, auth=self.auth, headers=self._header,
                                **kwargs)

        elif method == 'DELETE':
            resp = requests.delete(url, auth=self.auth, headers=self._header,
                                   **kwargs)
        else:
            raise SensuAPIException(
                'Method {} not implemented'.format(method)
            )

        if resp.status_code in self.good_status:
            logger.debug('{}: {}'.format(
                resp.status_code,
                ''.join(resp.text.split('\n'))[0:80]
            ))
            return resp

        else:
            logger.warning('{}: {}'.format(
                resp.status_code,
                resp.text
            ))
            raise SensuAPIException('API bad response')

    """
    Clients ops
    """
    def get_clients(self):
        """
        Returns a list of clients.
        """
        data = self._request('GET', '/clients')
        return data.json()

    def get_client_data(self, client):
        """
        Returns a client.
        """
        data = self._request('GET', '/clients/{}'.format(client))
        return data.json()

    def get_client_history(self, client):
        """
        Returns the history for a client.
        """
        data = self._request('GET', '/clients/{}/history'.format(client))
        return data.json()

    def delete_client(self, client):
        """
        Removes a client, resolving its current events. (delayed action)
        """
        self._request('DELETE', '/clients/{}'.format(client))
        return True

    """
    Events ops
    """
    def get_events(self):
        """
        Returns the list of current events.
        """
        data = self._request('GET', '/events')
        return data.json()

    def get_all_client_events(self, client):
        """
        Returns the list of current events for a given client.
        """
        data = self._request('GET', '/events/{}'.format(client))
        return data.json()

    def get_event(self, client, check):
        """
        Returns an event for a given client & check name.
        """
        data = self._request('GET', '/events/{}/{}'.format(client, check))
        return data.json()

    def delete_event(self, client, check):
        """
        Resolves an event for a given check on a given client. (delayed action)
        """
        self._request('DELETE', '/events/{}/{}'.format(client, check))
        return True

    def post_event(self, client, check):
        """
        Resolves an event. (delayed action)
        """
        self._request('POST', '/resolve',
                      json.dumps({'client': client, 'check': check}))
        return True

    """
    Checks ops
    """
    def get_checks(self):
        """
        Returns the list of checks.
        """
        data = self._request('GET', '/checks')
        return data.json()

    def get_check(self, check):
        """
        Returns a check.
        """
        data = self._request('GET', '/checks/{}'.format(check))
        return data.json()

    def post_check_request(self, check, subscribers):
        """
        Issues a check execution request.
        """
        data = {
            'check': check,
            'subscribers': subscribers
        }
        self._request('POST', '/request', json.dumps(data))
        return True

    """
    Stashes ops
    """
    def get_stashes(self):
        """
        Returns a list of stashes.
        """
        data = self._request('GET', '/stashes')
        return data.json()

    def create_stash(self, payload, path=None):
        """
        Create a stash. (JSON document)
        """
        if path:
            self._request('POST', '/stashes/{}'.format(path),
                          json=payload)
        else:
            self._request('POST', '/stashes', json=payload)
        return True

    def delete_stash(self, path):
        """
        Delete a stash. (JSON document)
        """
        self._request('DELETE', '/stashes/{}'.format(path))
        return True

    """
    Subscriptions ops (non on the API)
    """
    def get_subscriptions(self):
        """
        Returns all the channels where nodes are subscribed
        """
        data = self.get_clients()
        channels = []
        for client in data:
            if 'subscriptions' in client:
                if isinstance(client['subscriptions'], list):
                    for channel in client['subscriptions']:
                        if channel not in channels:
                            channels.append(channel)
                else:
                    if client['subscriptions'] not in channels:
                        channels.append(client['subscriptions'])
        return channels

    def get_subscriptions_channel(self, search_channel):
        """
        Return all the nodes that are subscribed to the specified channel
        """
        data = self.get_clients()
        clients = []
        for client in data:
            if 'subscriptions' in client:
                if isinstance(client['subscriptions'], list):
                    if search_channel in client['subscriptions']:
                        clients.append(client['name'])
                else:
                    if search_channel == client['subscriptions']:
                        clients.append(client['name'])
        return clients
