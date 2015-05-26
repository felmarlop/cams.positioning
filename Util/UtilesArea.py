#-*-encoding: cp1252-*-
from Clases.Recta import *
from Util.Posicion import *
from Util.Triangulacion import *

"""Metodo que devuelve las 4 rectas que rodean el pol�gono en forma de rectas."""
def rectasLados(poly):
    lados = []
    menorAbscisa = poly.coordenadaMenorAbscisa()
    mayorAbscisa = poly.coordenadaMayorAbscisa()
    menorOrdenada = poly.coordenadaMenorOrdenada()
    mayorOrdenada = poly.coordenadaMayorOrdenada()
    porcentajeAbscisa = (poly.coordenadaMayorAbscisa().getX() - 
                         poly.coordenadaMenorAbscisa().getX()) * 0.2
    porcentajeOrdenada = (poly.coordenadaMayorOrdenada().getY() -
                          poly.coordenadaMenorOrdenada().getY()) * 0.2
    ladoIzquierdo = recta(coordenada(menorAbscisa.getX() - porcentajeAbscisa,
                                     menorAbscisa.getY()),
                          coordenada(menorAbscisa.getX() - porcentajeAbscisa,
                           menorAbscisa.getY() + porcentajeAbscisa))
    lados.append(ladoIzquierdo)
    ladoSuperior = recta(coordenada(mayorOrdenada.getX(),
                                    mayorOrdenada.getY() + porcentajeOrdenada),
                         coordenada(mayorOrdenada.getX() + porcentajeOrdenada,
                                    mayorOrdenada.getY() + porcentajeOrdenada))
    lados.append(ladoSuperior)         
    ladoDerecho = recta(coordenada(mayorAbscisa.getX() + porcentajeAbscisa,
                                   mayorAbscisa.getY()),
                        coordenada(mayorAbscisa.getX() + porcentajeAbscisa,
                                   mayorAbscisa.getY() + porcentajeAbscisa))
    lados.append(ladoDerecho)    
    ladoInferior = recta(coordenada(menorOrdenada.getX(),
                                    menorOrdenada.getY() - porcentajeOrdenada),
                         coordenada(menorOrdenada.getX() + porcentajeOrdenada,
                                    menorOrdenada.getY() - porcentajeOrdenada))
    lados.append(ladoInferior)
    
    return lados

"""M�todo que devuelve los 4 puntos donde se cortan los bordes"""
def esquinas(poly):
    bordes = rectasLados(poly)
    esquinasS = []
    #Recorro los bordes y saco la intersecci�n para calcular las esquinas.
    for i in range(len(bordes)):
        if i == (len(bordes) - 1):
            esquina = bordes[i].interseccion(bordes[0])
            esquinasS.append(esquina)
        else:
            esquina = bordes[i].interseccion(bordes[i + 1])
            esquinasS.append(esquina)
    return esquinasS

"""M�todo que devuelve los segmentos que rodean al poligono"""
def bordes(poly):
    salida = []
    poligonoFuera = poligono(esquinas(poly))
    salida.extend(poligonoFuera.getRectas())
    return salida

"""M�todo cuya salida nos proporciona los segmentos para comenzar a calcular
el área visible de una posición"""
def segmentosPosicion(poly, p, bord):
    coords = []
    segmentosFinales = []
    segmentosABorrar = []
    #Listas de segmentos necesarias para el área en bolsas.
    segmentosAuxiliares = []
    segmentosInterior = []
    #bord = bordes(poly)
    coords.extend(poly.getCoordenadas())
    segmentosTotales = []
    segmentosTotales.extend(poly.getRectas())
    #Calculo las dos rectas implicadas en la posición
    rectasS = []
    ind = coords.index(p)
    if ind == 0:
        r1 = recta(coords[-1], coords[ind])
        r2 = recta(coords[ind], coords[ind + 1])
    elif ind == (len(coords) - 1):
        r1 = recta(coords[ind - 1], coords[ind])
        r2 = recta(coords[ind], coords[0])
    else:
        r1 = recta(coords[ind - 1], coords[ind])
        r2 = recta(coords[ind], coords[ind + 1])
    r1.ordena()
    r2.ordena()
    rectasS.append(r1)
    rectasS.append(r2)
    for r in rectasS:
        segmentosIniciales = []
        segmentosIntermedios = []
        #Una vez calculadas las rectas, calculo los segmentos de la recta que
        #tocan los bordes.
        for l in bord:
            if r.getPendiente() != l.getPendiente():
                inter = l.interseccion(r)
                segmento = recta(p, inter)
                segmento.ordena()
                if (intersectan(l, segmento)):
                    if segmento not in segmentosIniciales:
                        segmentosIniciales.append(segmento)
                        segmentosTotales.append(l)
        #Una vez calculados los segmentos, debemos sacar aquellos cuyo extremo
        #es el primer punto de corte que se ecuentra.
        for seg in segmentosIniciales:
            limite = float('inf')
            for sT in segmentosTotales:
                if seg.getPendiente() != sT.getPendiente():
                    if (intersectan(seg, sT)):
                        if sT in bord:
                            inter = seg.interseccion(sT)
                            dist = p.distancia(inter)
                            if dist <= limite:
                                limite = dist
                                extremo = inter
                        else:
                            if not (seg.getA().__eq__(sT.getA()) or seg.getA().__eq__(sT.getB()) or
                                seg.getB().__eq__(sT.getA()) or seg.getB().__eq__(sT.getB())): 
                                inter = seg.interseccion(sT)
                                dist = p.distancia(inter)
                                if dist <= limite:
                                    limite = dist
                                    extremo = inter     
            segmentoIntermedio = recta(p, extremo)
            segmentoIntermedio.ordena()
            segmentosIntermedios.append(segmentoIntermedio)
            segmentosIntermedios.append(seg)
        s0 = segmentosIntermedios[0]
        s1 = segmentosIntermedios[2]
        #Por último, debemos seleccionar qué segmento intermedio es el bueno, 
        #el que va hacia el exterior del poligono. Marcar para borrar los 
        #segmentos que coincidan con alguna recta del polígono.
        if estaDentro(s0.puntoMedio(), poly) and (s0 not in rectasS):
            segmentosFinales.append(s1)
            segmentosABorrar.append(s1)
            segmentosAuxiliares.append(segmentosIntermedios[1])
            segmentosInterior.append(segmentosIntermedios[3])
        elif s1 in rectasS:
            segmentosFinales.append(s0)
            segmentosABorrar.append(s1)
            segmentosInterior.append(segmentosIntermedios[1])
        #En el caso de tratarse de una posición cóncava (Cuando sus segmentos
        #están en rectasS), se cambia el orden de los segmentos (insert)
        if estaDentro(s1.puntoMedio(), poly) and (s1 not in rectasS):
            segmentosFinales.insert(0, s0)
            segmentosABorrar.append(s0)
            segmentosAuxiliares.append(segmentosIntermedios[3])
            segmentosInterior.append(segmentosIntermedios[1])
        elif s0 in rectasS:
            segmentosFinales.append(s1)
            segmentosABorrar.append(s0)
            segmentosInterior.append(segmentosIntermedios[3])
    res = []
    res.append(segmentosFinales)
    res.append(segmentosABorrar)
    res.append(segmentosAuxiliares)
    res.append(segmentosInterior)
    return res
                    
                    
    
        
                        
                        
            
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
    
    