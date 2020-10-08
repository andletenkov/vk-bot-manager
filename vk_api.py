import requests
from loguru import logger


class VK(object):

    def __init__(self, token, url="https://api.vk.com/", ver="5.130"):
        self._path = []
        self._api_url = url if url.endswith("/") else url + "/"
        self._ver = ver
        self._token = token

    def __getattr__(self, item):
        if not item.startswith('__') and not item.endswith('__'):
            self._path.append(item)
        return self

    def __call__(self, *args, **kwargs):
        if args:
            raise ValueError("method accepts only keyword arguments")

        path = self._api_url + "method/" + ".".join(self._path)
        payload = kwargs.copy()

        payload.update({
            "v": self._ver,
            "access_token": self._token
        })

        payload = '&'.join([f'{k}={v}' for k, v in payload.items()])
        logger.debug(f'Request -- URL: {path}, Payload: {payload}')

        try:
            resp = requests.post(f"{path}?{payload}").json()
            logger.debug(f'Response -- {resp}')
        finally:
            self._path.clear()
        return resp
