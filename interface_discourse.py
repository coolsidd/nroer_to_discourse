#!/usr/bin/env python

import requests
from time import sleep
import datetime
from pprint import pprint
from functools import wraps
import json
from urllib.parse import urljoin
import useful_utilities
import csv_db_funcs
import unittest.mock
import requests.models


def testable(func):
    @wraps(func)
    def wrapper(self, *args, **kwargs):
        try:
            if self.TEST_MODE:
                sample = csv_db_funcs.identify(
                    "samples", func.__name__, self.PATH_TO_SAMPLES_CSV
                )
                if ((sample is None) or (sample == [])) and (
                    not self.TEST_MODE_DEFAULT_EMPTY
                ):
                    raise NotImplementedError(
                        "Add sample response for {} to {} or pass '{} = True' as an argument".format(
                            func.__name__, self.PATH_TO_SAMPLES_CSV, default_none_key
                        )
                    )
                else:
                    test_response = unittest.mock.Mock(spec=requests.models.Response)
                    test_response.content = json.dumps(sample).encode("utf-8")
                    test_response.status_code = 200
                    test_response.ok = True
                    test_response.json = lambda: sample
                    return self.parse_response(test_response)

            else:
                return func(self, *args, **kwargs)
        except KeyError as e:
            return func(self, *args, **kwargs)

    # wrapper = useful_utilities.debug_func(wrapper)
    return wrapper


ADMIN_NAME = "DUMMY_NAME"
API_KEY_GLOBAL = "DUMMY_KEY"


