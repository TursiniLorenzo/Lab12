import networkx as nx
from database.dao import DAO
from model.rifugio import Rifugio

class Model:
    def __init__(self):
        """Definire le strutture dati utili"""
        # TODO
        self.G = nx.DiGraph ()
        self._objects_rifugio = []
        self.get_nodes ()

        self.lista_rifugi = DAO.readRifugi()
        self.dict_rifugi = {rifugio.id: rifugio for rifugio in self.lista_rifugi}
        self.pesi = []
        self._soglia = 0

        self.connessioni = []

    def get_nodes (self) :
        self._objects_rifugio = self.G.nodes()
        return self._objects_rifugio

    def build_weighted_graph(self, year: int):
        """
        Costruisce il grafo pesato dei rifugi considerando solo le connessioni con campo `anno` <= year passato
        come argomento.
        Il peso del grafo è dato dal prodotto "distanza * fattore_difficolta"
        """
        # TODO
        for connessione in DAO.readConnessioni (year) :
            peso = 0.0
            if connessione.difficolta == "facile" :
                difficolta_numerica = 1
                peso = float (difficolta_numerica) * float (connessione.distanza)
                id_connessione = (connessione.id_rifugio1, connessione.id_rifugio2, peso)
                self.connessioni.append (id_connessione)
                self.pesi.append(peso)

            elif connessione.difficolta == "media" :
                difficolta_numerica = 1.5
                peso = float (difficolta_numerica) * float (connessione.distanza)
                id_connessione = (connessione.id_rifugio1, connessione.id_rifugio2, peso)
                self.connessioni.append (id_connessione)
                self.pesi.append(peso)

            elif connessione.difficolta == "difficile" :
                difficolta_numerica = 2
                peso = float (difficolta_numerica) * float (connessione.distanza)
                id_connessione = (connessione.id_rifugio1, connessione.id_rifugio2, peso)
                self.connessioni.append (id_connessione)
                self.pesi.append(peso)

            self.G.add_edge (connessione.id_rifugio1, connessione.id_rifugio2, weight = peso)

    def get_edges_weight_min_max(self):
        """
        Restituisce min e max peso degli archi nel grafo
        :return: il peso minimo degli archi nel grafo
        :return: il peso massimo degli archi nel grafo
        """
        # TODO
        peso_minimo = min (self.pesi)
        peso_massimo = max (self.pesi)
        return peso_minimo, peso_massimo

    def count_edges_by_threshold(self, soglia):
        """
        Conta il numero di archi con peso < soglia e > soglia
        :param soglia: soglia da considerare nel conteggio degli archi
        :return minori: archi con peso < soglia
        :return maggiori: archi con peso > soglia
        """
        # TODO
        self._soglia = soglia
        lista_minori = []
        lista_maggiori = []

        for edge in self.G.edges (data = True) :
            if edge [2] ["weight"] < soglia :
                lista_minori.append (edge [2] ["weight"])
            elif edge [2] ["weight"] > soglia :
                lista_maggiori.append (edge [2] ["weight"])

        return len (lista_minori), len (lista_maggiori)

    """Implementare la parte di ricerca del cammino minimo"""
    # TODO
    def cammino_minimo (self, soglia) :
        diz_cammini = {}

        for connessione in self.connessioni:
            partenza = connessione[0]
            destinazione = connessione[1]
            peso = connessione[2]

            if peso > soglia:
                if partenza not in diz_cammini:
                    diz_cammini [partenza] = []

                diz_cammini [partenza].append ((destinazione, peso))

        tutti_i_cammini = []

        pila = []

        for nodo_iniziale in diz_cammini.keys ():
            pila.append(([nodo_iniziale], 0))

        while pila:

            cammino_corrente, peso_attuale = pila.pop ()
            ultimo_nodo = cammino_corrente [-1]

            if ultimo_nodo in diz_cammini:

                for vicino, peso_arco in diz_cammini [ultimo_nodo]:

                    if vicino not in cammino_corrente:

                        nuovo_cammino = cammino_corrente + [vicino]
                        nuovo_peso = peso_attuale + peso_arco

                        if len(nuovo_cammino) >= 3:
                            tutti_i_cammini.append ((tuple(nuovo_cammino), nuovo_peso))

                        pila.append((nuovo_cammino, nuovo_peso))

        cammino_minimo_completo = min (tutti_i_cammini, key=lambda item: item [1])

        nodi_cammino = cammino_minimo_completo [0]
        cammino_minimo = []
        for nodo in nodi_cammino:
            nodo_rifugio = f"[{self.dict_rifugi[nodo].id}] {self.dict_rifugi[nodo].nome} ({self.dict_rifugi[nodo].localita})"
            cammino_minimo.append (nodo_rifugio)

        peso_minimo = cammino_minimo_completo [1]

        return cammino_minimo, peso_minimo


