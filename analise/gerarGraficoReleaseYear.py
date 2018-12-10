import matplotlib.pyplot as plt
import json

with open('data/releaseYear.json', 'r') as file:
	releaseYear = json.load(file)

for x in releaseYear:
	print(x)

plt.figure(figsize=(15, 3))
plt.bar(range(len(releaseYear)), releaseYear.values(), align='center')
plt.xticks(range(len(releaseYear)), list(releaseYear.keys()), rotation=-80)
plt.title("Quantidade de Apps lançados por Ano")
plt.savefig('imagens/ReleaseYear.png', bbox_inches='tight')