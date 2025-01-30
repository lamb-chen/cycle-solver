from collections import namedtuple

class Pool(object):
    def __init__(self):
        self.altruists = []
        self.donor_patient_pair_nodes = []
    
    def add_donor_patient_node(self, donor_patient_node):
        self.donor_patient_pair_nodes.append(donor_patient_node)
     

class Donor(object):
    def __init__(self, dage, id):
        self.dage = dage
        self.id = id

class Altruist(object):
    def __init__(self, dage, id):
        self.edges = []
        self.dage = dage
        self.id = id

class AltruistEdge(object):
    def __init__(self, altruist, recipient, score):
        self.altruist = altruist
        self.recipient = recipient
        self.score = score

class Patient(object):
    def __init__(self, id, index):
        self.paired_donors = []
        self.id = id
        self.index = index

# donor patient pair = DPP
class DPPEdge(object):
    def __init__(self, recipient_pair, score):
        self.recipient = recipient_pair
        self.score = score

class DonorPatientPairNode(object):
    def __init__(self, donor, patient):
        self.pair = DonorPatientPair(donor, patient)



DonorPatientPair = namedtuple('DonorPatientPair', ['donor', 'patient'])


class Edge:
    def __init__(self, target, weight):
        self.target = target
        self.weight = weight

class Node:
    def __init__(self, name):
        self.name = name
        self.edges = []

    def add_edge(self, target, weight):
        self.edges.append(Edge(target, weight))

class Graph:
    def __init__(self):
        self.nodes = {}

    def add_node(self, name):
        self.nodes[name] = Node(name)

    def add_edge(self, source, target, weight):
        if source not in self.nodes:
            self.add_node(source)
        if target not in self.nodes:
            self.add_node(target)
        self.nodes[source].add_edge(target, weight)