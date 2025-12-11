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
    CICLO_EM_ROTA = 3

    configurado = False

    def configurar(self,ciclo_inicial=CICLO_PATRULHA):
        self.ciclo = ciclo_inicial
        self.fim = False
        self.distância_percorrida_em_rota = 0
        self.passos = 0
        self.fim = False
        self.visitado: set[MatrixCoord] = set()
        self.ultima_posição = self.posição
        self.retornar_para_estação = False
        self.ram:dict[int,dict] = {}
        self.ram[self.CICLO_PERIMETRO] = {}
        self.ram[self.CICLO_CIRCULAR] = {}
        self.ram[self.CICLO_PATRULHA] = {}
        self.configurado = True
        self.rota:list[MatrixCoord] = []
        
    def ativar(self):
        if not self.configurado:
            return False
        
        while not self.fim:
            time.sleep(1)

            ultima_posição = self.posição
            
            if self.bateria <= 0.5 and not self.retornar_estação:
                self.retornar_estação = True
            
            if self.retornar_para_estação:
                self.retornar_estação()
                self.retornar_para_estação = self.bateria <= 1
                continue
            
            if self.ciclo == self.CICLO_EM_ROTA and (self.distância_percorrida_em_rota+1)%5==0:
                self.navegar()
                if (self.ciclo!=self.CICLO_EM_ROTA):
                    self.limpar()
                continue

            kernel = self.observar()
            kernel_pos = Vector2D(self.raio,self.raio)
            
            direção_sujeira = self.detectar_sujeira(kernel) - kernel_pos

            #if direção_sujeira != Vector2D.ZERO():
            #    rota = self.buscar_via_Aestrela((direção_sujeira-Vector2D.from_matrix_coord(self.posição)).to_matrix_coord(),kernel)
            #    self.definir_rota(rota)
            #    self.navegar()
            #    if (self.ciclo!=self.CICLO_EM_ROTA):
            #        self.limpar()
            #    continue

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
        self.mover(destino)
        self.distância_percorrida_em_rota += 1

        if len(self.rota)==0:
            self.ciclo = self.CICLO_PATRULHA

    def buscar_via_largura(self,destino:MatrixCoord)->Tuple[MatrixCoord]:
        posição = self.posição
        
        coords:list[MatrixCoord] = []
        raise NotImplementedError
        return tuple(coords)
    
    def buscar_via_profundidade(self,destino:MatrixCoord)->Tuple[MatrixCoord]:
        posição = self.posição

        coords:list[MatrixCoord] = []
        raise NotImplementedError
        return tuple(coords)
    
    def buscar_via_Aestrela(self,destino:MatrixCoord,kernel:Matrix2D=None)->Tuple[MatrixCoord]:
        # f(n) = g(n) + 1.5*h(n)
        if kernel==None:
            kernel = self.observar()

        coords:list[MatrixCoord] = []

        kernel_pos = Vector2D(self.raio+1,self.raio+1)

        direção = Vector2D.from_matrix_coord(destino) - self.posição

        # custo para alcançar nó alvo
        # g(n)

        # custo do nó alvo para o nó final
        # h(n)
        raise NotImplementedError

        return tuple(coords)
    