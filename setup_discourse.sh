#!/bin/bash


# rake='/project/discourse_docker/rake'
# SETTINGS_JSON='/project/nroer_to_discourse/settings.json'
# TAGS_GROUPS_CSV='/project/nroer_to_discourse/tags_groups.csv'
rake='./discourse_docker/rake'
SETTINGS_JSON='./settings.json'
TAGS_GROUPS_CSV='./tags_groups.csv'
$rake admin:create <<< 'oasis2018.bits.pilani@gmail.com\nn\ny'
API_KEY=$($rake api_key:get)
API_USERNAME="coolsidd"
sed -i "s/DUMMY_KEY/$API_KEY/g" ./interface_discourse.py
sed -i "s/DUMMY_NAME/$API_USERNAME/g" ./interface_discourse.py
echo "API_KEY $API_KEY"
echo "API_USERNAME $API_USERNAME"
read -r -a OUTPUT <<< "$(python ./setup_settings.py $SETTINGS_JSON $TAGS_GROUPS_CSV $API_KEY $API_USERNAME | tr -d "[],'")"
echo misc_tag "${OUTPUT[1]}"
echo language_group_id "${OUTPUT[0]}"
sed -i "s/MISC_ID/$/g" ./interface_discourse.py
sed -i "s/LANG_ID/$API_USERNAME/g" ./interface_discourse.py
