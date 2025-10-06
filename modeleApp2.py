import json

class MagasinModel:
    # la classe MagasinModel est responsable de la gestion des données des magasins
    def __init__(self):
        # initialiser les magasins
        self.magasins = ["Magasin 1", "Magasin 2", "Magasin 3"]
        
        # Exemple de graphe pour le test
        self.graph = {
            'A': {'B': 1, 'C': 4},
            'B': {'A': 1, 'C': 2, 'D': 5},
            'C': {'A': 4, 'B': 2, 'D': 1},
            'D': {'B': 5, 'C': 1}
        }

    def get_magasins(self):
        # obtenir la liste des magasins
        return self.magasins
    
    def dijkstra(self, start):
        # implémenter l'algorithme de Dijkstra
        distances = {vertex: float('infinity') for vertex in self.graph}
        distances[start] = 0
        previous_nodes = {vertex: None for vertex in self.graph}
        vertices = list(self.graph.keys())

        while vertices:
            current_vertex = min(vertices, key=lambda vertex: distances[vertex])
            vertices.remove(current_vertex)

            if distances[current_vertex] == float('infinity'):
                break

            for neighbor, weight in self.graph[current_vertex].items():
                distance = distances[current_vertex] + weight
                if distance < distances[neighbor]:
                    distances[neighbor] = distance
                    previous_nodes[neighbor] = current_vertex

        return distances, previous_nodes

    def shortest_path(self, start, target):
        # obtenir le chemin le plus court
        distances, previous_nodes = self.dijkstra(start)
        path = []
        current_node = target

        while current_node is not None:
            path.append(current_node)
            current_node = previous_nodes[current_node]

        path = path[::-1]
        return path
    
    def test_dijkstra(self):
        # tester l'algorithme de Dijkstra
        start_node = 'A'
        target_node = 'D'
        distances, previous_nodes = self.dijkstra(start_node)
        path = self.shortest_path(start_node, target_node)

        print("Distances depuis le nœud de départ:", distances)
        print("Chemin le plus court de", start_node, "à", target_node, ":", path)

class ProduitModel:
    # la classe ProduitModel est responsable de la gestion des données des produits
    def __init__(self):
        # initialiser les produits
        with open('./listeProduit/liste_produits.json', 'r') as file:
            self.data = json.load(file)

    def get_produits(self):
        # obtenir la liste des produits
        return self.data

    def get_produits_magasin(self, magasin):
        # obtenir la liste des produits pour un magasin donné
        return self.data.get(magasin, [])
    
#exécution du test
if __name__ == '__main__':
    magasin_model = MagasinModel()
    magasin_model.test_dijkstra()