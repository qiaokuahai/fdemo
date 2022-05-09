# coding=utf-8
import pandas

g_result = {}


def load_ldns_data(in_file_path):
    pass


def load_fqdn_data(in_file_path):
    df_data = pandas.read_excel(in_file_path,
                                sheet_name="fqdn",
                                engine="openpyxl")
    print(df_data)


def send_request():
    # 使用多线程发
    print("  ")
    pass


def gen_result():
    pass


if __name__ == "__main__":
    in_path = "/root/workspace/fdemo/utils/fqdn.xlsx"
    load_fqdn_data(in_path)
