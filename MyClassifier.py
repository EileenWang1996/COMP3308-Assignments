import sys 
import collections 
import numpy as np
import csv

def compute_pdf(x, mu, sigma):
	'''Computes probability density function given x,mu and sigma.'''
	x = float(x)
	prob = (1/(sigma*np.sqrt(2*np.pi)))*np.exp((-1*np.square(x-mu))/(2*np.square(sigma)))
	return prob
	
def compute_stats(data, number_of_att): 
	'''Compute mean and standard deviations.'''
	attribute_means = [0]*number_of_att
	for i in range(0, len(data)):
		for j in range(0,number_of_att):
			attribute_means[j] += float(data[i][j])
	attribute_means = [x/len(data) for x in attribute_means]

	attribute_sum_of_squares = [0]*number_of_att
	for i in range(0, len(data)):
		for j in range(0,number_of_att):
			attribute_sum_of_squares[j] += np.square(float(data[i][j]) - attribute_means[j])
	attribute_sd = [np.sqrt(x/(len(data)-1)) for x in attribute_sum_of_squares]
	
	return attribute_means, attribute_sd
	
def run_naive_bayes(data, newExample, number_of_att):
	'''Classifies the new example using naive bayes algorithm.'''
	data_yes = [] #stores the observations that are yes 
	data_no = [] #stores the observatoins that are no
	for i in range(0, len(data)): 
		if data[i][-1] == "yes":
			data_yes.append(data[i])
		else:
			data_no.append(data[i])
	yes_attribute_means, yes_attribute_sd = compute_stats(data_yes, number_of_att)
	no_attribute_means, no_attribute_sd = compute_stats(data_no, number_of_att)
	
	#compute probabilities.
	yes_prob = len(data_yes)/len(data)
	no_prob = len(data_no)/len(data)
	yes_att_probs = []
	no_att_probs = []
	for i in range(0, number_of_att):
		yes_att_probs.append(compute_pdf(newExample[i], yes_attribute_means[i], yes_attribute_sd[i]))
		no_att_probs.append(compute_pdf(newExample[i], no_attribute_means[i], no_attribute_sd[i]))
	
	yes_prob_E = yes_prob * np.prod(yes_att_probs) 
	no_prob_E = no_prob * np.prod(no_att_probs)
	
	if yes_prob_E >= no_prob_E:
		return "yes"
	else:
		return "no"
	
	
def compute_dist(attributes, newExample, number_of_att):
	'''Computes the euclidean distance between observation and new example.'''
	sum_of_squares = 0
	for i in range(0, number_of_att):
		sum_of_squares += np.square(float(attributes[i]) - float(newExample[i]))
	distance = np.sqrt(sum_of_squares)
	return distance 

def run_knn(k, data, newExample, number_of_att): 
	'''Classify new examples using k-nearest algorithm.'''
	
	euclidean_dists = [] 
	attributes = []
	
	for i in range(0, len(data)): #iterate over rows 
		attributes = [] #stores the attributes and the class 
		for j in range(0, number_of_att+1): 
			attributes.append(data[i][j]) #grab the attributes of each row 
		distance = compute_dist(attributes, newExample, number_of_att)
		euclidean_dists.append((distance, attributes[-1])) #append class and distance from that observation
		
	sorted_euclidean_dists = sorted(euclidean_dists, key=lambda x: x[0]) #sort distances from smallest to largest
	#print(sorted_euclidean_dists)
	count_yes = 0
	count_no = 0
	for i in range(0, k):
		if sorted_euclidean_dists[i][1] == "yes": 
			count_yes += 1
		else:
			count_no += 1
	if count_yes >= count_no: #break ties by choosing yes 
		return "yes"
	else:
		return "no"

def compute_accuracy(k, folds, number_of_att):
	'''Computes classification accuracy of classifiers.'''
	train, test = [], []
	knn_accuracy = [0] * 10
	nb_accuracy = [0] * 10
	for i in range(0, len(folds)): 
		test = folds[i]
		train = []
		for j in range(0, len(folds)): 
			if j != i: 
				train += folds[j]
		for n in range(0, len(test)):
			if k != -1: #if this is true, then we are using NB.
				result = run_knn(k, train, test[n][0:number_of_att], number_of_att)
				if result == test[n][-1]: #if classification is correct 
					knn_accuracy[i] += 1 
			result = run_naive_bayes(train, test[n][0:number_of_att],number_of_att)
			if result == test[n][-1]:
				nb_accuracy[i] += 1
	
	#compute accuracy as percentage 
	for i in range(0, len(folds)): 
		knn_accuracy[i] = knn_accuracy[i]/len(folds[i])
		nb_accuracy[i] = nb_accuracy[i]/len(folds[i])
	
	knn_acc = sum(knn_accuracy)/len(knn_accuracy) * 100
	nb_acc = sum(nb_accuracy)/len(nb_accuracy) * 100
	return knn_acc, nb_acc 
	
