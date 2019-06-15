#!/usr/bin/env python

import json
import csv
import sys
from pprint import pprint
import interface_discourse
import datetime
import sql_db_funcs
from markdown import *
from time import sleep

from urllib.parse import urljoin

with open("./intestine.json", "r") as json_file:
    my_json = json.load(json_file)

DISCOURSE_DB = "./discourse_db.db"
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
            if func(obj) is not None:
                return [func(obj)]
            else:
                return []

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


def process_json(disc_interface, my_json, test_mode=False, skip=True, force=False):
    if type(disc_interface) != interface_discourse.discourse_interface:
        if not force:
            raise NotImplementedError(
                "param disc_interface should be of type {}".format(
                    interface_discourse.discourse_interface
                )
            )

    if my_json.pop("status", None) == "DRAFT":
        return None

    if skip is True:
        prev_data = sql_db_funcs.identify("unused_data", my_json["_id"], DISCOURSE_DB)
        if prev_data is not None:
            print("Already_done!")
            return json.loads(prev_data)

    access_policy = my_json.pop("access_policy", None)
    if access_policy == "PUBLIC":
        access_policy = None
    else:
        pprint(my_json)
        # TODO
        if not force:
            raise NotImplementedError
    category = get_from_nested_dicts(
        my_json["attribute_set"], "educationalsubject", delete=True
    )
    name = my_json.pop("name", None)
    if name is None or name == "" or name == "None":
        name = get_from_nested_dicts(my_json["attribute_set"], "name_eng", delete=True)
        if name is None or name == "":
            if not force:
                raise NotImplementedError("Name is empty!")

    alt_name = my_json.pop("altnames", None)
    if alt_name is None:
        alt_name = name
    if category is None:
        category = "Miscelaneous"
    category_id = sql_db_funcs.identify("category", category.title(), DISCOURSE_DB)
    if category_id is None:
        res = disc_interface.create_category(category, get_rand_color(), "FFFFFF")
        if res.status_code == 422:
            pass
        else:
            category_id = json.loads(res.content)["category"]["id"]
            sql_db_funcs.store("category", category, category_id, DISCOURSE_DB)
    created_at = my_json.pop("created_at", None)
    if created_at is not None:
        created_at = datetime.datetime.strptime(created_at.split()[0], "%d/%m/%Y")

    source = get_from_nested_dicts(my_json["attribute_set"], "source", delete=True)

    # TODO Add licencse to tagslist
    try:
        license = my_json["legal"]["copyright"]  # + " " + my_json["legal"]["license"]
        my_json.pop("legal")
    except:
        license = ""
    raw = None
    mime_type = my_json["if_file"].pop("mime_type", None)
    if mime_type is None:
        if not force:
            raise NotImplementedError("Unkown mime type")
    rel_url = my_json["if_file"]["original"]["relurl"]
    if rel_url is not None:
        url_joined = urljoin(MEDIA_URL, rel_url)
    else:
        url_joined = my_json.pop("url")
    if url_joined is None:
        if not force:
            raise NotImplementedError("No URL found")
    content = my_json.pop("content", None)
    if content is None or content == "":
        content = my_json.pop("content_org", None)
    if content is None or content == "":
        content = get_from_nested_dicts(
            my_json["attribute_set"], "description_eng", delete=True
        )

        if not force and content is None:
            raise NotImplementedError("No Content")
    raw = markdown_image(
        alt_name,
        content,
        url_joined,
        license,
        source,
        my_json.pop("author_set"),
        my_json.pop("collection_set"),
        my_json.pop("location"),
        my_json.pop("annotations"),
        force,
    )
    my_json.pop("if_file", None)

    uid = my_json["created_by"]
    user_data = sql_db_funcs.identify("user", uid, DISCOURSE_DB)

    if user_data is None:
        user_data = [-1, "NoneUser", None]
        uid = -1
    else:
        pass
    if user_data[2] is None:
        user_data[2] = "{}@sample.com".format(user_data[1])
    if sql_db_funcs.identify("user", uid, DISCOURSE_DB) is None:
        print("Creating new user")
        print(user_data)
        new_user_data = disc_interface.create_user(
            user_data[1], user_data[2], "samplepassword", user_data[1], active=True
        ).json()["user_id"]
        sql_db_funcs.store("user", uid, new_user_data, DISCOURSE_DB)
    disc_interface.API_USERNAME = user_data[1]
    # print(raw)
    if raw is None:
        if not force:
            raise NotImplementedError("The body generated was none!")
    res = disc_interface.create_topic(
        name,
        None,
        raw,
        category=category_id,
        archetype=access_policy,
        created_at=created_at,
    )
    if res.status_code == 422:
        for i in range(200):
            res = disc_interface.create_topic(
                name + " #{}".format(i),
                None,
                raw,
                category=category_id,
                archetype=access_policy,
                created_at=created_at,
            )
            if res.ok:
                break
    disc_interface.API_USERNAME = interface_discourse.ADMIN_NAME
    result_as_dict = res.json()
    discourse_id = result_as_dict["id"]
    topic_name = result_as_dict["topic_slug"]
    topic_id = result_as_dict["topic_id"]
    tags = my_json.pop("tags")
    tags = [convert_to_tag(x) for x in tags]
    existing_tags = sql_db_funcs.identify("tag", "all-misc-tags", DISCOURSE_DB)
    if existing_tags is None:
        existing_tags = []
    if type(existing_tags) is not list:
        existing_tags = [existing_tags]
    for tag in tags:
        tag_id = sql_db_funcs.identify("tag", tag, DISCOURSE_DB)
        if tag_id is None:
            pass
        sql_db_funcs.store("tag", tag, 8, DISCOURSE_DB)
        sql_db_funcs.store("tag", "all-misc-tags", tag, DISCOURSE_DB)
        existing_tags.append(tag)
        disc_interface.update_a_tag_group(8, "Misc Tags", existing_tags)

    existing_langs = sql_db_funcs.identify("tag", "languages", DISCOURSE_DB)
    if existing_langs is None:
        existing_langs = []
    if type(existing_langs) is not list:
        existing_langs = [existing_langs]
    language = my_json.pop("language")[-1]
    lagnuage = convert_to_tag(language)
    if language in existing_langs:
        tags.append(language)
    else:
        existing_langs.append(language)
        disc_interface.update_a_tag_group(7, "Languages", existing_langs)
        sql_db_funcs.store("tag", "languages", language, DISCOURSE_DB)
        tags.append(language)

    tags.extend(process_attributes(my_json["attribute_set"], delete=True))
    tags.append(mime_type)
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

    sql_db_funcs.store(
        "unused_data", my_json.pop("_id"), json.dumps(my_json), DISCOURSE_DB
    )
    sql_db_funcs.store("topic_ids", topic_name, topic_id, DISCOURSE_DB)
    return my_json
