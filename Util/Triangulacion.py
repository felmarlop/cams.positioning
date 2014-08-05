#-*-encoding: cp1252-*-
from Clases.Recta import *
from Clases.Poligono import *

"""Metodo que comprueba si un punto esta dentro de un poligono o no. El poligono debe estar
ordenado  conforme al metodo ordenaPoligono()"""
def estaDentro(a,poly):
    coords = []
    pol = poly.ordena()
    n = len(poly.getCoordenadas())
    coords.extend(pol.getCoordenadas())
    inside =False
    j = 0
    for i in range(n):
        j+=1
        if (j == n):
            j = 0
        if (coords[i].getY() < a.getY() and coords[j].getY() >= a.getY() or coords[j].getY() < a.getY() and coords[i].getY() >= a.getY()):
            if (coords[i].getX() + (a.getY() - coords[i].getY()) / (coords[j].getY() - coords[i].getY()) * (coords[j].getX() - coords[i].getX()) < a.getX()):
                inside = not inside
    return inside

"""Metodo que devuelve el baricentro de un triangulo"""
def baricentro(triangulo):
    a = round((triangulo.getCoordenadas()[0].getX() + triangulo.getCoordenadas()[1].getX() + triangulo.getCoordenadas()[2].getX())/float(3),2)
    b = round((triangulo.getCoordenadas()[0].getY() + triangulo.getCoordenadas()[1].getY() + triangulo.getCoordenadas()[2].getY())/float(3),2)    
    return coordenada(a, b)

"""Metodo que nos dices si dos segmentos se cortan o no. Tambien nos devuelve True si un segmento
esta sobre otro con la misma pendiente"""
def intersectan(r1, r2):
    res = False
    #Igualación de coordenadas
    if r1.getA().__eq__(r2.getA()):
        r1.setA(r2.getA())
    elif r1.getA().__eq__(r2.getB()):
        r1.setA(r2.getB())
    elif r1.getB().__eq__(r2.getA()):
        r1.setB(r2.getA())
    elif r1.getB().__eq__(r2.getB()):
        r1.setB(r2.getB())
    x11 = r1.getA().getX()
    x21 = r1.getB().getX()
    y11 = r1.getA().getY()
    y21 = r1.getB().getY()
    x12 = r2.getA().getX()
    x22 = r2.getB().getX()
    y12 = r2.getA().getY()
    y22 = r2.getB().getY()
    if not r1.__eq__(r2):
        if r1.getPendiente() != r2.getPendiente():
            inter = r1.interseccion(r2)
            #Igualación de intersección con coordenada
            if (inter.__eq__(r1.getA())):
                inter = r1.getA()
            elif (inter.__eq__(r1.getB())):
                inter = r1.getB()
            elif (inter.__eq__(r2.getA())):
                inter = r2.getA()
            elif (inter.__eq__(r2.getB())):
                inter = r2.getB()
            if x11 != x21:
                if (inter.getX() >= x11 and inter.getX() <= x21):
                    if x12 != x22:
                        if (inter.getX() >= x12 and inter.getX() <= x22):
                            res = True
                    else:
                        if (inter.getY() <= y12 and inter.getY() >= y22):
                            res = True
            else:
                if (inter.getX() >= x12 and inter.getX() <= x22):
                    if(inter.getY() <= y11 and inter.getY() >= y21):
                        res = True
        elif (r1.getEcuacion() == r2.getEcuacion()):
            if round(x11 - x21, 5) != 0:
                if ((x11 > x12 and x11 < x22) or (x21 > x12 and x21 < x22)):
                    res = True
                elif ((x12 > x11 and x12 < x21) or (x22 > x11 and x22 < x21)):
                    res = True
            elif round(x11 - x21, 5) == 0:
                if ((y11 < y12 and y11 > y22) or (y21 < y12 and y21 > y22)):
                    res = True
                elif (y12 < y11 and y12 > y21) or (y22 < y11 and y22 > y21):
                    res = True
                    
    return res  

"""Metodo que triangula un poligono. Nos devuelve una lista con los 
correspondientes triangulos"""
def triangular(poly, salida):
    coords = []
    borrado = []
    coords.extend(poly.getCoordenadas())
    if len(coords) >= 3:
        inicio = coords[0]
        for i in range(len(coords) - 2):
            flag = False
            cTriangulo = []
            if coords[i + 1] not in borrado:
                cTriangulo.append(inicio)
                cTriangulo.append(coords[i + 1])
                cTriangulo.append(coords[i + 2])
                r1 = recta(inicio, coords[i + 1])
                r2 = recta(inicio, coords[i + 2])
                pol = poligono(cTriangulo).ordena()
                bari = baricentro(pol)
                if (not estaDentro(bari, poly) and not 
                    estaDentro(r2.puntoMedio(), poly)):
                    flag = True
                if flag == False:
                    for c in coords:
                        if c not in cTriangulo and estaDentro(c, pol):
                                flag = True
                                break
                    if flag == False:
                        for r in poly.getRectas():
                            r1.ordena()
                            r2.ordena()
                            if (intersectan(r, r1) and (r.getPendiente() == 
                                                        r1.getPendiente()) or
                                intersectan(r, r2)  and (r.getPendiente() == 
                                                         r2.getPendiente())):
                                flag = True
                                break
                            if ((intersectan(r, r1) and not(r.getA().__eq__(r1.getA()) or 
                                                        r.getA().__eq__(r1.getB()) or
                                                        r.getB().__eq__(r1.getA()) or
                                                        r.getB().__eq__(r1.getB()))) or 
                                (intersectan(r, r2) and not(r.getA().__eq__(r2.getA()) or 
                                                         r.getA().__eq__(r2.getB()) or
                                                         r.getB().__eq__(r2.getA()) or
                                                         r.getB().__eq__(r2.getB())))):
                                flag = True
                                break
                if flag == False:
                    salida.append(pol)
                    borrado.append(coords[i + 1])
                elif len(coords) == 3:
                    borrado.append(coords[i + 1])
                else:
                    inicio = coords[i + 1]
        afterBorrado = [x for x in coords if x not in borrado]  
        poly = poligono(afterBorrado)
        triangular(poly, salida)
    return salida

