import config
from lib.parser import ProblemPatterns
from lib.basic import *
from lib.graph import plot

if config.pre_processing_required:
    csv_to_json()

data = json.load(open(config.data_json))

if config.NP_generation_required:
    np_to_json(data)

"""
a=ProblemPatterns(data, 8, _type="problem").get_graph()
for i in a.iterkeys():
    for j in a[i].iterkeys():
        print i+"<---->"+j, a[i][j]"""
graph = ProblemPatterns(data, 8, _type="domain").get_graph()
plot(graph)
#data = ProblemPatterns(data, 20, _type="domain").to_list()
#pattern = ProblemPatterns(data, 8, _type="problem")
#weights, nodes = pattern.get_sorted_degrees(isToDegree=True)
#for node in nodes:
    #print node, weights[node]
#data = pattern.to_list()
#for item in data:
    #print item, pattern.sequence_to_weight(item)
