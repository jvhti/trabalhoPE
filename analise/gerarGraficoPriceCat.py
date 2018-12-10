import matplotlib.pyplot as plt
import json

with open('pricesCat.json', 'r') as file:
	pricesCat = json.load(file)

plt.figure(figsize=(15, 3))
plt.bar(range(len(pricesCat)), pricesCat.values(), align='edge', width=1)
plt.xticks(range(len(pricesCat)), list(pricesCat.keys()), rotation=-80)
plt.title("Preço por Categorias")
plt.savefig('imagens/priceCat.png', bbox_inches='tight')