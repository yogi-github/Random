import sqlite3
import argparse
import os

header = ['ticket_id', 'time_spent_open', 'time_spent_waiting_on_customer',\
			'time_spent_waiting_for_response', 'time_till_resolution']

def display_op(data):
	data = [header] + list(data)
	for i, d in enumerate(data):
		line = '|'.join(str(x).ljust(31) for x in d)
		print(line)
		if i == 0:
			print('-' * len(line))

def get_data(fname, db):
	try:
		conn = sqlite3.connect(db)
		cursor = conn.cursor()

		file = open(fname, 'r')
		query = file.read()
		file.close()

		cursor.execute(query)
		display_op(cursor.fetchall())
		
		conn.commit()
		conn.close()
	except Exception as ex:
		print('{}: Exception in reading from DB - {}'.format(os.path.basename(__file__), ex))

if __name__ == '__main__':
	parser = argparse.ArgumentParser(description='Fetch Data')
	parser.add_argument('-f', type=str, required=True, help='Provide input sql script')
	parser.add_argument('-d', type=str, required=True, help='Provide DB name to connect')
	args = parser.parse_args()
	get_data(args.f.rstrip(), args.d.rstrip())
