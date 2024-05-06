# Application de dimensionnement d'interconnexion.

Ce projet est une application web Flask qui permet de calculer et de visualiser les distances entre plusieurs villes.


## Fonctionnalités


- Ajout de villes et calcul de la distance totale entre elles.

- Visualisation des villes et des distances sur une carte.
- Possibilité de réinitialiser les villes et les distances.
- Technologies utilisées
- Python
- Flask
- NetworkX
- Folium
- GeoPy
- NumPy
- Scikit-learn
## Installation
- Clonez ce dépôt sur votre machine locale.
- Installez les dépendances du projet avec la commande suivante : pip install -r 
## Utilisation
- Pour lancer l'application, exécutez la commande suivante dans le terminal : python app.py

- Ensuite, ouvrez votre navigateur web et accédez à http://localhost:5000.

## Comment ça marche
- L'application utilise Flask pour gérer les requêtes web. Lorsqu'une liste de villes est soumise, l'application utilise GeoPy pour obtenir les coordonnées de chaque ville. Ces villes sont ensuite ajoutées comme nœuds dans un graphe NetworkX.

- L'application utilise ensuite l'algorithme des k plus proches voisins de Scikit-learn pour trouver les villes les plus proches de chaque ville. Les distances entre ces villes sont calculées avec GeoPy et ajoutées comme arêtes dans le graphe.

- Enfin, l'application utilise Folium pour visualiser les villes et les distances sur une carte.

## Contribution
Les contributions à ce projet sont les bienvenues. Si vous souhaitez contribuer, veuillez forker le dépôt et créer une pull request.

## Licence
Ce projet est sous licence MIT. Voir le fichier LICENSE pour plus de détails.
