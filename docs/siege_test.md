### 测试数据量大的接口
```
使用Python main.py来启动
siege -c 50 -r 10 -b http://122.51.83.195:5000/resume/resume_info
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
siege -c 50 -r 10 -b http://122.51.83.195:5000/resume/resume_info
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
siege -c 50 -r 10 -b http://122.51.83.195:5000/resume/resume_info
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

### 测试数据量小的接口, 高并发量
```
注： 可以发现，当模拟2000个用户是，出错的概率大大增加
使用Python main.py来启动
siege -c 2000 -r 10 -b http://122.51.83.195:5000/job/job_status
{	"transactions":			        1181,
	"availability":			       38.05,
	"elapsed_time":			       31.03,
	"data_transferred":		        0.03,
	"response_time":		        1.71,
	"transaction_rate":		       38.06,
	"throughput":			        0.00,
	"concurrency":			       65.10,
	"successful_transactions":	        1181,
	"failed_transactions":		        1923,
	"longest_transaction":		       30.43,
	"shortest_transaction":		        0.00
}

使用gunicorn启动服务,开启多线程
{	"transactions":			        1080,
	"availability":			       36.40,
	"elapsed_time":			       31.26,
	"data_transferred":		        0.03,
	"response_time":		       13.96,
	"transaction_rate":		       34.55,
	"throughput":			        0.00,
	"concurrency":			      482.35,
	"successful_transactions":	        1080,
	"failed_transactions":		        1887,
	"longest_transaction":		       31.01,
	"shortest_transaction":		        0.06
}

使用gunicorn，开启多线程，并启用gevent模式
{	"transactions":			        1186,
	"availability":			       38.34,
	"elapsed_time":			       30.96,
	"data_transferred":		        0.03,
	"response_time":		        1.21,
	"transaction_rate":		       38.31,
	"throughput":			        0.00,
	"concurrency":			       46.25,
	"successful_transactions":	        1186,
	"failed_transactions":		        1907,
	"longest_transaction":		        3.74,
	"shortest_transaction":		        0.00
}

```

### 测试数据量小的接口, 模拟1000个用户
```
？？？？？？？为什么使用gevent并没有带来性能上的提升？？？？？？？

使用python main.py的方式
{	"transactions":			        9997,
	"availability":			       99.97,
	"elapsed_time":			       29.03,
	"data_transferred":		        0.29,
	"response_time":		        1.05,
	"transaction_rate":		      344.37,
	"throughput":			        0.01,
	"concurrency":			      360.09,
	"successful_transactions":	        9997,
	"failed_transactions":		           3,
	"longest_transaction":		       27.15,
	"shortest_transaction":		        0.00
}

使用gunicorn多线程方式
{	"transactions":			       10000,
	"availability":			      100.00,
	"elapsed_time":			       34.73,
	"data_transferred":		        0.24,
	"response_time":		        3.32,
	"transaction_rate":		      287.94,
	"throughput":			        0.01,
	"concurrency":			      954.71,
	"successful_transactions":	       10000,
	"failed_transactions":		           0,
	"longest_transaction":		       12.03,
	"shortest_transaction":		        0.11
}

使用gunicorn多线程加gevent方式，实际的处理效果很差，并没有传说中的速度快，原因是什么？？？？？？
{	"transactions":			        9435,
	"availability":			       94.35,
	"elapsed_time":			       39.94,
	"data_transferred":		        0.22,
	"response_time":		        1.02,
	"transaction_rate":		      236.23,
	"throughput":			        0.01,
	"concurrency":			      242.08,
	"successful_transactions":	        9435,
	"failed_transactions":		         565,
	"longest_transaction":		       37.63,
	"shortest_transaction":		        0.00
}

```
