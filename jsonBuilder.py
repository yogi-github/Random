import json
import argparse
from datetime import datetime as dt, timedelta as td
from collections import defaultdict
import random
import os

globalStTime = dt.now() - td(days=365)
data = defaultdict(dict)
status = ['Open', 'Waiting for Customer', 'Waiting for Third Party', 'Pending', 'Resolved', 'Closed']
product = ['mobile', 'tv', 'fridge', 'AC', 'fan', 'laptop', 'washing machine']
group = ['refund', 'damage', 'buy', 'sell']
category = ['electronics', 'appliances']

def get_rand(input):
	return random.choice(input)
	
def add_pre_data(total):
	temp = {}
	temp['start-at'] = str(globalStTime)
	temp['end_at'] = 'timestamp'
	temp['activities_count'] = total*len(status)

	data['metadata'] = temp
	data['activities_data'] = []

def gen_auto_no():
	start = 10
	while True:
		start += random.randint(60, 600)
		yield start

def gen_user_id():
	g_id = 149018
	counter = 0
	while True:
		value = g_id + counter
		counter += 1
		if (counter % 10 == 0):
			counter = 0
		yield value

def form_activity(no, p_id):
	final_lst = []
	rand_time = gen_auto_no()
	pdt =  get_rand(product)
	grp = get_rand(group)
	ctg = get_rand(category)
	end_time = ''

	for i in status:
		temp = {}
		temp['performed_at'] = str(globalStTime + td(minutes=next(rand_time)))
		temp['ticket_id'] = no
		temp['performer_id'] = next(p_id)
		temp['activity'] = {'status': i, 'product': pdt, 'group': grp, 'category': ctg}
		temp['performer_type'] = 'user'
		final_lst.append(temp)

	end_time = str(globalStTime + td(minutes=next(rand_time)))
	return final_lst, end_time

def generate_ticket(total, fname):
	try:
		p_id = gen_user_id()
		add_pre_data(total)
		for i in range(1, total+1):
			(activities, end_time) = form_activity(i, p_id)
			data['activities_data'].extend(activities)
			data['metadata']['end_at'] = end_time

		with open(fname, 'w') as file:
			json.dump(data, file)
	except Exception as ex:
		print('{}: Exception in writing to JSON file - {}'.format(os.path.basename(__file__), ex))

if __name__ == '__main__':
	parser = argparse.ArgumentParser(description='Generate Tickets')
	parser.add_argument('-m', type=int, required=True, help='Enter the no of tickets to generate')
	parser.add_argument('-o', type=str, required=True, help='Provide output file name')
	args = parser.parse_args()
	generate_ticket(args.m, args.o.rstrip())
