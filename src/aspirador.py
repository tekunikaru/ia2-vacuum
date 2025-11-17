from vectors import *
from sala import *

class Aspirador:
    def __init__(self,posição=MatrixCoord(0,0),raio:int=1,bateria:float=1.0):
        #                  ^ UTF-8 ftw 🥳
        self.posição = posição
        self.raio = raio
        self.bateria = bateria
        self.direção_estação = Vector2D(0,0)
        self.sala: Sala
        self.consumo: float
    
    def limpar(self):
        print(f'LIMPANDO {self.posição}')
        self.consumir_bateria()
        self.sala.piso.at(self.posição).write(LIMPO.data)

    def mover(self,dir:Vector2D):
        print(f'MOVENDO {dir} DE {self.posição}')
        self.consumir_bateria(dir.mag())
        pos_atual = Vector2D.from_matrix_coord(self.posição)
        destino = pos_atual + dir
        self.direção_estação = self.direção_estação - dir
        self.posição = destino.to_matrix_coord()
    
    def observar(self) -> Matrix2D:
        print(f'OBSERVANDO {self.posição}')
        self.consumir_bateria()
        kernel = [[INVALIDO for _ in range(self.raio*2+1)] for _ in range(self.raio*2+1)]
        inicio = (Vector2D.from_matrix_coord(self.posição) - Vector2D(self.raio,self.raio)).to_matrix_coord()
        
        for kernel_y in range(self.raio*2+1):
            piso_y = inicio.y + kernel_y
            if piso_x >= 0:
                for kernel_y in range(self.raio*2+1):
                    piso_y = inicio.y + kernel_y
                    if piso_x >= 0:
                        try:
                            kernel[kernel_x][kernel_y] = self.sala.piso.at(MatrixCoord(piso_x,piso_y))
                        except IndexError:
                            pass
        
        return Matrix2D(tuple(tuple(kernel_data) for kernel_data in kernel))
    
    def consumir_bateria(self,quantidade=1.0):
        if self.bateria <= 0:
            raise RuntimeError("Bateria esgotada!")
        self.bateria = self.bateria - self.consumo * quantidade
        print(f'DESCARRERGANDO {self.bateria}')

    def carregar(self):
        print("CARREGANDO")
        if self.posição == self.direção_estação:
            self.bateria += self.consumo*2