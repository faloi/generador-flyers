import numpy as np
import cv2
import textwrap

# Parametros
plantilla = './plantilla.png'
titulo = 'Cortacabello Inalambrico Remington Hc5350'
descripcion = 'Se puede lavar con agua. Cargador USB incluido, pero también se puede usar cualquier cargador de celular. 14 posiciones de corte, desde 3mm hasta 42mm.'
precio = '4500'

# Configuración
font = cv2.FONT_HERSHEY_DUPLEX
caracteres_por_linea = 50
interlineado = 10
siguiente_posicion = 775

def escribir_texto(texto, size, stroke, espacio_adicional = 0):
  global siguiente_posicion
  _, width, _ = image.shape
  sizeX, sizeY = cv2.getTextSize(texto, font, size, stroke)[0]
  x = (width - sizeX) // 2
  position = (x, siguiente_posicion)
  cv2.putText(
     image, 
     texto,
     position,
     font, 
     size, 
     (255, 255, 255, 255),
     stroke)
  siguiente_posicion += sizeY + interlineado + espacio_adicional

image = cv2.imread(plantilla, cv2.IMREAD_UNCHANGED)

escribir_texto(titulo, 1, 2)
escribir_texto(f"${precio}", 1, 2)

for linea in textwrap.wrap(descripcion, caracteres_por_linea):
  escribir_texto(linea, 0.8, 1)

cv2.imshow('image', image)
cv2.waitKey(0)
