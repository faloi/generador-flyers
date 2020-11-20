#!/usr/bin/env python3

import numpy as np
import cv2
import textwrap
import csv
from unidecode import unidecode
from functools import reduce, partial
from pathlib import Path

# Configuración
font = cv2.FONT_HERSHEY_DUPLEX
caracteres_por_linea = 45
interlineado = 10
font_base_size = 1.1
alto = 1150

def red(skk): return "\033[91m {}\033[00m" .format(skk)
def green(skk): return "\033[92m {}\033[00m" .format(skk)
def yellow(skk): return "\033[93m {}\033[00m" .format(skk)
def lightPurple(skk): return "\033[94m {}\033[00m" .format(skk)
def purple(skk): return "\033[95m {}\033[00m" .format(skk)
def cyan(skk): return "\033[96m {}\033[00m" .format(skk)
def lightGray(skk): return "\033[97m {}\033[00m" .format(skk)
def black(skk): return "\033[98m {}\033[00m" .format(skk)

def compose(*functions):
  return reduce(lambda f, g: lambda x: f(g(x)), functions, lambda x: x)

printError = compose(print, red)
printInfo = print

class Editor:
  def __init__(self, titulo, precio, descripcion, ruta_foto):
    self.siguiente_posicion = 870
    self.titulo = titulo
    self.precio = precio
    self.descripcion = descripcion
    self.ruta_foto = ruta_foto

  def generar_flyer(self):
    if not self.hay_foto():
      printError(f"Ojo, no hay foto para {self.titulo}")
      return

    flyer = compose(
      self.generar_etiqueta,
      self.agregar_borde,
      partial(self.redimensionar, 1080),
      self.leer_foto
    )(self.ruta_foto)
    cv2.imwrite(f"out/{self.titulo}.png", flyer)

  def hay_foto(self):
    return Path(self.ruta_foto).exists()

  def leer_foto(self, ruta):
    return cv2.imread(ruta, cv2.IMREAD_UNCHANGED)

  def redimensionar(self, ancho, imagen):
    y, x, _ = imagen.shape
    return cv2.resize(imagen, (ancho, int(ancho / x * y)))
  
  def agregar_borde(self, imagen):
    return cv2.copyMakeBorder(imagen, 0, alto - imagen.shape[0], 0, 0, cv2.BORDER_CONSTANT)

  def generar_etiqueta(self, imagen):
    self.escribir_texto(imagen, self.titulo, 1.2, 2)
    self.escribir_texto(imagen, f"${self.precio}", 2, 2, 2 * interlineado)

    for linea in textwrap.wrap(self.descripcion, caracteres_por_linea):
      self.escribir_texto(imagen, linea, 1.1, 1)

    return imagen

  def escribir_texto(self, image, texto, size, stroke, espacio_adicional=0):
    final_size = font_base_size * size
    _, width, _ = image.shape
    sizeX, sizeY = cv2.getTextSize(texto, font, final_size, stroke)[0]
    x = (width - sizeX) // 2
    position = (x, self.siguiente_posicion + espacio_adicional)
    cv2.putText(
        image,
        unidecode(texto),
        position,
        font,
        final_size,
        (255, 255, 255, 255),
        stroke)
    self.siguiente_posicion += sizeY + interlineado + espacio_adicional


with open('inventario.csv', mode='r') as csv_file:
  csv_reader = csv.DictReader(csv_file)
  articulos = [
    Editor(titulo=row['Nombre'], descripcion=row['Descripción'], precio=row['Valor estimado'], ruta_foto=f'in/{row["Nombre"]}.jpg')
    for row 
    in csv_reader 
    if row['¿Vender ahora?'] == 'Sí'
  ]
  
  printInfo(f"Hay {len(articulos)} artículos para vender. Generando flyers...")
  
  for editor in articulos:
    editor.generar_flyer()
  
  printInfo(f"¡Fin! Se pudieron armar {len([x for x in articulos if x.hay_foto()])} flyers.")
