from sala import *
from aspirador import *
from vectors import *
from agente import AspiradorGuloso

agente_guloso = AspiradorGuloso(MatrixCoord(1,1),raio=1)

sala = Sala(piso = Matrix2D((
    (LIMPO(),LIMPO(),LIMPO(),LIMPO(),LIMPO()),
    ( SUJO(),LIMPO(),LIMPO(),LIMPO(),LIMPO()),
    (LIMPO(),LIMPO(),LIMPO(),LIMPO(),LIMPO()),
    (LIMPO(),LIMPO(), SUJO(),LIMPO(),LIMPO()),
    (LIMPO(),LIMPO(),LIMPO(),LIMPO(),LIMPO()),
    (LIMPO(),LIMPO(),LIMPO(),LIMPO(),LIMPO())
)))

# A unidade de consumo não foi definida, então parsa, EU vou defini-la dinamicamente.
agente_guloso.consumo = 1/((sala.piso.x_size() + sala.piso.x_size())*2.5)

agente_guloso.sala = sala

agente_guloso.configurar()
agente_guloso.ativar()