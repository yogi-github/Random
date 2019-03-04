#!/bin/sh
# 1. Generate a JSON file for N ticekts
python jsonBuilder.py -m 100 -o data.json
# 2. Read a JSON file and write to a DB
python dbDump.py -f data.json -d aginic.db
# 3. Execute a SQL script to fetch data from the DB
python fetchData.py -f sqlScript.sql -d aginic.db