import sys
import matplotlib.pyplot as plt 
from matplotlib.backends.backend_pdf import PdfPages 
from matplotlib.ticker import FormatStrFormatter
import numpy as np 
import pandas as pd 
from itertools import groupby
#%matplotlib inline

filename = sys.argv[-1] #get the filename from command line, last arg

def generateHistogram():

	sizes = getSizes() #get the sizes of the cyles
	sizes.sort() #sort the sizes

	generatePlot(sizes)


def generatePlot(sizes):

	sizeSet = set(sizes)
	sizeSetList = list(sizeSet)

	sizeFrequencyList = [len(list(group)) for key, group in groupby(sizes)]
	print sizeFrequencyList

	#with PdfPages('histogram.pdf') as pdf: #display histogram, save to pdf
	fig, ax = plt.subplots()
	counts, bins, patches = plt.hist(sizes, normed=False, bins = len(sizeFrequencyList))
	plt.ylabel('Frequency')
	plt.xlabel('Size')
	plt.title('Cycles Histogram')
	# Set the ticks to be at the edges of the bins.
	ax.set_xticks(sizeSetList)

	for i in range(len(sizeFrequencyList)):
		plt.text(bins[i], sizeFrequencyList[i], str(sizeFrequencyList[i]), fontsize = 6)

	print bins
	# Set the xaxis's tick labels to be formatted with 1 decimal place...
	#ax.xaxis.set_major_formatter(FormatStrFormatter('%0.1f'))

	plt.setp(ax.get_xticklabels(), rotation='vertical', fontsize=6)

	twentyfifth, seventyfifth = np.percentile(sizes, [25, 75])
	for patch, rightside, leftside in zip(patches, bins[1:], bins[:-1]):
		if rightside < twentyfifth:
			patch.set_facecolor('green')
		elif leftside > seventyfifth:
			patch.set_facecolor('red')

	
	# Give ourselves some more room at the bottom of the plot
	plt.subplots_adjust(bottom=0.1)
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

