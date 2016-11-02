import pickle
import os
import json
from unittest.mock import Mock

# ABSPATH = os.path.dirname(__file__)
# PATH = '\\response\\'

# __all__ = ['get', 'export']


def side_effect_get(*args, **kwargs):
    url = args[0]
    headers = kwargs.get('headers')

    d = load_map('GET')
    for key, val in d.items():
        if url == val[0] or val[1] in url:
            return load_file(key)


def load_file(path):
    with open(path, 'rb') as fileobj:
        return pickle.load(fileobj)

get = Mock(side_effect=side_effect_get)


def dump(request):
    method = request.request.method

    i = 1
    while os.path.exists('response/%s/response%s.p' % (method, i)):
        i += 1
    filename = 'response%s.p' % i
    with open('response/%s/%s' % (method, filename), 'wb') as fileobj:
        pickle.dump(request, fileobj)
    return filename


def load_map(method):

    try:
        with open('response/%s/map.json' % method, 'r') as fileobj:
            d = json.load(fileobj)
    except FileNotFoundError:
        d = {}
    return d


def save_map(d, method):
    if not d:
        d = {}
    with open('response/%s/map.json' % method, 'w') as fileobj:
        json.dump(d, fileobj)


def export(request, regex=None, strict=False):
    url = request.request.url
    headers = request.request.headers
    method = request.request.method

    filename = dump(request)

    d = load_map(method)
    d[filename] = [url, regex, strict]
    save_map(d, method)
