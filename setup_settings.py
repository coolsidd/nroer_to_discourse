#!/usr/bin/env python
import os
import json
import interface_discourse
import sys

json_file_path = os.path.abspath(sys.argv[1])
csv_file_path = os.path.abspath(sys.argv[2])
with open(json_file_path, "r") as json_file:
    my_json = json.load(json_file)
interface_instance = interface_discourse.discourse_interface(
    API_USERNAME=str(sys.argv[4]).strip(),
    API_KEY=str(sys.argv[3]).strip(),
    QUIET_MODE=True,
)
interface_instance.upload_settings_from_json(my_json)
interface_instance.upload_tags_from_csv(csv_file_path)
tag_groups = interface_instance.get_tag_groups().json()
language_id = [
    x["id"] for x in tag_groups["tag_groups"] if x["name"].lower() == "languages"
][0]
misc_id = [
    x["id"] for x in tag_groups["tag_groups"] if x["name"].lower() == "misc tags"
][0]
print([language_id, misc_id])
