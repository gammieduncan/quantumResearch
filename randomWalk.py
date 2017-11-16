from dwave_sapi2.remote import RemoteConnection
from dwave_sapi2.core import solve_ising, solve_qubo
from random import *


url = 'https://qfe.nas.nasa.gov/sapi'
token = 'USRA-d8907d3de65f4b5c3310b584cf95948ea6665d9a'

# create a remote connection
conn = RemoteConnection(url, token)

# get the solver
solver = conn.get_solver('C16')

qubits = solver.properties.get("qubits") #list of qubits
couplers = solver.properties.get("couplers") #list of couplers

path = [] #the list of couplers in our random walk, to be written to a file
randCoupler = [] #the random coupler connected to q1

q1 = randint(qubits[0], qubits[len(qubits) - 1]) #random qubit index from range of indices

#loop until we find a qubit we've already added to path
while True: 
	#get list of couplers attached to q1
	q1Couplers = [(i,j) for i, row in enumerate(couplers) for j, elem in enumerate(row) if elem == q1]
	#assign a random coupler from that list
	randCoupler = q1Couplers[randint(0, len(q1Couplers)-1)]
	#assign q2 to be the qubit in the coupler that is not equal to q1
	q2 = randCoupler[0] if randCoupler[0] != q1 else randCoupler[1]
	#if q2 is already in the path then we breal
	if any(q2 in i for i in path):
		break
	#otherwise add it to the path and set q1 to q2
	else:
		path.append(randCoupler)
		q1 = q2

#add the last coupler to the path, the "closing" coupler of the cycle
path.append(randCoupler)

print path

#print couplers[0][0]


