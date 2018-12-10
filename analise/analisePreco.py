from pymongo import MongoClient
import matplotlib.pyplot as plt
import math
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

prices = []
pricesCat = {}
promocao = {"Desconto": 0, "Normal": 0}

categoryPrice = {}
categoryCount = {}

sum = 0
count = 0
for g in gamesList:
	if not(g): continue
	if ('steamdata' in g):
		steamData = g['steamdata']
		if (steamData == "None" or not(steamData)) : continue

		if 'price_overview' in steamData and 'final' in steamData['price_overview']:
			p = int(steamData['price_overview']['final'])/100
			if(p == 0): continue
			sum += p
			count += 1
			prices.append(p)

			cat = math.floor(p / 5)
			lowCat = cat - 1
			highCat = cat + 1
			if lowCat <= 0: lowCat = 0

			# print(p, " is between ", lowCat*5, " and ", highCat*5)
			s = str(lowCat*5)
			if s in pricesCat:
				pricesCat[s] += 1
			else:
				pricesCat[s] = 1

			if steamData['price_overview']['final'] != steamData['price_overview']['initial']:
				promocao["Desconto"] += 1
			else:
				promocao["Normal"] += 1

			if('genres' in steamData):
				for cat in steamData['genres']:

					if cat['description'] in categoryPrice:
						categoryPrice[cat['description']] += p
						categoryCount[cat['description']] += 1
					else:
						categoryPrice[cat['description']] = p
						categoryCount[cat['description']] = 1





print("Sum: ",sum)
print("Count: ",count)
print("Media: ",sum/count)

for x in categoryPrice:
	categoryPrice[x] /= categoryCount[x]

print(categoryPrice)
print(categoryCount)

with open('prices.json', 'w') as file:
     file.write(json.dumps(prices))
with open('pricesCat.json', 'w') as file:
     file.write(json.dumps(pricesCat))
with open('promocao.json', 'w') as file:
     file.write(json.dumps(promocao))
with open('categoryPrice.json', 'w') as file:
     file.write(json.dumps(categoryPrice))