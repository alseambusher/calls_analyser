import nltk
import config

# generates problem patterns
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
    def get_customer_history(self, table_column):
        customer_history = {}
        for _id in range(0, len(self.data)):
            _id = str(_id)
            try:
                customer_history[self.data[_id][config.table_cid]].append(self.data[_id][table_column])
            except:
                customer_history[self.data[_id][config.table_cid]] = [self.data[_id][table_column]]
        return customer_history

    # gets noun phrases
    @staticmethod
    def get_NP(document):
        data = []
        sentences = nltk.sent_tokenize(document)
        sentences = [nltk.word_tokenize(sent) for sent in sentences]
        sentences = [nltk.pos_tag(sent) for sent in sentences][0]
        grammar = "NP: {<JJ>*<NN|NNP|CD>*}"
        cp = nltk.RegexpParser(grammar)
        nlp_tree = cp.parse(sentences)
        for _node in nlp_tree:
            try:
                if _node.node is "NP":
                    data.append(" ".join([_word[0] for _word in _node]))
            except:
                pass
        return data

    # pass column index construct graph
    def get_column_chain_graph(self, table_column):
        customer_history = self.get_customer_history(table_column)
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
        # todo fix this
        graph = {}
        # get problem history of each customer
        customer_history = self.get_customer_history(config.table_problem)
        for history in customer_history.itervalues():
            prev_problem = None
            NP_prev_problem = None
            for problem in history:
                if problem is not u'':
                    NP_problem = self.get_NP(problem)
                    if prev_problem is not None:
                        for phrase1 in NP_prev_problem:
                            for phrase2 in NP_problem:
                                print phrase1, phrase2
                                try:
                                    graph[phrase1][phrase2] += 1
                                except:
                                    graph[phrase1] = dict({phrase2: 1})
                    prev_problem = problem
                    NP_prev_problem = NP_problem
        return graph


    def get_problem_subgraphs(self, length):
        patterns = []
        for node in self.graph.iterkeys():
            patterns.extend(self.get_longest_pattern(node, [node], length - 1))

        return sorted(patterns, key=self.sequence_to_weight, reverse=True)

    def get_longest_pattern(self, node, sequence, length):
        patterns = []
        for adj in self.graph[node].iterkeys():
            # if last node permittable is supposed to be added OR
            # if you have reached leaf nodes
            if length == 1 or len(self.graph[adj]) == 0:
                # discard the sequence below weight limit
                if self.sequence_to_weight(sequence+[adj]) > self.weight_min:
                    patterns.append(sequence+[adj])
            # if you have encountered a cycle and have already entered the cycle, skip it
            elif ("".join(sequence)).find(sequence[-1]+adj) is not -1:
                patterns.append(sequence)
            #elif sequence[-1] == adj and len(sequence) > 1 and sequence[-2] == sequence[-1]:
                #patterns.append(sequence)
                #patterns.extend(self.get_longest_pattern(adj, sequence, length))
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

