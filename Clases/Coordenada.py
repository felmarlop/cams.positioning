#-*-encoding: cp1252-*-
"""
Objeto: Coordenada
Atributos: X e Y
"""
import math

class coordenada():
    x = float
    y = float
    def  __init__(self, x, y):
        self.x = x
        self.y = y
    
    """Getters"""
    def getX(self):
        return self.x
    
    def getY(self):
        return self.y
    
    """Distancia entre dos coordenadas"""
    def distancia(self, other):
        restaX = other.getX() - self.getX()
        restaY = other.getY() - self.getY()
        suma = (restaX * restaX) + (restaY * restaY)
        return math.sqrt(suma)
    
    """Devuelve una tupla"""
    def tuple(self):
        return (self.x, self.y)
    
    def __eq__(self, other):
        res = (self.x, self.y) == (other.x, other.y)
        if res == False:
            if (round(self.x - other.x, 7) == 0) and (round(self.y - other.y, 7) == 0):
                res = True
        return res
        
    def __repr__(self):
        return "("+str(self.x)+","+str(self.y)+")"