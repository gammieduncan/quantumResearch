from dwave_sapi2.remote import RemoteConnection
from dwave_sapi2.core import solve_ising, solve_qubo
from random import *

filename = "cycles.txt"
filename = "cycles.txt" #file for the paths of couplers
f = open(filename, "a+")

def randomWalk(qubits, couplers):

	path = [] #the list of couplers in our random walk, to be written to a file
	randCoupler = [] #the random coupler connected to q1
	
	q1 = randint(qubits[0], qubits[len(qubits) - 1]) #random qubit index from range of indices

	q1Couplers = []

	#check to make sure there are couplers the random qubit's attached to
	while len(q1Couplers) == 0:
		q1 = randint(qubits[0], qubits[len(qubits) - 1]) #random qubit index from r$
		q1Couplers = getCouplers(couplers, q1)

	randCoupler = []

	#loop until we find a qubit we've already added to path
	while True:

		#assign a random coupler from that list
		while True:
			randCoupler = q1Couplers[randint(0, len(q1Couplers)-1)]		
			if checkCoupler(randCoupler, path):
				break			

		#assign q2 to be the qubit in the coupler that is not equal to q1
		q2 = randCoupler[0] if randCoupler[0] != q1 else randCoupler[1]
	
		randCoupler = [q1, q2] #reformat coupler so q1 is always first

		#if q2 is already in the path then we break, we've found a cycle
		if any(q2 in i for i in path):
			path = trimPath(q2, path)
			break

		#otherwise add it to the path and set q1 to q2
		else:
			path.append(randCoupler)
			q1 = q2
			q1Couplers = getCouplers(couplers, q1)

	#add the last coupler to the path, the "closing" coupler of the cycle
	path.append(randCoupler)
	
	print path

	for i in path:
		f.write("%s\n" % i) #, '\n')

	#record the length
	#f.write("%s\n" % len(randCouplers)) 

#check if this is a valid random coupler to branch off to
def checkCoupler(randCoupler, path):

	for i in path:  #go thru every coupler in path
		if set(randCoupler) == set(i):  #if randCoupler has same elements as some i
			return False  #then return false
	
	return True

#trim the path so it's only the cycle without a "tail"
def trimPath(q2, path):
	
	for i in path:  #examine each coupler
		if i[0] == q2:    #if the coupler's q1 index = q2
			ind = path.index(i)
			path = path[ind:]    #then slice path from i-end
			break

	return path

#returns list of couplers in c with q1 included
def getCouplers(couplers, q1):
	
	toReturn = []
	
	#iterate through the couplers, if q1 is in one of them then add to list
	for i in couplers:
		if q1 in i:
			toReturn.append(i)

	return toReturn


#returns the solver after setting up the connection
def setUpConnection():

 	url = 'https://qfe.nas.nasa.gov/sapi'
	token = 'USRA-d8907d3de65f4b5c3310b584cf95948ea6665d9a'

	# create a remote connection
	conn = RemoteConnection(url, token)

    	# get the solver
    	solver = conn.get_solver('C16')

	return solver

		
# have a function call it 10,000 times and fill up a file
# we now open the solver here, once, as oppposed to opening everytime in randomWalk
def generateCycles():

	solver = setUpConnection() #grab the solver

	couplers = solver.properties.get("couplers") #list of couplers
	qubits = solver.properties.get("qubits")

	print qubits 
	
	size = 10000
	#size = 100
	for j in range(int(size)):
		f.write("%s\n" % j) #records which cycle # it is
		randomWalk(qubits, couplers)
		f.write("\n")


#open the file, generate the cycles, close the file
def main():
	generateCycles()
	f.close()


main()



