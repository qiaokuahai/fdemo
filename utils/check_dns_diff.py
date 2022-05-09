# -*- coding=utf-8 -*-
import sys
import datetime
import time
import pandas


def load_result(file_path):
    df_data = pandas.read_csv(
        file_path,
        sep="|",
        header=None,
        names=["tmp", "fqdn", "result", "zone", "isp", "ldns"],
        index_col="tmp")
    df_data["fqdn_ldns"] = df_data["fqdn"] + "&" + df_data["ldns"]
    df_data = df_data.set_index(["fqdn_ldns"])
    return df_data


def check_result(old_df, new_df):
    res = pandas.concat([old_df, new_df], axis=1)
    res = pandas.merge(old_df,
                       new_df,
                       how="outer",
                       left_index=True,
                       right_index=True,
                       suffixes=('_old', '_new'))
    res.drop(["fqdn_old", "zone_old", "isp_old", "ldns_old"],
             axis=1,
             inplace=True)
    out_file_name = "result_check_dns_" + str(
        datetime.datetime.now())[:19].replace(" ", "_") + ".xlsx"
    res = res[[
        "fqdn_new", "result_old", "result_new", "zone_new", "isp_new",
        "ldns_new"
    ]]
    res_eq = res[res["result_old"] == res["result_new"]]
    tmp = res.dropna()
    res_neq = tmp[tmp["result_old"] != tmp["result_new"]]
    writer = pandas.ExcelWriter(out_file_name)
    res.to_excel(writer, sheet_name="all_result")
    res_neq.to_excel(writer, sheet_name="neq_result")
    res_eq.to_excel(writer, sheet_name="eq_result")
    # res_eq.to_csv(out_file_name, sep="|")
    # res.to_csv(out_file_name, sep="|")
    writer.save()
    writer.close()
    return res


def task_start(old_path, new_path):
    old_result = load_result(old_path)
    new_result = load_result(new_path)
    res = check_result(old_result, new_result)
    return res


if __name__ == '__main__':
    # 执行： python check_dns_diff.py old_file_path new_file_path
    # old_file和new_file为 check_fqdn_process.py脚本生成的.csv文件
    in_args = sys.argv
    old_file_path = in_args[1]
    new_file_path = in_args[2]
    start_time = time.time()
    task_start(old_file_path, new_file_path)
    end_time = time.time()
    print("total cost time is %s" % str(end_time - start_time))
