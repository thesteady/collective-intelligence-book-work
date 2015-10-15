# From Ch2: Making Recommendations
# a dictionary of movie critics and their ratings of a samll set of movies
from math import sqrt

critics = {
	'Lisa Rose': {
		'Lady in the Water': 2.5,
		'Snakes on a Plane': 3.5,
		'Just My Luck': 3.0,
		'Superman Returns': 3.5,
		'You, Me and Dupree': 2.5,
		'The Night Listener': 3.0
	},
	'Gene Seymour': {
		'Lady in the Water': 3.0,
		'Snakes on a Plane': 3.5,
		'Just My Luck': 1.5,
		'Superman Returns': 5.0,
		'The Night Listener': 3.5,
		'You, Me and Dupree': 3.0
	},
	'Michael Phillips': {
		'Lady in the Water': 2.5,
		'Snakes on a Plane': 3.0,
		'Superman Returns': 3.5,
		'The Night Listener': 4.0
	},
	'Claudia Piug': {
		'Snakes on a Plane': 3.5,
		'Just My Luck': 3.0,
		'The Night Listener': 4.5,
		'Superman Returns': 4.0,
		'You, Me and Dupree': 2.5
	},
	'Mick LaSalle': {
		'Lady in the Water': 3.0,
		'Snakes on a Plane': 4.0,
		'Just My Luck': 2.0,
		'Superman Returns': 3.0,
		'The Night Listener': 3.0,
		'You, Me and Dupree': 2.0
	},
	'Jack Matthews': {
		'Lady in the Water': 3.0,
		'Snakes on a Plane': 4.0,
		'The Night Listener': 3.0,
		'Superman Returns': 5.0,
		'You, Me and Dupree': 3.5
	},
	'Toby': {
		'Snakes on a Plane': 4.5,
		'You, Me and Dupree': 1.0,
		'Superman Returns': 4.0
	}
}

#my refactoring of shared code in the distance methods
def gather_shared_items(prefs, person1, person2):
	shared_items = {}
	for item in prefs[person1]:
		if item in prefs[person2]:
			shared_items[item]=1

	return shared_items

# Return distance-based similarity score for person1 and person2
# Euclidean
def sim_distance(prefs, person1, person2):
	# get list of shared items
	shared_items = gather_shared_items(prefs, person1, person2)
	# if no ratings in common, return 0
	if len(shared_items)==0: return 0

	# add up squares of all the differences
	sum_of_squares= sum([pow(prefs[person1][item] - prefs[person2][item], 2) for item in shared_items])
	return 1/(1+sqrt(sum_of_squares))


# Returns Pearson correlation coefficient for p1 and person2
def sim_pearson(prefs, person1, person2):
	p1prefs = prefs[person1]
	p2prefs = prefs[person2]

	shared_items = gather_shared_items(prefs, person1, person2)

	# find length of shared items
	n = len(shared_items)
	# if nothing in common, return 0
	if n == 0: return 0

	# Add up all preferences
	sum1 = sum([p1prefs[item] for item in shared_items])
	sum2 = sum([p2prefs[item] for item in shared_items])

	# Sum up squares
	sum1Sq = sum([pow(p1prefs[item], 2) for item in shared_items])
	sum2Sq = sum([pow(p2prefs[item], 2) for item in shared_items])

	# sum up products
	pSum = sum([p1prefs[item] * p2prefs[item] for item in shared_items])

	#Calculate Pearson score
	num = pSum - (sum1 * sum2 / n)
	den = sqrt( (sum1Sq - pow(sum1, 2)/ n) * (sum2Sq - pow(sum2, 2) / n))
	if den == 0: return 0;

	r = num/den
	return r

# best matches for person from the prefs dict. # results and similarity function are optional params
def topMatches(prefs, person, n=5, similarity=sim_pearson):
	scores = [(similarity(prefs, person, other), other) for other in prefs if other != person]

	#sort list so highest scores at top
	scores.sort()
	scores.reverse()
	return scores[0:n]

# gets recommendations for a person by using a weighted average of every other user's rankings
def getRecommendations(prefs, person, similarity=sim_pearson):
	totals = {}
	simSums = {}
	for other in prefs:
		#dont compare person to themselves
		if other == person: continue
		sim = similarity(prefs, person, other)

		# ignore scores of 0 or <
		if sim <= 0: continue
		for item in prefs[other]:

			# only score movies i haven't seen yet
			if item in prefs[person] or prefs[person][item] == 0:
				#Similarity * Score
				totals.setdefault(item, 0)
				totals[item] += prefs[other][item] * sim

				#sum of similarities
				simSums.setdefault(item, 0)
				simSums[item] =+ sim

	# create normalized list:
	rankings = [ (total/simSums[item], item) for item, total in totals.items()]

	# return sorted list
	rankings.sort()
	rankings.reverse()
	return rankings
