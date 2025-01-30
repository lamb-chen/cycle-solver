import json
from collections import namedtuple

class DonorPatientEdge:
    def __init__(self, donor_recipient_pair, weight):
        self.recipient = donor_recipient_pair
        self.weight = weight

class DonorPatientNode:
    def __init__(self, donor_patient_pair):
        self.donor_patient_pair = donor_patient_pair
        self.edges = []

    def add_edge(self, donor_recipient_pair, weight):
        self.edges.append(DonorPatientEdge(donor_recipient_pair, weight))

class Donor(object):
    def __init__(self, dage, id):
        self.dage = dage
        self.id = id
        self.altruistic = False

class Patient(object):
    def __init__(self, id):
        self.id = id

class Pool:
    def __init__(self):
        self.donor_patient_nodes =[]
        self.altruists = []

    def add_donor_patient_node(self, donor_patient_pair):
        self.donor_patient_nodes.append(DonorPatientNode(donor_patient_pair))
    
    def add_altruists(self, altruist):
        self.altruists.append(altruist)

    def add_edge(self, donor_patient_pair, donor_recipient_pair, weight):
        if donor_patient_pair not in self.donor_patient_nodes:
            self.add_donor_patient_node(donor_patient_pair)
        if donor_recipient_pair not in self.donor_patient_nodes:
            self.add_donor_patient_node(donor_recipient_pair)
        self.donor_patient_nodes[donor_patient_pair].add_edge(donor_recipient_pair, weight)

DonorPatientPair = namedtuple('DonorPatientPair', ['donor', 'patient'])

# with open("test.json") as dataset_json:
#     json_data = json.load(dataset_json)["data"]

#     created_ids = set()
#     pool = Pool()
#     for id in json_data:
#         dage = json_data[id]["dage"]
#         is_altruistic = json_data[id].has_key("altruistic") and json_data[id]["altruistic"]
#         if is_altruistic:
#             altruist = Donor(int(dage), int(id), True)
#             pool.altruists.append(altruist)
#         else:
#             donor = Donor(int(dage), int(id), False)
#             for patient_id in json_data[id]["sources"]:
#                 patient = Patient(int(patient_id))
#                 donor_patient_pair = DonorPatientPair(donor, patient)
#                 pool.add_donor_patient_node(donor_patient_pair)
#             for matched_recipient in json_data[id]["matches"]:
#                 recipient_id = matched_recipient["id"]
#                 recipient = Patient(int(recipient_id))
#                 donor_patient_pair = DonorPatientPair(donor, recipient)
#                 pool.add_donor_patient_node(donor_patient_pair)
#                 for donor_recipient_pair in matched_recipient["matches"]:
#                     recipient_id = donor_recipient_pair["id"]
#                     recipient = Patient(int(recipient_id))
#                     donor_recipient_pair = DonorPatientPair(donor, recipient)
#                     pool.add_edge(donor_patient_pair, donor_recipient_pair, donor_recipient_pair["score"])

