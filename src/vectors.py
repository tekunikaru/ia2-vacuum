import math
from typing import Tuple, Any
from dataclasses import dataclass, field
from collections import namedtuple

MatrixCoord = namedtuple("MatrixCoord",['x','y'])

# gud stuff
@dataclass
class Vector2D():
    @staticmethod
    def ZERO(): return Vector2D(0,0)
    @staticmethod
    def UP(): return Vector2D(0,1)
    @staticmethod
    def DOWN(): return Vector2D(0,1)
    @staticmethod
    def RIGHT(): return Vector2D(1,0)
    @staticmethod
    def LEFT(): return Vector2D(-1,0)
    @staticmethod
    def from_matrix_coord(coord:MatrixCoord):
        return Vector2D(coord.x,coord.y)
    def to_matrix_coord(self):
        return MatrixCoord(int(self.x),int(self.y))
    x: float
    y: float
    def __add__(self, other): return Vector2D(self.x+other.x, self.y+other.y)
    def __sub__(self, other): return Vector2D(self.x-other.x, self.y-other.y)
    def __mul__(self, scalar: float): return Vector2D(self.x*scalar, self.y*scalar)
    def __rmul__(self, scalar: float): return self*scalar
    def __len__(self): return int(self.mag())
    def dot(self, other): return self.x * other.x + self.y * other.y
    def mag(self): return math.hypot(self.x, self.y)
    def norm(self):
        l = self.mag()
        return Vector2D(self.x/l, self.y/l) if l else Vector2D(0,0)

@dataclass
class MatrixData():
    data: Any
    def read(self): return self.data
    def write(self,data): self.data = data

@dataclass
class Matrix2D():
    data: Tuple[Tuple[MatrixData,...],...]
    def at(self,pos:MatrixCoord) -> MatrixData: return self.data[pos.x][pos.y]