#-*-encoding: cp1252-*-
from Clases.Poligono import *
from Util.Triangulacion import *

"""Método que colorea las coordenadas del polígono de Lee con
dos colores. La  última coordenada tratada se pinta de ambos colores en el caso de
haber vértices impares"""
def dosColoracion(poly):
    coordsLee = poly.algoritmoDeLee().getCoordenadas()
    coords = poly.getCoordenadas()
    dic = {"Rojo": [], "Verde": []}
    for i in range(len(coordsLee)):
        if i%2 == 0:
            dic["Rojo"].append(coordsLee[i])
        else:
            dic["Verde"].append(coordsLee[i])
        if (i == (len(coordsLee) - 1) and len(coordsLee)%2 != 0
            and coords[-1] == coordsLee[i]):
            if coordsLee[i] in dic["Rojo"]:
                dic["Verde"].append(coordsLee[i])
            else:
                dic["Rojo"].append(coordsLee[i])
    return dic

"""Metodo que nos devuelve la lista de coordenadas optima desde donde podemos visionar todo 
el poligono"""
def galeriaDeArte(poly, flag):
    triangulos = []
    tr = []
    pintados = []
    #limite = float('inf')
    triangulos.extend(triangular(poly, tr))
    #Creamos un diccionario de colores y pintamos la primera y ultima coordenada del poligono
    #segun el valor de flag.
    dic  = {"Rojo": [],"Verde": [], "Azul": []}
    if flag == True:
        dic["Rojo"].append(poly.getCoordenadas()[0])
        dic["Verde"].append(poly.getCoordenadas()[1])
    else:
        dic["Rojo"].append(poly.getCoordenadas()[1])
        dic["Verde"].append(poly.getCoordenadas()[0])
    cComprueba = []
    cComprueba.append(poly.getCoordenadas()[0])
    cComprueba.append(poly.getCoordenadas()[1])
    while len(pintados) != len(triangulos):
        #Estudiamos el triangulo sin pintar que tenga dos de sus coordenadas en cComprueba.
        for t in triangulos:
            if t not in pintados:
                if ((t.getCoordenadas()[0] in cComprueba and t.getCoordenadas()[1] in cComprueba) or
                    (t.getCoordenadas()[0] in cComprueba and t.getCoordenadas()[2] in cComprueba) or
                    (t.getCoordenadas()[1] in cComprueba and t.getCoordenadas()[2] in cComprueba)):
                    #Seleccionamos la coordenada sin pintar.
                    for c in t.getCoordenadas():
                        if (c not in dic.values()[0] and
                            c not in dic.values()[1] and
                            c not in dic.values()[2]):
                            #Pintamos esa coordenada del color que ninguna de las del triangulo tengan.
                            for l in dic.values():
                                if not any(cor in t.getCoordenadas() for cor in l):
                                    l.append(c)
                                    cComprueba.extend(t.getCoordenadas())
                                    pintados.append(t)
                                    
    return dic



"""Método que colorea las coordenadas del polígono completo. Las bolsas
se colorean con 3 colores, incluyendo los dos anteriormente utilizados."""
def coloracionPoligono(poly):
    
    #Obtenemos las bolsas del polígono y creamos el diccionario.
    bolsas = poly.getBolsas()
    dic = {"Rojo": [], "Verde": [], "Azul": []}
    
    #Dos-coloración
    dosColores = dosColoracion(poly)
    dic["Rojo"].extend(dosColores["Rojo"])
    dic["Verde"].extend(dosColores["Verde"])
    
    #Galería de arte en cada bolsa y fusión con la dos-coloración.
    for b in bolsas:
        flag = True
        coords = b.getCoordenadas()
        if coords[0] not in dosColores["Rojo"] or coords[0] in dosColores["Verde"]:
            flag = False
        colores = galeriaDeArte(b, flag)
        dic["Rojo"].extend([elem for elem in colores["Rojo"]
                                if elem not in dic["Rojo"]])
        dic["Verde"].extend([elem for elem in colores["Verde"]
                                if elem not in dic["Verde"]])
        dic["Azul"].extend([elem for elem in colores["Azul"]
                                if elem not in dic["Azul"]])
    return dic

"""Metodo que devuelve un conjunto de vértices suficientes y razonables para la visión 
total del polígono"""
def posicionesTopograficas(poly):
    colores = coloracionPoligono(poly)
    res = []
    if len(colores["Rojo"]) <= len(colores["Verde"]):
        res.extend(colores["Rojo"])
    else:
        res.extend(colores["Verde"])
    return res
    
    
    
    
    
        
    
    
    
    
    
    
    
    