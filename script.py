import sys
sys.path.append(path)
import GA
reload(GA)
from GA import DNA


import pickle


if flag == "run":

	with open(path + "process.pkl", 'rb') as f:
		process = pickle.load(f)

	if active and process["bestScore"] < 1.0:

		print "ACTIVE"
		
		with open(path + "data.pkl", 'rb') as f:
			data = pickle.load(f)
		
		i = process["design"]

		process["population"][i].update_fitness(data)
		print process["population"][i].fitness
		
		if process["population"][i].fitness > process["bestScore"]:
			process["bestDesign"] = process["population"][i].getPhrase()
			process["bestScore"] = process["population"][i].fitness
		
		process["design"] += 1
		
		if process["design"] > len(process["population"]) - 1:
			process["generation"] += 1
			process["design"] = 0
			
			matingPool = []
			
			population = process["population"][:]
			
			process["population"] = []
			
			for i in range(len(population)):
				n = int(population[i].fitness * 100)
				for j in range(n):
					matingPool.append(population[i])
				
			for i in range(len(population)):
				a = random.choice(range(len(matingPool)))
				b = random.choice(range(len(matingPool)))
				
				parentA = matingPool[a]
				parentB = matingPool[b]
				print parentA.getPhrase()
				print parentB.getPhrase()
				child = parentA.crossover(parentB)
				child.mutate()
				print child.getPhrase()
				
				process["population"].append(child)
		
		
		with open(path + "process.pkl", 'wb') as f:
			pickle.dump(process, f, pickle.HIGHEST_PROTOCOL)
		
	if reset:

		print ""
		
		process = {"population": [], "generation": 0, "design": 0, "bestScore": 0, "bestDesign": ""}
		
		for i in range(int(pop)):
		   process["population"].append(DNA())
		
		with open(path + "process.pkl", 'wb') as f:
			pickle.dump(process, f, pickle.HIGHEST_PROTOCOL)

	output = pickle.dumps(process)

if flag == "print":

	process = pickle.loads(input)

	print "Generation: " + str(process["generation"])
	print "Current design: " + str(process["design"])
	print "Best design: " + str(process["bestDesign"])
	print "Best score: " + str(process["bestScore"])
	print " "
	print "Designs:"

	for i in range(len(process["population"])):
	    print i, ": ", process["population"][i].getPhrase(), ": ", process["population"][i].fitness

if flag == "extract":
	process = pickle.loads(input)

	i = process["design"]

	design = process["population"][i].getPhrase()

	print process["population"][i].fitness

if flag == "score":
	score = 0

	for i in range(len(design)):
	    if design[i] == target[i]:
	        score += 1

	fitness = float(score)/len(target)

if flag == "export":
	if active:
	    with open(path + "data.pkl", 'w') as f:
	        pickle.dump(data, f)