import nltk
import config
import json

# converts main csv to main json
def pre_processing(csv_file, json_file):
    _file = open(csv_file)
    _data = ("".join(_file.readlines())).replace("\r\n", " ").split(",")
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
    json_file = open(json_file, "w")
    json.dump(new_data, json_file, ensure_ascii=True)


# gets noun phrases
def get_NP(document):
    sentences = nltk.sent_tokenize(document)
    sentences = [nltk.word_tokenize(sent) for sent in sentences]
    sentences = [nltk.pos_tag(sent) for sent in sentences][0]
    grammar = "NP: {<JJ>*<NN|NNP|CD>*}"
    cp = nltk.RegexpParser(grammar)
    nlp_tree = cp.parse(sentences)

    for _node in nlp_tree:
        if _node.node is "NP":
            yield " ".join([_word[0] for _word in _node])


# generates problem patterns
# todo modify the class to more generic form
class ProblemPatterns:
    def __init__(self, data):
        self.data = data
        graph = self.get_problem_chain_graph()
        self.patterns = self.get_problem_subgraphs(graph)

    def get_problem_chain_graph(self):

        # get history of problems ordered by time from each of the customers
        customer_history = {}
        for _id in range(0, len(self.data)):
            try:
                customer_history[self.data[_id][config.table_cid]].append(self.data[_id][config.table_problem])
            except:
                customer_history[self.data[_id][config.table_cid]] = [self.data[_id][config.table_problem]]

        # now create a directed problem graph
        graph = {}
        for history in customer_history:
            #history has history of individual customer
            prev_problem = None
            for problem in history:
                if prev_problem is not None:
                    try:
                        graph[problem][prev_problem] += 1
                    except:
                        # new edge
                        graph[problem] = {prev_problem: 1}

        return graph

    def get_problem_subgraphs(self, graph):
        # TODO
        return []

    def to_list(self):
        return self.patterns
