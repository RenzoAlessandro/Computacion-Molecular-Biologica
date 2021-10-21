import sys
import numpy as np
sys.setrecursionlimit(5000)

nombre_fichero = "Salida_Estrella_.txt"
distancia = -2
identicoMatch = 1
noIdenticoMatch = -1

def guardar_fichero(F, row, column):
    fichero = open(nombre_fichero, "w")
    fichero.write('LAS CADENAS: '+ '\n')
    for i in range(len(cadenas)):
        fichero.write(cadenas[i]+'\n')
        
    fichero.write('\n' + 'LA MATRIZ DE SCORES: '+ '\n')
    for r in range(row):
        for c in range(column):
            #fichero.write(' [ '+ '{}'.format(F[r][c][0])+'] ')
            fichero.write(' [ '+ '{}'.format(F[r][c][0])+' '+'{}'.format(F[r][c][1])+'] ')
        fichero.write('\n')
    fichero.close()

    fichero = open(nombre_fichero, "r")
    #print(fichero.read())

def get_score(secuencia1, secuencia2):
    score = 0
    secuencia3 = ''
    for i in range(len(secuencia1)):
    # Mismas Letras
        if secuencia1[i] == secuencia2[i]:
            #print (identicoMatch, end='', sep='')
            secuencia3 = secuencia3 + str(identicoMatch)
            score = score + identicoMatch
        else:
            # Existe un GAB
            if secuencia1[i]=='-' or secuencia2[i]=='-':
                #print ('(',distancia,')', end='', sep='')
                secuencia3 = secuencia3 + '(' + str(distancia) + ')'
                score = score + distancia
            # Diferentes letras
            else:
                #print ('(',noIdenticoMatch ,')', end='', sep='')
                secuencia3 = secuencia3 + '(' + str(noIdenticoMatch) + ')'
                score = score + noIdenticoMatch
        #print ('+', end='', sep='')
        secuencia3 = secuencia3 + '+'
    #print("\b",end="")
    secuencia3 = secuencia3 + ' = ' + str(score) + '\n'
    #print(' =', score)
    fichero = open(nombre_fichero, "a+")
    fichero.write(secuencia3)
    fichero.close()
 
			
def alineamiento_optimo(Final, i, j, secuencia_1, secuencia_2, alineacion_secuencia_1 = "", alineacion_secuencia_2 = ""):
    # Caso Base - Cuando llegamos al Final
    if Final[i][j][1]==0:
        #print(alineacion_secuencia_1)
        #print(alineacion_secuencia_2)
        fichero = open(nombre_fichero, "a+")
        fichero.write('\n')
        fichero.write(alineacion_secuencia_1 + '\n')
        fichero.write(alineacion_secuencia_2 + '\n')
        fichero.close()
        get_score(alineacion_secuencia_1, alineacion_secuencia_2)
        #print("\n")
        return

    # Caso Recursivo
    elif len(Final[i][j][1]) == 1:
        # D - Mismas Letras
        if Final[i][j][1] == 'D':
            #print(i , j, ' - ', F[i][j][1])
            alineacion_secuencia_1 = secuencia_1[j-1] + alineacion_secuencia_1
            alineacion_secuencia_2 = secuencia_2[i-1] + alineacion_secuencia_2
            alineamiento_optimo(Final, i-1, j-1, secuencia_1, secuencia_2, alineacion_secuencia_1, alineacion_secuencia_2)
            
        # U - Diferentes Letras
        elif Final[i][j][1]=='L':
            #print(i , j, ' - ', F[i][j][1])
            alineacion_secuencia_1 = secuencia_1[j-1] + alineacion_secuencia_1
            alineacion_secuencia_2 = "-" + alineacion_secuencia_2
            alineamiento_optimo(Final, i, j-1, secuencia_1, secuencia_2, alineacion_secuencia_1, alineacion_secuencia_2)

        # L - Diferentes Letras
        elif Final[i][j][1]=='U':
            #print(i , j, ' - ', F[i][j][1])
            alineacion_secuencia_1 = "-" + alineacion_secuencia_1   
            alineacion_secuencia_2 = secuencia_2[i-1] + alineacion_secuencia_2
            alineamiento_optimo(Final, i-1, j, secuencia_1, secuencia_2, alineacion_secuencia_1, alineacion_secuencia_2) 			


def alineacion_global_origin(Final, i, j, secuencia_1, secuencia_2, row, column):
    direcciones = ''

    valor = identicoMatch
    if secuencia_2[i-1] != secuencia_1[j-1]:
        valor = noIdenticoMatch

    diag = Final[i-1][j-1][0] + valor
    up   = Final[i-1][j  ][0] + distancia
    left = Final[i  ][j-1][0] + distancia

    Final[i][j][0] = max(diag, up, left)

    # <- LEFT
    if Final[i][j][0]==left:
        direcciones = direcciones + 'L'
    # \ DIAGONAL
    if Final[i][j][0]==diag:
        direcciones = direcciones + 'D'
    # | UP
    if Final[i][j][0]==up:
        direcciones = direcciones + 'U'

    Final[i][j][1] = direcciones

    if i==row-1 and j==column-1:
        alineamiento_optimo(Final, i, j, secuencia_1, secuencia_2,)
        return
    elif j<column-1:
        alineacion_global_origin(Final, i ,j+1, secuencia_1, secuencia_2, row, column)
    else:
        alineacion_global_origin(Final,i+1,1, secuencia_1, secuencia_2, row, column)							


