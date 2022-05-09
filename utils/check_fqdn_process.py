# -*- coding=utf-8 -*-
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


def to_dig(fqdns, df_ldns, lifetime=2.0, out_file_name=None):
    resolver = dns.resolver.Resolver()
    ldns_lst = df_ldns["ip_address"].values
    for fqdn in fqdns:
        df = DataFrame()
        for ldns in ldns_lst:
            zone = df_ldns.loc[ldns, "zone"]
            isp = df_ldns.loc[ldns, "isp"]
            resolver.nameservers = [ldns]
            try:
                res1 = resolver.query(fqdn, lifetime=lifetime)
            except Exception as e:
                df_ldns.loc[ldns, "status"] = str(e)
                print(e) 
            else:
                ans = res1.response.answer
                ip_list = [str(x) for x in ans[-1].items.keys()]
                q_res = ",".join(ip_list)
                _d = {
                    "fqdn": fqdn,
                    "result": q_res,
                    "ldns": ldns,
                    "zone": zone,
                    "isp": isp
                }
                df = df.append(_d, ignore_index=True)
                print("--- process ok: res is %s ---" % q_res)
        df = df[["fqdn", "result", "zone", "isp", "ldns"]]
        df.to_csv(out_file_name, mode="a", header=False, sep="|")


def load_fqdn(file_path):
    df_data = pandas.read_excel(file_path,
                                sheet_name="fqdn",
                                engine="openpyxl")
    return df_data


def load_ldns(file_path):
    df_data = pandas.read_excel(file_path,
                                sheet_name="ldns",
                                engine="openpyxl")
    return df_data


def list_of_groups(init_list, childern_list_len):
    '''
    init_list为初始化的列表，childern_list_len初始化列表中的几个数据组成一个小列表
    :param init_list:
    :param childern_list_len:
    :return:
    '''
    list_of_group = zip(*(iter(init_list), ) * childern_list_len)
    end_list = [list(i) for i in list_of_group]
    count = len(init_list) % childern_list_len
    end_list.append(init_list[-count:]) if count != 0 else end_list
    return end_list


def single_process(sep_fqdns, df_ldns, out_file_name, per_cpu_task_count):
    df_ldns.set_index(keys=["ip_address"], drop=False, inplace=True)
    thread_fqdns_lst = list_of_groups(sep_fqdns, per_cpu_task_count)
    thread_list = []
    for one_fqdns in thread_fqdns_lst:
        t = threading.Thread(target=to_dig,
                             args=(one_fqdns, df_ldns, 2.0, out_file_name))
        t.start()
        print("====== start a thread ======")
        thread_list.append(t)
    for th in thread_list:
        th.join()


def task_start(fqdn_path, ldns_path, per_cpu_task_count):
    # 1. 获取cpu的个数，有多少个cpu就启多少个process
    # 2. 拆分fqdn_list, 将fqdn平均分配到每个cpu中
    # 3. 针对每个fqdn，启动一个thread
    process_count = multiprocessing.cpu_count()
    df_fqdn = load_fqdn(fqdn_path)
    df_ldns = load_ldns(ldns_path)
    out_file_name = "result_boardcast_" + str(
        datetime.datetime.now())[:19].replace(" ", "_") + ".csv"
    df_ldns.set_index(keys=["ip_address"], drop=False, inplace=True)
    all_fqdns = df_fqdn["fqdn"].values
    _tmp = int(len(all_fqdns) / process_count)
    _count = _tmp if _tmp == len(all_fqdns) / process_count else (_tmp + 1)
    sep_fqdns_lst = list_of_groups(all_fqdns, _count)
    p_list = []
    for sep_fqdns in sep_fqdns_lst:
        if sep_fqdns:
            p = Process(target=single_process,
                        args=(sep_fqdns, df_ldns, out_file_name,
                              per_cpu_task_count))
            p.start()
            print("======  start a process ======")
            p_list.append(p)
    for pr in p_list:
        pr.join()


if __name__ == '__main__':
    # 执行： python check_fqdn_process.py fqdn_file_path ldns_file_path 3
    # fqdn_file 和 ldns_file 请按照标准来命名
    in_args = sys.argv
    fqdn_file_path = in_args[1]
    ldns_file_path = in_args[2]
    per_cpu_task = int(in_args[3])
    start_time = time.time()
    task_start(fqdn_file_path, ldns_file_path, per_cpu_task)
    # task_start("/root/fqdn.xlsx", "/root/ldns.xlsx", 3)
    end_time = time.time()
    print("total cost time is %s" % str(end_time - start_time))
