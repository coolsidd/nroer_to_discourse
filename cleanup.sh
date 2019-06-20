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
FILENAME=$(date '+%Y-%m-%d-%H-%M')-"discourse_db.db"
mv ./discourse_db.db "$FILENAME"
echo "Creating empty files..."
touch ./discourse_db.db
echo "Adding admin default entry"
sqlite3 ./discourse_db.db "CREATE TABLE IF NOT EXISTS user (value TEXT, data TEXT)"
sqlite3 ./discourse_db.db "INSERT INTO user values(1,1)"
echo "Moving error file to backup"
FILENAME=$(date '+%Y-%m-%d-%H-%M')-"errors.csv"
echo "$FILENAME"
mv "./errors.csv" "$FILENAME"
touch "./errors.csv"
# echo "Running unit tests"
echo "Cleaning discourse categories and tags..."
read -r -a OUTPUT <<< "$(python3 ./empty_tags_and_return_categories.py | tr -d "[],'")"
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
