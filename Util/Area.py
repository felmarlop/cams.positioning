#-*-encoding: cp1252-*-
from Util.UtilesArea import *
from shapely.geometry import *
from Clases.Recta import *

def areaPosicion(poly, pos):
    factor = 0
    coordenadas = poly.getCoordenadas()
    bords = bordes(poly)
    bolsas = poly.getBolsas()
    rectasPoly = poly.getRectas()
    limiteBolsa = False
    interiorBolsa = False
    segPosicion = segmentosPosicion(poly, pos, bords)
    segPosicionFinal = []
    segPosicionFinal.extend(segPosicion[3])
    #Compruebo si la posición se encuentra en una bolsa. Si está en un límite
    #de la bolsa calculo cual es y creo el segmento límite.
    for b in bolsas:
        coords = b.getCoordenadas()
        if pos in coords:
            #Si está en una bolsa debemos crear los bordes propios
            #de la posición, a partir de los triángulos en los que ésta se 
            #encuentra implicada.
            triangulosBolsa = []
            coordenadasVisibles = []
            triangular(b, triangulosBolsa)
            puntosBordes = []
            for tr in triangulosBolsa:
                coordsTr = tr.getCoordenadas()
                if pos in coordsTr:
                    coordenadasVisibles.extend(coordsTr)
            for c in coords:
                if (c in coordenadasVisibles and c not in puntosBordes):
                    puntosBordes.append(c)
            if pos.__eq__(coords[0]):
                limiteBolsa = True
                factor = 1
                segmentoLimite = segmentosPosicion(poly, coords[1], bords)[0][0]
            elif pos.__eq__(coords[1]):
                limiteBolsa = True
                segmentoLimite = segmentosPosicion(poly, coords[0], bords)[0][1]
            else:
                pMedioLimite = recta(coords[0], coords[1]).puntoMedio()
                interiorBolsa = True
                break
    if limiteBolsa == True:
        segPosicionFinal = []
        segPosicionFinal.extend(segPosicion[0])
        for br in bords:
            if br.getPendiente() != segmentoLimite.getPendiente():
                if (intersectan(br, segmentoLimite)):
                    bords.insert(bords.index(br) + factor, segmentoLimite)
                    break
    elif interiorBolsa == True:
        #Si nos encontramos en el caso de que la posición sea un vértice convexo, los segmentos
        #de la posición son de distinto orden. Si no cambiamos esto no eligirá bien todos los
        #bordes tocados.
        if segPosicion[2]:
            segPosicionFinal = []
            segRever = segPosicion[3]
            segRever.reverse()
            segPosicionFinal.extend(segRever)
        rectasPoly = poly.getRectas()
        cruzan = False
        segPosicion1 = segPosicion[1][0]
        segPosicion2 = segPosicion[1][1]
        rectaLimite = recta(coords[0], coords[1])
        
        #Los bordes, en este caso, son los correspondientes de la triangulación de la bolsa.
        #Si los dos segmentos de la posicion chocan con el límite de la bolsa, los bordes son
        #los exteriores, los que rodean el polígono.
        poligonoBordes = poligono(puntosBordes).ordenaDesde(pos)
        pBordesOptimizado = poligonoBordes.optimiza()
        rectasP = pBordesOptimizado.getRectas()
        rectasPFinales = []
        indexImaginaria = 0
        distancia = float('inf')
        for rectaImaginaria in rectasP:
            pMedio = rectaImaginaria.puntoMedio()
            distanciaAlLimite = pMedio.distancia(pMedioLimite)
            if rectaImaginaria not in rectasPoly and distanciaAlLimite < distancia:   
                distancia = distanciaAlLimite
                puntosAlargamiento = []
                indexImaginaria = rectasP.index(rectaImaginaria)
                coordsBolsaDesdePosicion = b.ordenaDesde(pos).getCoordenadas()
                for c in coordsBolsaDesdePosicion:
                    if c.__eq__(rectaImaginaria.getA()) or c.__eq__(rectaImaginaria.getB()):
                        puntosAlargamiento.insert(0, c)
                
        if puntosAlargamiento:
            segPosicionA = []
            segPos1 = segmentosPosicion(poly, puntosAlargamiento[0], bords)
            segPos2 = segmentosPosicion(poly, puntosAlargamiento[1], bords)
            #Debemos comprobar si es cónvexo el vértice por el que vamos. El alargamiento dependerá de ello.
            if segPos1[2]:
                seg1 = segPos1[3][1]
                segPosicionA.append(seg1)
            else:
                seg1 = segPos1[3][0]
                segPosicionA.append(seg1)
            if segPos2[2]:
                seg2 = segPos2[3][0] 
                segPosicionA.append(seg2)
            else:
                seg2 = segPos2[3][1]
                segPosicionA.append(seg2)
            rectasPFinales.extend(rectasP[:indexImaginaria])
            #Una vez encontrados los vértices de la recta imaginaria los alargamos hasta los bordes,
            #siempre que no choquen con otra recta del polígono. Pueden chocar entre ellos.
            for r in rectasPoly:
                if not r.__eq__(rectaLimite):
                    extremos = [seg2.getA(), seg2.getB(), seg1.getA(), seg1.getB()]
                    if (r.getA() not in extremos and r.getB() not in extremos):
                        if intersectan(r, seg1) and r.interseccion(seg1) not in coords:
                            cruzan = True
                            break
                        elif intersectan(r, seg2) and r.interseccion(seg2) not in coords:
                            cruzan = True
                            break
            if cruzan == False:
                if intersectan(seg1, seg2):
                    rectasPFinales.extend(segPosicionA)
                    rectasPFinales.extend(rectasP[indexImaginaria + 1:])
                else:
                    rectasSustitucion = areaHastaBordes(puntosAlargamiento[0], segPosicionA, bords).getRectas()[:-2]
                    rectasPFinales.append(seg2)
                    rectasPFinales.extend(rectasSustitucion)
                    rectasPFinales.append(seg1)
                    rectasPFinales.extend(rectasP[indexImaginaria + 1:])
                    
            else:
                rectasPFinales.extend(rectasP[indexImaginaria:])
        else:
            rectasPFinales.extend(rectasP)
        bords = []
        bords.extend(rectasPFinales)   
        bords.remove(segPosicion1)
        bords.remove(segPosicion2)
    else: 
        bords = bordes(poly)
    pol = areaHastaBordes(pos, segPosicionFinal, bords)  
    return pol

