#-*-encoding: cp1252-*-
from Clases.Recta import *  

"""Caminos de Lee. El flag indica si queremos obtener el camino superior o el
inferior de un polígono (True y False)"""
def caminoLee(camino, resCaminoLee, flag):
    inicio = camino[0]
    resCaminoLee.append(inicio)
    if len(camino) > 1:
        lista = []
        if flag:
            pendiente = float('-inf')
        else:
            pendiente = float('inf')
        for c in camino[1:]:
            if ((not (c.getY() < inicio.getY()  and c.getX() < 
                      inicio.getX()) and flag) 
                or (not (c.getY() > inicio.getY()  and c.getX() < 
                         inicio.getX()) and not flag)):
                pendActual =  recta(inicio, c).getPendiente()
                posicion = camino.index(c)
                if pendActual == pendiente:
                    lista.append(c)
                    pos = posicion
                elif ((pendActual > pendiente and flag) or 
                      (pendActual <= pendiente and not flag)):
                    lista = []
                    lista.append(c)
                    pendiente = pendActual
                    pos = posicion
        resCaminoLee.extend(lista[:-1])
        caminoLee(camino[pos:], resCaminoLee, flag)
    return resCaminoLee
