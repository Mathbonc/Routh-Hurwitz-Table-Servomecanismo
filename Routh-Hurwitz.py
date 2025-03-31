import numpy as np

#! Exception

class CoefficientError(Exception):
    pass

#! Funções de matriz

def get_element_value(det, row1, row2,an1):
    det = np.hstack([det, np.array([[row1,row2]]).T]) 
    print("======================================================")
    print_matrix(det)
    print("======================================================")
    #calcula o valor do determinante
    det_value = np.linalg.det(det)
    # print(det_value)
    #retorna o valor dividido pelo primeiro elemento da linha anterior
    return (-1) * round(det_value / an1, 2)


def get_Next_Row(rT, Row):
    new_Row = []
    # * primeira coluna dos derminantes dessa linha
    an = rT[Row][0]
    an1 = rT[Row + 1][0] # * denominador, sempre o primeiro elemento da linha anterior

    zipp = list(zip(*rT))
    for idx, column in enumerate(zipp[1:]): # itera pelas colunas da matriz (começando pela segunda)
        # Criando o determinante de cada coluna
        det = np.array([[an],[an1]])

        if idx == len(zipp[1:]) - 1:  # Última iteração (gera o penultima e última coluna)
            print(f"Determinante do elemento ({Row+2},{idx})")
            det_value = get_element_value(det,column[Row],column[Row + 1],an1)
            print(f"Determinante do elemento ({Row+2},{idx+1})")
            det_value_final = get_element_value(det,0,0,an1)
            new_Row.append(float(det_value))
            new_Row.append(float(det_value_final))
        else:   
            #adiciona uma nova coluna ao determinante, de acordo com a iteração atual
            print(f"Determinante do elemento ({Row+2},{idx})")
            det_value = get_element_value(det,column[Row],column[Row + 1],an1)
            new_Row.append(float(det_value))

    for val in new_Row:
        print(float(val), end=", ")
    print("======================================================")

    # Checa se o primeiro valor é 0
    if(float(new_Row[0]) == 0):
        # Caso seja, checa os próximos valores, se em algum momento o valor for != 0, ele tenta reverter os coeficientes
        for i in new_Row:
            if(float(i) == 0):
                continue
            else:
                raise CoefficientError
        print("Linha nula: o sistema não é estável")
        raise SystemExit
    
    return new_Row

def createRouthTable(coef):
    Row1 = coef[::2]  # Coeficientes de índice par
    Row2 = coef[1::2]  # Coeficientes de índice ímpar
    routhTable_num_Rows = len(coef) # Número de linhas da tabela de routh

    # Garantir que as duas linhas tenham o mesmo tamanho 
    max_len = max(len(Row1), len(Row2))
    while len(Row1) < max_len:
        Row1.append(0)
    while len(Row2) < max_len:
        Row2.append(0)

    # Inicializar a tabela de Routh
    rT = [Row1, Row2]

    for Row in range(routhTable_num_Rows - 2):
        print(f"ESTAMOS NA LINHA {Row + 2}")
        next_Row = get_Next_Row(rT, Row)
        rT.append(next_Row)

    return rT

#! Funções Auxiliares 

def check_stability(table):
    print(table[0])
    for i in range(1, len(table[0])):
        if table[i] * table[i - 1] < 0:  # Produto negativo indica mudança de sinal
            return "INSTÁVEL"
    return "ESTÁVEL"

def getCoef():
    coef = list(map(int, input("Por favor, digite apenas os coeficientes da função de transferência: (as^n + bs^(n-1) + cs^(n-2) ... zs^0)\n").split()))
    return coef

def quitProgram ():
    q = input("Deseja sair? (Y/N): ").strip().upper()

    while(q != "Y" and q != "N"):
        q = input("Entrada inválida! Por favor, digite 'Y' para sair ou 'N' para continuar.").strip().upper()

    if q == "Y":
        print("Saindo... Até logo!")
        return True 
    elif q == "N":
        return False  

def print_matrix(matrix):
    for row in matrix:
        print(" ".join(map(str, row))) 

def print_table(matrix):
    # Calcular a largura máxima de cada coluna para formatação
    col_widths = [max(len(str(item)) for item in column) for column in zip(*matrix)]
    
    # Função para imprimir a linha separadora
    def print_separator():
        print("-" * (sum(col_widths) + len(col_widths) - 1))
    
    # Imprimir a tabela
    print_separator()
    for row in matrix:
        print(" | ".join(f"{str(value):{col_widths[i]}}" for i, value in enumerate(row)))
    print_separator()

#! Main !#

print("Bem-vindo ao Critério de Routh-Hurwitz")
while True:
    coef = getCoef()

    try:
        rT = createRouthTable(coef)
    except CoefficientError:
        print("Linha iniciada com 0, tentando reverter os coeficientes.")
        coef.reverse()
        print(f"Novos coeficientes: {coef}")
        rT = createRouthTable(coef)

    print("Tabelha de Routh-Hurwitz gerada:")
    print_table(rT)
    print(f"Esse sistema é {check_stability(list(zip(*rT)))}")
    if(quitProgram()):
        break
    

    
    