#!/usr/bin/env python

from pydiscourse import DiscourseClient


client = DiscourseClient(
    "http://localhost:9292",
    api_key="8302ca56136b04e4b2b82bc03ca4d4346cb5dc3dad6e3881138b9c232d7d4b94",
    api_username="coolsidd",
)


res = client.upload_image("/home/sidd/Downloads/profile.png", "avatar", True, userid=1)
