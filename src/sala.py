from vectors import *

PAREDE = lambda: MatrixData(-1)
LIMPO    = lambda: MatrixData(0)
SUJO     = lambda: MatrixData(1)

class Sala():
    def __init__(self,piso:Matrix2D) -> None:
        self.piso = piso