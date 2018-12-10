import matplotlib.pyplot as plt
import json

with open('data/releaseYear.json', 'r') as file:
	releaseYear = json.load(file)

plt.plot(range(len(releaseYear)), releaseYear.values(), linestyle='--', marker='o')
plt.title("Quantidade de Apps lançados por Ano")
plt.savefig('imagens/ReleaseYear.png', bbox_inches='tight')
