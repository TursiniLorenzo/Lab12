from dataclasses import dataclass

from model.rifugio import Rifugio

@dataclass
class Connessione :
    id_rifugio1 : Rifugio
    id_rifugio2 : Rifugio
    anno : int
    distanza : float
    difficolta : str

    def __str__ (self) :
        return f"{self.id_rifugio1} -> {self.id_rifugio2} | "




