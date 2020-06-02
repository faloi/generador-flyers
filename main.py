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
  def __init__(self, posicion_inicial):
    self.siguiente_posicion = posicion_inicial

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


def generar_imagen(titulo, precio, descripcion):
  image = cv2.imread(plantilla, cv2.IMREAD_UNCHANGED)
  editor = Editor(posicion_inicial_y)

  editor.escribir_texto(image, titulo, 1.2, 2)
  editor.escribir_texto(image, f"${precio}", 2, 2, 2 * interlineado)

  for linea in textwrap.wrap(descripcion, caracteres_por_linea):
    editor.escribir_texto(image, linea, 1, 1)

  cv2.imwrite(f"out/{titulo}.png", image)


with open('inventario.csv', mode='r') as csv_file:
  csv_reader = csv.DictReader(csv_file)
  for row in csv_reader:
    if row['¿Vender ahora?'] == 'Sí':
      generar_imagen(
          titulo=row['Nombre'], descripcion=row['Descripción'], precio=row['Valor estimado'])
