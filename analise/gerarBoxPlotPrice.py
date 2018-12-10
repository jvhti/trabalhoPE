import matplotlib.pyplot as plt
import json

with open('prices.json', 'r') as file:
	data = json.load(file)


res = plt.boxplot(data)
plt.title("BoxPlot dos Preços")
plt.savefig('imagens/priceBoxPlot.png', bbox_inches='tight')
plt.show();

print(res['caps'][1].get_ydata())