def write_folds(folds, number_of_att):
	'''Write the stratified cv folds to a csv file.'''
	cvFolds = open("pima-folds.csv", "w")
	counter = 1 
	for fold in folds: #for each fold 
		cvFolds.write("fold" + str(counter) + "\n")
		for obs in fold: #for each observation in each fold 
			for i in range(0, number_of_att + 1): 
				if i == number_of_att:
					cvFolds.write("%s\n" % obs[i])
				else:
					cvFolds.write("%s," % obs[i])
		cvFolds.write("\n")
		counter += 1

def get_10folds(data, number_of_att): 
	'''Creates 10 folds for stratified 10-fold cross-validation.'''
	data_yes = [] #stores the observations that are yes 
	data_no = [] #stores the observatoins that are no
	for i in range(0, len(data)): 
		if data[i][-1] == "yes":
			data_yes.append(data[i])
		else:
			data_no.append(data[i])
	
	fold1, fold2, fold3, fold4, fold5, fold6, fold7, fold8, fold9, fold10 = [], [], [], [], [], [], [], [], [], []
	counter = 1
	
	for i in range(0, len(data_yes)): 
		if counter == 1: 
			fold1.append(data_no[i])
			fold1.append(data_yes[i])
		if counter == 2: 
			fold2.append(data_no[i])
			fold2.append(data_yes[i])
		if counter == 3: 
			fold3.append(data_no[i])
			fold3.append(data_yes[i])
		if counter == 4: 
			fold4.append(data_no[i])
			fold4.append(data_yes[i])
		if counter == 5: 
			fold5.append(data_no[i])
			fold5.append(data_yes[i])
		if counter == 6: 
			fold6.append(data_no[i])
			fold6.append(data_yes[i])
		if counter == 7: 
			fold7.append(data_no[i])
			fold7.append(data_yes[i])
		if counter == 8: 
			fold8.append(data_no[i])
			fold8.append(data_yes[i])
		if counter == 9: 
			fold9.append(data_no[i])
			fold9.append(data_yes[i])
		if counter == 10: 
			fold10.append(data_no[i])
			fold10.append(data_yes[i])
			counter = 0
		counter += 1
	
	for i in range(len(data_yes), len(data_no)): 
		if counter == 1: 
			fold1.append(data_no[i])
		if counter == 2: 
			fold2.append(data_no[i])
		if counter == 3: 
			fold3.append(data_no[i])
		if counter == 4: 
			fold4.append(data_no[i])
		if counter == 5: 
			fold5.append(data_no[i])
		if counter == 6: 
			fold6.append(data_no[i])
		if counter == 7: 
			fold7.append(data_no[i])
		if counter == 8: 
			fold8.append(data_no[i])
		if counter == 9: 
			fold9.append(data_no[i])
		if counter == 10: 
			fold10.append(data_no[i])
			counter = 0
		counter += 1
	folds = [fold1, fold2, fold3, fold4, fold5, fold6, fold7, fold8, fold9, fold10]
	write_folds(folds, number_of_att)
	return folds 
	
def main(): 
	
	if len(sys.argv) != 4: 
		print("Not enough arguments!")
		return 
	
	fileName1 = sys.argv[1] #pima.csv 
	fileName2 = sys.argv[2] #to be classified 
	algorithm = sys.argv[3] #either kNN or NaiveBayes 
	
	data = []
	with open(fileName1, 'r') as f: #stores the pima dataset 
		reader = csv.reader(f)
		data = list(reader)

	examples = []
	with open(fileName2, 'r') as f: #new points to be classified )
		reader = csv.reader(f)
		examples = list(reader)
	
	number_of_att = len(data[0])-1
	
	k = -1
	if algorithm != "NB": #knn case 
		k_string = "" #extract k from command line arguments. 
		for character in algorithm: 
			if character.isdigit(): 
				k_string += character 
			else:
				break
		k = int(k_string)
		for i in range(0, len(examples)):
			print(run_knn(k, data, examples[i], number_of_att))
	else: 
		for i in range(0, len(examples)):
			print(run_naive_bayes(data, examples[i], number_of_att))
	
	compute_acc = True
	if compute_acc == True: 
		folds = get_10folds(data, number_of_att)
		knn_acc, nb_acc = compute_accuracy(k, folds, number_of_att)
		print(knn_acc, nb_acc)
		
if __name__ == "__main__": 
	main() 