"""Devuelve el área comprendida entre un vertice del poligono hasta los bordes."""
def areaHastaBordes(pos, segmentosPosicion, bordes):
    listaPuntos = []
    limitesInterseccion = []
    indicesTocadas = []
    intersecciones = []
    tocadas = []
    interBueno = float('inf')
    ind =  -1
    #Recorro los bordes y caculo las intersecciones con los segmentos de la
    #posición. Las introduzco en limitesIntersección.
    for s in segmentosPosicion:
        distanciaInter = float('inf')
        for bor in bordes:
            if s.getPendiente() != bor.getPendiente():
                inter = bor.interseccion(s)
                if (intersectan(bor, s)):
                    dist = pos.distancia(inter)
                    if dist <= distanciaInter:
                        distanciaInter = dist
                        interBueno = inter
                        ind = bordes.index(bor)
        if interBueno not in limitesInterseccion and interBueno != float('inf'):
            limitesInterseccion.append(interBueno)
        if ind not in indicesTocadas and ind != -1:
            indicesTocadas.append(ind)
    #Calculo las demas intersecciones existentes entre las dos calculadas
    #anteriormente.
    if len(indicesTocadas) > 1:
        indice1 = indicesTocadas[0]
        indice2 = indicesTocadas[1]
        if indice1 >= indice2:
            tocadas.extend(bordes[indice2:indice1 + 1])
        else:
            tocadas.extend(bordes[indice2:])
            tocadas.extend(bordes[:indice1 + 1])
        for i in range(len(tocadas) - 1):
            if tocadas[i].getPendiente() != tocadas[i + 1].getPendiente():
                interBorde = tocadas[i].interseccion(tocadas[i + 1])
                if interBorde not in intersecciones:
                    intersecciones.append(interBorde)
    #Finalmente añado entre las dos intersecciones límites(limitesInterseccion)
    #las que he calculado en el paso anterior. Por último añado pos 
    #(posición tratada) 
    listaPuntos.append(limitesInterseccion[-1])
    listaPuntos.extend(intersecciones)
    listaPuntos.append(limitesInterseccion[0])
    listaPuntos.append(pos)
    pol = poligono(listaPuntos)
    return pol

