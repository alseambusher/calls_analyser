import config
import json
from lib.parser import csv_to_json, ProblemPatterns

if config.pre_processing_required:
    csv_to_json()

data = json.load(open(config.data_json))

#print ProblemPatterns(data, 3).to_list()
"""a=ProblemPatterns(data, 8, _type="problem_type").get_graph()
for i in a.iterkeys():
    for j in a[i].iterkeys():
        print i,j,a[i][j]"""
#data = ProblemPatterns(data, 8, _type="problem_type").to_list()
data = ProblemPatterns(data, 8).to_list()
for item in data:
    print item

