#!/usr/bin/env python

IGNORE_THESE_SLUGS = ["uncategorized", "staff", "lounge", "site-feedback"]
import sys
import interface_discourse

my_interface = interface_discourse.discourse_interface(QUIET_MODE=True)
res = my_interface.get_categories()
categoies_id = {x["slug"]: x["id"] for x in res.json()["category_list"]["categories"]}
for k in sys.argv[1:]:
    my_interface.delete_category(categoies_id[k])
