import sqlite3
import json
import argparse
import os

def parse_json(filename, db):
	try:
		data = json.load(open('data.json'))
		activities = data['activities_data']
		 
		activity_dict = {}
		logs_lst = []
		tickets_lst = []

		for i in activities:
			data = (i['ticket_id'], i['activity']['product'], i['activity']['group'], i['activity']['category'], 
				i['activity']['status'], i['performer_id'], i['performer_type'], i['performed_at'])
			activity_dict[i['ticket_id']] = data

			data = (i['ticket_id'], i['activity']['status'], i['performed_at'])
			logs_lst.append(data)

		for j in activity_dict.keys():
			tickets_lst.append(activity_dict[j])	

		create_store_db(tickets_lst, logs_lst, db)
	except Exception as ex:
		print('{}: Exception in reading from JSON file - {}'.format(os.path.basename(__file__), ex))

def create_store_db(tickets_lst, logs_lst, db):
	try:
		conn = sqlite3.connect(db)
		c = conn.cursor()

		c.execute("create table if not exists tickets (id integer primary key, products text, \
			groups text, category text, status text, perf_id integer, perf_type text, perf_at timestamp)")	

		c.execute("create table if not exists logs (id integer primary key, tkt_id integer, status text, \
			perf_at timestamp, foreign key(tkt_id) references tickets(id))")

		# Truncate table
		c.execute("delete from tickets")
		c.execute("delete from logs")

		c.executemany("insert into tickets(id, products, groups, category, status, perf_id, perf_type, perf_at) \
			values (?, ?, ?, ?, ?, ?, ?, ?)", tickets_lst)

		c.executemany("insert into logs(tkt_id, status, perf_at) \
			values (?, ?, ?)", logs_lst)

		conn.commit()
		c.close()
	except Exception as ex:
		print('{}: Exception in writing to DB - {}'.format(os.path.basename(__file__), ex))

if __name__ == '__main__':
	parser = argparse.ArgumentParser(description='Create Database')
	parser.add_argument('-f', type=str, required=True, help='Provide input file name')
	parser.add_argument('-d', type=str, required=True, help='Provide DB name to connect')
	args = parser.parse_args()
	parse_json(args.f.rstrip(), args.d.rstrip())
