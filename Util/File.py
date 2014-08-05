#-*-encoding: cp1252-*-
from Clases.Coordenada import *
from Clases.Poligono import *
from Util.Triangulacion import *

def stringToPolygon(datos):
    flag = False
    coordenadas = []
    error = ''
    indice = 0
    cad = ''
    #Recorremos las lineas guardando en 'cad' lo que hay entre paréntesis.
    for line in datos:
        for i in range(len(line)):
            if flag == True and line[i] != ")" and line[i] != "(":
                cad = cad + line[i]
            elif flag == True and line[i] == ")":
                indice = indice + 1
                flag = False
                #Creamos la coordenada separando 'cad por comas.'
                cad = cad.split(",")
                if len(cad) != 2:
                    error = error + 'ERROR en polígono: La coordenada '+str(indice)+' es errónea. Formato correcto: (x, y).\n'
                else:
                    try: 
                        float(cad[0]), float(cad[1])
                    except: 
                        error = error + 'ERROR en polígono: Valores de la coordenada '+str(indice)+' erróneos. Ambos deben ser números.\n'
                if error == '':
                    c = coordenada(float(cad[0]), float(cad[1]))
                    coordenadas.append(c)  
            elif line[i] == "(":
                cad = ''
                flag = True
    if error == '':
        if not coordenadas:
            error = 'ERROR de archivo: No existe ninguna coordenada en el fichero.\n'
        elif len(coordenadas) < 3:
            error = 'ERROR en Polígono: El polígono debe estar formado por 3 coordenadas como mínimo.\n'
    if error == '':  
        poly = poligono(coordenadas)  
        polyOptimizado = poly.optimiza()  
        #Validación de rectas que se cortan.     
        for r1 in polyOptimizado.getRectas():
            for r2 in polyOptimizado.getRectas():
                if (intersectan(r1, r2) and not(r2.getA().__eq__(r1.getA()) or 
                                             r2.getA().__eq__(r1.getB()) or
                                             r2.getB().__eq__(r1.getA()) or
                                             r2.getB().__eq__(r1.getB()))):
                    error = 'ERROR en Polígono: Los segmentos '+r1.__repr__()+' y '+r2.__repr__()+' se cortan.\n'
                    break
    if error == '':
        res = polyOptimizado
    else:
        res = error  
    return res