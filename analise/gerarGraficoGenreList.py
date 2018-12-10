import matplotlib.pyplot as plt
import json

with open('data/genreList.json', 'r') as file:
	genreList = json.load(file)

for x in genreList:
	print(x)

plt.figure(figsize=(15, 3))
plt.bar(range(len(genreList)), genreList.values(), align='center')
plt.xticks(range(len(genreList)), list(genreList.keys()), rotation=-80)
plt.title("Quantidade de Apps por Gênero")
plt.savefig('imagens/genero.png', bbox_inches='tight')