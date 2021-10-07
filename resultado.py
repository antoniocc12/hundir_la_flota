import numpy as np
import random as rand
from time import sleep
import sys

class tablero:  

    def __init__(self, id, matriz, mascara, acierto_fallo):
        self.id = id
        self.matriz = matriz
        self.mascara = mascara
        self.acierto_fallo = acierto_fallo
        
    def coordenada(self, coor_x, coor_y):

        var = None
        if self.matriz[coor_x][coor_y] == 'O':
            self.matriz[coor_x][coor_y] = 'X'
            self.mascara[coor_x][coor_y] = 'X'
            self.acierto_fallo = True
            var = True
        elif self.matriz[coor_x][coor_y] == ' ':
            self.matriz[coor_x][coor_y] = '/'
            self.mascara[coor_x][coor_y] = '/'
            self.acierto_fallo = False
            var = False
        return var

def turno_us(lista_us, us, cpu):
    print('Es su turno')
    opciones(us, cpu)
    coor_x = int(input('Introduzca la coordenada en x: '))
    coor_y = int(input('Introduzca la coordenada en y: '))
    pos = (coor_x, coor_y)
    while pos in lista_us:
        print('ERROR: Coordenadas introducidas anteriormente.')
        coor_x = int(input('Introduzca la coordenada en x: '))
        coor_y = int(input('Introduzca la coordenada en y: '))
        pos = (coor_x, coor_y)
    lista_us.append(pos)
    if cpu.coordenada(coor_x, coor_y) == True:
        print('Has acertado!')
        show(us, cpu, 0)
    else:
        print('Has fallado.')
        show(us, cpu, 0)
    return lista_us

def turno_cpu(lista_cpu, us, cpu):
    coor_x = rand.randint(0, 9)
    coor_y = rand.randint(0, 9)
    pos = (coor_x, coor_y)
    while pos in lista_cpu:
        coor_x = rand.randint(0, 10)
        coor_y = rand.randint(0, 10)
        pos = (coor_x, coor_y)
    lista_cpu.append(pos)
    if us.coordenada(coor_x, coor_y) == True:
        print('Te han golpeado!')
        show(us, cpu, 1)  
    else:
        print('La máquina ha fallado.')
        show(us, cpu, 1)   
    return lista_cpu

def show(us, cpu, us_o_cpu):
    if us_o_cpu == 0:
        print('Tablero cpu:\n', cpu.mascara)
        sleep(4)
    elif us_o_cpu == 1:
        print('Tu tablero:\n', us.matriz)
        sleep(4)
    elif us_o_cpu == 2:
        print('Tablero cpu:\n', cpu.mascara)
        print('Tu tablero:\n', us.matriz)
        sleep(4)

def crear_us():
    lon = 10
    lista = []
    for i in range(lon**2):
        lista.append(' ')
    matriz = np.array(lista, dtype = str).reshape((10, 10))
    matriz[8][5:9] = 'O' 
    matriz[5][6:9] = 'O' 
    matriz[3][1] = 'O'
    matriz[4][1] = 'O'
    matriz[5][1] = 'O'
    matriz[0][7:9] = 'O'
    matriz[2][2:4] = 'O'
    matriz[2][5] = 'O'
    matriz[3][5] = 'O'
    matriz[0][0] = 'O'
    matriz[9][0] = 'O'
    matriz[7][3] = 'O'
    matriz[2][8] = 'O'
    mascara = np.array(lista, dtype = str).reshape((10, 10))
    return matriz, mascara

def crear_ale():
    lista = []
    for i in range(100):
        lista.append(' ')
    matriz = np.array(lista, dtype = str).reshape((10, 10))
    mascara = np.array(lista, dtype = str).reshape((10, 10))
    lon = 4
    cont = 1
    while lon > 0:
        for i in range(cont):
            forma = rand.randint(0, 1) # barco en vertical = 0 u horizontal = 1
            if forma == 0: # si va en vertical
                pos_x = rand.randint(0, 9 - lon + 1) # irá siempre hacia abajo desde este punto
                pos_y = rand.randint(0, 9)
                l_copia = lon
                while l_copia > 0:
                    matriz[pos_x + l_copia - 1][pos_y] = 'O'
                    l_copia -= 1
            else:
                pos_x = rand.randint(0, 9) 
                pos_y = rand.randint(0, 9 - lon + 1) # irá siempre hacia la derecha desde este punto
                l_copia = lon
                while l_copia > 0:
                    matriz[pos_x][pos_y + l_copia - 1] = 'O'
                    l_copia -= 1
        lon -= 1
        cont += 1
    return matriz, mascara

def crear_cpu():
    cont_os = 0
    mascara = crear_ale()[1]
    while cont_os != 20:
            matriz = crear_ale()[0]
            cont_os = 0
            for i in range(10):
                    for j in range(10):
                            if matriz[i][j] == 'O':
                                    cont_os += 1

    return matriz, mascara

def opciones(us, cpu):
    print('¿Que desea hacer?:', '1. Seguir con las coordenadas. 2. Visualizar los tableros. 3. Terminar el juego.')
    res = int(input('Introduzca el número: '))
    if res == 1:
        return None
    elif res == 2:
        print('Tablero cpu:\n', cpu.matriz)
        print('Tu tablero:\n', us.matriz)
        sleep(4)
    elif res == 3:
        sys.exit('FIN DEL JUEGO')

def hundir_la_flota():

    lista_us = []
    lista_cpu = []
    us = tablero(0, crear_us()[0], crear_us()[1], False) # ASIGNAMOS EL ID = 0 AL USUARIO SIEMPRE
    cpu = tablero(1, crear_cpu()[0], crear_cpu()[1], False) # ASIGNAMOS EL ID = 1 AL CPU SIEMPRE

    print('BIENVENIDO A HUNDIR LA FLOTA')
    sleep(2)
    print('Tanto tu, como la maquina tenéis un tablero con barcos, y se trata de ir "disparando" y hundiendo los del adversario hasta que un jugador se queda sin barcos, y por tanto, pierde.')
    print('Funciona por turnos y empiezas tu.')
    print('En cada turno disparas a una coordenada (X, Y) del tablero adversario. **Si aciertas, te vuelve a tocar**. En caso contrario, le toca a la maquina.')
    print('En los turnos de la maquina, si acerta también le vuelve a tocar. ¿Dónde dispara la maquina? A un punto aleatorio en tu tablero.')
    print('Si se hunden todos los barcos de un jugador, el juego acaba y gana el otro.')
    sleep(4)

    show(us, cpu, 2)  

    while 'O' in us.matriz and 'O' in cpu.matriz:

        turno_us(lista_us, us, cpu)
        while cpu.acierto_fallo:
            turno_us(lista_us, us, cpu)

        turno_cpu(lista_cpu, us, cpu)
        while us.acierto_fallo:
            turno_cpu(lista_cpu, us, cpu)
    
    if 'O' not in cpu.matriz:
        print('ENHORABUENA, has ganado!')
        print('Tablero cpu:\n', cpu.matriz)
    else:
        print('Has perdido!')
        print('Tablero usuario:\n', us.matriz)

hundir_la_flota()