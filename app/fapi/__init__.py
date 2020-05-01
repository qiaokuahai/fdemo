from app.utils import util
from flask import Blueprint
import inspect


def import_sub_module():
    import_info = util.import_submodules("app.fapi", recursive=True)
    return import_info


def get_curr_bps():
    bp_dict = {}
    import_info = import_sub_module()
    bp_func = lambda x: isinstance(x, Blueprint)
    for _, v in import_info.items():
        bp_obj_list = inspect.getmembers(v, bp_func)
        for bp_obj in bp_obj_list:
            bp_dict[bp_obj[1].import_name] = bp_obj[1]
    return bp_dict

