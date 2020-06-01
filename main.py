import numpy as np
import cv2

plantilla = './plantilla.png'
titulo = 'Cortacabello Inalambrico Remington Hc5350'
descripcion = 'Se puede lavar con agua. Cargador USB incluido, pero también se puede usar cualquier cargador de celular. 14 posiciones de corte, desde 3mm hasta 42mm.'
precio = '4500'

image = cv2.imread(plantilla, cv2.IMREAD_UNCHANGED)
font = cv2.FONT_HERSHEY_SIMPLEX
size = 1
stroke = 2

height, width, _ = image.shape

textsize = cv2.getTextSize(titulo, font, size, stroke)[0]

textX = (width - textsize[0]) // 2
textY = (height + textsize[1]) // 2

position = (textX, 780)
cv2.putText(
     image, 
     titulo,
     position,
     font, 
     size, 
     (255, 255, 255, 255),
     stroke) 
cv2.imshow('image',image)
cv2.waitKey(0)
