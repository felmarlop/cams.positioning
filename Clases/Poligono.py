#-*-encoding: cp1252-*-
"""
Objeto: Poligono
Atributos: Lista de coordenadas
"""
from Clases.Recta import *
from Util.CaminosDeLee import *
from Drawings.Drawings import *

class poligono():
    coordenadas = []
    def __init__(self, coordenadas):
        self.coordenadas = coordenadas
    
    """Getters y setters"""
    def getCoordenadas(self):
        return self.coordenadas
    
    def setCoordenadas(self, newCoordenadas):
        self.coordenadas = newCoordenadas
        
    def getTuplas(self):
        tuplas = []
        for c in self.getCoordenadas():
            tuplas.append(c.tuple())
        tuplas.append(self.getCoordenadas()[0].tuple())
        return tuplas
    
    def __eq__(self, other):
        inicio = self.getCoordenadas()[0]
        selfOrd = self.ordenaDesde(inicio)
        if inicio in other.getCoordenadas():
            other = other.ordenaDesde(inicio)
        return selfOrd.getCoordenadas().__eq__(other.getCoordenadas())
    
    def __repr__(self):
        return self.coordenadas.__repr__()
    
    """Devuelve la coordenada de mayor abscisa"""
    def coordenadaMayorAbscisa(self):
        res = coordenada
        if(self.coordenadas == []):
            res = coordenada(0, 0)
        else:
            res = sorted(self.coordenadas, key = lambda 
                         coordenada: coordenada.x)[-1]
        return res
    
    """Devuelve la coordenada de menor abscisa"""
    def coordenadaMenorAbscisa(self):
        res = coordenada
        if(self.coordenadas == []):
            res = [0,0]
        else:
            res = sorted(self.coordenadas, key = lambda
                       coordenada: coordenada.x)[0]
        return res
    
    """Debuelve la coordenada de mayor ordenada"""
    def coordenadaMayorOrdenada(self):
        res = coordenada
        if(self.coordenadas == []):
            res = coordenada(0,0)
        else:
            res = sorted(self.coordenadas, key = lambda
                       coordenada: coordenada.y)[-1]
        return res
    
    """Devuelve la coordenada de menor ordenada"""
    def coordenadaMenorOrdenada(self):
        res = []
        if(self.coordenadas == []):
            res = [0,0]
        else:
            res = sorted(self.coordenadas, key = lambda
                       coordenada: coordenada.y)[0]
        return res
    
    """Devuelve los dos caminos, superior e infeior, del polígono"""
    def getCaminos(self):
        res = []
        camino1 = []
        camino2 = []
        posMenorAbscisa = self.coordenadas.index(self.coordenadaMenorAbscisa())
        posMayorAbscisa = self.coordenadas.index(self.coordenadaMayorAbscisa())
        
        #Construcion de los dos caminos desde la coordenada de menor
        #abscisa a la de mayor.
        if posMenorAbscisa < posMayorAbscisa:
            camino1.extend(self.coordenadas[posMenorAbscisa:posMayorAbscisa+1])
            camino2.extend(self.coordenadas[posMayorAbscisa:])
            camino2.extend(self.coordenadas[:posMenorAbscisa+1])
        else:
            camino1.extend(self.coordenadas[posMayorAbscisa:posMenorAbscisa+1])
            camino2.extend(self.coordenadas[posMenorAbscisa:])
            camino2.extend(self.coordenadas[:posMayorAbscisa+1])
            
        #Ordenar caminos, ambos de izquierda a derecha.
        if not camino1[0].__eq__(self.coordenadaMenorAbscisa()):
            camino1.reverse()
        else:
            camino2.reverse()
            
        #Diferenciar cual es el superior e inferior. Tratando los casos en los
        #que los caminos sólo tienen dos puntos.
        pendienteCamino1 = recta(camino1[0], camino1[1]).getPendiente()
        pendienteCamino2 = recta(camino2[0], camino2[1]).getPendiente()
        if pendienteCamino1 > pendienteCamino2:
            res.append(camino1)
            res.append(camino2)
        else:
            res.append(camino2)
            res.append(camino1)
        return res
    
    """Aplica el algoritmo de Lee al polígono y devuelve el nuevo polígono"""
    def algoritmoDeLee(self):
        superior = []
        inferior = []
        LS = []
        LI = []
        res = []
        superior.extend(caminoLee(self.getCaminos()[0], LS, True))
        inferior.extend(caminoLee(self.getCaminos()[1], LI, False))
        inferior.reverse()
        res.extend(superior)
        res.extend(inferior[1:-1])
        return poligono(res)
    
    """Devuelve el poligono ordenado en sentido horario"""
    def ordena(self):
        res = []
        reverse = []
        res.extend(self.getCaminos()[0])
        reverse.extend(self.getCaminos()[1])
        reverse.reverse()
        res.extend(reverse[1:-1])
        pol = poligono(res)
        return pol
    
    """Metodo para ordenar poligono desde una determinada coordenada"""
    def ordenaDesde(self, c):
        res = []
        coords = []
        pOrdenado = self.ordena()
        coords.extend(pOrdenado.getCoordenadas())
        pos = coords.index(c)
        res.extend(coords[pos:])
        res.extend(coords[0:pos])
        pol = poligono(res)
        return pol
    
    """Devuelve el polígono sin coordenadas repetidas, si se da el caso, y sin
    coordenadas que no formen un vértice."""
    def optimiza(self):
        res = []
        coords = self.getCoordenadas()
        for c in coords:
            if c not in res:
                res.append(c)
        polySinrepeticion = poligono(res)
        rectasS = polySinrepeticion.getRectas()
        for i in range(len(rectasS)):
            if i == len(rectasS) - 1:
                r1 = rectasS[i]
                r2 = rectasS[0]
            else:
                r1 = rectasS[i]
                r2 = rectasS[i + 1]
            if r1.getPendiente() == r2.getPendiente():
                if r1.getA().__eq__(r2.getA()) or r1.getA().__eq__(r2.getB()):
                    res.remove(r1.getA())
                else:
                    res.remove(r1.getB())
        polySalida = poligono(res)
        return polySalida
    
    """Bolsas de un poligono"""
    def getBolsas(self):
        pLee = self.algoritmoDeLee()
        pOrd = self.ordena()
        pLeeCoords = pLee.getCoordenadas()
        pCoords = pOrd.getCoordenadas()
        res = []
        pFin = []
        ultimaP = pCoords[-1]
        ultimaPLee = pLeeCoords[-1]
        for i in range(len(pLeeCoords)-1):
            c1 = pLeeCoords[i]
            c2 = pLeeCoords[i+1]
            indexC1 = pCoords.index(c1)
            indexC2 = pCoords.index(c2)
            if indexC2 -  indexC1 != 1:
                pRes = poligono(pCoords[indexC1:indexC2+1])
                res.append(pRes.ordenaDesde(pRes.getCoordenadas()[0]))
        if not ultimaP.__eq__(ultimaPLee):
            indexFinal = pCoords.index(ultimaPLee)
            pFin.extend(pCoords[indexFinal:])
            pFin.append(pCoords[0])
            res.append(poligono(pFin).ordenaDesde(poligono(pFin).getCoordenadas()[0]))
        return res
    
    """Método que nos devuelve las rectas del polígono"""
    def getRectas(self):
        res = []
        for i in range(len(self.getCoordenadas()) - 1):
                    r = recta(self.getCoordenadas()[i], self.getCoordenadas()[i + 1])
                    r.ordena()
                    res.append(r)
        r = recta(self.getCoordenadas()[-1], self.getCoordenadas()[0])
        r.ordena()
        res.append(r)
        return res
    
    """Representa el polígono en una ventana de Graphics"""
    def drawing(self):
        g = window(self)
        p = polygon(self, [], "grey", "orange")
        p[0].draw(g)
        for l in p[1]:
            l.draw(g)
        mensaje = message(self, "Éste es tu polígono. Click para cerrar.")
        mensaje.draw(g)
        g.getMouse()
        g.close()
        
        
        
        
        
        
        