import nltk
import config
import json


# gets noun phrases
def get_noun_phrases(document):
    data = []
    sentences = nltk.sent_tokenize(document)
    sentences = [nltk.word_tokenize(sent) for sent in sentences]
    sentences = [nltk.pos_tag(sent) for sent in sentences][0]
    grammar = "NP: {<JJ>*<NN|NNP|CD>*}"
    cp = nltk.RegexpParser(grammar)
    nlp_tree = cp.parse(sentences)
    for _node in nlp_tree:
        try:
            if _node.node == "NP":
                data.append(" ".join([_word[0] for _word in _node]))
        except:
            pass
    return data


class ProblemPatterns:
    def __init__(self, data, length, _type="domain", weight_min=0):
        self.data = data
        self.max_length = length
        self.weight_min = weight_min

        if _type is "domain":
            self.graph = self.get_column_chain_graph(config.table_domain)
        elif _type is "problem_type":
            self.graph = self.get_column_chain_graph(config.table_problem_type)
        elif _type is "problem":
            self.graph = self.get_problem_chain_graph()
        else:
            self.graph = {}

        self.patterns = self.get_problem_subgraphs(length)

    # get history of problems ordered by time from each of the customers
    # set get_ids to true if you want ids and not any columns
    def get_customer_history(self, table_column=None, get_ids=False):
        customer_history = {}
        for _id in range(0, len(self.data)):
            _id = str(_id)
            if not get_ids:
                try:
                    customer_history[self.data[_id][config.table_cid]].append(self.data[_id][table_column])
                except:
                    customer_history[self.data[_id][config.table_cid]] = [self.data[_id][table_column]]
            else:
                try:
                    customer_history[self.data[_id][config.table_cid]].append(_id)
                except:
                    customer_history[self.data[_id][config.table_cid]] = [_id]
        return customer_history

    # pass column index construct graph
    def get_column_chain_graph(self, column):
        customer_history = self.get_customer_history(table_column=column)
        # now create a directed problem graph
        graph = {}
        for history in customer_history.itervalues():
            #history has history of individual customer
            prev_problem = None
            for problem in history:
                if problem is not u'':
                    if prev_problem is not None:
                        try:
                            graph[prev_problem][problem] += 1
                        except:
                            # new edge
                            graph[prev_problem] = dict({problem: 1})
                    prev_problem = problem
        return graph

    def get_problem_chain_graph(self):
        graph = {}
        noun_phrases = json.load(open(config.data_np))
        # get call id history of each customer
        customer_history = self.get_customer_history(get_ids=True)
        for _ids in customer_history.itervalues():
            prev_problem = None
            for _id in _ids:
                try:
                    problem = noun_phrases[_id]
                except:
                    problem = []
                if problem:
                    if prev_problem is not None:
                        for phrase1 in prev_problem:
                            phrase1 = phrase1.lower()
                            for phrase2 in problem:
                                phrase2 = phrase2.lower()
                                try:
                                    graph[phrase1][phrase2] +=1
                                except:
                                    graph[phrase1] = dict({phrase2: 1})
                    prev_problem = problem

        return graph

    def get_problem_subgraphs(self, length):
        patterns = []
        for node in self.graph.iterkeys():
            patterns.extend(self.get_longest_pattern(node, [node], length - 1))

        return sorted(patterns, key=self.sequence_to_weight, reverse=True)

    def get_longest_pattern(self, node, sequence, length):
        patterns = []
        for adj in self.graph[node].iterkeys():
            # if last node permitable is supposed to be added OR
            # if you have reached leaf nodes
            if length == 1 or adj not in self.graph or len(self.graph[adj]) == 0:
                # discard the sequence below weight limit
                if self.sequence_to_weight(sequence+[adj]) > self.weight_min:
                    patterns.append(sequence+[adj])
            # if you have encountered a cycle and have already entered the cycle, skip it
            elif ("".join(sequence)).find(sequence[-1]+adj) is not -1:
                patterns.append(sequence)
            else:
                patterns.extend(self.get_longest_pattern(adj, sequence+[adj], length-1))
        return patterns

    def sequence_to_weight(self, sequence):
        weight = 0
        node1 = sequence[0]
        for node2 in sequence[1:]:
            weight += self.graph[node1][node2]
            node1 = node2
        return weight

    def to_list(self):
        return self.patterns

    def get_graph(self):
        return self.graph