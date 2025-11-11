from vectors import *
from aspirador import Aspirador

INVALIDO = MatrixData(-1)
LIMPO = MatrixData(0)
SUJO = MatrixData(1)

class Sala():
    def __init__(self,piso:Matrix2D,aspirador:Aspirador,estação:MatrixCoord=MatrixCoord(0,0)) -> None:
        self.piso = piso
        self.aspirador = aspirador
        self.aspirador.sala = self
        self.aspirador.estação = estação
        # A unidade de consumo não foi definida, então parsa, EU vou defini-la dinamicamente.
        self.aspirador.consumo = 1/((self.piso.x_size() + self.piso.x_size() - 1)*2)