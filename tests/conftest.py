# -*- coding: utf-8 -*-

import json
import os
from urllib.parse import urlunparse
from urllib.request import Request, urlopen

import pytest
import yaml

COMMON_YAML = os.path.join(os.path.dirname(__file__),
                           'common.yaml')
AUTHENTICATION_YAML = os.path.join(os.path.dirname(__file__),
                                   'components',
                                   'authentication.yaml')

with open(COMMON_YAML, 'r') as file:
    config = yaml.safe_load(file)['variables']['service']
    PROTOCOL = config['protocol']
    HOST = config['host']
    PORT = config['port']

with open(AUTHENTICATION_YAML, 'r') as file:
    config = yaml.safe_load(file)['variables']
    USER = config['user']


@pytest.fixture(scope='session', autouse=True, name='access_token')
def get_access_token() -> str:
    ''' create API credential with operator
    '''

    url = urlunparse((PROTOCOL,
                      f'{HOST}:{PORT}',
                      '/login',
                      None, None, None))
    # HTTP request headers
    headers = { 'Content-Type': 'application/json' }
    req = Request(url=url, data=json.dumps(USER).encode(), headers=headers)
    with urlopen(req) as res:
        body = json.loads(res.read().decode())
    return body['token']
