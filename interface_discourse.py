#!/usr/bin/env python

import requests
import datetime
from pprint import pprint
from functools import wraps
import json
from urllib.parse import urljoin
import useful_utilities
import csv_db_funcs
import unittest.mock
import requests.models




class discourse_interface:
    def __init__(
        self,
        URL="http://localhost",
        API_KEY="6e325593588c04671f879c99b120c3da656772209ffc60b056ef6a8979e32ce4",
        API_USERNAME="coolsidd",
        RETRIES=20,
        TEST_MODE=False,
        TEST_MODE_DEFAULT_EMPTY=False,
        QUIET_MODE=False,
        PATH_TO_SAMPLES_CSV="./sampleresponses.csv",
    ):
        for key, value in locals().items():
            setattr(self, key, value)

    # _requst_copy = _request
    # # TODO
    # def enable_test_mode(self):
    #     _request_copy = _request
    #     _request = debug_func(_request)
    #     TEST_MODE = True

    # def disable_test_mode():
    #     _request = _requst_copy
    #     TEST_MODE = False

    @staticmethod
    def _request(
        _type,
        url,
        json,
        data,
        headers,
        files,
        params,
        timeout,
        allow_redirects,
        **kwargs
    ):
        for i in range(RETRIES):
            res = requests.request(
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
            if res.status_code == 429:
                time = json.loads(res.content)["extras"]["wait_seconds"]
                if not QUIET_MODE:
                    pprint(res.content)
                    print("Waiting for throttle...")
                    print("Sleeping for {} seconds".format(time))
                sleep(int(time))
            else:
                return res

    @staticmethod
    def parse_response(response):
        LAST_RES = response
        if QUIET_MODE:
            return response
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
        self,
        data,
        url,
        files={},
        params={},
        json={},
        timeout=None,
        allow_redirects=False,
        **kwargs
    ):
        params.setdefault("api_key", self.API_KEY)
        params.setdefault("api_username", self.API_USERNAME)
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
        self,
        data,
        url,
        files={},
        params={},
        json={},
        timeout=None,
        allow_redirects=False,
        **kwargs
    ):
        params.setdefault("api_key", self.API_KEY)
        params.setdefault("api_username", self.API_USERNAME)
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
        self,
        data,
        url,
        files={},
        params={},
        json={},
        timeout=None,
        allow_redirects=False,
        **kwargs
    ):
        params.setdefault("api_key", self.API_KEY)
        params.setdefault("api_username", self.API_USERNAME)
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

    def get_categories(self,):
        end_point = "/categories.json"
        url_with_end_point = urljoin(URL, end_point)
        data = dict()
        return self.get_request(data, url_with_end_point)

    def create_category(self, name, color, text_color):
        end_point = "/categories.json"
        url_with_end_point = urljoin(URL, end_point)
        data = {"name": name, "color": color, "text_color": text_color}
        return self.post_request(data, url_with_end_point)

    def create_user(
        self,
        name,
        email,
        password,
        username,
        active=True,
        approved=True,
        user_fields="",
    ):
        end_point = "/users"
        url_with_end_point = urljoin(URL, end_point)
        data = locals()
        return self.post_request(data, url_with_end_point)

    def upload_image_or_avatar(self, _type, userid=None, synchronous=False, image=None):
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
        return self.post_request(data, url_with_end_point, files=files)

    def get_tag(self, tag):
        end_point = "/tags/{}".format(tag)
        url_with_end_point = urljoin(URL, end_point)
        data = {}
        return self.get_request(data, url_with_end_point)

    def get_tag_groups(self,):
        end_point = "/tag_groups.json"
        url_with_end_point = urljoin(URL, end_point)
        data = locals()
        return self.get_request(data, url_with_end_point)

    def create_new_tag_group(self, name, tag_names):
        end_point = "/tag_groups.json"
        url_with_end_point = urljoin(URL, end_point)
        data = locals()
        return self.post_request(data, url_with_end_point)

    def create_topic(
        self,
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
        return self.post_request(data, url_with_end_point)

    def set_tags_to_topic(self, topic_name, topic_id, tags):
        end_point = "/t/{}/{}.json".format(topic_name, topic_id)
        url_with_end_point = urljoin(URL, end_point)
        data = {"tags[]": tags}
        return self.put_request(data, url_with_end_point)

    def update_a_tag_group(self, group_id, group_name, tags):
        end_point = "/tag_groups/{}.json".format(group_id)
        url_with_end_point = urljoin(URL, end_point)
        data = {"name": group_name, "tag_names[]": tags}
        return self.put_request(data, url_with_end_point)

    def close_topic(self, topic_name, topic_id):
        end_point = "/t/{}/{}/status.json".format(topic_name, topic_id)
        url_with_end_point = urljoin(URL, end_point)
        data = {"status": "closed", "enabled": "true"}
        return self.put_request(data, url_with_end_point)

    def open_topic(self, topic_name, topic_id):
        end_point = "/t/{}/{}/status.json".format(topic_name, topic_id)
        url_with_end_point = urljoin(URL, end_point)
        data = {"status": "closed", "enabled": "false"}
        return self.put_request(data, url_with_end_point)

    def pin_topic(self, topic_name, topic_id, datetime_obj=None):
        end_point = "/t/{}/{}/status.json".format(topic_name, topic_id)
        if datetime_obj is None:
            datetime_obj = datetime.datetime(year=3019, month=12, day=31)
        url_with_end_point = urljoin(URL, end_point)
        data = {"status": "pinned", "enabled": "true", "until": datetime_obj}
        return self.put_request(data, url_with_end_point)

    def unpin_topic(self, topic_name, topic_id):
        end_point = "/t/{}/{}/status.json".format(topic_name, topic_id)
        url_with_end_point = urljoin(URL, end_point)
        data = {"status": "pinned", "enabled": "false"}
        return self.put_request(data, url_with_end_point)
