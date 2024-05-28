import networkx as nx

from database.DAO import DAO


class Model:
    def __init__(self):
        self._listYears = []
        self._listColor = []
        self._idMap = {}
        self._grafo = nx.Graph()

    def buildGraph(self, color, anno):
        #self._grafo.edges.clear()
        self._nodi = DAO.getAllFilteredProducts(color)
        for p in self._nodi:
            self._idMap[p.Product_number] = p
        #print(self._idMap)
        self._grafo.add_nodes_from(self._nodi)
        self._addEdges(anno, color)
        self.printGraph()

    def _addEdges(self, anno, color):
        allConnessioni = DAO.getAllEdges(anno,color, self._idMap)
        for p in allConnessioni:
            v1 = p.P1
            v2 = p.P2
            #peso = p.N
            if v1 in self._grafo and v2 in self._grafo:
                if self._grafo.has_edge(v1, v2):
                    self._grafo[v1][v2]['weight'] += 1
                else:
                    self._grafo.add_edge(v1, v2, weight=1)

    def printGraph(self):
        for e in self._grafo.edges:
            print(self._grafo[e[0]][e[1]])
            print(self._grafo[e[0]])

    def getArchiPesoMaggiore(self):
        if len(self._grafo.edges) == 0:
            print("Il grafo è vuoto")
            return

        edges = self._grafo.edges
        result = []
        for u, v in edges:
            peso = self._grafo[u][v]["weight"]
            #if peso > 1:
            result.append((u, v, peso))
        result.sort(key=lambda x: x[2], reverse=True)
        return result


    def getEdgeWeight(self, v1,v2):
        return self._grafo[v1][v2]['weight']

    def getYears(self):
        self._listYears = DAO.getAllYears()
        return self._listYears

    def getColor(self):
        self._listColor = DAO.getAllColors()
        print(self._listColor)
        return self._listColor

    def getNumNodi(self):
        return len(self._grafo.nodes)

    def getNumArchi(self):
        return len(self._grafo.edges)