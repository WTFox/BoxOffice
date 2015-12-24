import json
import requests
from requests.auth import HTTPBasicAuth

__author__ = 'afox'


class PushBullet(object):
    def __init__(self, apiKey):
        self.apiKey = apiKey
        self.HOST = "https://api.pushbullet.com/v2"

    def _request(self, method, url, postdata=None, params=None, files=None):
        headers = {"Accept": "application/json",
                   "Content-Type": "application/json",
                   "User-Agent": "pyPushBullet"}

        if postdata:
            postdata = json.dumps(postdata)

        r = requests.request(method,
                             url,
                             data=postdata,
                             params=params,
                             headers=headers,
                             files=files,
                             auth=HTTPBasicAuth(self.apiKey, ""))

        r.raise_for_status()
        return r.json()

    def pushNote(self, title, body, recipient='', recipient_type="device_iden"):
        """ Push a note
            https://docs.pushbullet.com/v2/pushes
            Arguments:
            title -- a title for the note
            body -- the body of the note
            recipient -- a recipient
            recipient_type -- a type of recipient (device, email, channel or client)
        """
        data = dict(
            type="note",
            title=title,
            body=body
        )

        data[recipient_type] = recipient

        return self._request("POST", self.HOST + "/pushes", data)

