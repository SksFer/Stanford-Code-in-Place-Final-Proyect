from PIL import Image
import math
import os

COLORES_KAREL = {
    'red': (255, 0, 0), 'green': (0, 255, 0), 'blue': (0, 0, 255),
    'yellow': (255, 255, 0), 'cyan': (0, 255, 255), 'magenta': (255, 0, 255),
    'white': (255, 255, 255), 'black': (0, 0, 0), 'orange': (255, 165, 0),
    'pink': (255, 192, 203), 'gray': (128, 128, 128)
}

def obtener_color_mas_cercano(rgb):
    r, g, b = rgb
    dist_min = float('inf')
    mejor = 'white'
    for nombre, (cr, cg, cb) in COLORES_KAREL.items():
        dist = math.sqrt((r-cr)**2 + (g-cg)**2 + (b-cb)**2)
        if dist < dist_min:
            dist_min = dist
            mejor = nombre
    return mejor

def generar_codigo_karel(ruta_imagen, tamaño=50):
    try:
        img = Image.open(ruta_imagen).convert('RGB')
    except FileNotFoundError:
        print(f"Error: No se encontró la imagen '{ruta_imagen}'.")
        return

    img = img.resize((tamaño, tamaño), Image.Resampling.NEAREST)

    codigo = "from stanfordkarel import *\n\n"
    codigo += "def main():\n"
    
    for y in range(tamaño - 1, -1, -1): 
        fila_karel = tamaño - 1 - y
        fila_es_par = (fila_karel % 2 == 0)
        rango_x = range(tamaño) if fila_es_par else range(tamaño - 1, -1, -1)

        for i, x in enumerate(rango_x):
            r, g, b = img.getpixel((x, y))
            color = obtener_color_mas_cercano((r, g, b))
            codigo += f"    paint_corner({color.upper()})\n"
            
            if i < tamaño - 1:
                codigo += "    move()\n"

        if y > 0: 
            if fila_es_par:
                codigo += "    turn_left()\n    move()\n    turn_left()\n"
            else:
                codigo += "    turn_right()\n    move()\n    turn_right()\n"

    codigo += "\ndef turn_right():\n"
    codigo += "    for i in range(3):\n"
    codigo += "        turn_left()\n\n"
    
    codigo += "if __name__ == '__main__':\n"
    codigo += "    run_karel_program('karel_dibuja_mi_foto')\n"

    nombre_py = "karel_dibuja_mi_foto.py"
    with open(nombre_py, "w") as f:
        f.write(codigo)
        
    if not os.path.exists("worlds"):
        os.makedirs("worlds")

    nombre_mundo = "worlds/karel_dibuja_mi_foto.w"
    with open(nombre_mundo, "w") as f:
        f.write(f"Dimension: ({tamaño}, {tamaño})\n")

    print(f"¡Éxito total! Se generó el código y el mapa gigante de {tamaño}x{tamaño}.")

generar_codigo_karel("persona3.png", tamaño=50)