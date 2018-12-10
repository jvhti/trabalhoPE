from pymongo import MongoClient
import matplotlib.pyplot as plt
import json

client = MongoClient('mongodb://localhost:27017')

def RepresentsInt(s):
	# https://stackoverflow.com/questions/1265665/how-can-i-check-if-a-string-represents-an-int-without-using-try-except
    try: 
        int(s)
        return True
    except ValueError:
        return False

db = client.pe
games = db.games
gamesList = games.find({})

listOfTypes = {}
totalCount = {"withSteamData": 0, "total": 0, "free": 0}
requiredAge = {}
categoryCountPerGame = {}
categoryList = {}
genreCountPerGame = {}
genreList = {}
releaseDate = {}
releaseYear = {"NaN": 0}
releasedState = {}

platforms = {'windows': 0, 'mac': 0, 'linux': 0, 'windows&linux': 0, 'windows&mac': 0, 'mac&linux': 0, 'windows&mac&linux': 0}
platformsPerGame = {0: 0, 1: 0, 2: 0, 3: 0}

developersList = {}
developersPerGame = {}

publishersList = {}
publishersPerGame = {}

publishersVsDevelopers = {}

moviesCount = {}
screenshootsCount = {}

achievementsCount = {}

for g in gamesList:
	totalCount['total'] += 1;
	if not(g): continue
	if ('steamdata' in g):
		steamData = g['steamdata']
		if (steamData == "None" or not(steamData)) : continue
		
		totalCount['withSteamData'] += 1;

		if(steamData["is_free"]):
			totalCount['free'] += 1;			

		if steamData['type'] in listOfTypes:
			listOfTypes[steamData['type']] += 1
		else:
			listOfTypes[steamData['type']] = 1

		if steamData['required_age'] in requiredAge:
			requiredAge[steamData['required_age']] += 1
		else:
			requiredAge[steamData['required_age']] = 1

		if('categories' in steamData):
			ccPg = len(steamData['categories'])

			if ccPg in categoryCountPerGame:
				categoryCountPerGame[ccPg] += 1
			else:
				categoryCountPerGame[ccPg] = 1

			for cat in steamData['categories']:

				if cat['description'] in categoryList:
					categoryList[cat['description']] += 1
				else:
					categoryList[cat['description']] = 1

		if('genres' in steamData):
			gcpG = len(steamData['genres'])

			if gcpG in genreCountPerGame:
				genreCountPerGame[gcpG] += 1
			else:
				genreCountPerGame[gcpG] = 1

			for cat in steamData['genres']:

				if cat['description'] in genreList:
					genreList[cat['description']] += 1
				else:
					genreList[cat['description']] = 1

		if(steamData['release_date']['date'] in releaseDate):
			releaseDate[steamData['release_date']['date']] += 1
		else: 
			releaseDate[steamData['release_date']['date']] = 1

		rY = (steamData['release_date']['date'])[-4:]
		if(RepresentsInt(rY) and not(steamData['release_date']['coming_soon'])):
			if(rY in releaseYear):
				releaseYear[rY] += 1
			else: 
				releaseYear[rY] = 1
		else:
			releaseYear["NaN"] += 1

		if(steamData['release_date']['coming_soon'] in releasedState):
			releasedState[steamData['release_date']['coming_soon']] += 1
		else: 
			releasedState[steamData['release_date']['coming_soon']] = 1

		if('platforms' in steamData):
			pQnt = 0
			p = steamData['platforms']
			if(p['windows'] == True):
				pQnt += 1
				platforms['windows'] += 1
			if(p['mac'] == True):
				pQnt += 1
				platforms['mac'] += 1
			if(p['linux'] == True):
				pQnt += 1
				platforms['linux'] += 1

			if(p['windows'] and p['mac']):
				platforms['windows&mac'] += 1
			if(p['windows'] and p['linux']):
				platforms['windows&linux'] += 1
			if(p['mac'] and p['linux']):
				platforms['mac&linux'] += 1
			if(p['windows'] and p['mac'] and p['linux']):
				platforms['windows&mac&linux'] += 1

			platformsPerGame[pQnt] += 1

		if('developers' in steamData):
			dC = len(steamData['developers'])

			if dC in developersPerGame:
				developersPerGame[dC] += 1
			else:
				developersPerGame[dC] = 1

			for dev in steamData['developers']:

				if dev in developersList:
					developersList[dev] += 1
				else:
					developersList[dev] = 1

		if('publishers' in steamData):
			dP = len(steamData['publishers'])

			if dP in publishersPerGame:
				publishersPerGame[dP] += 1
			else:
				publishersPerGame[dP] = 1

			for pub in steamData['publishers']:

				if pub in publishersList:
					publishersList[pub] += 1
				else:
					publishersList[pub] = 1


		if('developers' in steamData and 'publishers' in steamData):
			dC = len(steamData['developers'])
			dP = len(steamData['publishers'])
			res = str(dP)+"_"+str(dC)

			if res in publishersVsDevelopers:
				publishersVsDevelopers[res] += 1
			else:
				publishersVsDevelopers[res] = 1

		if('movies' in steamData):
			mC = len(steamData['movies'])

			if mC in moviesCount:
				moviesCount[mC] += 1
			else:
				moviesCount[mC] = 1

		if('screenshots' in steamData):
			sC = len(steamData['screenshots'])

			if sC in screenshootsCount:
				screenshootsCount[sC] += 1
			else:
				screenshootsCount[sC] = 1

		if('achievements' in steamData):
			aC = steamData['achievements']['total']

			if aC in achievementsCount:
				achievementsCount[aC] += 1
			else:
				achievementsCount[aC] = 1


