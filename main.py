import config
import json
import temp
from lib import parser

if config.pre_processing_required:
    parser.pre_processing(config.data_csv, config.data_json)

temp.DATA = {"calls": json.load(open(config.data_json))}

# print parser.problem_patterns().to_list()
