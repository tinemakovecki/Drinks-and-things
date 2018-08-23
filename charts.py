import matplotlib.pyplot as plt
import numpy as np


#GRAF DRŽAVE VINA
drzave_vina = ("United States", "France", "Italy", "Spain", "Australia", "Portugal", "Israel", "Argentina",
               "Germany", "New Zealand", "Other")
stevilo_vina = (554, 529, 204, 78, 66, 55, 42, 39, 34, 28, 81)


fig, ax = plt.subplots()

index = np.arange(11)

chart = ax.barh(index, stevilo_vina[::-1], color=(0.1, 0.1, 0.1, 0.1), edgecolor='blue')


ax.set_ylabel('Countries')
ax.set_xlabel('Number of wines')
ax.set_title('Number of wines from a country')
ax.set_yticks(index)
ax.set_yticklabels(drzave_vina[::-1])

fig.tight_layout()
plt.savefig('countries_wine.jpg')

#GRAF REGIJE
regije = ("California","Burgundy","Tuscany","Rhone","Bordeaux","Champagne","South Australia","Piedmont",
               "Oregon","Israel")
stevilo_regije = (437, 153, 90, 80, 78, 58, 53, 49, 44, 42)

fig, ax = plt.subplots()

index = np.arange(10)

chart = ax.barh(index, stevilo_regije[::-1], color=(0.1, 0.1, 0.1, 0.1), edgecolor='blue')


ax.set_ylabel('Regions')
ax.set_xlabel('Number of wines')
ax.set_title('Number of wines from a region', style='oblique')
ax.set_yticks(index)
ax.set_yticklabels(regije[::-1])

fig.tight_layout()
plt.savefig('regions_wine.jpg')

#GRAF DRŽAVE PIVA
drzave_piva = ("England","United States","Belgium","Scotland","Denmark","Germany","New Zealand","Netherlands",
               "Australia","Japan","Iceland","United Kingdom")
stevilo_piva = (415, 179, 122, 114, 75, 47, 29, 27, 18, 9, 6, 1)

fig, ax = plt.subplots()

index = np.arange(12)

chart = ax.barh(index, stevilo_piva[::-1], color=(0.1, 0.1, 0.1, 0.1), edgecolor='blue')


ax.set_ylabel('Countries')
ax.set_xlabel('Number of beers')
ax.set_title('Number of beers from a country')
ax.set_yticks(index)
ax.set_yticklabels(drzave_piva[::-1])

fig.tight_layout()
plt.savefig('countries_beer.jpg')

#GRAF VRSTE PIVA
vrste_piva=("IPA","Pale Ale","Lager/Pilsner","Stout","Wheat Beer","Saison Beer","Fruit Beer","APA","Cask-Aged Beer",
            "Sour/Lambic Beer","Blonde Beer","Porter","Dark Ale")
stevilo_piva = (210, 106, 89, 76, 60, 53, 48, 45, 42, 40, 37, 33, 32)

fig, ax = plt.subplots()
ax.set_title('Most represented types of beer')
chart = plt.pie(stevilo_piva, labels=vrste_piva)
plt.savefig('types_beer.jpg')


#GRAF VRSTE VINA
vrste_vina=("blend","Chardonnay","Pinot Noir","Cabernet Sauvignon","Riesling","Sauvignon Blanc","Sangiovese","Syrah",
            "Nebbiolo","Gamay","Pinot Gris","Merlot","Grenache","Port Varieties")
stevilo_vrst = (551, 237, 189, 164, 70, 63, 51, 43, 39, 37, 35, 34, 29, 27)


fig, ax = plt.subplots()
ax.set_title('Most represented types of wines')
chart = plt.pie(stevilo_vrst, labels=vrste_vina, explode=[0.1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0])
plt.savefig('types_wine.jpg')