print(listOfTypes)
print(totalCount)

print(requiredAge)

print(categoryCountPerGame)
print(categoryList)

print(genreCountPerGame)
print(genreList)

print(releaseYear)
print(releaseDate)
print(releasedState)

print(platforms)
print(platformsPerGame)

print(developersList)
print(developersPerGame)

print(publishersList)
print(publishersPerGame)

print(publishersVsDevelopers)

print(moviesCount)
print(screenshootsCount)

print(achievementsCount)

with open('listOfTypes.json', 'w') as file:
     file.write(json.dumps(listOfTypes))
with open('totalCount.json', 'w') as file:
     file.write(json.dumps(totalCount))
with open('requiredAge.json', 'w') as file:
     file.write(json.dumps(requiredAge))
with open('categoryCountPerGame.json', 'w') as file:
     file.write(json.dumps(categoryCountPerGame))
with open('categoryList.json', 'w') as file:
     file.write(json.dumps(categoryList))
with open('genreCountPerGame.json', 'w') as file:
     file.write(json.dumps(genreCountPerGame))
with open('genreList.json', 'w') as file:
     file.write(json.dumps(genreList))
with open('releaseYear.json', 'w') as file:
     file.write(json.dumps(releaseYear))
with open('releaseDate.json', 'w') as file:
     file.write(json.dumps(releaseDate))
with open('releasedState.json', 'w') as file:
     file.write(json.dumps(releasedState))
with open('platforms.json', 'w') as file:
     file.write(json.dumps(platforms))
with open('platformsPerGame.json', 'w') as file:
     file.write(json.dumps(platformsPerGame))
with open('developersList.json', 'w') as file:
     file.write(json.dumps(developersList))
with open('developersPerGame.json', 'w') as file:
     file.write(json.dumps(developersPerGame))
with open('publishersList.json', 'w') as file:
     file.write(json.dumps(publishersList))
with open('publishersPerGame.json', 'w') as file:
     file.write(json.dumps(publishersPerGame))
with open('publishersVsDevelopers.json', 'w') as file:
     file.write(json.dumps(publishersVsDevelopers))
with open('moviesCount.json', 'w') as file:
     file.write(json.dumps(moviesCount))
with open('screenshootsCount.json', 'w') as file:
     file.write(json.dumps(screenshootsCount))
with open('achievementsCount.json', 'w') as file:
     file.write(json.dumps(achievementsCount))