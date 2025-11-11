from vectors import *
from sala import *

class Aspirador:
    def __init__(self,posição:MatrixCoord=MatrixCoord(0,0),bateria:float=1.0,raio:int=4):
        #                  ^ UTF-8 ftw 🥳
        self.posição = posição
        self.bateria = bateria
        self.raio = raio
        self.estação = posição
        self.sala: Sala
        self.consumo:float
    
    def limpar(self):
        if self.bateria <= 0:
            raise RuntimeError("Bateria esgotada!")
        self.sala.piso.at(self.posição).write(LIMPO)

    def mover(self,dir:Vector2D):
        if self.bateria <= 0:
            raise RuntimeError("Bateria esgotada!")
        atual = Vector2D.from_matrix_coord(self.posição)
        destino = atual + dir
        self.posição = MatrixCoord(destino.x,destino.y)
    
    def observar(self) -> Matrix2D:
        kernel = [[INVALIDO for _ in range(self.raio)] for _ in range(self.raio)]
        inicio = Vector2D.from_matrix_coord(self.posição) - self.raio
        
        for kernel_x in range(self.raio*2):
            piso_x = inicio.x + kernel_x
            if piso_x >= 0:
                for kernel_y in range(self.raio*2):
                    piso_y = inicio.y + kernel_y
                    if piso_y >= 0:
                        try:
                            kernel[kernel_x][kernel_y] = self.sala.piso.at(MatrixCoord(piso_x,piso_y))
                        except IndexError:
                            pass
        
        return Matrix2D(tuple(tuple(kernel_data) for kernel_data in kernel))
    
    def carregar(self):
        if self.posição == self.estação:
            self.bateria = 1