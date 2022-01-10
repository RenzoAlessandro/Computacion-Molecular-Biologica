# Estructura Secuendaria - DP
import numpy as np
#Plot Letras
import matplotlib.pyplot as plt
text_kwargs = dict(ha='center', va='center', fontsize=12, color='BLACK')

name_file = "Salida_estructura_secundaria_.txt"
min_loop_length = 2

def plot_struct(structure_secuence):
    px = 1/plt.rcParams['figure.dpi']
    plt.subplots(figsize=(400*px, 600*px))

    distance = 1.0
    for i in range(len(structure_secuence)):
        plt.text(0.5, distance, structure_secuence[i][0]+' === '+structure_secuence[i][1], **text_kwargs)
        distance = distance -0.05

    #https://github.com/ViennaRNA/RNAsketch

    plt.axis('off')
    plt.savefig('plot_struct.png')
    plt.show()

def par_check(tup):
    if tup in [('A', 'U'), ('U', 'A'), ('C', 'G'), ('G', 'C')]:
        return True
    return False

# Retorna la puntuación del emparejamiento óptimo entre los índices i y j
def OPT(i, j, sequence):
    # Caso base: no se permiten pares cuando i y j están a menos de 4 bases de distancia
    if i >= j - min_loop_length:
        return 0
    else:
        # i y j pueden estar emparejados o no emparejados, si no están emparejados,
        # la puntuación óptima es OPT (i, j-1)
        unpaired = OPT(i, j - 1, sequence)

        # Comprobar si j puede participar en un emparejamiento con una posición t
        pairing = [1 + OPT(i, t - 1, sequence) + OPT(t + 1, j - 1, sequence) for t in range(i, j - min_loop_length) \
                   if par_check((sequence[t], sequence[j]))]
        if not pairing:
            pairing = [0]
        paired = max(pairing)

        return max(unpaired, paired)


def traceback(i, j, structure, structure_secuence, DP, sequence):
    # En este caso hemos pasado por toda la secuencia.
    if j <= i:
        return
    # Si j no está emparejado, no habrá ningún cambio en la puntuación cuando lo eliminemos,
    # por lo que simplemente recurrimos al siguiente índice
    elif DP[i][j] == DP[i][j - 1]:
        traceback(i, j - 1, structure, structure_secuence, DP, sequence)
    # Considere los casos en los que j forma un par.
    else:
        # intentamos emparejar j con un índice k coincidente a su izquierda.
        for k in [b for b in range(i, j - min_loop_length)
                  if par_check((sequence[b], sequence[j]))]:
            # Si la puntuación en i, j es el resultado de sumar 1 del emparejamiento (j, k) y cualquier puntuación
            # viene de la subestructura a su izquierda (i, k-1) y a su derecha (k + 1, j-1)
            if k - 1 < 0:
                if DP[i][j] == DP[k + 1][j - 1] + 1:
                    structure.append((k, j))
                    structure_secuence.append((sequence[k], sequence[j]))
                    traceback(k + 1, j - 1, structure, structure_secuence, DP, sequence)
                    break
            elif DP[i][j] == DP[i][k - 1] + DP[k + 1][j - 1] + 1:
                # Agregue el par (j, k) a nuestra lista de pares
                structure.append((k, j))
                structure_secuence.append((sequence[k], sequence[j]))
                # Mover la recursividad a las dos subestructuras formadas por este emparejamiento
                traceback(i, k - 1, structure, structure_secuence, DP, sequence)
                traceback(k + 1, j - 1, structure, structure_secuence, DP, sequence)
                break


def write_estructura(sequence, structure):
    dot_bracket = ["." for _ in range(len(sequence))]
    for s in structure:
        dot_bracket[min(s)] = "("
        dot_bracket[max(s)] = ")"
    return "".join(dot_bracket)


# Inicializar la matriz con ceros donde no se pueden tener emparejamientos
def inicializacion(N):
    # Matriz NxN que almacena las puntuaciones de los emparejamientos óptimos.
    DP = np.empty((N, N))
    DP[:] = np.NAN
    for k in range(0, min_loop_length):
        for i in range(N - k):
            j = i + k
            DP[i][j] = 0
    return DP


def estructura_secundaria(sequence):
    N = len(sequence)
    DP = inicializacion(N)
    structure = []
    loop = []
    loop_pos = []
    structure_secuence = []

    # Llenar la matriz DP en diagonal
    for k in range(min_loop_length, N):
        for i in range(N - k):
            j = i + k
            DP[i][j] = OPT(i, j, sequence)

    # Copiar valores al triángulo inferior para evitar referencias nulas
    for i in range(N):
        for j in range(0, i):
            DP[i][j] = DP[j][i]

    traceback(0, N - 1, structure, structure_secuence, DP, sequence)
    the_structure = write_estructura(sequence, structure)
    print("La matriz: \n", DP)
    print("\n Regiones helicoidales (letras): \n", structure_secuence)
    print("\n Regiones helicoidales (posici): \n", structure)

    for i in range(len(the_structure)):
        if(the_structure[i] == "."):
            loop.append(sequence[i])
            loop_pos.append(i)
            
    print("\n Regiones Lopps (letras): \n", loop)
    print("\n Regiones Loops (posici): \n", loop_pos)

    print("\n La estructura:")
    print(" ".join(the_structure))
    print(" ".join(sequence))

    plot_struct(structure_secuence)
    
    fichero = open(name_file, "w")
    fichero.write('LA MATRIZ: ' + '\n')
    fichero.write(str(DP) + '\n')
    fichero.write("\n Regiones helicoidales (letras): \n" + str(structure_secuence) + '\n')
    fichero.write("\n Regiones helicoidales (posici): \n" + str(structure) + '\n')
    fichero.write("La estructura: \n" + the_structure + '\n')
    fichero.close()


if __name__ == "__main__":
    #sequence = 'GGAAAUCC'
    #sequence = 'ACGUGCCACGAUUCAACGUGGCACAG'
    #sequence = 'GGCCAGAUCUGAGCCUGGGAGCUCUCUGGCC'
    sequence = 'GCUCAAAGUATACCAGGAGG'
    estructura_secundaria(sequence)
