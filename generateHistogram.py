import sys
import matplotlib.pyplot as plt 
from matplotlib.backends.backend_pdf import PdfPages 
import numpy as np 
#%matplotlib inline

filename = sys.argv[-1] #get the filename from command line, last arg

def generateHistogram():

	sizes = getSizes() #get the sizes of the cyles
	sizes.sort() #sort the sizes

	#with PdfPages('histogram.pdf') as pdf: #display histogram, save to pdf
	arr = plt.hist(sizes, normed=False, bins = 10)
	plt.ylabel('Frequency')
	plt.xlabel('Size')
	plt.title('Cycles Histogram')
	for i in range(10):
		plt.text(arr[1][i],arr[0][i],str(arr[0][i]))
	plt.show()


def getSizes():

	sizes = []
	numCycles = 10000

	with open(filename, 'r+') as f: #open the file
		lines = iter(f) #create an iterable version of the file

		for i in range(numCycles): #get sizes of all 10,000 cycles
			next(lines) #skip past line listing number of iteration
			count = 0

			while len(next(lines).strip()) != 0: #as long as line isn't blank, keep reading
				count += 1

			sizes.append(count) #add the size to the list

	f.close() #close the file
	return sizes #return the sizes


generateHistogram()

