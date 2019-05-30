#!/usr/bin/env python

import requests
from pprint import pprint
import json
from urllib.parse import urljoin
from useful_utilities import *

URL = "http://localhost:9292"
API_KEY = "8302ca56136b04e4b2b82bc03ca4d4346cb5dc3dad6e3881138b9c232d7d4b94"
API_USERNAME = "coolsidd"

def parse_response(response):
    try:
        pprint(json.loads(response.content))
    except:
        print(response.content)
    if(response.ok):
        print("Success!")
    elif response.status_code == 403:
        print("Access denied")
    elif response.status_code == 400:
        print("Missing Param/Invalid Request")
    else:
        print("Unknown Response")
        print(response.status_code)
    return response

def get_request(data, url,files={},params={},json={},timeout=None, allow_redirects=False, **kwargs):
    params.setdefault("api_key" , API_KEY)
    params.setdefault("api_username", API_USERNAME)
    headers = {"Accept": "application/json; charset=utf-8"}
    # data.update(args)
    # data.setdefault("Api-Key" , API_KEY)
    # data.setdefault("Api-Username", API_USERNAME)
    # response = requests.get(url, data=data_as_str)
    response = requests.request("GET", url, json=json, data=data, headers = headers, files=files, params=params,timeout=timeout,allow_redirects=allow_redirects,**kwargs)
    return parse_response(response)

def post_request(data, url, files = {},params={}, json={},timeout=None, allow_redirects=False, **kwargs): 
    params.setdefault("api_key" , API_KEY)
    params.setdefault("api_username", API_USERNAME)
    headers = {"Accept": "application/json; charset=utf-8"}
    # headers = {
    #     # "Accept": "application/json; charset=utf-8",
    #     "Content-Type":"multipart/form-data",
    #     "Api-Key": API_KEY,
    #     "Api-Username": API_USERNAME
    # }
    response = requests.request("POST", url, json=json, data=data, headers = headers, files=files, params=params,timeout=timeout,allow_redirects=allow_redirects,**kwargs)
    return parse_response(response)
