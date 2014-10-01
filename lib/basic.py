import json
import config
from parser import get_noun_phrases
import threading


# converts main csv to main json
def csv_to_json():
    _file = open(config.data_csv)
    _data = ("".join(_file.readlines())).replace("\r\n", " ").split(config.csv_delimiter)
    new_data = {}
    _part = []
    _part_size = config.table_size - 1
    _part_id = 0
    for index in range(0, len(_data)):
        if index % _part_size is 0 and index is not 0:
            _part.append(_data[index].split(" ")[0])
            new_data[_part_id] = _part[:]
            _part_id += 1
            try:
                _part = [" ".join(_data[index].split(" ")[1:])]
            except:
                pass
        else:
            _part.append(_data[index])
    json_file = open(config.data_json, "w")
    json.dump(new_data, json_file, ensure_ascii=True)


# maps problem id with noun phrases of problem
def np_to_json(calls):
    data = {}
    # number of threads doing this operation
    pieces = 30

    def np_to_json_part(part):
        for _id in part:
            problem = calls[_id][config.table_problem]
            if problem is u'':
                data[_id] = []
            else:
                phrases = get_noun_phrases(problem)
                data[_id] = phrases

    keys = calls.keys()
    threads = []
    for limit in range(0, pieces):
        _start = limit*(len(keys)/pieces)
        _end = (limit+1)*(len(keys)/pieces)
        thread = threading.Thread(target=np_to_json_part, args=(keys[_start:_end],))
        thread.start()
        threads.append(thread)

    for thread in threads:
        thread.join()

    json.dump(data, open(config.data_np, "w"), ensure_ascii=True)
