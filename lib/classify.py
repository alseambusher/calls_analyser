import parser
import config
from temp import DATA

# classifies based on noun phrases
def NP_classifier(documents):
    classification = {}
    for _id in documents.iterkeys():
        problem = documents[_id][config.table_problem]
        for NP in parser.get_NP(problem):
            try:
                classification[NP].append(_id)
            except:
                classification[NP] = [_id]
    return classification


def problem_domain_classifier(documents):
    classification = {}
    for _id in documents.iterkeys():
        domain = documents[_id][config.table_domain]
        try:
            classification[domain].append(_id)
        except:
            classification[domain] = [_id]
