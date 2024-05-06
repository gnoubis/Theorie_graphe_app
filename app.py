from flask import Flask, request, render_template, redirect, url_for, flash, session
import numpy as np
import secrets
from sklearn.neighbors import NearestNeighbors
import networkx as nx
import folium
from geopy.geocoders import Nominatim
from geopy.distance import geodesic

app = Flask(__name__)
app.secret_key = secrets.token_hex(16)
geolocator = Nominatim(user_agent=app.name)

# Créer un nouveau graphe vide
G = nx.Graph()

@app.route('/', methods=['GET', 'POST'])
def home():
    total_distance = 0  # Initialiser total_distance
    if request.method == 'POST':
        if 'cities' in request.form:
            cities = request.form.get('cities').split(',')
            for city in cities:
                location = geolocator.geocode(city)
                if location is not None:
                    lat, lon = location.latitude, location.longitude
                    G.add_node(city, pos=(lat, lon))
                    flash(f"Node {city} ajouté avec succès")
                else:
                    flash(f"Impossible de trouver les coordonnées pour {city}")

            positions = nx.get_node_attributes(G, 'pos')
            positions = np.array(list(positions.values()))

            # Obtenir le nombre d'échantillons
            n_samples = len(positions)

            # Assurer que n_neighbors est inférieur ou égal au nombre d'échantillons
            n_neighbors = min(n_samples, 3)

            neigh = NearestNeighbors(n_neighbors=3)
            neigh.fit(positions)

            indices = neigh.kneighbors(positions, n_neighbors=n_neighbors, return_distance=False)

            nodes = list(G.nodes)

            for i in range(len(nodes)):
                for j in indices[i][1:]:
                    pos1 = G.nodes[nodes[i]]['pos']
                    pos2 = G.nodes[nodes[j]]['pos']
                    distance = geodesic(pos1, pos2).km
                    G.add_edge(nodes[i], nodes[j], distance=distance)
                    total_distance += distance  # Ajouter la distance à total_distance

            session['nodes'] = list(G.nodes(data=True))
            session['edges'] = list(G.edges(data=True))
            session['total_distance'] = total_distance  # Stocker total_distance dans la session

    nodes = session.get('nodes', [])
    edges = session.get('edges', [])
    total_distance = session.get('total_distance', 0)  # Obtenir total_distance de la session
    return render_template('index.html', nodes=nodes, edges=edges, total_distance=total_distance)  # Passer total_distance au template

@app.route('/clear', methods=['POST'])
def clear():
    # Effacer les nœuds, les arêtes et total_distance de la session
    session.pop('nodes', None)
    session.pop('edges', None)
    session.pop('total_distance', None)  # Effacer total_distance de la session

    global G  # Déclarer G comme global
    G.clear()  # Effacer G

    return redirect(url_for('home'))  # Rediriger vers la page d'accueil

@app.route('/map', methods=['GET'])
def map():
    # Créer une nouvelle carte centrée sur le Cameroun
    m = folium.Map(location=[7.3697, 12.3547], zoom_start=6)

    # Obtenir les nœuds du graphe
    nodes = G.nodes(data=True)

    # Pour chaque nœud dans le graphe
    for node in nodes:
        # Obtenir les coordonnées du nœud
        lat, lon = node[1]['pos']

        # Ajouter un marqueur pour le nœud à la carte
        folium.Marker([lat, lon], popup=node[0]).add_to(m)

    # Obtenir les arêtes du graphe
    edges = G.edges(data=True)

    # Pour chaque arête dans le graphe
    for edge in edges:
        # Obtenir les coordonnées des nœuds de l'arête
        lat1, lon1 = G.nodes[edge[0]]['pos']
        lat2, lon2 = G.nodes[edge[1]]['pos']

        # Ajouter une ligne entre les nœuds à la carte
        line = folium.PolyLine([(lat1, lon1), (lat2, lon2)], color="red", weight=2.5, opacity=1)
        line.add_to(m)

        # Ajouter la distance à la ligne
        distance = edge[2]['distance']
        folium.Marker(
            location=((lat1+lat2)/2, (lon1+lon2)/2),
            icon=folium.DivIcon(
                icon_size=(150,36),
                icon_anchor=(0,0),
                html=f'<div style="font-size: 12pt">{distance:.1f} km</div>',
                )
            ).add_to(m)

    # Sauvegarder la carte en HTML
    m.save('templates/map.html')

    # Retourner le HTML de la carte
    return render_template('map.html')

if __name__ == '__main__':
    app.run(debug=True, port=5000)