select  t1.tkt_id, 
(strftime('%s', t2.perf_at) - strftime('%s', t1.perf_at))/60 as time_spent_open_mins,
(strftime('%s', t3.perf_at) - strftime('%s', t2.perf_at))/60 as time_spent_waiting_on_customer_mins,
(strftime('%s', t4.perf_at) - strftime('%s', t3.perf_at))/60 as time_spent_waiting_for_response_mins,
(strftime('%s', t4.perf_at) - strftime('%s', t1.perf_at))/60 as time_till_resolution_mins
from logs t1 
join logs t2 on t2.tkt_id = t1.tkt_id
join logs t3 on t3.tkt_id = t1.tkt_id
join logs t4 on t4.tkt_id = t1.tkt_id
where 
t1.status = 'Open' and t2.status = 'Waiting for Customer'
and t3.status = 'Pending' and t4.status = 'Resolved'
group by t1.tkt_id;
