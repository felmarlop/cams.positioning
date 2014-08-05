#-*-encoding: cp1252-*-
"""
Objeto: Recta
Atributos: Dos coordenadas
"""
from Clases.Coordenada import *

class recta():
    a = coordenada
    b = coordenada
    def __init__(self, a, b):
        self.a = a
        self.b = b
    
    """Getters y setters"""      
    def getA(self):
        return self.a
    
    def getB(self):
        return self.b
    
    def setA(self, nuevaA):
        self.a = nuevaA
    
    def setB(self, nuevaB):
        self.b = nuevaB
    
    """Método que devuelve la pendiente de una recta"""
    def getPendiente(self):
        numerador = float(self.b.getY() - self.a.getY())
        denominador = float(self.b.getX() - self.a.getX())
        res = 0
        if denominador == 0:
            if numerador < 0:
                res = float('-inf')
            if numerador > 0:
                res = float('inf')
        else:
            res = (numerador/denominador)
        return res
    
    """Método que ordena una recta desde izquierda a derecha"""
    def ordena(self):
        nuevaA = self.getB()
        nuevaB = self.getA()
        if self.getA().getX() != self.getB().getX():
            if self.getA().getX() > self.getB().getX():
                self.a = nuevaA
                self.b = nuevaB
        elif self.getA().getY() < self.getB().getY():
                self.a = nuevaA
                self.b = nuevaB
    
    """Método que devuelve el punto medio de una recta"""
    def puntoMedio(self):
        return coordenada(float(self.getA().getX() + self.getB().getX())/float(2), 
                          float(self.getA().getY() + self.getB().getY())/float(2))
      
    """Parámetro necesario para la ecuación de una recta"""  
    def bEcuacion(self):
        b = self.getA().getY() - (self.getPendiente() * self.getA().getX())
        return b
    
    """Método que devuelve la ecuación de una recta"""
    def getEcuacion(self):
        if (self.getPendiente() == float('inf') or
            self.getPendiente() == float('-inf')):
            res = "Y = "+str(self.getA().getX())+"X"
        elif self.getPendiente() == 0:
            res = "Y = "+str(self.getA().getY())
        else:
            res = "Y = "+str(self.getPendiente())+"X + "+str(self.bEcuacion())
        return res
    
    """Método que comprueba si una coordenada está en una recta"""
    def contieneA(self, punto):
        res = False
        if (self.getPendiente() == float('inf') or
            self.getPendiente() == float('-inf')):
            res = (punto.getY() == self.getA().getX() + punto.getX())
        elif self.getPendiente() == 0:
            res = (punto.getY() == self.getA().getX())
        else:
            res = (punto.getY() == (self.getPendiente() + punto.getX()*self.bEcuacion()))
        return res
    
    """Método que devuelve la coordenada de corte entre dos rectas"""
    def interseccion(self, other):
        if (self.getPendiente() == float('inf') or
            self.getPendiente() == float('-inf')):
            xr = self.getA().getX()
            yr = other.bEcuacion() + (xr*other.getPendiente())
            res = coordenada(round(xr, 2), round(yr, 2))
        elif (other.getPendiente() == float('inf') or
            other.getPendiente() == float('-inf')):
            xr = other.getA().getX()
            yr = self.bEcuacion() + (xr*self.getPendiente())
            res = coordenada(round(xr, 2), round(yr, 2))
        else: 
            incrementoS = (-self.getPendiente()) - (-other.getPendiente())
            incrementoX = (self.bEcuacion()) - (other.bEcuacion())
            incrementoY = (-self.getPendiente()*other.bEcuacion()) - (-other.getPendiente()*self.bEcuacion()) 
            xr = incrementoX/incrementoS
            yr = incrementoY/incrementoS
            res = coordenada(round(xr, 2), round(yr, 2))
        return res
    
    def __eq__(self, other):
        return (self.getA().__eq__(other.getA()) and self.getB().__eq__(other.getB()))
    
    def __repr__(self):
        return str(self.a)+" - "+str(self.b)
    
    