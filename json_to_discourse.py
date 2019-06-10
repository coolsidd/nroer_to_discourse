#!/usr/bin/env python

import json
import csv
import sys
from pprint import pprint
import interface_discourse
import datetime
import csv_db_funcs
from markdown import *
from time import sleep

from urllib.parse import urljoin

with open("./intestine.json", "r") as json_file:
    my_json = json.load(json_file)

DISCOURSE_METADATA = "disc_meta.csv"
UNUSED_DATA = "mongo_unused.csv"
DISCOURSE_TOPIC_IDS = "disc_topics.csv"
DISCOURSE_USER_IDS = "disc_users.csv"
DISCOURSE_EXISTING_USERS = "disc_users_created.csv"

MEDIA_URL = "https://nroer.gov.in/media/"


def convert_to_tag(x):
    if x is None:
        return None
    return "-".join(x.lower().split())


def get_rand_color():
    import random

    r = lambda: random.randint(0, 255)
    return "%02X%02X%02X" % (r(), r(), r())


def get_from_nested_dicts(category_list, key, delete=False):
    for k in category_list:
        try:
            category = k[key]
            if delete:
                category_list.remove(k)
            return category
        except KeyError:
            continue
    else:
        return None


def process_attributes(attr_list, delete=False):
    def apply(obj, func):
        """Applies function to object/list and *always* returns it as a list"""
        if type(obj) is list:
            values = []
            for k in obj:
                values.append(func(k))
            return values
        else:
            return [func(obj)]

    if delete is False:
        attr_list = attr_list.copy()
    tags = []
    curricular = get_from_nested_dicts(attr_list, "curricular", delete=True)
    if curricular:
        tags.append("curricular")
    else:
        tags.append("not-curricular")

    # This function transform json values to tag names

    known_tag_groups = [
        "educationalalignment",
        "interactivitytype",
        "educationallevel",
        "educationaluse",
        "audience",
        "timerequired",
        "interactivitytype",
        "agerange",
    ]

    for k in known_tag_groups:
        try:
            tags += apply(
                get_from_nested_dicts(attr_list, k, delete=True), convert_to_tag
            )
        except KeyError:
            continue
    return tags


