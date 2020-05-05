import datetime
import copy
from bson.objectid import ObjectId


def trans_mongodb_data_to_json(m_data):
    if isinstance(m_data, list):
        for obj in m_data:
            if isinstance(obj, (list, dict)):
                trans_mongodb_data_to_json(obj)
    if isinstance(m_data, dict):
        cp_data = copy.deepcopy(m_data)
        for k, v in cp_data.items():
            if isinstance(v, (list, dict)):
                trans_mongodb_data_to_json(m_data[k])
            else:
                if isinstance(v, (datetime.datetime, ObjectId)):
                    new_value = str(v)
                    if isinstance(k, str) and k.startswith("_"):
                        new_k = k[1:]
                        m_data.pop(k, None)
                        m_data[new_k] = new_value
                    else:
                        m_data[k] = new_value
