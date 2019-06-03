#!/usr/bin/env python

import json
import csv
import sys
from pprint import pprint
from interface_discourse import *
import datetime
from markdown import *
from csv_db_funcs import *
from urllib.parse import urljoin

with open("./politics.json", "r") as json_file:
    my_json = json.load(json_file)


class json_pop:
    def __init__(self, my_json):
        assert type(my_json) is dict
        self.data = my_json

    def __getitem__(self, idx):
        k = self.data[idx]
        del self.data[idx]
        return k

    def __str__(self):
        return self.data.__str__()

    def __repr__(self):
        return self.data.__repr__()


DISCOURSE_METADATA = "disc_meta.csv"
UNUSED_DATA = "mongo_unused.csv"
MEDIA_URL = "https://nroer.gov.in/media/"


def get_rand_color():
    import random

    r = lambda: random.randint(0, 255)
    return "%02X%02X%02X" % (r(), r(), r())


def get_from_nested_dicts(category_list, key, delete=False):
    for k in category_list:
        try:
            category_list = k[key]
            return category_list
        except:
            continue
    else:
        raise NotImplementedError


def process_json(my_json):
    access_policy = my_json["access_policy"]
    if access_policy == "PUBLIC":
        access_policy = None
    else:
        pprint(my_json)
        # TODO
        raise NotImplementedError

    category = get_from_nested_dicts(
        my_json.data["attribute_set"], "educationalsubject"
    )
    name = my_json["name"]
    alt_name = my_json["altnames"]
    category_id = identify("category", category, DISCOURSE_METADATA)
    if category_id is None:
        res = create_category(category, get_rand_color(), "FFFFFF")
        category_id = json.loads(res.content)["category"]["id"]
        store("category", category, category_id, DISCOURSE_METADATA)
    else:
        category_id = category_id[-1]
    created_at = my_json["created_at"]
    created_at = datetime.datetime.strptime(created_at.split()[0], "%d/%m/%Y")
    source = get_from_nested_dicts(my_json["attribute_set"], "source")
    license = my_json.data["legal"]["copyright"] + " " + my_json["legal"]["license"]
    if "video" in my_json.data["if_file"]["mime_type"].lower():
        url_joined = urljoin(MEDIA_URL, my_json.data["if_file"]["original"]["relurl"])
        thumbnail = urljoin(MEDIA_URL, my_json.data["if_file"]["thumbnail"]["relurl"])
        raw = markdown_video(
            alt_name,
            my_json.data["content"],
            thumbnail,
            url_joined,
            license,
            source,
            my_json.data["author_set"],
            my_json.data["collection_set"],
            my_json.data["location"],
        )
        res = create_topic(
            name,
            None,
            raw,
            category=category_id,
            archetype=access_policy,
            created_at=created_at,
        )
        discourse_id = json.loads(res.content)["id"]
        append_data(my_json["_id"], discourse_id, UNUSED_DATA, **my_json.data)

    if "image" in my_json.data["if_file"]["mime_type"].lower():
        url_joined = urljoin(MEDIA_URL, my_json["if_file"]["original"]["relurl"])
        raw = markdown_image(
            alt_name,
            my_json.data["content"],
            url_joined,
            license,
            source,
            my_json.data["author_set"],
            my_json.data["collection_set"],
            my_json.data["location"],
        )
        res = create_topic(
            name,
            None,
            raw,
            category=category_id,
            archetype=access_policy,
            created_at=created_at,
        )
        discourse_id = json.loads(res.content)["id"]
        append_data(my_json["_id"], discourse_id, UNUSED_DATA, **my_json.data)
