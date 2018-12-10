import matplotlib.pyplot as plt
import json

with open('data/moviesCount.json', 'r') as file:
	moviesCount = json.load(file)

plt.plot(range(len(moviesCount)), moviesCount.values(), linestyle='--', marker='o')
plt.title("Quantidade de Vídeos por App")
plt.savefig('imagens/VídeosPorApp.png', bbox_inches='tight')

sum = 0
total = 0
max = 0
for x in moviesCount:
	sum += moviesCount[x] * int(x)
	total += moviesCount[x]
	if max < int(x):
		max = int(x)

print("Total: ",total)
print("Max: ",max)
print("Media: ",sum/total)