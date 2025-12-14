from vectors import *

PAREDE   = lambda: MatrixData(-1)
LIMPO    = lambda: MatrixData(0)
SUJO     = lambda: MatrixData(1)

class Sala():
    def __init__(self,piso:Matrix2D) -> None:
        self.piso = piso

def retornar_nos_validos(kernel:Matrix2D)->tuple[MatrixCoord,...]:
    coords:list[MatrixCoord] = []
    tamanho = kernel.x_size()
    for y in range(tamanho):
        for x in range(tamanho):
            piso = kernel.at(MatrixCoord(x,y))
            if piso != PAREDE():
                coords.append(MatrixCoord(x,y))
    return tuple(coords)