import matplotlib.pyplot as plt
import json

with open('data/screenshootsCount.json', 'r') as file:
	screenshotCount = json.load(file)

with open('data/moviesCount.json', 'r') as file:
	moviesCount = json.load(file)

data = [[],[]]

for x in screenshotCount:
	if x == "144": continue
	for i in range(screenshotCount[x]):
		data[0].append(int(x))

for x in moviesCount:
	for i in range(moviesCount[x]):
		data[1].append(int(x))

res = plt.boxplot(data)
plt.title("BoxPlot de Screenshots e Movies por App")
plt.savefig('imagens/ScreenshotsPorAppBoxPlot.png', bbox_inches='tight')
plt.show();

print(res['caps'][1].get_ydata())