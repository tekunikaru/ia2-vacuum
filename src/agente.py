from collections import deque
from math import inf
from aspirador import Aspirador
from vectors import *
from sala import SUJO, PAREDE, MatrixCoord, retornar_nos_validos
import time

from vectors import MatrixCoord

def por_a_estrela(cg:float,g:float,ch:float,h:float)->float:
    return cg*g+ch*h

@dataclass
class Genes:
    raio = 1
    ciclo_inicial = 0
    passos_para_troca_de_ciclo = 300
    a_peso_g = 1
    a_peso_h = 1
    
    def misturar(self,genes:"Genes")-> "Genes":
        return Genes()
    
    def mutar(self) -> "Genes":
        return Genes()

#             nome bão
#            🤤🧹🥴😋
class AspiradorGuloso(Aspirador):
    CICLO_PERIMETRO = 0
    CICLO_CIRCULAR  = 1
    CICLO_PATRULHA  = 2
    CICLO_EM_ROTA   = 3

    configurado = False

    def __init__(self, genes:Genes, posição=MatrixCoord(0,0)):
        super().__init__(posição, raio=genes.raio, bateria=1.0)
        self.genes = genes

    def configurar(self):
        self.ciclo = self.genes.ciclo_inicial
        self.fim = False
        self.distância_percorrida_em_rota = 0
        self.passos = 0
        self.fim = False
        self.visitado: set[MatrixCoord]= set()
        self.retornar_para_estação     = False
        self.ram:dict[int,dict]        = {}
        self.ram[self.CICLO_PERIMETRO] = {}
        self.ram[self.CICLO_CIRCULAR]  = {}
        self.ram[self.CICLO_PATRULHA]  = {}
        self.rota:list[MatrixCoord]    = []

        self.configurado = True

    def ativar(self):
        if not self.configurado:
            return
        
        while not self.fim:
            time.sleep(1)

            ultima_posição = self.posição
            
            if self.bateria <= 0.5 and not self.retornar_estação:
                self.retornar_estação = True
            
            if self.retornar_para_estação:
                self.retornar_estação()
                self.retornar_para_estação = self.bateria <= 1
                continue
            
            if self.ciclo == self.CICLO_EM_ROTA:# and (self.distância_percorrida_em_rota+1)%5==0:
                self.navegar()
                if (self.ciclo!=self.CICLO_EM_ROTA):
                    self.limpar()
                continue

            kernel = self.observar()
            kernel_pos = Vector2D(self.raio,self.raio)
            
            direção_sujeira = self.detectar_sujeira(kernel) - kernel_pos

            if direção_sujeira != Vector2D.ZERO():
                rota = self.buscar_via_Aestrela((direção_sujeira-Vector2D.from_matrix_coord(self.posição)).to_matrix_coord(),kernel)
                raise NotImplementedError("Incompleto")
                self.definir_rota(rota)
                self.navegar()
                if (self.ciclo!=self.CICLO_EM_ROTA):
                    self.limpar()
            else:

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
            self.ultima_posição = ultima_posição

            if self.passos >= self.genes.passos_para_troca_de_ciclo and self.ciclo != self.CICLO_EM_ROTA:
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


    def retornar_estação(self):
        if self.direção_estação != Vector2D.ZERO():
            self.mover(self.direção_estação)
            return
        self.carregar()

    def detectar_sujeira(self,kernel:Matrix2D)->Vector2D:
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
    
    def definir_rota(self,rota:tuple[MatrixCoord]):
        self.ciclo = self.CICLO_EM_ROTA
        self.rota = list(rota)
        self.distância_percorrida_em_rota = 0

    def navegar(self):
        if self.ciclo != self.CICLO_EM_ROTA:
            return
        
        destino = self.rota.pop(0)
        self.mover(Vector2D.from_matrix_coord(destino) - Vector2D.from_matrix_coord(self.posição))
        self.distância_percorrida_em_rota += 1

        if len(self.rota)==0:
            self.ciclo = self.CICLO_PATRULHA

    def buscar_via_largura(self, destino: MatrixCoord,kernel:Matrix2D|None = None) -> tuple[MatrixCoord,...]:
        if kernel == None:
            kernel = self.observar()

        lin, col = kernel.y_size(), kernel.x_size()

        kernel_pos = Vector2D(self.raio+1,self.raio+1).to_matrix_coord()

        fila = deque([[kernel_pos]])
        visitado = {kernel_pos}

        while fila:
            rota = fila.popleft()    
            pos = rota[-1]       

            if pos == destino:
                return tuple(rota)           
            
            alin, acol = pos
            for vizinho in [
                MatrixCoord(acol - 1, alin), MatrixCoord(acol + 1, alin),
                MatrixCoord(acol, alin - 1), MatrixCoord(acol, alin + 1)
            ]:
                if (0 <= vizinho.x < col and 
                    0 <= vizinho.y < lin and
                    kernel.at(vizinho).read() != PAREDE() and
                    vizinho not in visitado
                ):
                    visitado.add(vizinho)
                    nova_rota = rota + [vizinho]
                    fila.append(nova_rota)

        return tuple()
    
    def buscar_via_profundidade(self,destino:MatrixCoord,kernel:Matrix2D|None = None) -> Tuple[MatrixCoord,...]:
        if kernel == None:
            kernel = self.observar()

        inicio = Vector2D(self.raio+1,self.raio+1).to_matrix_coord()
        pilha = [(inicio, [inicio])]

        visitado = self.visitado.copy()
        lin, col = kernel.y_size(), kernel.x_size()
        
        rota:list[MatrixCoord] = []

        while pilha:
            current, rota = pilha.pop()
            if current == destino:
                return tuple(rota)
            if current not in visitado:
                visitado.add(current)

            
            alin, acol = current
            # neighbor = [(x -+ num, y),
            #             (x, y -+ num)]
            vizinhos = [
                MatrixCoord(acol - 1, alin),
                MatrixCoord(acol + 1, alin),
                MatrixCoord(acol, alin - 1),
                MatrixCoord(acol, alin + 1)
            ]

            for vizinho in vizinhos:
                if (0 <= vizinho.x < col and 
                    0 <= vizinho.y < lin and 
                    vizinho not in visitado and
                    kernel.at(vizinho).read() != PAREDE()
                ):
                    visitado.add(vizinho)
                    pilha.append((vizinho, rota + [vizinho]))
        
        return tuple()
    
    def buscar_via_Aestrela(self,destino:MatrixCoord,kernel:Matrix2D|None=None)->Tuple[MatrixCoord,...]:
        # f(n) = gene_g*g(n) + gene_h*h(n)
        if kernel==None:
            kernel = self.observar()

        kernel_pos = MatrixCoord(self.raio+1,self.raio+1)

        nos_validos = list(retornar_nos_validos(kernel))

        if kernel_pos not in nos_validos:
            raise AttributeError("Kernel inválido")

        # custo para alcançar nó alvo (euclideano, impreciso e pode colidir com paredes)
        # cg*g(n) + ch*h(n)
        custo:dict[MatrixCoord,float] = {
            no:
            #cg*g(n)
            (self.genes.a_peso_g * (Vector2D.from_matrix_coord(kernel_pos) - Vector2D.from_matrix_coord(no)).mag())+
            #ch*h(n)
            (self.genes.a_peso_h * (Vector2D.from_matrix_coord(destino) - Vector2D.from_matrix_coord(no)).mag())
            for no in nos_validos
        }

        return tuple(sorted(custo,key=lambda no:custo[no]))