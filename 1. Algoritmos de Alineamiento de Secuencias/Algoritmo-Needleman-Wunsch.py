import sys
import numpy as np
sys.setrecursionlimit(5000)

nombre_fichero = "Comparacion_.txt"
distancia = -2
identicoMatch = 1
noIdenticoMatch = -1

def guardar_fichero(F):
    fichero = open(nombre_fichero, "w")

    fichero.write('CADENA 1: '+ secuencia_1 + '\n')
    fichero.write('CADENA 2: '+ secuencia_2 + '\n')

    fichero.write('           ')
    for i in range(column-1):
        fichero.write(secuencia_1[i]+'      ')

    fichero.write('\n')

    secuencia2_t = ' '+ secuencia_2

    for r in range(row):
        fichero.write(secuencia2_t[r])
        for c in range(column):
            #fichero.write(' [ '+ '{}'.format(F[r][c][0])+'] ')
            fichero.write(' [ '+ '{}'.format(F[r][c][0])+' '+'{}'.format(F[r][c][1])+'] ')
        fichero.write('\n')
    fichero.close()

    fichero = open(nombre_fichero, "r")
    print(fichero.read())

def get_score(secuencia1, secuencia2):
    score = 0
    secuencia3 = ''
    for i in range(len(secuencia1)):
    # Mismas Letras
        if secuencia1[i] == secuencia2[i]:
            print (identicoMatch, end='', sep='')
            secuencia3 = secuencia3 + str(identicoMatch)
            score = score + identicoMatch
        else:
            # Existe un GAB
            if secuencia1[i]=='-' or secuencia2[i]=='-':
                print ('(',distancia,')', end='', sep='')
                secuencia3 = secuencia3 + '(' + str(distancia) + ')'
                score = score + distancia
            # Diferentes letras
            else:
                print ('(',noIdenticoMatch ,')', end='', sep='')
                secuencia3 = secuencia3 + '(' + str(noIdenticoMatch) + ')'
                score = score + noIdenticoMatch
        print ('+', end='', sep='')
        secuencia3 = secuencia3 + '+'
    print("\b",end="")
    secuencia3 = secuencia3 + ' = ' + str(score) + '\n'
    print(' =', score)
    fichero = open(nombre_fichero, "a+")
    fichero.write(secuencia3)
    fichero.close()
 
			
def alineamiento_optimo(Final, i, j, alineacion_secuencia_1 = "", alineacion_secuencia_2 = ""):
    # Caso Base - Cuando llegamos al Final
    if Final[i][j][1]==0:
        print(alineacion_secuencia_1)
        print(alineacion_secuencia_2)
        fichero = open(nombre_fichero, "a+")
        fichero.write('\n')
        fichero.write(alineacion_secuencia_1 + '\n')
        fichero.write(alineacion_secuencia_2 + '\n')
        fichero.close()
        get_score(alineacion_secuencia_1, alineacion_secuencia_2)
        print("\n")
        return

    # Caso Recursivo - Cuando una celda tiene mas de una direccion
    if len(Final[i][j][1])>1:
        direcciones = Final[i][j][1]
        for n in range(len(direcciones)):
            Final[i][j][1] = direcciones[n]
            alineamiento_optimo(Final, i, j, alineacion_secuencia_1, alineacion_secuencia_2)

    # Caso Recursivo
    else:
        # D - Mismas Letras
        if Final[i][j][1] == 'D':
            alineacion_secuencia_1 = secuencia_1[j-1] + alineacion_secuencia_1
            alineacion_secuencia_2 = secuencia_2[i-1] + alineacion_secuencia_2
            i = i-1
            j = j-1
        # U - Diferentes Letras
        elif Final[i][j][1]=='L':
            alineacion_secuencia_1 = secuencia_1[j-1] + alineacion_secuencia_1
            alineacion_secuencia_2 = "-" + alineacion_secuencia_2
            j = j-1
            
        # L - Diferentes Letras
        elif Final[i][j][1]=='U':
            alineacion_secuencia_1 = "-" + alineacion_secuencia_1
            alineacion_secuencia_2 = secuencia_2[i-1] + alineacion_secuencia_2
            i = i-1

        alineamiento_optimo(Final, i, j, alineacion_secuencia_1, alineacion_secuencia_2)			


def alineacion_global(Final, i, j):
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
        guardar_fichero(Final)
        alineamiento_optimo(Final, i, j)
        return
    elif j<column-1:
        alineacion_global(Final, i ,j+1)
    else:
        alineacion_global(Final,i+1,1  )							


if __name__ == "__main__":

    #secuencia_1 = "AGC"
    #secuencia_2 = "AAAC"

    secuencia_1 = "GGGGGGGACACCACA"
    secuencia_2 = "GGGCATGGACATTCTC"

    # Numero de Columnas y Filas de la Matriz Final
    column = len(secuencia_1)+1
    row = len(secuencia_2)+1

    Matriz_F = np.zeros([row, column], dtype='i,O')

    # Datos iniciales de la Columna
    for i in range(1,column):
        Matriz_F[0][i][0] = i*distancia
        Matriz_F[0][i][1] = 'L'

    # Datos iniciales de la Fila
    for i in range(1,row):
        Matriz_F[i][0][0] = i*distancia
        Matriz_F[i][0][1] = 'U'

    alineacion_global(Matriz_F, 1, 1)
