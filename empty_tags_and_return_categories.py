#!/usr/bin/env python

import interface_discourse
import json

IGNORE_THESE_SLUGS = ["uncategorized", "staff", "lounge", "site-feedback"]

disc_interface = interface_discourse.discourse_interface(QUIET_MODE=True)
disc_interface.QUIET_MODE = True


disc_interface.update_a_tag_group(13, "Misc Tags", [])
disc_interface.update_a_tag_group(14, "Languages", [])

res = disc_interface.get_categories()
json.loads(res.content)
my_dict = json.loads(res.content)["category_list"]["categories"]
slugs = [x["slug"] for x in my_dict if x["slug"] not in IGNORE_THESE_SLUGS]
print(slugs)