def process_json(disc_interface, my_json, test_mode=False, skip=True):
    if type(disc_interface) != interface_discourse.discourse_interface:
        raise NotImplementedError(
            "param disc_interface should be of type {}".format(
                interface_discourse.discourse_interface
            )
        )
    if my_json.pop("status") == "DRAFT":
        return None
    prev_data = csv_db_funcs.identify_name(my_json["_id"], UNUSED_DATA)
    if prev_data is not None and skip is True:
        return prev_data
    access_policy = my_json.pop("access_policy")
    if access_policy == "PUBLIC":
        access_policy = None
    else:
        pprint(my_json)
        # TODO
        raise NotImplementedError
    category = get_from_nested_dicts(
        my_json["attribute_set"], "educationalsubject", delete=True
    )
    name = my_json.pop("name")
    alt_name = my_json.pop("altnames")
    if category is None:
        category = "Miscelaneous"
    category_id = csv_db_funcs.identify("category", category, DISCOURSE_METADATA)
    if category_id is None:

        res = disc_interface.create_category(category, get_rand_color(), "FFFFFF")
        category_id = json.loads(res.content)["category"]["id"]
        if not test_mode:
            csv_db_funcs.store("category", category, category_id, DISCOURSE_METADATA)
    created_at = my_json.pop("created_at")
    created_at = datetime.datetime.strptime(created_at.split()[0], "%d/%m/%Y")
    source = get_from_nested_dicts(my_json["attribute_set"], "source", delete=True)

    # TODO Add licencse to tagslist
    license = my_json["legal"]["copyright"]  # + " " + my_json["legal"]["license"]
    my_json.pop("legal")
    raw = None
    if "video" in my_json["if_file"]["mime_type"].lower():
        url_joined = urljoin(MEDIA_URL, my_json["if_file"]["original"]["relurl"])
        # thumbnail = urljoin(MEDIA_URL, my_json["if_file"]["thumbnail"]["relurl"])
        raw = markdown_video(
            alt_name,
            my_json.pop("content"),
            # thumbnail,
            url_joined,
            license,
            source,
            my_json.pop("author_set"),
            my_json.pop("collection_set"),
            my_json.pop("location"),
            my_json.pop("annotations"),
        )
    elif "image" in my_json["if_file"]["mime_type"].lower():
        url_joined = urljoin(MEDIA_URL, my_json["if_file"]["original"]["relurl"])
        raw = markdown_image(
            alt_name,
            my_json.pop("content"),
            url_joined,
            license,
            source,
            my_json.pop("author_set"),
            my_json.pop("collection_set"),
            my_json.pop("location"),
            my_json.pop("annotations"),
        )
    my_json.pop("if_file")

    uid = my_json["created_by"]
    user_data = csv_db_funcs.identify("user", uid, DISCOURSE_USER_IDS)

    if user_data is None:
        user_data = [-1, "NoneUser", None]
    else:
        print("Existing user found!!!!")
    if user_data[2] is None:
        user_data[2] = "{}@sample.com".format(user_data[1])
    if csv_db_funcs.identify("user", uid, DISCOURSE_EXISTING_USERS) is None:
        print("Creating new user")
        new_user_data = disc_interface.create_user(
            user_data[1], user_data[2], "samplepassword", user_data[1], active=True
        ).json()["user_id"]
        csv_db_funcs.store("user", uid, new_user_data, DISCOURSE_EXISTING_USERS)
    disc_interface.API_USERNAME = user_data[1]
    res = disc_interface.create_topic(
        name,
        None,
        raw,
        category=category_id,
        archetype=access_policy,
        created_at=created_at,
    )
    disc_interface.API_USERNAME = interface_discourse.ADMIN_NAME
    result_as_dict = res.json()
    discourse_id = result_as_dict["id"]
    topic_name = result_as_dict["topic_slug"]
    topic_id = result_as_dict["topic_id"]
    tags = my_json.pop("tags")
    tags = [convert_to_tag(x) for x in tags]
    existing_tags = csv_db_funcs.identify("tag", "all-misc-tags", DISCOURSE_METADATA)
    if existing_tags is None:
        existing_tags = []

    for tag in tags:
        tag_id = csv_db_funcs.identify("tag", tag, DISCOURSE_METADATA)
        if tag_id is None:
            csv_db_funcs.store("tag", tag, 13, DISCOURSE_METADATA)
            csv_db_funcs.store("tag", "all-misc-tags", [tag], DISCOURSE_METADATA)
        existing_tags.append(tag)
        disc_interface.update_a_tag_group(13, "Misc Tags", existing_tags)

    existing_langs = csv_db_funcs.identify("tag", "languages", DISCOURSE_METADATA)
    if existing_langs is None:
        existing_langs = []
    language = my_json.pop("language")[-1]
    lagnuage = convert_to_tag(language)
    if language in existing_langs:
        tags.append(language)
    else:
        existing_langs.append(language)
        disc_interface.update_a_tag_group(14, "Languages", existing_langs)
        csv_db_funcs.store("tag", "languages", [language], DISCOURSE_METADATA)
        tags.append(language)

    tags.extend(process_attributes(my_json["attribute_set"], delete=True))
    disc_interface.set_tags_to_topic(topic_name, topic_id, tags)
    # print("******************************")
    # print(tags)
    # print("******************************")
    # disc_interface.set_tags_to_topic(topic_name, topic_id, tags)

    ## MANIPULATE TAGS EARLIER ONLY!
    discussion_enable = get_from_nested_dicts(
        my_json["attribute_set"], "discussion_enable", delete=True
    )
    if discussion_enable is None or discussion_enable is True:
        disc_interface.open_topic(topic_name, topic_id)
    else:
        disc_interface.close_topic(topic_name, topic_id)
    if my_json.pop("featured"):
        disc_interface.pin_topic(topic_name, topic_id)
    else:
        # disc_interface.unpin_topic(topic_name, topic_id)
        pass

    csv_db_funcs.append_data(my_json.pop("_id"), topic_id, UNUSED_DATA, **my_json)
    csv_db_funcs.append_data(
        topic_id, topic_name, DISCOURSE_TOPIC_IDS, **result_as_dict
    )
    return my_json
