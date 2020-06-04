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


class Editor:
  def __init__(self, titulo, precio, descripcion, ruta_foto):
    self.siguiente_posicion = 800
    self.titulo = titulo
    self.precio = precio
    self.descripcion = descripcion
    self.ruta_foto = ruta_foto

  def generar_flyer(self):
    etiqueta = self.generar_etiqueta()
    foto = self.leer_foto()
    flyer = self.combinar(foto, etiqueta)
    cv2.imwrite(f"out/{self.titulo}.png", flyer)

  def leer_foto(self):
    foto = cv2.imread(self.ruta_foto, cv2.IMREAD_UNCHANGED)
    return cv2.copyMakeBorder(foto, 0, 1080 - foto.shape[0], 0, 0, cv2.BORDER_CONSTANT)

  def combinar(self, src, overlay, pos=(0, 0)):
    h, w, _ = overlay.shape
    rows, cols, _ = src.shape
    x, y = pos[0], pos[1]
 
    for i in range(h):
      for j in range(w):
        if x + i >= rows or y + j >= cols:
            continue
        alpha = float(overlay[i][j][3] / 255.0)
        src[x + i][y + j] = alpha * overlay[i][j][:3] + \
            (1 - alpha) * src[x + i][y + j]
    return src

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
                      precio=row['Valor estimado'], ruta_foto='in/out.jpg')
      editor.generar_flyer()