class discourse_interface:
    def __init__(
        self,
        URL="http://localhost",
        API_KEY=API_KEY_GLOBAL,
        API_USERNAME=ADMIN_NAME,
        RETRIES=20,
        TEST_MODE=False,
        TEST_MODE_DEFAULT_EMPTY=False,
        QUIET_MODE=False,
        PATH_TO_SAMPLES_CSV="./sampleresponses.csv",
    ):
        for key, value in locals().items():
            setattr(self, key, value)
        self.LAST_RES = None

    # _requst_copy = _request
    # # TODO
    # def enable_test_mode(self):
    #     _request_copy = _request
    #     _request = debug_func(_request)
    #     TEST_MODE = True

    # def disable_test_mode():
    #     _request = _requst_copy
    #     TEST_MODE = False

    def _request(
        self,
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
        self.LAST_RES = None
        self.LAST_RQST = locals()
        for i in range(self.RETRIES):
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
            self.LAST_RES = res
            if res.status_code == 429:
                try:
                    time = res.json()["extras"]["wait_seconds"]
                except Exception as e:
                    time = 10
                if not self.QUIET_MODE:
                    pprint(res.content)
                    print("Waiting for throttle...")
                    print("Sleeping for {} seconds".format(time))
                sleep(int(time))
            else:
                return res

    def parse_response(self, response):
        if self.QUIET_MODE:
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
        elif response.status_code == 422:
            raise NotImplementedError
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
        response = self._request(
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
        return self.parse_response(response)

    def delete_request(
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
        response = self._request(
            "DELETE",
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
        return self.parse_response(response)

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
        response = self._request(
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
        return self.parse_response(response)

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
        response = self._request(
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
        return self.parse_response(response)

    @testable
    def get_categories(self):
        end_point = "/categories.json"
        url_with_end_point = urljoin(self.URL, end_point)
        data = dict()
        return self.get_request(data, url_with_end_point)

    @testable
    def create_category(self, name, color, text_color):
        end_point = "/categories.json"
        url_with_end_point = urljoin(self.URL, end_point)
        data = {"name": name, "color": color, "text_color": text_color}
        return self.post_request(data, url_with_end_point)

    @testable
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
        url_with_end_point = urljoin(self.URL, end_point)
        data = locals()
        del data["self"]
        return self.post_request(data, url_with_end_point)

    @testable
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
        url_with_end_point = urljoin(self.URL, end_point)
        synchronous = str(synchronous).lower()
        data = {"type": _type, "userid": userid, "synchronous": synchronous}

        files = {"file": open(image, "rb")}
        return self.post_request(data, url_with_end_point, files=files)

    @testable
    def get_tag(self, tag):
        end_point = "/tags/{}".format(tag)
        url_with_end_point = urljoin(self.URL, end_point)
        data = {}
        return self.get_request(data, url_with_end_point)

    @testable
    def get_tag_groups(self,):
        end_point = "/tag_groups.json"
        url_with_end_point = urljoin(self.URL, end_point)
        data = locals()
        del data["self"]
        return self.get_request(data, url_with_end_point)

    @testable
    def create_new_tag_group(self, name, tag_names):
        end_point = "/tag_groups.json"
        url_with_end_point = urljoin(self.URL, end_point)
        data = locals()
        del data["self"]
        return self.post_request(data, url_with_end_point)

    @testable
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
        url_with_end_point = urljoin(self.URL, end_point)
        data = locals()
        del data["self"]
        data = {k: v for k, v in data.items() if v is not None}
        return self.post_request(data, url_with_end_point)

    @testable
    def set_tags_to_topic(self, topic_name, topic_id, tags):
        end_point = "/t/{}/{}.json".format(topic_name, topic_id)
        url_with_end_point = urljoin(self.URL, end_point)
        data = {"tags[]": tags}
        return self.put_request(data, url_with_end_point)

    @testable
    def update_a_tag_group(self, group_id, group_name, tags):
        end_point = "/tag_groups/{}.json".format(group_id)
        url_with_end_point = urljoin(self.URL, end_point)
        data = {"name": group_name, "tag_names[]": tags}
        return self.put_request(data, url_with_end_point)

    @testable
    def close_topic(self, topic_name, topic_id):
        end_point = "/t/{}/{}/status.json".format(topic_name, topic_id)
        url_with_end_point = urljoin(self.URL, end_point)
        data = {"status": "closed", "enabled": "true"}
        return self.put_request(data, url_with_end_point)

    @testable
    def open_topic(self, topic_name, topic_id):
        end_point = "/t/{}/{}/status.json".format(topic_name, topic_id)
        url_with_end_point = urljoin(self.URL, end_point)
        data = {"status": "closed", "enabled": "false"}
        return self.put_request(data, url_with_end_point)

    @testable
    def pin_topic(self, topic_name, topic_id, datetime_obj=None):
        end_point = "/t/{}/{}/status.json".format(topic_name, topic_id)
        if datetime_obj is None:
            datetime_obj = datetime.datetime(year=3019, month=12, day=31)
        url_with_end_point = urljoin(self.URL, end_point)
        data = {"status": "pinned", "enabled": "true", "until": datetime_obj}
        return self.put_request(data, url_with_end_point)

    @testable
    def unpin_topic(self, topic_name, topic_id):
        end_point = "/t/{}/{}/status.json".format(topic_name, topic_id)
        url_with_end_point = urljoin(self.URL, end_point)
        data = {"status": "pinned", "enabled": "false"}
        return self.put_request(data, url_with_end_point)

    # NO SAMPLE RESPONSES BELOW
    @testable
    def delete_category(self, category_id):
        end_point = "/categories/{}".format(category_id)
        url_with_end_point = urljoin(self.URL, end_point)
        return self.delete_request(None, url_with_end_point)

    @testable
    def impersonate_user(self, username_or_email):
        end_point = "admin/impersonate"
        url_with_end_point = urljoin(self.URL, end_point)
        data = locals()
        del data["self"]
        self.API_USERNAME = username_or_email
        return self.post_request(data, url_with_end_point)

    @testable
    def change_trust_level(self, userid, level):
        end_point = "/admin/users/{}/trust_level.json".format(userid)
        url_with_end_point = urljoin(self.URL, end_point)
        data = {"level": level}
        return self.put_request(data, url_with_end_point)

    @testable
    def grant_admin(self, userid):
        end_point = "/admin/users/{}/grant_admin.json".format(userid)
        url_with_end_point = urljoin(self.URL, end_point)
        return self.put_request(None, url_with_end_point)

    @testable
    def generate_api_key(self):
        end_point = "/admin/api/key.json"
        url_with_end_point = urljoin(self.URL, end_point)
        data = {"id": 1}
        return self.put_request(data, url_with_end_point)

    @testable
    def upload_settings_from_json(self, json_data):
        for key, value in json_data.items():
            end_point = "/admin/site_settings/{}".format(key)
            url_with_end_point = urljoin(self.URL, end_point)
            data = {key: value}
            res = self.put_request(data, url_with_end_point)
            if res.ok:
                pass
            else:
                raise NotImplementedError(
                    "Settings could not be implemented successfully"
                )

    @testable
    def upload_tags_from_csv(self, csv_file):
        end_point = "/tags/upload.json"
        url_with_end_point = urljoin(self.URL, end_point)
        files = {"file": open(csv_file, "rb")}
        return self.post_request(None, url_with_end_point, files=files)
