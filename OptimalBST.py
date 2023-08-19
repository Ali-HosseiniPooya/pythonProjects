def optCost(freq, i, j):	

	if j < i:
		return 0
	if j == i:
		return freq[i]

	fsum = Sum(freq, i, j)
	Min = 999999999999
	
	for r in range(i, j + 1):
		cost = (optCost(freq, i, r - 1) + optCost(freq, r + 1, j))
		if cost < Min:
			Min = cost

	return Min + fsum


def optimalSearchTree(keys, freq, n):
	return optCost(freq, 0, n - 1)


def Sum(freq, i, j):
	sum = 0
	for k in range(i, j + 1):
		sum += freq[k]
	return sum



if __name__ == '__main__':
	keys = [10, 15, 20]
	freq = [20, 30, 50]
	n = len(keys)
	print("Cost of Optimal BST: ", optimalSearchTree(keys, freq, n))
	