def alineacion_global(Final, i, j, fila_G, columna_G, secuencia_2, secuencia_1):
    direcciones = ''

    valor = identicoMatch
    if secuencia_2[i-1] != secuencia_1[j-1]:
        valor = noIdenticoMatch

    diag = Final[i-1][j-1][0] + valor
    up   = Final[i-1][j  ][0] + distancia
    left = Final[i  ][j-1][0] + distancia

    Final[i][j][0] = max(diag, up, left)

    # <- LEFT
    if Final[i][j][0]==left:
        direcciones = direcciones + 'L'
    # \ DIAGONAL
    if Final[i][j][0]==diag:
        direcciones = direcciones + 'D'
    # | UP
    if Final[i][j][0]==up:
        direcciones = direcciones + 'U'

    Final[i][j][1] = direcciones

    if i==fila_G-1 and j==columna_G-1:
        return Final[i][j][0]
        
    elif j<columna_G-1:
        return alineacion_global(Final, i ,j+1, fila_G, columna_G, secuencia_2, secuencia_1)
    else:
        return alineacion_global(Final,i+1,1  , fila_G, columna_G, secuencia_2, secuencia_1)								


def alineacion_estrella(cadenas):
    filas_estrellas = len(cadenas)
    columnas_estrella = len(cadenas) + 1

    Matriz_E = np.zeros([filas_estrellas, columnas_estrella], dtype='i,O')
    # Llenado del diagonal
    for i in range(0, filas_estrellas):
        Matriz_E[i][i][0] = 0

    z = 1
    for x in range(0, filas_estrellas-1):
        for y in range(z, columnas_estrella-1):

            columna_G = len(cadenas[x])+1
            fila_G = len(cadenas[y])+1

            Matriz_G = np.zeros([fila_G, columna_G], dtype='i,O')

            # Datos iniciales de la Columna
            for k in range(1,columna_G):
                Matriz_G[0][k][0] = k*distancia
                Matriz_G[0][k][1] = 'L'

            # Datos iniciales de la Fila
            for k in range(1,fila_G):
                Matriz_G[k][0][0] = k*distancia
                Matriz_G[k][0][1] = 'U'

            score = alineacion_global(Matriz_G, 1, 1, fila_G, columna_G, cadenas[y], cadenas[x])

            Matriz_E[x][y][0] = score # Triangulo Superior
            Matriz_E[y][x][0] = score # Triangulo Inferior
            
        z = z + 1

    # Suma de escores
    for i in range(filas_estrellas):
        suma_temp = 0
        for j in range(columnas_estrella-1):
            suma_temp = suma_temp + Matriz_E[i][j][0]
        Matriz_E[i][columnas_estrella-1][0] = suma_temp
        
    guardar_fichero(Matriz_E,filas_estrellas, columnas_estrella)

    # Hallamos el maximo
    maximo = Matriz_E[0][columnas_estrella-1][0]
    for i in range(0, filas_estrellas-1):
        if Matriz_E[i+1][columnas_estrella-1][0] > maximo:
            maximo = Matriz_E[i+1][columnas_estrella-1][0] 

    #print("El valor maximo es: ", maximo)
    for i in range(0, filas_estrellas):
        if Matriz_E[i][columnas_estrella-1][0] == maximo:
            id_centro = i

    #print("Cadena Centro: ", cadena_centro)

    fichero = open(nombre_fichero, "a+")
    fichero.write('\n')
    fichero.write("El valor maximo es: " + str(maximo) + '\n')
    fichero.write("Cadena Centro: " + str(cadenas[id_centro]) + '\n')
    fichero.close()

    for z in range(len(cadenas)):
        if (id_centro != z):
            print(cadenas[id_centro], " - ", cadenas[z])
            seq_1 = cadenas[id_centro]
            seq_2 = cadenas[z]
            column = len(seq_1)+1
            row = len(seq_2)+1
            Matriz_F = np.zeros([row, column], dtype='i,O')
            for i in range(1,column):
                Matriz_F[0][i][0] = i*distancia
                Matriz_F[0][i][1] = 'L'
            for i in range(1,row):
                Matriz_F[i][0][0] = i*distancia
                Matriz_F[i][0][1] = 'U'
            alineacion_global_origin(Matriz_F, 1, 1, seq_1, seq_2, row, column)
            
            
        else:
            print("no se hace nada")

        

    
        


if __name__ == "__main__":

    #cadenas = ['GGGGGGGACACCACA',
    #           'GGGCATGGACATTCTC',
    #           'TGGGGAATTTGCTACACT',
    #           'CCCCGCTAGGGG',
    #           'GCTAGGGGTAT']

    cadenas = ['CCCCGCTAGGGG',
               'GCTAGGGGTAT',
               'CAAATGCGCTAGGGGGGGACACCACA',
               'TTCTGGGTCACGGTGCTAGGGG']

    alineacion_estrella(cadenas)

