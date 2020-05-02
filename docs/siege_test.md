```
siege -c 50 -r 10 -b http://122.51.83.195:5000/resume/resume_info

使用Python main.py来启动
{	"transactions":			         500,
	"availability":			      100.00,
	"elapsed_time":			       36.14,
	"data_transferred":		       20.95,
	"response_time":		        2.64,
	"transaction_rate":		       13.84,
	"throughput":			        0.58,
	"concurrency":			       36.51,
	"successful_transactions":	         500,
	"failed_transactions":		           0,
	"longest_transaction":		       31.76,
	"shortest_transaction":		        0.00
}

使用gunicorn来启动
{	"transactions":			         500,
	"availability":			      100.00,
	"elapsed_time":			       28.70,
	"data_transferred":		       16.02,
	"response_time":		        1.97,
	"transaction_rate":		       17.42,
	"throughput":			        0.56,
	"concurrency":			       34.24,
	"successful_transactions":	         500,
	"failed_transactions":		           0,
	"longest_transaction":		       16.88,
	"shortest_transaction":		        0.00
}

使用gevent来启动
{	"transactions":			         500,
	"availability":			      100.00,
	"elapsed_time":			       27.16,
	"data_transferred":		       16.02,
	"response_time":		        1.92,
	"transaction_rate":		       18.41,
	"throughput":			        0.59,
	"concurrency":			       35.38,
	"successful_transactions":	         500,
	"failed_transactions":		           0,
	"longest_transaction":		       25.67,
	"shortest_transaction":		        0.00
}


```