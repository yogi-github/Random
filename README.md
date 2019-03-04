# Aginic
## Problem Statement

Introduction

Freshdesk, a helpdesk system, allows the export of activity information of all tickets. The export takes the following form:

{

"metadata": {

"start_at": "20-04-2017 10:00:00 +0000",

"end_at": "21-04-2017 09:59:59 +0000",

"activities_count": 2

},

"activities_data": [

{

"performed_at": "21-04-2017 09:33:38 +0000",

"ticket_id": 600,

"performer_type": "user",

"performer_id": 149018,

"activity": {

"note": {

"id": 4025864,

"type": 4

}

}

},

{

"performed_at": "21-04-2017 09:38:24 +0000",

"ticket_id": 704,

"performer_type": "user",

"performer_id": 149018,

"activity": {

"shipping_address": "N/A",

"shipment_date": "21 Apr, 2017",

"category": "Phone",

"contacted_customer": true,

"issue_type": "Incident",

"source": 3,

"status": "Open",

"priority": 4,

"group": "refund",

"agent_id": 149018,

"requester": 145423,

"product": "mobile"

}

}

]

}

The status column can be any of the following values:

"Open"
"Closed"
"Resolved"
"Waiting for Customer"
"Waiting for Third Party"
"Pending"

Steps

1. Write a Python program which will randomly generate realistic ticket data based on the above JSON format and store the data in a JSON file on disk. It should generate a random activity distribution for a configurable number of tickets. The program will be checked for realism of data, and for the ability to handle large amounts of records.Example: ticket_gen -n 1000 -o activities.json to generate 1000 tickets with random activities into the activities.json file.

2. Write a program (in a language if your choice) to read the above generated JSON file and store the data into a SQLite database in a relational format. The program will be checked for relational modelling.

3. Write a SQL script that can be run on the database to generate the following attributes for each ticket:
Time spent Open
Time spent Waiting on Customer
Time spent waiting for response (Pending Status)
Time till resolution
Time to first response
Example:| ticket_id | time_spent_open | time_spent_waiting_on_customer | time_spent_waiting_for_response | time_till_resolution | time_to_first_response | | 704 | 12 | 90 | 1200 | 1300 | 10 |

4. Ensure all the above programs can be run in sequence using a bash script, Makefile, or equivalent.
---------------------------------------------------------------------------------------------------------------------

## Solution

### Requirements

- Python 3.7

- Sqlite3 Database

1. Task #1 to generate a JSON file is completed and the code is in file jsonBuilder.py. Running this script produces an ouput json file.

python jsonBuilder.py -m 100 -o data.json

2. Task #2 to store the data in Sqlite DB is in dbDump.py. Running this script creates a DB, creates tables and inserts data from a json file.

python dbDump.py -f data.json -d aginic.db

3. Task #3 to execute a script and display the intended results is in fetchData.py and sqlScript.sql files. Running this script fetches the data from tables and apply the SQL script to get the results.

python fetchData.py -f sqlScript.sql -d aginic.db

4. Task #4 to create a bash script and execute all the above tasks is in run.sh file.

./run.sh

### Database design

There are 2 tables tickets and logs. 

Table tickets has the information about all the tickets, last status of the activity and details pertaining to a ticket. It references Table logs in one-many relationship.

Table logs has the information about the status of the ticket's activity and its timestamp. Basically it logs all the changes to the activity of a ticket.

### TODO
time_to_first_response calculation is still pending. I would need clarification to implement it.