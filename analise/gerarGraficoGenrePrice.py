import matplotlib.pyplot as plt
import json

with open('categoryPrice.json', 'r') as file:
	genreList = json.load(file)

for x in genreList:
	print(x)

plt.figure(figsize=(15, 3))
plt.bar(range(len(genreList)), genreList.values(), align='center')
plt.xticks(range(len(genreList)), list(genreList.keys()), rotation=-80)
plt.title("Preço médio por Gênero")
plt.savefig('imagens/generoPrice.png', bbox_inches='tight')