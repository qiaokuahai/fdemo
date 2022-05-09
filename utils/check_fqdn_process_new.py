#-*- coding=utf-8 -*-
import sys
import time
import datetime
import threading
import pandas
import multiprocessing
import dns
import dns.resolver
from multiprocessing import Process
from pandas import DataFrame

def to_dig():
	resolver = dns.resolver.Resolver()
	res1 = resolver.query("www.baidu.com", rdtype=dns.rdatatype.RdataType.AAAA)
	print(res1.response.answer)


if __name__ == '__main__':
	to_dig()


