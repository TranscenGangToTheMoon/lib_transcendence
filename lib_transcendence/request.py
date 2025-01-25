import json
from typing import Literal

from lib_transcendence.utils import datetime_serializer
from lib_transcendence.exceptions import Conflict, ServiceUnavailable, Throttled
from rest_framework.exceptions import AuthenticationFailed, PermissionDenied, MethodNotAllowed, NotFound, ParseError
import requests


def request_service(service: Literal['localhost', 'auth', 'chat', 'game', 'matchmaking', 'users'], endpoint: str, method: Literal['GET', 'POST', 'PUT', 'PATCH', 'DELETE'] | str, data=None, token=None, port=8000):
    if data is not None:
        data = json.dumps(data, default=datetime_serializer)

    headers = {'Content-Type': 'application/json'}
    if token is not None:
        headers['Authorization'] = token

    url_protocol = 'http'
    if port == 4443:
        url_protocol += 's'
    try:
        print(method, f'[{service}] => /{endpoint}' + ('' if data is None else f' - {data}'), flush=True)
        response = requests.request(
            method=method,
            url=f'{url_protocol}://{service}:{port}/{endpoint}',
            headers=headers,
            data=data
        )

        if response.status_code == 204:
            print('', flush=True)
            return

        json_data = response.json()
        print(f'JSON[{response.status_code}] =', json_data, end='\n\n', flush=True)
        if response.status_code == 400:
            raise ParseError(json_data)
        if response.status_code == 401:
            raise AuthenticationFailed(json_data)
        if response.status_code == 403:
            raise PermissionDenied(json_data)
        if response.status_code == 404:
            raise NotFound(json_data)
        if response.status_code == 405:
            raise MethodNotAllowed(method)
        if response.status_code == 409:
            raise Conflict(json_data)
        if response.status_code == 409:
            raise Throttled()
        if response.status_code == 503:
            raise ServiceUnavailable(service)
    except (requests.ConnectionError, requests.exceptions.JSONDecodeError):
        raise ServiceUnavailable(service)
    return json_data
