import numpy as np
import cv2
import textwrap

# Parametros
plantilla = './plantilla.png'
titulo = 'Cortacabello Inalambrico Remington Hc5350'
descripcion = 'Se puede lavar con agua. Cargador USB incluido, pero también se puede usar cualquier cargador de celular. 14 posiciones de corte, desde 3mm hasta 42mm.'
precio = '4500'

# Configuración
font = cv2.FONT_HERSHEY_SIMPLEX
caracteres_por_linea = 50

def escribir_texto(texto, size, stroke, y):
  height, width, _ = image.shape
  textsize = cv2.getTextSize(titulo, font, size, stroke)[0]
  x = (width - textsize[0]) // 2
  position = (x, y)
  cv2.putText(
     image, 
     texto,
     position,
     font, 
     size, 
     (255, 255, 255, 255),
     stroke) 

image = cv2.imread(plantilla, cv2.IMREAD_UNCHANGED)

escribir_texto(titulo, 1, 2, 780)

cv2.imshow('image',image)
cv2.waitKey(0)
