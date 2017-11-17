from dwave_sapi2.remote import RemoteConnection
from dwave_sapi2.core import solve_ising, solve_qubo
from random import *

def randomWalk():

	path = [] #the list of couplers in our random walk, to be written to a file
	randCoupler = [] #the random coupler connected to q1

	q1 = randint(qubits[0], qubits[len(qubits) - 1]) #random qubit index from range of indices

	#loop until we find a qubit we've already added to path
	while True: 
		#get list of couplers attached to q1
		q1Couplers = getCouplers(q1)
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

	#finally, write to file
	#f = open('couplersFile.txt', 'w')
	
	for i in path:
		f.write("%s\n" % i) #, '\n')

	#f.close()
	print path

	#print couplers[0][0]

#returns list of couplers in c with q1 included
def getCouplers(q1):
	toReturn = []
	#iterate through the couplers, if q1 is in one of them then add to list
	for i in couplers:
		if q1 in i:
			toReturn.append(i)

	return toReturn

# have a function call it 10,000 times and fill up a file
# we now open the solver here, once, as oppposed to opening everytime in randomWalk
def generateCycles():

	url = 'https://qfe.nas.nasa.gov/sapi'
	token = 'USRA-d8907d3de65f4b5c3310b584cf95948ea6665d9a'

	# create a remote connection
	conn = RemoteConnection(url, token)

	# get the solver
	solver = conn.get_solver('C16')

	qubits = solver.properties.get("qubits") #list of qubits
	couplers = solver.properties.get("couplers") #list of couplers

	for i in range(0, 10,000):
		f.write("%s\n" % i) #include the number of the trial
      	randomWalk()
	  	f.write("\n") #make a line break after it

#open the file, generate the cycles, close the file
def main():
	filename = "couplersFile.txt"
	f = open(filename, "a+") #a+ for append
	generateCycles()
	f.close()

#f (the file), and the sets of qubits and couplers are now global variables
f, qubits, couplers = None, None, None
main()


#randomWalk()

