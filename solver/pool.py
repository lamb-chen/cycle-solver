import json
from collections import namedtuple

# the donors act as the nodes!
class Donor(object):
    def __init__(self, dage, id):
        self.dage = dage
        self.id = id
        self.paired_patients = []
        
class Altruist(object):
    def __init__(self, dage, id):
        self.dage = dage
        self.id = id
        self.paired_patients = []
        self.out_edges = []

class Patient(object):
    def __init__(self, id):
        self.id = id
        self.paired_donors = []

class Cycle(object):
    def __init__(self, pd_pairs):
        self.pd_pairs = pd_pairs

class Pool:
    def __init__(self):
        self.patients = {}
        self.altruists = {}
        self.paired_donors = {}
        self.edges = {}  # {donor_id: [(recipient_id, score)]}
    
    def find_cycles(self, max_cycle_length):
        cycles = []
        for initial_donor in self.paired_donors.values():
            initial_donor_id = initial_donor.id
            for curr_patient in initial_donor.paired_patients:
                initial_dp_pair = DonorPatientPair(initial_donor_id, curr_patient)
                out_edges = self.get_out_edges(initial_donor_id)
                for out_edge in out_edges:


    def add_edge(self, donor_id, recipient_id, score):
        if donor_id not in self.edges:
            self.edges[donor_id] = []
        self.edges[donor_id].append(RecipientWithScore(recipient_id, score))

    def get_out_edges(self, donor_id):
        return self.edges.get(donor_id, [])

    def get_in_edges(self, donor_id):
        in_edges = []
        if donor_id in self.paired_donors:
            curr_donor = self.paired_donors[donor_id]
            for patient in curr_donor.paired_patients:
                for donor_id, edges in self.edges.items():
                    for edge in edges:
                        if edge.recipient_patient == patient:
                            in_edges.append((donor_id, edge.score))
            return in_edges

    def add_altruists(self, altruist):
        self.altruists.append(altruist)

def print_edges(pool):
    print("\nDonor Edges:")
    for donor_id in pool.edges:
        out_edges = pool.get_out_edges(donor_id)
        in_edges = pool.get_in_edges(donor_id)
        
        print(f"Donor ID: {donor_id}")
        
        print("  Out-Edges:")
        for recipient_id, score in out_edges:
            print(f"    -> Recipient ID: {recipient_id}, Score: {score}")
        
        print("  In-Edges:")
        if in_edges:
            for donor, score in in_edges:
                print(f"    <- From Donor ID: {donor}, Score: {score}")
        else: print(f"    None")

DonorPatientPair = namedtuple('DonorPatientPair', ['donor', 'patient'])
RecipientWithScore = namedtuple('RecipientWithScore', ['recipient_patient', 'score'])

# reading from test.json and creating pool graph
with open("test.json") as dataset_json:
    json_data = json.load(dataset_json)["data"]

    pool = Pool()
    seen_patient_ids = set()
    for donor_id in json_data:
        dage = int(json_data[donor_id]["dage"])
        
        is_altruistic = "altruistic" in json_data[donor_id] and json_data[donor_id]["altruistic"]
        if is_altruistic:
            altruist = Altruist(dage, donor_id)
            for matched_patient in json_data[donor_id]["matches"]:
                recipient_patient_id = matched_patient["recipient"]
                if recipient_patient_id not in seen_patient_ids: 

                    patient = Patient(recipient_patient_id)
                    pool.patients[recipient_patient_id] = patient
                    seen_patient_ids.add(recipient_patient_id)
                # add to altruist an outgoing edge to the recipient patient 
                # with the score 
                score = int(matched_patient["score"])
                pool.add_edge(donor_id, recipient_patient_id, score)
            pool.altruists[donor_id] = altruist
        else:
            donor = Donor(dage, donor_id)
            for paired_patient_id in json_data[donor_id]["sources"]:
                donor.paired_patients.append(paired_patient_id)
                if paired_patient_id not in seen_patient_ids: 
                    patient = Patient(paired_patient_id)
                    pool.patients[paired_patient_id] = patient
                    seen_patient_ids.add(paired_patient_id)
                else:
                    patient = pool.patients[paired_patient_id]
                    patient.paired_donors.append(donor_id)
            if "matches" in json_data[donor_id]:
                for matched_patient in json_data[donor_id]["matches"]:
                    recipient_patient_id = matched_patient["recipient"]
                    if recipient_patient_id not in seen_patient_ids: 
                        patient = Patient(recipient_patient_id)
                        pool.patients[recipient_patient_id] = patient
                        seen_patient_ids.add(recipient_patient_id)
                    # the graph is really going from donors to recipient patients 
                    # with source patients attached to the donors representing 
                    # an individual node
                    score = int(matched_patient["score"])
                    pool.add_edge(donor_id, recipient_patient_id, score)
            pool.paired_donors[donor_id] = donor
# Print out the results of the Pool
print("Altruists:")
for altruist_id, altruist in pool.altruists.items():
    print(f"Altruist ID: {altruist.id}, Age: {altruist.dage}")
    for edge in pool.get_out_edges(altruist.id):
        print(f"  -> Recipient ID: {edge.recipient_patient}, Score: {edge.score}")

print("\nPatients:")
for patient_id, patient in pool.patients.items():
    print(f"Patient ID: {patient_id}")

print("\nPaired Donors:")
for donor_id, donor in pool.paired_donors.items():
    print(f"Donor ID: {donor.id}, Age: {donor.dage}")
    for patient_id in donor.paired_patients:
        print(f"  -> Paired Patient ID: {patient_id}")
    for edge in pool.get_out_edges(donor.id):
        print(f"  -> Recipient ID: {edge.recipient_patient}, Score: {edge.score}")

print_edges(pool)