#!/usr/bin/env python3

import numpy as np
import cv2
import textwrap
import csv
from unidecode import unidecode

# Parametros
plantilla = './plantilla.png'

# Configuración
font = cv2.FONT_HERSHEY_DUPLEX
caracteres_por_linea = 50
interlineado = 10
font_base_size = 1.1
posicion_inicial_y = 800


class Editor:
  def __init__(self, posicion_inicial, titulo, precio, descripcion):
    self.siguiente_posicion = posicion_inicial
    self.titulo = titulo
    self.precio = precio
    self.descripcion = descripcion

  def generar_flyer(self):
    etiqueta = self.generar_etiqueta()
    cv2.imwrite(f"out/{self.titulo}.png", etiqueta)

  def generar_etiqueta(self):
    etiqueta = cv2.imread(plantilla, cv2.IMREAD_UNCHANGED)

    self.escribir_texto(etiqueta, self.titulo, 1.2, 2)
    self.escribir_texto(etiqueta, f"${self.precio}", 2, 2, 2 * interlineado)

    for linea in textwrap.wrap(self.descripcion, caracteres_por_linea):
      self.escribir_texto(etiqueta, linea, 1, 1)

    return etiqueta

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
  for row in csv_reader:
    if row['¿Vender ahora?'] == 'Sí':
      editor = Editor(titulo=row['Nombre'], descripcion=row['Descripción'],
                      precio=row['Valor estimado'], posicion_inicial=posicion_inicial_y)
      editor.generar_flyer()