"""Devuelve el área óptima de una posicion, es decir, con la interseccion de las áreas de
los vértices cóncavos que vea, si os hay."""
def areaOptima(poly, pos):
    res = []
    bolsas = poly.getBolsas()
    bords = bordes(poly)
    verticesConvexos = []
    area = areaPosicion(poly, pos)
    for b in bolsas:
        coords = b.getCoordenadas()
        if pos in coords:
            #Si está en una bolsa debemos crear los bordes propios
            #de la posición, a partir de los triángulos en los que ésta se 
            #encuentra implicada.
            triangulosBolsa = []
            coordenadasVisibles = []
            triangular(b, triangulosBolsa)
            puntosBordes = []
            for tr in triangulosBolsa:
                coordsTr = tr.getCoordenadas()
                if pos in coordsTr:
                    coordenadasVisibles.extend(coordsTr)
            for c in coords:
                if (c in coordenadasVisibles and c not in puntosBordes):
                    puntosBordes.append(c)
            #Procedemos a calcular si en los bordes calculados hay algún vértice convexo.
            coordsBordes = poligono(puntosBordes).getCoordenadas()
            for ver in coordsBordes:
                segmentosPosicionEnBolsa = segmentosPosicion(poligono(puntosBordes), ver, bords)[2]
                if (not ver.__eq__(pos) and 
                    len(segmentosPosicionEnBolsa) > 0):
                    conjunto = []
                    conjunto.append(ver)
                    segmentosPosicionEnBolsa.reverse()
                    conjunto.append(segmentosPosicionEnBolsa)
                    verticesConvexos.append(conjunto)
    #Si existen vertices convexos, calculamos el área a partir de ellos y después la interseccion
    #con el área correspondiente al punto que estamos tratando.
    if (verticesConvexos):
        coordenadasArea = []
        conjuntoDeAreas = []
        coordenadasArea.extend(area.getCoordenadas())
        conjuntoDeAreas.append(area)
        for vc in verticesConvexos:
            areavc = areaHastaBordes(vc[0], vc[1], bords)
            conjuntoDeAreas.append(areavc)
        inters = intersecciones(conjuntoDeAreas)
        if inters:
            res.extend(inters[0].getCoordenadas())
        else:
            res.extend(area.getCoordenadas())
    else:
        res.extend(area.getCoordenadas())
    return poligono(res).optimiza()

"""Nos devuelve las intersecciones de un conjunto de áreas, cuando las hay."""
def intersecciones(areas):
    salida = []
    #Recorremos áreas transformándolas en formato Shapely y comprobando las intersecciones.
    for a in areas:
        hayInterseccion = False
        aShapely = Polygon(a.getTuplas())
        for b in areas:
            bShapely = Polygon(b.getTuplas())
            if not a.__eq__(b):
                interseccion = aShapely.intersection(bShapely)
                if isinstance(interseccion, Polygon):
                    aShapely = interseccion
                    hayInterseccion = True
        #Si hay interseccion la transformamos de nuevo a objeto Polígono y lo guardamos.
        if hayInterseccion:
            coordenadasArea = []
            for tupl in aShapely.exterior.coords[:]:
                c = coordenada(round(tupl[0], 2), round(tupl[1], 2))
                if c not in coordenadasArea:
                    coordenadasArea.append(c)
            if len(coordenadasArea) > 2:
                polyInter = poligono(coordenadasArea).ordena()
                polyInterOrd = polyInter.optimiza()
                if polyInterOrd not in salida:
                    salida.append(polyInterOrd)
    return salida
    
            
            











        