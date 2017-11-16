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

print couplers[0][0]
