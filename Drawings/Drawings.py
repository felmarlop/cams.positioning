#-*-encoding: cp1252-*-
import random
from Libs.graphics import *

def window(poly):
    g = GraphWin("Drawing", 600, 600)
    g.setBackground("black")
    porcentajeAbscisa = (poly.coordenadaMayorAbscisa().getX() - 
                         poly.coordenadaMenorAbscisa().getX()) * 0.2
    porcentajeOrdenada = (poly.coordenadaMayorOrdenada().getY() -
                          poly.coordenadaMenorOrdenada().getY()) * 0.2
    maximaX = (poly.coordenadaMayorAbscisa().getX() + porcentajeAbscisa)
    maximaY = (poly.coordenadaMayorOrdenada().getY() + porcentajeOrdenada)
    minimaX = (poly.coordenadaMenorAbscisa().getX() - porcentajeAbscisa)
    minimaY = (poly.coordenadaMenorOrdenada().getY() - porcentajeOrdenada)
    g.setCoords(minimaX, minimaY, maximaX, maximaY)
    return g

def message(poly, message):
    porcentajeAbscisa = poly.coordenadaMayorAbscisa().getX() * 0.2
    porcentajeOrdenada = poly.coordenadaMayorOrdenada().getY() * 0.2
    maximaY = (poly.coordenadaMayorOrdenada().getY() + porcentajeOrdenada/2)
    minimaX = (poly.coordenadaMenorAbscisa().getX() + porcentajeAbscisa)
    message = Text(Point(minimaX, maximaY), message)
    message.setFill("white")
    return message

def polygon(poly, posiciones, color1, color2):
    puntos = []
    labels = []
    pos = []
    circles = []
    salida = []
    for c in poly.getCoordenadas():
        point = Point(c.getX(), c.getY())
        if c in posiciones:
            polyUnPunto = []
            polyUnPunto.append(point)
            polyPosicion = Polygon(polyUnPunto)
            polyPosicion.setOutline("Lime Green")
            polyPosicion.setWidth(7)
            circles.append(polyPosicion)
            pos.append(point)
            label = Text(point, "("+str(c.getX())+", "+str(c.getY())+")")
            label.setFill("#8b8989")
            label.setStyle('italic')
            labels.append(label)
        else:
            label = Text(point, "("+str(c.getX())+", "+str(c.getY())+")")
            label.setFill("#8b8989")
            labels.append(label)
        puntos.append(point)
    p = Polygon(puntos)
    p.setWidth(2)
    p.setOutline(color1)
    p.setFill(color2)
    salida.append(p)
    salida.append(labels)
    salida.append(circles)
    return salida 

def drawPosiciones(poly, posiciones):
    pol = polygon(poly, posiciones, "white", "orange red")
    gWin = window(poly)
    p = pol[0]
    p.draw(gWin)
    for c in pol[2]:
        c.draw(gWin)
    for l in pol[1]:
        l.draw(gWin)
    mensaje = message(poly, "Click en la imagen para ver áreas de visión.")
    mensaje.draw(gWin)
    gWin.getMouse()
    gWin.close()
    
"""Metodo que dibuja un conjunto de poligonos"""
def leeDraw(listaPoligonos):
    dibujos = []
    colores =  ["blue", "red"]
    for pol in listaPoligonos:
        puntos = []
        for c in pol.getCoordenadas():
            point = Point(c.getX(), c.getY())
            puntos.append(point)
        p = Polygon(puntos)
        p.setWidth(2)
        dibujos.append(p)
    maximaX = (listaPoligonos[0].coordenadaMayorAbscisa().getX() + 1).__abs__()
    maximaY = (listaPoligonos[0].coordenadaMayorOrdenada().getY() + 1).__abs__()
    minimaX = (listaPoligonos[0].coordenadaMenorAbscisa().getX() - 1).__abs__()
    minimaY = (listaPoligonos[0].coordenadaMenorOrdenada().getY() - 1).__abs__()
    g = GraphWin("Drawing", 400, 400)
    g.setBackground("beige")
    g.setCoords(minimaX, minimaY, maximaX, maximaY)
    for d2 in dibujos[2:]:
        d2.setFill("white")
        d2.draw(g)
    for d in dibujos[:2]:
        for color in colores:
            d.setOutline(color)
            colores.remove(color)
        d.draw(g)
    g.mainloop()
    

def drawAreas(poly, areas):
    gWin = window(poly)
    coloresArea = ['#98fb98', '#7fffd4', '#add8e6', '#ffc0cb', '#ffdab9']
    p = polygon(poly, [], "white", "orange red")
    for a in areas:
        ind = random.choice(range(len(coloresArea)))
        pol = polygon(a, [], "Lime Green", coloresArea[ind])
        pol[0].draw(gWin)
    p[0].draw(gWin)
    for l in p[1]:
        l.draw(gWin)
    mensaje = message(poly, "Click en la imagen para cerrar")
    mensaje.draw(gWin)
    gWin.getMouse()
    gWin.close()
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    