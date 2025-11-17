from aspirador import Aspirador
from vectors import *
from sala import SUJO
import time

#             nome bão
#            🤤🧹🥴😋
class AspiradorGuloso(Aspirador):
    CICLO_PERIMETRO = 0
    CICLO_CIRCULAR = 1
    CICLO_PATRULHA = 2

    configurado = False

    def configurar(self,ciclo_inicial=CICLO_PATRULHA):
        self.ciclo = ciclo_inicial
        self.fim = False
        self.distância_percorrida = 0
        self.passos = 0
        self.fim = False
        self.visitado: set[MatrixCoord] = set()
        self.ultima_posição = self.posição
        self.retornar_estação = False
        self.ram:dict[int,dict] = {}
        self.ram[self.CICLO_PERIMETRO] = {}
        self.ram[self.CICLO_CIRCULAR] = {}
        self.ram[self.CICLO_PATRULHA] = {}
        self.configurado = True
        
    def ativar(self):
        if not self.configurado:
            return False
        
        while not self.fim:
            time.sleep(1)

            ultima_posição = self.posição
            
            if self.bateria <= 0.5 and not self.retornar_estação:
                self.retornar_estação = True
            
            if self.retornar_estação:
                self._retornar_estação()
                self.retornar_estação = self.bateria <= 1
                continue
            
            kernel = self.observar()
            kernel_pos = Vector2D(self.raio,self.raio)
            
            direção_sujeira = self._detectar_sujeira(kernel) - kernel_pos

            if direção_sujeira != Vector2D.ZERO():
                self.mover(direção_sujeira)
                self.limpar()
                continue

            match self.ciclo:
                case self.CICLO_PERIMETRO:
                    ram = self.ram[self.CICLO_PERIMETRO]
                    
                case self.CICLO_CIRCULAR:
                    ram = self.ram[self.CICLO_CIRCULAR]
                    
                case self.CICLO_PATRULHA:
                    ram = self.ram[self.CICLO_PATRULHA]
                    colisões:int = ram.get("colisões",0)
                    
            pass

                    
            
            self.passos = self.passos + 1
            self.distância_percorrida += 1
            self.ultima_posição = ultima_posição

            if self.passos >= 300:
                self.passos = 0
                self.ram[self.CICLO_PERIMETRO] = {}
                self.ram[self.CICLO_CIRCULAR] = {}
                self.ram[self.CICLO_PATRULHA] = {}
                self.ciclo += 1
                if self.ciclo > self.CICLO_PATRULHA:
                    self.ciclo = self.CICLO_PERIMETRO
                pass
            pass
            self.visitado.add(self.posição)

        pass
            
        self.configurado = False


    def _retornar_estação(self):
        if self.direção_estação != Vector2D.ZERO():
            self.mover(self.direção_estação)
        self.carregar()

    def _detectar_sujeira(self,kernel:Matrix2D)->Vector2D:
        tamanho = kernel.x_size()
        if tamanho != kernel.y_size():
            raise RuntimeError("O kernel de detecção não é uma matriz quadrada")
        if tamanho > self.raio * 2 + 1:
            raise RuntimeError("O kernel de detecção é maior que a capacidade de observação")
        
        for y in range(tamanho):
            for x in range(tamanho):
                piso = kernel.at(MatrixCoord(x,y))
                if piso == SUJO():
                    return Vector2D.from_matrix_coord(MatrixCoord(x,y))
        return Vector2D.ZERO()


# f(n) = g(n) + 1.5*h(n)
# Não tem obstaculo, não sera necessário um A*
def a_star(n):
    pass