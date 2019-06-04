#!/usr/bin/env python

import requests
import datetime
from pprint import pprint
import json
from urllib.parse import urljoin
from useful_utilities import *

URL = "http://localhost:9292"
API_KEY = "8302ca56136b04e4b2b82bc03ca4d4346cb5dc3dad6e3881138b9c232d7d4b94"
API_USERNAME = "coolsidd"
TEST_MODE = False

# _requst_copy = _request
# # TODO
# def enable_test_mode():
#     _request_copy = _request
#     _request = debug_func(_request)
#     TEST_MODE = True


# def disable_test_mode():
#     _request = _requst_copy
#     TEST_MODE = False


def _request(
    _type, url, json, data, headers, files, params, timeout, allow_redirects, **kwargs
):
    return requests.request(
        _type,
        url,
        json=json,
        data=data,
        headers=headers,
        files=files,
        params=params,
        timeout=timeout,
        allow_redirects=allow_redirects,
        **kwargs
    )


def parse_response(response):
    try:
        pprint(json.loads(response.content))
    except:
        pass
    if response.ok:
        print("Success!")
    elif response.status_code == 403:
        print("Access denied")
    elif response.status_code == 400:
        print("Missing Param/Invalid Request")
    else:
        print("Unknown Response")
        print(response.status_code)
    return response


def get_request(
    data,
    url,
    files={},
    params={},
    json={},
    timeout=None,
    allow_redirects=False,
    **kwargs
):
    params.setdefault("api_key", API_KEY)
    params.setdefault("api_username", API_USERNAME)
    headers = {"Accept": "application/json; charset=utf-8"}
    response = _request(
        "GET",
        url,
        json=json,
        data=data,
        headers=headers,
        files=files,
        params=params,
        timeout=timeout,
        allow_redirects=allow_redirects,
        **kwargs
    )
    return parse_response(response)


def put_request(
    data,
    url,
    files={},
    params={},
    json={},
    timeout=None,
    allow_redirects=False,
    **kwargs
):
    params.setdefault("api_key", API_KEY)
    params.setdefault("api_username", API_USERNAME)
    headers = {"Accept": "application/json; charset=utf-8"}
    response = _request(
        "PUT",
        url,
        json=json,
        data=data,
        headers=headers,
        files=files,
        params=params,
        timeout=timeout,
        allow_redirects=allow_redirects,
        **kwargs
    )
    return parse_response(response)


def post_request(
    data,
    url,
    files={},
    params={},
    json={},
    timeout=None,
    allow_redirects=False,
    **kwargs
):
    params.setdefault("api_key", API_KEY)
    params.setdefault("api_username", API_USERNAME)
    headers = {"Accept": "application/json; charset=utf-8"}
    # headers = {
    #     # "Accept": "application/json; charset=utf-8",
    #     "Content-Type":"multipart/form-data",
    #     "Api-Key": API_KEY,
    #     "Api-Username": API_USERNAME
    # }
    response = _request(
        "POST",
        url,
        json=json,
        data=data,
        headers=headers,
        files=files,
        params=params,
        timeout=timeout,
        allow_redirects=allow_redirects,
        **kwargs
    )
    return parse_response(response)


def get_categories():
    end_point = "/categories.json"
    url_with_end_point = urljoin(URL, end_point)
    data = dict()
    return get_request(data, url_with_end_point)


def create_category(name, color, text_color):
    end_point = "/categories.json"
    url_with_end_point = urljoin(URL, end_point)
    data = {"name": name, "color": color, "text_color": text_color}
    return post_request(data, url_with_end_point)


def create_user(
    name, email, password, username, active=True, approved=True, user_fields=""
):
    end_point = "/users"
    url_with_end_point = urljoin(URL, end_point)
    data = locals()
    return post_request(data, url_with_end_point)


def upload_image_or_avatar(_type, userid=None, synchronous=False, image=None):
    assert type(userid) == int
    assert _type in {
        "avatar",
        "profile_background",
        "card_background",
        "custom_emoji",
        "composer",
    }
    end_point = "/uploads.json"
    url_with_end_point = urljoin(URL, end_point)
    synchronous = str(synchronous).lower()
    data = {"type": _type, "userid": userid, "synchronous": synchronous}

    files = {"file": open(image, "rb")}
    return post_request(data, url_with_end_point, files=files)


def get_tag(tag):
    end_point = "/tags/{}".format(tag)
    url_with_end_point = urljoin(URL, end_point)
    data = {}
    return get_request(data, url_with_end_point)


def get_tag_groups():
    end_point = "/tag_groups.json"
    url_with_end_point = urljoin(URL, end_point)
    data = locals()
    return get_request(data, url_with_end_point)


def create_new_tag_group(name, tag_names):
    end_point = "/tag_groups.json"
    url_with_end_point = urljoin(URL, end_point)
    data = locals()
    return post_request(data, url_with_end_point)


def create_topic(
    title,
    topic_id,
    raw,
    category=None,
    target_usernames=None,
    archetype=None,
    created_at=None,
):
    end_point = "/posts.json"
    url_with_end_point = urljoin(URL, end_point)
    data = locals()
    data = {k: v for k, v in data.items() if v is not None}
    return post_request(data, url_with_end_point)


def set_tags_to_topic(topic_name, topic_id, tags):
    end_point = "/t/{}/{}.json".format(topic_name, topic_id)
    url_with_end_point = urljoin(URL, end_point)
    data = {"tags[]": tags}
    return put_request(data, url_with_end_point)


def update_a_tag_group(group_id, group_name, tags):
    end_point = "/tag_groups/{}.json".format(group_id)
    url_with_end_point = urljoin(URL, end_point)
    data = {"name": group_name, "tag_names[]": tags}
    return put_request(data, url_with_end_point)


def close_topic(topic_name, topic_id):
    end_point = "/t/{}/{}/status.json".format(topic_name, topic_id)
    url_with_end_point = urljoin(URL, end_point)
    data = {"status": "closed", "enabled": "true"}
    return put_request(data, url_with_end_point)


def open_topic(topic_name, topic_id):
    end_point = "/t/{}/{}/status.json".format(topic_name, topic_id)
    url_with_end_point = urljoin(URL, end_point)
    data = {"status": "closed", "enabled": "false"}
    return put_request(data, url_with_end_point)


def pin_topic(topic_name, topic_id, datetime_obj=None):
    end_point = "/t/{}/{}/status.json".format(topic_name, topic_id)
    if datetime_obj is None:
        datetime_obj = datetime.datetime(year=3019, month=12, day=31)
    url_with_end_point = urljoin(URL, end_point)
    data = {"status": "pinned", "enabled": "true", "until": datetime_obj}
    return put_request(data, url_with_end_point)


def unpin_topic(topic_name, topic_id):
    end_point = "/t/{}/{}/status.json".format(topic_name, topic_id)
    url_with_end_point = urljoin(URL, end_point)
    data = {"status": "pinned", "enabled": "false"}
    return put_request(data, url_with_end_point)
