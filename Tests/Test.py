#-*-encoding: utf-8-*-
'''
Created on 08/12/2013

@author: Felix
'''
import time, pprint, json
from Clases.Poligono import *
from Util.Triangulacion import *
from Util.File import *
from Util.Area import *
from Drawings.Drawings import *
from shapely.geometry import *
"""Polígono 1"""
l = []
c8 = coordenada(1,9)
c1 = coordenada(1,2)
c2 = coordenada(2,4)
c3 = coordenada(1,5)
c5 = coordenada(5,5)
c6 = coordenada(4,4)
c7 = coordenada(6,2)
l.append(c7)
l.append(c1)
l.append(c2)
l.append(c3)
l.append(c8)
l.append(c5)
l.append(c6)
p = poligono(l).ordena()
"""Polígono 2"""
l2 = []
cc4 = coordenada(4,6)
cc5 = coordenada(5,8)
cc6 = coordenada(6,4)
cc7 = coordenada(6,6)
cc8 = coordenada(6.2,1)
cc9 = coordenada(5,3)
cc1 = coordenada(4,2)
cc2 = coordenada(3,3)
cc3 = coordenada(3,4)
cc10 = coordenada(4,4)
cc11 = coordenada(7,6)
cc12 = coordenada(6,2.5)
cc13 = coordenada(5.5,5)
cc14 = coordenada(5,5)
l2.append(cc7)
l2.append(cc11)
l2.append(cc12)
l2.append(cc8)
l2.append(cc9)
l2.append(cc1)
l2.append(cc2)
l2.append(cc3)
l2.append(cc10)
l2.append(cc4)
l2.append(cc5)
l2.append(cc13)
l2.append(cc14)
l2.append(cc6)
p2 = poligono(l2).ordena()
"""OR#DENAR Y OPTIMIZAR SIEMPRE LOS POLÍGONOS CREADOS"""
ain = time.time()
#pp = stringToPolygon("(1,2) (2,2) (3,2) (5,4) (4,4)(3.5, 2.7) (3, 3.2) (3,4) (3.5, 3.8) (5,6) (5,6) (5,7)")
#pp = stringToPolygon("(1,2) (2,2) (3,2) (5,3) (5,4) (3.5, 3.5) (3.5, 4.5) (5,6) (5,6) (5,7)")
#pp = stringToPolygon("(1,2) (2,2) (3,2)(5, 3) (5,4) (4,4) (4,3.5)(3, 3.2) (3,4) (3.5, 3.5) (5,6) (5,6) (5,7)")
#pp = stringToPolygon("(3, 3) (3.5, 2) (3.5, 1)(7, 1) (5, 5) (5, 4)(6, 1.5)(5, 1.5)(4, 3)(5.5, 2)(4,4)(3.8, 5)(4.5, 6) (3.5, 5) (3.5, 3.3)")
#pp = stringToPolygon("(3, 3) (3.5, 1)(7, 1) (5, 5) (4.5, 5)(6, 1.5)(5.5, 1.5)(5.5, 2)(5, 1.5) (4, 6)")
#pp = stringToPolygon("(3.5, 5)(3.5, 1)(7, 1) (7, 5) (5, 5)(5, 4.5) (4.5,4.5)(6, 4)(6, 2)(5.5, 2.2)(5,2)(4, 5)")
#pp = stringToPolygon("(1,2) (2,2) (3,2) (5,4) (4,6) (3.8, 5)(4, 4.8) (4.3, 4.3) (4, 4) (3, 4) (3.8, 6)")
#pp = stringToPolygon("(1.0,2.0), (4,5.5), (4.0,5.0), (3.5,4.6), (4.5,4.5), (4.0,3.5), (3.0,3.5), (3.0,3.0), (5.0,2.5), (3.0,2.0)")
#pp = stringToPolygon("(10,6)(10, 40) (20,40) (20, 20)(25, 20)(25, 50) (30,50)(35, 30)(30,20)(40,20) (40,3) (30, 13) (25, 11)(20, 5)")
#pp = stringToPolygon("(1.5,1)(1.3, 2)(2.2, 2.2)(2, 3)(3, 4)(3.5, 3)(3, 2.5)(4.3, 2.3)(4.3, 2.1)(3.5, 1.8)(3.6, 1.5)(4.5, 1.5)(4.4, 1)")
#pp =stringToPolygon("(1,2) (2,2) (3,2) (5,4) (4,4) (3.5,2.7)(3, 3.2) (3,4) (3.5, 3.8) (5,6) (5,6) (5,7)")
#pp =stringToPolygon("(4, 5) (7,4) (6.5, 2) (7,1) (6,1) (6,2) (5, 2) (5.5, 3) (6, 2.5) (6.5, 3) (5, 4.5) (4.5, 1.5) (5.5, 1.5) (4,1) (3, 1) (3.5, 1.5)(3.5, 2)(4,2) (3.5, 3)(3,2) (3,4)")
#pp =stringToPolygon("(1,1)(20, 1)(35, 3)(25, 3)(20, 5)(28, 5)(35, 9)(35, 10)(25, 7)(15, 7)")
#pp = p2
#pp = p
#pp.drawing()

#Creación del polígono
pp = stringToPolygon("(9,6) (12,21) (13, 14)(20, 14)(15, 10)(10, 10)(10, 7)(14,3)(14,7.5)(12,7)(12.7,5)(11,8)(15,8)(15, 1)")

#Ordenamos el polígono
pO = pp.ordena()

#Calculamos los puntos o las posiciones de visión
conjuntoPosiciones = posicionesTopograficas(pO)

#A partir de las posiciones creamos las áreas a partir de dichos puntos.
l = []
for ps in conjuntoPosiciones:
    a = areaOptima(pO, ps)
    l.append(a)
b = time.time()
print("Tiempo de ejecución: "+str(b - ain)+" segundos")

#Dibujamos la salida
drawAreas(pO, l)

























