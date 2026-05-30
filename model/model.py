from database.DAO import DAO
import networkx as nx

class Model:
    def __init__(self):
        self._fermate = DAO.getAllFermate()
        self._grafo=nx.DiGraph()
        #creo id map per ricavare dalla connessione idstaza
        self._idMapFermate = {}
        for f in self._fermate:
            self._idMapFermate[f.id_fermata] = f



    def buildGraph(self):
        #orientato e non pesato -->digraph()
        #nodi fermate --> lette dal drop down che si rifa a dao e dataclass fermata
        #1.pulire
        self._grafo.clear()
        #2.popolare i nodi
        self._grafo.add_nodes_from(self._fermate)
        self.addEdges2()


    #metodo uno - troppo lento - sconsigliato
    def addEdges(self):
        for u in self._fermate:
            for v in self._fermate:
                if DAO.hasconn(u,v):
                    self._grafo.add_edge(u,v)
                    #adesso vado nel dao e controllo la connessione
    #metodo 2
    def addEdges2(self):
        for u in self._fermate:
            for conn in DAO.getVicini(u):
                v = self._idMapFermate[conn.id_stazA]
                self._grafo.add_edge(u,v)
                #adesso vado nel dao e creo DAO.getVicini

        # metodo 3 trovo tutte nel dao e poi uso la idmap per ricavarmi le ferma e t
    def addEdges3(self):
        alledges= DAO.getAllEdges()
        for conn in alledges:
            u = self._idMapFermate[conn.id_stazP]
            v = self._idMapFermate[conn.id_stazA]
            self._grafo.add_edge(u, v)

        # punto 2
    def getBFSNodesFromEdges(self, source):
        archi = nx.bfs_edges(self._grafo, source)
        nodiBfs = []
        for u, v in archi:
            nodiBfs.append(v)
        return nodiBfs

    def getDFSNodesFromEdges(self, source):
        archi = nx.dfs_edges(self._grafo, source)
        nodiDfs = []
        for u, v in archi:
            nodiDfs.append(v)
        return nodiDfs

        # altra opzione per il punto due usando i tree
    def getBFSNodesFromTree(self, source):
        tree = nx.bfs_tree(self._grafo, source)
        archi = list(tree.edges)
        nodi = list(tree.nodes)
        return nodi

    def getDFSNodesFromTree(self, source):
        tree = nx.dfs_tree(self._grafo, source)
        archi = list(tree.edges)
        nodi = list(tree.nodes)
        return nodi

    #multidigraph
    def buildGraphPesato(self):
        self._grafo.clear()
        self._grafo.add_nodes_from(self._fermate)
        self.addEdgesPesati()


    @property
    def fermate(self):
        return self._fermate

    #per ottenere numero nodi e archi
    def get_num_nodi(self):
        return len(self._grafo.nodes)
    def get_num_archi(self):
        return len(self._grafo.edges)

    def addEdgesPesati(self):
        #riutilizzo il metodo addedges 3 ma contando gli archi che provo ad aggiungere tra due nodi
        self._grafo.clear_edges()
        alledges = DAO.getAllEdges()
        for conn in alledges:
            u = self._idMapFermate[conn.id_stazP]
            v = self._idMapFermate[conn.id_stazA]
            if self._grafo.has_edge(u,v):
                self._grafo[u][v]['weight'] += 1
            else:
                self._grafo.add_edge(u, v, weight=1)
            #alternativa e fare la group by nel dao
    def addEdgesPesati2(self):
        #riutilizzo il metodo addedges 3 ma contando gli archi che provo ad aggiungere tra due nodi
        self._grafo.clear_edges()
        allEdgesP = DAO.getAllEdgesPesati()
        #(idstazp,idstaza, peso) ---> output dao
        for e in allEdgesP:
            u = self._idMapFermate[e[0]]
            v = self._idMapFermate[e[1]]
            peso = e[2]
            self._grafo.add_edge(u, v, weight=peso)
    def getArchiPesoMaggiore(self):
        #metodo per il test model
        edges = self._grafo.edges(data=True)
        pesoMaggiore = []
        for e in edges:
            if self._grafo.get_edge_data(e[0], e[1])["weight"] > 1:
                pesoMaggiore.append(e)
        return pesoMaggiore