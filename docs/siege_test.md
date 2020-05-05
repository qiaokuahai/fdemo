### 纵向测试
```
主要测试使用gevent和不使用两种情况。
不使用gevent情况下：
[root@VM_0_6_centos scripts]# siege -c 300 -r 1 -b http://122.51.83.195:5000/resume/resume_info

{	"transactions":			         300,
	"availability":			      100.00,
	"elapsed_time":			       29.09,
	"data_transferred":		        9.61,
	"response_time":		        8.76,
	"transaction_rate":		       10.31,
	"throughput":			        0.33,
	"concurrency":			       90.35,
	"successful_transactions":	         300,
	"failed_transactions":		           0,
	"longest_transaction":		       29.01,
	"shortest_transaction":		        0.03
}

[root@VM_0_6_centos scripts]# siege -c 300 -r 5 -b http://122.51.83.195:5000/resume/resume_info
^C
{	"transactions":			        1407,
	"availability":			      100.00,
	"elapsed_time":			      200.78,
	"data_transferred":		       45.08,
	"response_time":		       11.58,
	"transaction_rate":		        7.01,
	"throughput":			        0.22,
	"concurrency":			       81.17,
	"successful_transactions":	        1407,
	"failed_transactions":		           0,
	"longest_transaction":		      113.91,
	"shortest_transaction":		        0.00
}

[root@VM_0_6_centos scripts]# siege -c 50 -r 5 -b http://122.51.83.195:5000/resume/resume_info

{	"transactions":			         250,
	"availability":			      100.00,
	"elapsed_time":			       14.58,
	"data_transferred":		        8.01,
	"response_time":		        1.92,
	"transaction_rate":		       17.15,
	"throughput":			        0.55,
	"concurrency":			       32.85,
	"successful_transactions":	         250,
	"failed_transactions":		           0,
	"longest_transaction":		       13.74,
	"shortest_transaction":		        0.00
}

----------------------
使用gevent情况下
[root@VM_0_6_centos scripts]# siege -c 300 -r 1 -b http://122.51.83.195:5000/resume/resume_info

{	"transactions":			         280,
	"availability":			       93.33,
	"elapsed_time":			       27.49,
	"data_transferred":		        8.97,
	"response_time":		        9.30,
	"transaction_rate":		       10.19,
	"throughput":			        0.33,
	"concurrency":			       94.71,
	"successful_transactions":	         280,
	"failed_transactions":		          20,
	"longest_transaction":		       27.33,
	"shortest_transaction":		        0.04
}


[root@VM_0_10_centos ~]# siege -c 300 -r 5 -b http://122.51.83.195:5000/resume/resume_info
^C
{	"transactions":			        1402,
	"availability":			      100.00,
	"elapsed_time":			      517.98,
	"data_transferred":		       44.92,
	"response_time":		       11.11,
	"transaction_rate":		        2.71,
	"throughput":			        0.09,
	"concurrency":			       30.08,
	"successful_transactions":	        1402,
	"failed_transactions":		           0,
	"longest_transaction":		       70.98,
	"shortest_transaction":		        0.00
}

[root@VM_0_10_centos ~]# siege -c 50 -r 5 -b http://122.51.83.195:5000/resume/resume_info

{	"transactions":			         250,
	"availability":			      100.00,
	"elapsed_time":			       13.62,
	"data_transferred":		        8.01,
	"response_time":		        2.03,
	"transaction_rate":		       18.36,
	"throughput":			        0.59,
	"concurrency":			       37.19,
	"successful_transactions":	         250,
	"failed_transactions":		           0,
	"longest_transaction":		       12.98,
	"shortest_transaction":		        0.00
}


```