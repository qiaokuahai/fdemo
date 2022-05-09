#-*- coding=utf-8 -*-
import sys
import datetime
import time
import threading
from pandas.core.frame import DataFrame
import requests
import pandas
import socket
import dns.resolver
import traceback

all_count = []
error_ldns = []
right_ldns = []
data_map = {}


def to_dig(fqdns, df_ldns, lifetime=2.0, out_file_name=None):
    resolver = dns.resolver.Resolver()
    ldns_lst = df_ldns["ip_address"].values
    for fqdn in fqdns:
        # df = DataFrame(columns=["fqdn", "result", "ldns", "zone", "isp"])
        df = DataFrame()
        for ldns in ldns_lst:
            zone = df_ldns.loc[ldns, "zone"]
            isp = df_ldns.loc[ldns, "isp"]
            resolver.nameservers=[ldns]
            try:
                res1 = resolver.query(fqdn, lifetime=lifetime)
            except Exception as e:
                error_ldns.append(ldns)
                df_ldns.loc[ldns, "status"] = str(e)
                print(e)
            else:
                ans = res1.response.answer
                ip_list = [str(x) for x in ans[-1].items.keys()]
                q_res = ",".join(ip_list)
                _d = {"fqdn": fqdn, "result": q_res, "ldns": ldns, "zone": zone, "isp": isp}
                df = df.append(_d, ignore_index=True)
                print("--- process ok: res is %s ---" % q_res)
        df = df[["fqdn", "result", "zone", "isp", "ldns"]]
        df.to_csv(out_file_name, mode="a", header=False, sep="|")

    if len(all_count) > 1:
        num = all_count.pop()
        print("finsh %" % str(num/num[0]))

    df_ldns.to_excel("new_ldns.xlsx", sheet_name="ldns")

def load_fqdn(file_path):
    df_data = pandas.read_excel(file_path, sheet_name="fqdn", engine="openpyxl")
    return df_data


def load_ldns(file_path):
    df_data = pandas.read_excel(file_path, sheet_name="ldns", engine="openpyxl")
    return df_data


def list_of_groups(init_list, childern_list_len):
    '''
    init_list为初始化的列表，childern_list_len初始化列表中的几个数据组成一个小列表
    :param init_list:
    :param childern_list_len:
    :return:
    '''
    list_of_group = zip(*(iter(init_list),) *childern_list_len)
    end_list = [list(i) for i in list_of_group]
    count = len(init_list) % childern_list_len
    end_list.append(init_list[-count:]) if count !=0 else end_list
    return end_list


def task_start(thread_count, fqdn_path, ldns_path):
    df_fqdn = load_fqdn(fqdn_path)
    df_ldns = load_ldns(ldns_path)
    df_ldns.set_index(keys=["ip_address"], drop=False, inplace=True)
    sep_fqdns_lst = list_of_groups(df_fqdn["fqdn"].values, thread_count)
    out_file_name = "result_bordcast" + str(datetime.datetime.now())[:19].replace(" ", "_") + ".csv"
    for sep_fqdns in sep_fqdns_lst:
        t = threading.Thread(target=to_dig, args=(sep_fqdns, df_ldns, 2.0, out_file_name))
        t.start()
        print("====== start a thread ======")
    
  
if __name__ == '__main__':
    start_time = time.time()
    task_start(2, "/root/fqdn.xlsx", "/root/ldns.xlsx")
    for i in range(100, -1, -1):
        all_count.append(i)
    end_time = time.time()
    print("total cost time is %s" % str(end_time-start_time))
