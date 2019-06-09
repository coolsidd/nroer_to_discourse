#!/usr/bin/env bash

E_WRONG_ARGS=85
script_parameters="<Path to docker's rake>"

#                  -a = all, -h = help, etc.
Number_of_expected_args=1
if [ $# -ne $Number_of_expected_args ]
then
    echo "Usage: `basename $0` $script_parameters"
  # `basename $0` is the script's filename.
  exit $E_WRONG_ARGS
fi



echo "Removing old data..."
rm ./mongo_unused.csv ./disc_meta.csv ./disc_topics.csv ./disc_users.csv ./disc_users_created.csv
echo "Creating empty files..."
touch ./mongo_unused.csv ./disc_meta.csv ./disc_topics.csv ./disc_users.csv ./disc_users_created.csv
echo "Adding admin default entry"
echo "user, 1, 1" >| ./disc_users_created.csv
echo "Moving error file to backup"
FILENAME=$(date '+%Y-%m-%d-%H-%M')-"errors.csv"
echo "$FILENAME"
mv "./errors.csv" "$FILENAME"
touch "./errors.csv"
# echo "Running unit tests"
echo "Cleaning discourse categories and tags..."
read -r -a OUTPUT <<< "$(python ./empty_tags_and_return_categories.py | tr -d "[],'")"
echo "${OUTPUT[@]}"
for category in "${OUTPUT[@]}"
do
    echo "Cleaning:"
    echo "$category"
    $1 destroy:topics["$category"]

done
echo "Done!"
echo "Deleting categories"
echo "${OUTPUT[@]}"
python ./delete_all_categories.py "${OUTPUT[@]}"
# echo "Remember to manually delete all the categories!"
