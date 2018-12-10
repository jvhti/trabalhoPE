import matplotlib.pyplot as plt
import json

with open('data/screenshootsCount.json', 'r') as file:
	screenshotCount = json.load(file)

plt.plot(range(len(screenshotCount)), screenshotCount.values(), linestyle='--', marker='o')
plt.title("Quantidade de Screenshots por App")
plt.savefig('imagens/ScreenshotsPorApp.png', bbox_inches='tight')

sum = 0
total = 0
max = 0
for x in screenshotCount:
	sum += screenshotCount[x] * int(x)
	total += screenshotCount[x]
	if max < int(x):
		max = int(x)

print("Total: ",total)
print("Max: ",max)
print("Media: ",sum/total)