from dataclasses import dataclass
from agente import AspiradorGuloso
from sala import *
from random import *
# N = salas
# G = iteração

# cada aspirador vai ser testado em N salas
# seu desempenho vai ser medido em quantidade de N salas limpas sobre total de N * G^10

@dataclass
class Fabrica():
    aspiradores: list[AspiradorGuloso]
    sala       : list[Sala]
    geração    : int = 0
    def gerar_aspirador()->list[AspiradorGuloso]:
        pass

    def gerar_sala(quantidade:int,tamanho:int)->list[Sala]:
        salas:list[Sala] = []
        for _salas in range(quantidade):
            pisox = []
            for _x in range(tamanho):
                pisoy = []
                for _y in range(tamanho):
                    pisoy.append(choice([-1,0,0,0,0,0,0,0,0,1,1,1,1]))
                pass
                pisox.append(tuple(pisoy))
            pass
            salas.append(Sala(Matrix2D(tuple(pisox))))
        pass
        return salas

if __name__ == "__main__":
    print("HELLO! UwU")
    salas: list[Sala] = Fabrica.gerar_sala(5,10)