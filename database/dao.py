from database.DB_connect import DBConnect
from model.rifugio import Rifugio
from model.connessione import Connessione

class DAO:
    """
    Implementare tutte le funzioni necessarie a interrogare il database.
    """
    # TODO
    @staticmethod
    def readRifugi () :
        cnx = DBConnect.get_connection ()
        results = []
        if not cnx :
            print ("Errore di connessione al database.")
            return None
        cursor = cnx.cursor (dictionary = True)
        query = "SELECT * FROM rifugio"
        cursor.execute (query)
        for row in cursor :
            results.append (Rifugio (**row))
        cursor.close ()
        cnx.close ()
        return results

    @staticmethod
    def readConnessioni (year) :
        cnx = DBConnect.get_connection ()
        results = []
        if not cnx :
            print ("Errore di connessione al database.")
            return None
        cursor = cnx.cursor (dictionary = True)
        query = ("SELECT id_rifugio1, id_rifugio2, anno, difficolta, distanza "
                 "FROM connessione "
                 "WHERE anno <= %s ")
        cursor.execute (query, (year, ))
        for row in cursor :
            results.append (Connessione (**row))
        cursor.close ()
        cnx.close ()
        return results
