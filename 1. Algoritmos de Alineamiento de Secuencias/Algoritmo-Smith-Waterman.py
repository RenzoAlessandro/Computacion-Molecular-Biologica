import sys
import numpy as np

nombre_fichero = "Salida.txt"
distancia = -2
identicoMatch = 1
noIdenticoMatch = -1

def guardar_fichero(F):
    fichero = open(nombre_fichero, "w")

    fichero.write('          ')
    for i in range(column-1):
        fichero.write(secuencia_1[i]+'      ')

    fichero.write('\n')

    secuencia2_t = ' '+ secuencia_2

    for r in range(row):
        fichero.write(secuencia2_t[r])
        for c in range(column):
            fichero.write(' [ '+ '{}'.format(F[r][c][0])+' ] ')
            #fichero.write(' [ '+ '{}'.format(F[r][c][0])+':'+'{}'.format(F[r][c][1])+' ] ')
        fichero.write('\n')
    fichero.close()

    fichero = open(nombre_fichero, "r")
    print(fichero.read())	

def alineamiento_optimo(Final, i, j, alineacion_secuencia_1 = "", alineacion_secuencia_2 = ""):
    # Caso Base - Cuando llegamos al Final
    if Final[i][j][0]==0:
        print (alineacion_secuencia_1)
        print (alineacion_secuencia_2)
        fichero = open(nombre_fichero, "a+")
        fichero.write('\n')
        fichero.write(alineacion_secuencia_1 + '\n')
        fichero.write(alineacion_secuencia_2 + '\n')
        fichero.close()
        print("\n")
        return

    if len(Final[i][j][1])>1:
        directions = Final[i][j][1]
        for n in range(len(directions)):
            Final[i][j][1] = directions[n]
            alineamiento_optimo(Final, i, j, alineacion_secuencia_1, alineacion_secuencia_2)

    else:
        if Final[i][j][1] == 'D':
            alineacion_secuencia_1 = secuencia_1[j-1] + alineacion_secuencia_1
            alineacion_secuencia_2 = secuencia_2[i-1] + alineacion_secuencia_2
            i = i-1
            j = j-1
        elif Final[i][j][1]=='U':
            alineacion_secuencia_1 = "-" + alineacion_secuencia_1
            alineacion_secuencia_2 = secuencia_2[i-1] + alineacion_secuencia_2
            i = i-1
        else:
            alineacion_secuencia_2 = "-" + alineacion_secuencia_2
            alineacion_secuencia_1 = secuencia_1[j-1] + alineacion_secuencia_1
            j = j-1
        alineamiento_optimo(Final, i, j, alineacion_secuencia_1, alineacion_secuencia_2)			


def alineacion_local(Final, i, j):
    direcciones = ''
    
    valor = identicoMatch
    if secuencia_2[i-1] != secuencia_1[j-1]:
        valor = noIdenticoMatch

    diag = Final[i-1][j-1][0] + valor
    up   = Final[i-1][j  ][0] + distancia
    left = Final[i  ][j-1][0] + distancia

    Final[i][j][0] = max(diag, up, left, 0)

    if Final[i][j][0]==diag:
        direcciones = direcciones + 'D'
        #F[i][j][1] = 'D'

    if Final[i][j][0]==up:
        direcciones = direcciones + 'U'
        #F[i][j][1] = 'U'

    if Final[i][j][0]==left:
        direcciones = direcciones + 'L'
        #F[i][j][1] = 'L'

    Final[i][j][1] = direcciones

    if i==row-1 and j==column-1:
        guardar_fichero(Final)

        major = -1000
        s_i = 0
        s_j = 0
        for r in range(1,row):
            for c in range(1, column):
                if Final[r][c][0]>=major:
                    s_i = i
                    s_j = j
                    i = r
                    j = c
                    major = Final[r][c][0]

        alineamiento_optimo(Final, i, j)
        alineamiento_optimo(Final, s_i, s_j)
        return

    if j<column-1:
        alineacion_local(Final, i ,j+1)
    else:
        alineacion_local(Final, i+1 ,1)


if __name__ == "__main__":

    secuencia_1 = "GCA"
    secuencia_2 = "AGCT"

    #secuencia_1 = "ACTGATTCA"
    #secuencia_2 = "ACGCATCA"

    # Numero de Columnas y Filas de la Matriz Final
    column = len(secuencia_1)+1
    row = len(secuencia_2)+1

    # Datos iniciales de la Columna y Fila de la Matriz Final
    Matriz_F = np.zeros([row, column], dtype='i,O')

    alineacion_local(Matriz_F, 1, 1)
