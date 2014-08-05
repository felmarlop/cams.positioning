# -*- coding: utf-8 -*
import datetime
import time

import tornado.httpserver
import tornado.ioloop
import tornado.options
import tornado.web
from tornado.template import Template

import sys
import os, uuid
import json

from Util.File import *
from Util.Area import *

portNumber = int(8888)

from tornado.options import define, options

define("port", default=portNumber, help="run on the given port", type=int)

__UPLOADS__ = "uploads/"

class Application(tornado.web.Application):
        def __init__(self):
                handlers = [
                        (r"/main", mainHandler),
                        (r"/sentPolygon", formHandler),
                        (r'/JS/(.*)', tornado.web.StaticFileHandler, {'path': 'JS/'}),
                        (r'/Libs/jquery/(.*)', tornado.web.StaticFileHandler, {'path': 'Libs/jquery/'}),
                        (r'/Libs/jquery/css/(.*)', tornado.web.StaticFileHandler, {'path': 'Libs/jquery/css/'}),
                ]

                settings = dict(
                        autoescape=None,
                )

                tornado.web.Application.__init__(self, handlers, **settings)


class mainHandler(tornado.web.RequestHandler):
    
    def initialize(self):
        self.errores = ''
        self.name = ''
        
    def get(self):
        self.render("main.html", error=self.errores, nombreFichero=self.name)

class formHandler(tornado.web.RequestHandler):
    
    def initialize(self):
        self.extensiones = [".txt"]
        self.name = self.request.arguments.get("name")[0]
        self.fileinfo = self.request.files['filearg'][0]
        self.fname = self.fileinfo['filename']
        self.extn = os.path.splitext(self.fname)[1]
        self.namee = os.path.splitext(self.fname)[0]
        self.errores = ''
    
    def get(self):
        self.render("main.html", error="", nombreFichero="")
        
    def post(self):
        errores = self.errores
        #Guardado del fichero del polígono. (NO NECESARIO)
        """cname = str(uuid.uuid4()) + extn
        fh = open(__UPLOADS__ + cname, 'w')
        fh.write(fileinfo['body'])"""
        #Validación:
        if self.name == '':
            errores = errores + 'Nombre del Pol\u00edgono est\u00e1 vac\u00edo.<br>'
        if self.extn not in self.extensiones:
            errores = errores + 'Extensi\u00f3n de archivo err\u00f3nea. Extensiones soportadas: '+self.extensiones+'<br>'
        #Creación del poígono o errores. Volver al formulario si los hay.
        resFile = stringToPolygon(self.fileinfo['body'])
        if isinstance(resFile, str):
            errores = errores + resFile
            self.render("main.html", error=errores, nombreFichero=self.name)
        else:
            ini = time.time()
            
            #Optimizamos el polígono.
            polyOpt = resFile.optimiza()
            polyOrd = polyOpt.ordena()
            areasVar = []
            areas = []
            puntosPoligono = []
            #Posiciones topográficas
            for p in polyOrd.getCoordenadas():
                puntosPoligono.append(vars(p))
                
            posiciones = posicionesTopograficas(polyOrd)
            
            #Áreas
            for ps in posiciones:
                a = areaOptima(polyOrd, ps)
                areas.append(a)
                l = []
                for ar in a.getCoordenadas():
                    l.append(vars(ar))
                areasVar.append(l);
            number = len(areasVar)
            
            #Intersecciones
            interseccionesVar = []
            inters = intersecciones(areas)
            for inter in inters:
                l2 = []
                for coorde in inter.getCoordenadas():
                    l2.append(vars(coorde))
                interseccionesVar.append(l2)
            numberInter = len(inters)
            fin = time.time()
            tiempo = str(round(fin - ini, 3))+" segundos"
            print("#####################################")
            print(self.name+" ha sido enviado con éxito")
            print("#####################################")
            #Creación de la escala.
            porcentajeAbscisa = (polyOrd.coordenadaMayorAbscisa().getX() - 
                         polyOrd.coordenadaMenorAbscisa().getX()) * 0.2
            porcentajeOrdenada = (polyOrd.coordenadaMayorOrdenada().getY() -
                          polyOrd.coordenadaMenorOrdenada().getY()) * 0.2
            minimaX = polyOrd.coordenadaMenorAbscisa().getX() - porcentajeAbscisa
            maximaX = polyOrd.coordenadaMayorAbscisa().getX() + porcentajeAbscisa
            minimaY = polyOrd.coordenadaMenorOrdenada().getY() - porcentajeOrdenada
            maximaY = polyOrd.coordenadaMayorOrdenada().getY() + porcentajeOrdenada
            escalas = []
            escalas.append(minimaX)
            escalas.append(maximaX)
            escalas.append(minimaY)
            escalas.append(maximaY)
            
            #Envío al cliente.
            self.render("index.html", coordsPoly = polyOrd, puntosVision = posiciones,
                        numeroAreas = number, numeroIntersecciones = numberInter,
                        nombreFichero=self.namee, 
                        poligono = json.dumps(puntosPoligono, sort_keys= True), 
                        zonasVision = areas,
                        intersec = inters,
                        visiones = json.dumps(areasVar, sort_keys = True), 
                        intersecciones = json.dumps(interseccionesVar),
                        escala = json.dumps(escalas, sort_keys = True), 
                        tejecucion=tiempo)

def main():
        tornado.options.parse_command_line()
        http_server = tornado.httpserver.HTTPServer(Application())
        http_server.listen(options.port)
        tornado.ioloop.IOLoop.instance().start()

if __name__ == "__main__":
        main()
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
