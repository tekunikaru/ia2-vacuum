from vectors import *

INVALIDO = MatrixData(-1)
LIMPO = MatrixData(0)
SUJO = MatrixData(1)

class Sala():
    def __init__(self,piso:Matrix2D) -> None:
        self.piso = piso